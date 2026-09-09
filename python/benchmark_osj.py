"""
Benchmark comparativo do OSJ contra os metodos classicos e o DPES.

Produz, em ../resultados/ :
    benchmark_osj.csv        dados brutos de todas as medicoes
    benchmark_osj.md         tabelas em Markdown, prontas para o relatorio
    benchmark_tempo.png      curvas de tempo por distribuicao
    benchmark_comparacoes.png curvas de comparacoes por distribuicao

O grafico de escalabilidade (escalabilidade_loglog.png) NAO sai daqui: ele
pertence ao scaling_osj.py, que mede ate N = 10^4. Este benchmark para em
N = 2000 por causa dos baselines quadraticos, e um ajuste feito sobre essa
faixa contradiria o expoente que o relatorio publica.

Reaproveita o gerador de datasets do benchmark.py do pacote da disciplina,
para que os cenarios sejam exatamente os mesmos usados nos baselines.
"""

import csv
import math
import os
import random
import statistics
import time
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from benchmark import generate_dataset
from classical import (bubble_sort, insertion_sort, merge_sort,
                       quick_sort, selection_sort)
from authorial import dpes_sort
from osj import my_authorial_sort, my_authorial_sort_stable

# Ancorado no arquivo, nao no diretorio atual: o script pode ser chamado
# de qualquer lugar sem que as saidas mudem de lugar.
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resultados")

ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "DPES (referencia)": dpes_sort,
    "OSJ": my_authorial_sort,
    "OSJ estavel": my_authorial_sort_stable,
}

QUADRATIC = ("Bubble Sort", "Selection Sort", "Insertion Sort")

SIZES = [10, 50, 100, 250, 500, 1000, 2000]
DISTRIBUTIONS = ["random", "sorted", "reverse", "duplicates", "almost_sorted"]
TRIALS = 5


def run():
    rows = []
    results = defaultdict(lambda: defaultdict(dict))

    for dist in DISTRIBUTIONS:
        print("Distribuicao:", dist)
        for n in SIZES:
            datasets = [generate_dataset(n, dist) for _ in range(TRIALS)]
            expected = [sorted(d) for d in datasets]

            for name, fn in ALGORITHMS.items():
                if n > 1000 and name in QUADRATIC and dist in ("random", "reverse"):
                    continue

                samples = []
                comp_samples = []
                move_samples = []
                for data, exp in zip(datasets, expected):
                    d = list(data)
                    t0 = time.perf_counter()
                    out, c, m = fn(d)
                    samples.append((time.perf_counter() - t0) * 1000.0)
                    assert out == exp, "ERRO DE ORDENACAO em {} n={}".format(name, n)
                    comp_samples.append(c)
                    move_samples.append(m)

                rec = {"time_ms": statistics.fmean(samples),
                       "time_sd": statistics.stdev(samples),
                       "comps": statistics.fmean(comp_samples),
                       "comps_sd": statistics.stdev(comp_samples),
                       "moves": statistics.fmean(move_samples),
                       "moves_sd": statistics.stdev(move_samples)}
                results[dist][name][n] = rec
                rows.append({"distribuicao": dist, "algoritmo": name, "n": n,
                             "tempo_ms": round(rec["time_ms"], 4),
                             "tempo_dp_ms": round(rec["time_sd"], 4),
                             "comparacoes": round(rec["comps"]),
                             "comparacoes_dp": round(rec["comps_sd"], 1),
                             "movimentacoes": round(rec["moves"]),
                             "movimentacoes_dp": round(rec["moves_sd"], 1)})
            print("  N = {:>5} ok".format(n))
    return results, rows


def fit_exponent(ns, ys):
    pts = [(math.log(n), math.log(y)) for n, y in zip(ns, ys) if y > 0]
    if len(pts) < 2:
        return float("nan")
    m = len(pts)
    sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0] ** 2 for p in pts); sxy = sum(p[0] * p[1] for p in pts)
    return (m * sxy - sx * sy) / (m * sxx - sx * sx)


