"""
Experimento de escalabilidade do OSJ.

Objetivo: confrontar o expoente empirico com o expoente deduzido na analise.
A teoria preve custo total Theta(n^(5/3)) com s = w = n^(2/3), pois as duas
fases ficam equilibradas: Fase 1 custa n*s = n^(5/3) e Fase 2 custa n*w em
poucas varreduras.

O ajuste e feito em escala log-log: se T(n) ~ c * n^k, entao
log T = log c + k * log n, e k e a inclinacao da reta.
"""

import math
import random
import statistics
import time

from osj import osj_sort, default_s, default_w


def fit_exponent(ns, ys):
    """Minimos quadrados sobre (log n, log y). Devolve a inclinacao k."""
    pts = [(math.log(n), math.log(y)) for n, y in zip(ns, ys) if y > 0]
    m = len(pts)
    sx = sum(p[0] for p in pts)
    sy = sum(p[1] for p in pts)
    sxx = sum(p[0] * p[0] for p in pts)
    sxy = sum(p[0] * p[1] for p in pts)
    return (m * sxy - sx * sy) / (m * sxx - sx * sx)


def main():
    sizes = [250, 500, 1000, 2000, 4000, 8000, 10000]
    trials = 5
    random.seed(42)

    print("{:>7} {:>6} {:>6} {:>14} {:>14} {:>8} {:>10} {:>10}".format(
        "N", "s", "w", "comparacoes", "movimentacoes", "passadas",
        "tempo(ms)", "dp(ms)"))
    print("-" * 83)

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
        print("{:>7} {:>6} {:>6} {:>14,.0f} {:>14,.0f} {:>8.1f} {:>10.1f} {:>10.1f}".format(
            n, default_s(n), default_w(n), c, m_acc / trials, p_acc / trials,
            t, statistics.stdev(samples)))
        ns.append(n); comps.append(c); times.append(t)

    print()
    print("Expoente teorico previsto            : 5/3 = {:.4f}".format(5.0 / 3.0))
    print("Expoente empirico (comparacoes)      : {:.4f}".format(fit_exponent(ns, comps)))
    print("Expoente empirico (tempo)            : {:.4f}".format(fit_exponent(ns, times)))
    print()
    print("Referencia: 1.0 = linear, 1.5 = n^1.5, 2.0 = quadratico.")
    print("n log n tem inclinacao aparente ~1.1 nesta faixa de N.")


if __name__ == "__main__":
    main()
