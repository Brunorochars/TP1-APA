"""
Benchmark comparativo do OSJ contra os metodos classicos e o DPES.

Produz, em ../resultados/ :
    benchmark_osj.csv        dados brutos de todas as medicoes
    benchmark_osj.md         tabelas em Markdown, prontas para o relatorio
    benchmark_tempo.png      curvas de tempo por distribuicao
    benchmark_comparacoes.png curvas de comparacoes por distribuicao
    escalabilidade_loglog.png ajuste log-log com expoentes empiricos

Reaproveita o gerador de datasets do benchmark.py do pacote da disciplina,
para que os cenarios sejam exatamente os mesmos usados nos baselines.
"""

import csv
import math
import os
import random
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
TRIALS = 3


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

                t_acc = c_acc = m_acc = 0.0
                for data, exp in zip(datasets, expected):
                    d = list(data)
                    t0 = time.perf_counter()
                    out, c, m = fn(d)
                    t_acc += (time.perf_counter() - t0) * 1000.0
                    assert out == exp, "ERRO DE ORDENACAO em {} n={}".format(name, n)
                    c_acc += c
                    m_acc += m

                rec = {"time_ms": t_acc / TRIALS,
                       "comps": c_acc / TRIALS,
                       "moves": m_acc / TRIALS}
                results[dist][name][n] = rec
                rows.append({"distribuicao": dist, "algoritmo": name, "n": n,
                             "tempo_ms": round(rec["time_ms"], 4),
                             "comparacoes": round(rec["comps"]),
                             "movimentacoes": round(rec["moves"])})
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
        f.write("Media de {} repeticoes por celula. Tracos indicam medicoes "
                "omitidas por custo proibitivo.\n\n".format(TRIALS))

        for metric, label, fmt in (("time_ms", "Tempo medio (ms)", "{:.3f}"),
                                   ("comps", "Comparacoes", "{:,.0f}"),
                                   ("moves", "Movimentacoes", "{:,.0f}")):
            f.write("## {}\n\n".format(label))
            for dist in DISTRIBUTIONS:
                f.write("### Distribuicao `{}`\n\n".format(dist))
                f.write("| Algoritmo | " + " | ".join("N={}".format(s) for s in SIZES) + " |\n")
                f.write("| :--- | " + " | ".join("---:" for _ in SIZES) + " |\n")
                for name in ALGORITHMS:
                    cells = []
                    for s in SIZES:
                        if s in results[dist][name]:
                            cells.append(fmt.format(results[dist][name][s][metric]))
                        else:
                            cells.append("--")
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


def plot_scaling(results):
    """OSJ isolado contra as curvas de referencia n log n, n^(5/3) e n^2."""
    sm = results["random"]["OSJ"]
    ns = sorted(sm)
    ys = [sm[n]["comps"] for n in ns]
    k = fit_exponent(ns, ys)

    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.plot(ns, ys, marker="o", linewidth=2.4, label="OSJ (medido)")

    anchor = ys[-1]; n_last = ns[-1]
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
    return path, k


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    random.seed(42)
    results, rows = run()
    print()
    print("CSV      ->", write_csv(rows))
    print("Markdown ->", write_markdown(results))
    print("Grafico  ->", plot_metric(results, "time_ms", "tempo (ms)", "benchmark_tempo.png"))
    print("Grafico  ->", plot_metric(results, "comps", "comparacoes", "benchmark_comparacoes.png"))
    p, k = plot_scaling(results)
    print("Grafico  ->", p)
    print()
    print("Expoente empirico do OSJ (comparacoes, random) = {:.4f}".format(k))
    print("Expoente teorico previsto                      = {:.4f}".format(5.0 / 3.0))