def write_csv(rows):
    path = os.path.join(OUT_DIR, "benchmark_osj.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)
    return path


def write_markdown(results):
    path = os.path.join(OUT_DIR, "benchmark_osj.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Resultados experimentais - OSJ vs. metodos classicos\n\n")
        f.write("Media de {} repeticoes por celula, acompanhada do desvio-padrao "
                "amostral das repeticoes (media +/- dp) em todas as metricas: a "
                "dispersao das comparacoes e das movimentacoes e que mede a "
                "aleatoriedade da Fase 1, enquanto a do tempo mede sobretudo "
                "ruido de maquina. Tracos indicam medicoes omitidas por custo "
                "proibitivo.\n\n".format(TRIALS))

        for metric, sd_key, label, fmt in (
                ("time_ms", "time_sd", "Tempo medio (ms)", "{:.3f}"),
                ("comps", "comps_sd", "Comparacoes", "{:,.0f}"),
                ("moves", "moves_sd", "Movimentacoes", "{:,.0f}")):
            f.write("## {}\n\n".format(label))
            for dist in DISTRIBUTIONS:
                f.write("### Distribuicao `{}`\n\n".format(dist))
                f.write("| Algoritmo | " + " | ".join("N={}".format(s) for s in SIZES) + " |\n")
                f.write("| :--- | " + " | ".join("---:" for _ in SIZES) + " |\n")
                for name in ALGORITHMS:
                    cells = []
                    for s in SIZES:
                        if s not in results[dist][name]:
                            cells.append("--")
                            continue
                        rec = results[dist][name][s]
                        cells.append(fmt.format(rec[metric]) + " +/- "
                                     + fmt.format(rec[sd_key]))
                    f.write("| {} | ".format(name) + " | ".join(cells) + " |\n")
                f.write("\n")

        f.write("## Expoentes empiricos (ajuste log-log, distribuicao `random`)\n\n")
        f.write("| Algoritmo | expoente (comparacoes) | expoente (tempo) |\n")
        f.write("| :--- | ---: | ---: |\n")
        for name in ALGORITHMS:
            sm = results["random"][name]
            ns = sorted(sm)
            if len(ns) < 3:
                continue
            f.write("| {} | {:.3f} | {:.3f} |\n".format(
                name,
                fit_exponent(ns, [sm[n]["comps"] for n in ns]),
                fit_exponent(ns, [sm[n]["time_ms"] for n in ns])))
        f.write("\nReferencia: 1.0 linear, ~1.1 para n log n nesta faixa de N, "
                "1.667 para n^(5/3), 2.0 quadratico.\n")
    return path


def plot_metric(results, metric, ylabel, filename):
    fig, axes = plt.subplots(1, len(DISTRIBUTIONS), figsize=(5 * len(DISTRIBUTIONS), 4.2))
    for ax, dist in zip(axes, DISTRIBUTIONS):
        for name in ALGORITHMS:
            sm = results[dist][name]
            ns = sorted(sm)
            if not ns:
                continue
            style = dict(marker="o", linewidth=2.2) if name.startswith("OSJ") \
                else dict(marker=".", linewidth=1.0, alpha=0.75)
            ax.plot(ns, [sm[n][metric] for n in ns], label=name, **style)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_title(dist)
        ax.set_xlabel("N")
        ax.set_ylabel(ylabel)
        ax.grid(True, which="both", linestyle="--", alpha=0.4)
    axes[0].legend(fontsize=7)
    fig.suptitle("{} (escala log-log)".format(ylabel))
    fig.tight_layout()
    path = os.path.join(OUT_DIR, filename)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    random.seed(42)
    results, rows = run()
    print()
    print("CSV      ->", write_csv(rows))
    print("Markdown ->", write_markdown(results))
    print("Grafico  ->", plot_metric(results, "time_ms", "tempo (ms)", "benchmark_tempo.png"))
    print("Grafico  ->", plot_metric(results, "comps", "comparacoes", "benchmark_comparacoes.png"))
    print()
    print("O grafico de escalabilidade sai do scaling_osj.py, que mede ate "
          "N = 10^4 - a faixa que o relatorio publica.")
