"""
Gera o exemplo numerico passo a passo usado no README.
Usa as funcoes reais de osj.py, nao uma reimplementacao: o rastro impresso
e exatamente o que o algoritmo faz.
"""
import random
from osj import Stats, _insertion_window, inversions, max_displacement

VETOR = [42, 7, 19, 88, 3, 61, 25, 54, 12, 77, 33, 96]
S = 4
W = 4
SEED = 2024


def fase1_com_rastro(a, s, rng, st):
    n = len(a)
    print("FASE 1 - SONDAGEM   (s = {} testemunhas por elemento)\n".format(s))
    print("  {:>5} | {:>28} | {:>3} | {:>6} | {:>8}".format(
        "valor", "testemunhas sorteadas", "c", "c/s", "posicao"))
    print("  " + "-" * 66)
    buckets = [[] for _ in range(n)]
    for i in range(n):
        ai = a[i]
        c = 0
        vistas = []
        for _ in range(s):
            j = rng.randrange(n)
            vistas.append(a[j])
            st.comparisons += 1
            if a[j] < ai:
                c += 1
        pos = (c * (n - 1)) // s
        buckets[pos].append(ai)
        print("  {:>5} | {:>28} | {:>3} | {:>6} | {:>8}".format(
            ai, str(vistas), c, "{}/{}".format(c, s), pos))
    out = []
    for b in buckets:
        out.extend(b)
    st.moves += n
    return out


def main():
    rng = random.Random(SEED)
    st = Stats()

    print("=" * 70)
    print("EXEMPLO NUMERICO - OSJ")
    print("=" * 70)
    print("\nEntrada  : {}".format(VETOR))
    print("Ordenado : {}".format(sorted(VETOR)))
    print("Inv(A) inicial = {}   |   deslocamento maximo = {}\n".format(
        inversions(VETOR), max_displacement(VETOR)))

    b = fase1_com_rastro(list(VETOR), S, rng, st)

    print("\n  Vetor apos a Fase 1: {}".format(b))
    print("  Inv(A) = {} (era {})   |   deslocamento maximo = {} (era {})".format(
        inversions(b), inversions(VETOR), max_displacement(b), max_displacement(VETOR)))

    n = len(b)
    w = W
    step = w // 2
    starts = list(range(0, n - w + 1, step))
    if starts[-1] != n - w:
        starts.append(n - w)

    print("\n\nFASE 2 - SANFONA   (w = {}, passo = {}, janelas em {})\n".format(w, step, starts))

    passada = 0
    while True:
        passada += 1
        moved = False
        print("  Passada {}:".format(passada))
        for p in starts:
            antes = list(b)
            houve = _insertion_window(b, p, p + w, st)
            marca = "  <- ordenou" if houve else ""
            print("    janela [{:>2}:{:>2}]  {} -> {}{}".format(
                p, p + w, antes[p:p + w], b[p:p + w], marca))
            if houve:
                moved = True
        st.passes += 1
        print("    estado: {}   Inv = {}".format(b, inversions(b)))
        if not moved:
            print("    nenhuma movimentacao na passada inteira -> PONTO FIXO, encerra\n")
            break
        print()

    print("Saida : {}".format(b))
    print("Correto? {}".format(b == sorted(VETOR)))
    print("\nTotais: {} comparacoes, {} movimentacoes, {} trocas de vizinhos, "
          "{} passadas".format(st.comparisons, st.moves, st.shifts, st.passes))
    print("Verificacao do teorema: trocas de vizinhos ({}) == Inv apos a Fase 1 ({})".format(
        st.shifts, inversions(fase1_com_rastro_silencioso())))


def fase1_com_rastro_silencioso():
    rng = random.Random(SEED)
    st = Stats()
    n = len(VETOR)
    a = list(VETOR)
    buckets = [[] for _ in range(n)]
    for i in range(n):
        ai = a[i]
        c = 0
        for _ in range(S):
            j = rng.randrange(n)
            if a[j] < ai:
                c += 1
        buckets[(c * (n - 1)) // S].append(ai)
    out = []
    for bk in buckets:
        out.extend(bk)
    return out


if __name__ == "__main__":
    main()
