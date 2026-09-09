"""
Experimento de escalabilidade do OSJ.

Objetivo: confrontar o expoente empirico com o expoente deduzido na analise.
A teoria preve custo total Theta(n^(5/3)) com s = w = n^(2/3), pois as duas
fases ficam equilibradas: Fase 1 custa n*s = n^(5/3) e Fase 2 custa n*w em
poucas varreduras.

O ajuste e feito em escala log-log: se T(n) ~ c * n^k, entao
log T = log c + k * log n, e k e a inclinacao da reta.

Produz, em ../resultados/ :
    escalabilidade_osj.csv    pontos medidos e os expoentes ajustados
    escalabilidade_loglog.png ajuste log-log contra as curvas de referencia

O grafico mora aqui, e nao no benchmark_osj.py, porque e aqui que a medicao
vai ate N = 10^4 - a faixa que o relatorio publica. Gerado la, sobre os
N <= 2000 do benchmark comparativo, o titulo do grafico traria um expoente
diferente do da tabela.
"""

import csv
import math
import os
import random
import statistics
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from osj import osj_sort, default_s, default_w

# Ancorado no arquivo, nao no diretorio atual: o script pode ser chamado
# de qualquer lugar sem que as saidas mudem de lugar.
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resultados")


def fit_exponent(ns, ys):
    """Minimos quadrados sobre (log n, log y). Devolve a inclinacao k."""
    pts = [(math.log(n), math.log(y)) for n, y in zip(ns, ys) if y > 0]
    m = len(pts)
    sx = sum(p[0] for p in pts)
    sy = sum(p[1] for p in pts)
    sxx = sum(p[0] * p[0] for p in pts)
    sxy = sum(p[0] * p[1] for p in pts)
    return (m * sxy - sx * sy) / (m * sxx - sx * sx)


def write_csv(rows: list[dict], k_comps: float, k_time: float) -> str:
    """Grava os pontos medidos e, ao final, os expoentes ajustados.

    O expoente e propriedade da serie inteira, nao de um ponto: por isso vai
    num bloco proprio depois da tabela, em vez de repetido em cada linha.

    Args:
        rows: Um registro por tamanho N medido.
        k_comps: Expoente ajustado sobre as comparacoes.
        k_time: Expoente ajustado sobre o tempo.

    Returns:
        O caminho do arquivo escrito.
    """
    path = os.path.join(OUT_DIR, "escalabilidade_osj.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)
        f.write("\n")
        wr2 = csv.writer(f)
        wr2.writerow(["expoente", "valor"])
        wr2.writerow(["teorico", round(5.0 / 3.0, 4)])
        wr2.writerow(["empirico_comparacoes", round(k_comps, 4)])
        wr2.writerow(["empirico_tempo", round(k_time, 4)])
    return path


def plot_scaling(ns: list[int], comps: list[float], k: float) -> str:
    """OSJ isolado contra as curvas de referencia n, n log n, n^(5/3) e n^2.

    Args:
        ns: Tamanhos medidos, em ordem crescente.
        comps: Comparacoes medias em cada tamanho.
        k: Expoente ajustado sobre esses pontos, exibido no titulo.

    Returns:
        O caminho do grafico escrito.
    """
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.plot(ns, comps, marker="o", linewidth=2.4, label="OSJ (medido)")

    anchor = comps[-1]; n_last = ns[-1]
    for expo, lbl in ((1.0, "n"), (5.0 / 3.0, "n^(5/3)"), (2.0, "n^2")):
        ax.plot(ns, [anchor * (n / n_last) ** expo for n in ns],
                linestyle="--", linewidth=1.1, alpha=0.7, label=lbl)
    ax.plot(ns, [anchor * (n * math.log2(n)) / (n_last * math.log2(n_last)) for n in ns],
            linestyle=":", linewidth=1.4, alpha=0.85, label="n log n")

    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("N"); ax.set_ylabel("comparacoes")
    ax.set_title("Escalabilidade do OSJ\nexpoente empirico = {:.3f}   |   "
                 "expoente teorico = 5/3 = {:.3f}".format(k, 5.0 / 3.0))
    ax.grid(True, which="both", linestyle="--", alpha=0.4)
    ax.legend()
    fig.tight_layout()
    path = os.path.join(OUT_DIR, "escalabilidade_loglog.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def main() -> None:
    sizes = [250, 500, 1000, 2000, 4000, 8000, 10000]
    trials = 5
    random.seed(42)
    os.makedirs(OUT_DIR, exist_ok=True)

    print("{:>7} {:>6} {:>6} {:>14} {:>14} {:>10} {:>10} {:>10}".format(
        "N", "s", "w", "comparacoes", "movimentacoes", "varreduras",
        "tempo(ms)", "dp(ms)"))
    print("-" * 85)

    rows = []
    ns, comps, times = [], [], []
    for n in sizes:
        c_acc = m_acc = p_acc = 0
        samples = []
        for _ in range(trials):
            data = [random.randint(0, 10 * n) for _ in range(n)]
            t0 = time.perf_counter()
            out, st = osj_sort(data)
            samples.append((time.perf_counter() - t0) * 1000.0)
            assert out == sorted(data), "erro de ordenacao em n={}".format(n)
            c_acc += st.comparisons
            m_acc += st.moves
            p_acc += st.passes
        c = c_acc / trials
        t = statistics.fmean(samples)
        sd = statistics.stdev(samples)
        print("{:>7} {:>6} {:>6} {:>14,.0f} {:>14,.0f} {:>10.1f} {:>10.1f} {:>10.1f}".format(
            n, default_s(n), default_w(n), c, m_acc / trials, p_acc / trials,
            t, sd))
        rows.append({"n": n, "s": default_s(n), "w": default_w(n),
                     "comparacoes": round(c),
                     "movimentacoes": round(m_acc / trials),
                     "varreduras": round(p_acc / trials, 1),
                     "tempo_ms": round(t, 4),
                     "tempo_dp_ms": round(sd, 4)})
        ns.append(n); comps.append(c); times.append(t)

    k_comps = fit_exponent(ns, comps)
    k_time = fit_exponent(ns, times)

    print()
    print("Expoente teorico previsto            : 5/3 = {:.4f}".format(5.0 / 3.0))
    print("Expoente empirico (comparacoes)      : {:.4f}".format(k_comps))
    print("Expoente empirico (tempo)            : {:.4f}".format(k_time))
    print()
    print("Referencia: 1.0 = linear, 1.5 = n^1.5, 2.0 = quadratico.")
    print("n log n tem inclinacao aparente ~1.1 nesta faixa de N.")
    print()
    print("CSV      ->", write_csv(rows, k_comps, k_time))
    print("Grafico  ->", plot_scaling(ns, comps, k_comps))


if __name__ == "__main__":
    main()
