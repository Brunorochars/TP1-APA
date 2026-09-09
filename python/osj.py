"""
OSJ - Ordenacao por Sondagem e Janelas
======================================

Metodo de ordenacao autoral em duas fases.

FASE 1 - SONDAGEM (heuristica)
    Cada elemento estima o proprio posto final consultando s "testemunhas"
    sorteadas do vetor e contando quantas sao menores que ele. A fracao
    obtida, escalada para [0, n-1], da a posicao estimada, e o elemento e
    depositado la. Esta fase pode errar; errar nao compromete a corretude,
    apenas o custo da fase seguinte.

FASE 2 - SANFONA (corretude)
    Uma janela de largura w varre o vetor com passo w/2, ordenando por
    insercao cada trecho coberto, e repete a varredura ate uma passada
    inteira ocorrer sem nenhuma movimentacao. Esta fase sozinha ordena
    qualquer entrada: e nela que mora toda a corretude do algoritmo.

SEPARACAO DE RESPONSABILIDADES
    A Fase 1 responde pelo desempenho; a Fase 2 responde pela corretude.
    A Fase 1 nao pode errar de modo fatal, apenas de modo caro. Por isso a
    aleatoriedade da sondagem nunca produz saida errada, so saida mais lenta.
    A funcao sanfona_sort() abaixo existe para evidenciar isso: ela e o
    algoritmo sem a Fase 1, e ordena tudo do mesmo jeito.

POR QUE O PASSO E w/2 E NAO w
    Com passo w as janelas ficam disjuntas e o processo ganha pontos fixos
    espurios: [3, 4, 1, 2] com w = 2 tem as duas janelas internamente
    ordenadas, nenhuma troca ocorre, o laco encerra e a saida esta errada.
    Com sobreposicao, todo par de posicoes vizinhas (k, k+1) cai dentro de
    alguma janela, e uma passada sem movimentacao forca A[k] <= A[k+1] para
    todo k. O unico ponto fixo passa a ser o vetor ordenado.

TERMINO
    Seja Inv(A) o numero de pares fora de ordem. A insercao dentro da janela
    so troca vizinhos, e cada troca de vizinhos fora de ordem reduz Inv(A) em
    exatamente 1 (nenhum outro par muda de status, pois nada mais se move e
    nao ha posicao estritamente entre k e k+1). Como Inv(A) e inteiro, nunca
    negativo, e comeca em no maximo n(n-1)/2, o numero de trocas em toda a
    execucao e finito e limitado por n(n-1)/2. Logo o laco termina.
    Inv(A) e uma grandeza da analise, nao do algoritmo: nao e calculada em
    lugar nenhum do codigo. A funcao inversions() abaixo serve apenas a
    instrumentacao experimental.

CONVENCAO DE CONTAGEM
    Para permitir comparacao justa com classical.py, a contagem de
    comparacoes e movimentacoes segue exatamente a mesma convencao usada la
    (cada leitura de chave, cada deslocamento e cada gravacao final conta uma
    movimentacao). O contador adicional 'shifts' registra apenas os
    deslocamentos de uma casa, que sao as trocas de vizinhos da prova de
    termino, e serve para verificar experimentalmente o limite n(n-1)/2.

Autor: Bruno da Silva Rocha
Disciplina: Analise e Projeto de Algoritmos - TP1
"""

from typing import Any, List, Optional, Tuple
import random


# ---------------------------------------------------------------------------
# Instrumentacao
# ---------------------------------------------------------------------------

class Stats:
    """Contadores de operacoes elementares de uma execucao."""

    __slots__ = ("comparisons", "moves", "shifts", "passes", "s", "w")

    def __init__(self) -> None:
        self.comparisons = 0   # comparacoes entre elementos
        self.moves = 0         # movimentacoes (convencao de classical.py)
        self.shifts = 0        # deslocamentos de uma casa = trocas de vizinhos
        self.passes = 0        # varreduras completas da Fase 2
        self.s = 0             # testemunhas efetivamente usadas
        self.w = 0             # largura de janela efetivamente usada

    def as_dict(self) -> dict:
        return {k: getattr(self, k) for k in self.__slots__}

    def __repr__(self) -> str:
        return ("Stats(comparisons={0.comparisons}, moves={0.moves}, "
                "shifts={0.shifts}, passes={0.passes}, s={0.s}, w={0.w})").format(self)


# ---------------------------------------------------------------------------
# Parametros padrao
# ---------------------------------------------------------------------------

def default_s(n: int) -> int:
    """Numero de testemunhas por elemento.

    O custo da Fase 1 e n*s. O desvio-padrao do estimador de posto e
    O(1/sqrt(s)), logo o deslocamento tipico apos a Fase 1 e O(n/sqrt(s)).
    Equilibrar as duas fases leva a s = Theta(n^(2/3)).
    """
    if n <= 1:
        return 0
    return max(1, int(round(n ** (2.0 / 3.0))))


def default_w(n: int) -> int:
    """Largura da janela.

    Escolhida na ordem do deslocamento esperado apos a Fase 1, que com
    s = n^(2/3) vale Theta(n / sqrt(s)) = Theta(n^(2/3)). Assim a Fase 2
    converge em poucas varreduras.
    """
    if n <= 2:
        return 2
    return max(2, min(n, int(round(n ** (2.0 / 3.0)))))


# ---------------------------------------------------------------------------
# Fase 2 - Sanfona
# ---------------------------------------------------------------------------

def _insertion_window(a: List[Any], lo: int, hi: int, st: Stats) -> bool:
    """Ordena a[lo:hi] por insercao. Devolve True se houve troca de vizinhos.

    Usa comparacao estrita (a[j] > key), portanto e estavel.
    Cada troca de vizinhos reduz Inv(A) em 1.
    """
    moved = False
    for i in range(lo + 1, hi):
        key = a[i]
        st.moves += 1
        j = i - 1
        while j >= lo:
            st.comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                st.moves += 1
                st.shifts += 1
                j -= 1
                moved = True
            else:
                break
        a[j + 1] = key
        st.moves += 1
    return moved


def _sweep(a: List[Any], w: int, st: Stats) -> bool:
    """Executa UMA varredura: percorre os inicios de janela em ordem
    crescente, ordenando cada trecho por insercao. Devolve True se houve
    troca de vizinhos.

    A ordem crescente dos inicios nao e detalhe de implementacao: junto com
    a sobreposicao, e premissa do lema do avanco (Secao 4.2 do relatorio).
    """
    n = len(a)
    w = max(2, min(w, n))
    step = max(1, w // 2)

    starts = list(range(0, n - w + 1, step))
    if starts[-1] != n - w:
        starts.append(n - w)          # janela encostada na borda direita

    moved = False
    for p in starts:
        if _insertion_window(a, p, p + w, st):
            moved = True
    return moved


def _phase2(a: List[Any], w: int, st: Stats) -> None:
    """Varreduras de janela deslizante ate o ponto fixo."""
    if len(a) < 2:
        return

    while True:
        moved = _sweep(a, w, st)
        st.passes += 1
        if not moved:
            break


# ---------------------------------------------------------------------------
# Fase 1 - Sondagem
# ---------------------------------------------------------------------------

def _phase1_independent(a: List[Any], s: int, rng, st: Stats) -> List[Any]:
    """Cada elemento sorteia as proprias s testemunhas.

    Os erros de estimativa sao independentes entre elementos, o que torna a
    analise probabilistica mais limpa. Nao preserva estabilidade: duas chaves
    iguais podem receber estimativas diferentes e trocar de ordem relativa.
    Custo: n*s comparacoes.
    """
    n = len(a)
    buckets: List[List[Any]] = [[] for _ in range(n)]

    for i in range(n):
        ai = a[i]
        c = 0
        for _ in range(s):
            j = rng.randrange(n)
            st.comparisons += 1
            if a[j] < ai:
                c += 1
        buckets[(c * (n - 1)) // s].append(ai)

    out: List[Any] = []
    for b in buckets:
        out.extend(b)
    st.moves += n
    return out


def _phase1_shared(a: List[Any], s: int, rng, st: Stats) -> List[Any]:
    """Todas as chaves consultam a MESMA amostra de testemunhas.

    Consequencia teorica: chaves iguais recebem sempre a mesma estimativa,
    caem no mesmo balde e preservam a ordem original. Como a insercao da
    Fase 2 e estavel, o algoritmo inteiro passa a ser estavel.
    Custo por elemento cai de s para log2(s) (busca binaria na amostra).
    Preco: os erros deixam de ser independentes entre elementos.
    """
    n = len(a)
    sample = sorted(a[rng.randrange(n)] for _ in range(s))

    buckets: List[List[Any]] = [[] for _ in range(n)]
    for i in range(n):
        ai = a[i]
        lo, hi = 0, s
        while lo < hi:                       # conta testemunhas < ai
            mid = (lo + hi) // 2
            st.comparisons += 1
            if sample[mid] < ai:
                lo = mid + 1
            else:
                hi = mid
        buckets[(lo * (n - 1)) // s].append(ai)

    out: List[Any] = []
    for b in buckets:
        out.extend(b)
    st.moves += n
    return out


# ---------------------------------------------------------------------------
# Algoritmo completo
# ---------------------------------------------------------------------------

def osj_sort(arr: List[Any],
             s: Optional[int] = None,
             w: Optional[int] = None,
             shared_witnesses: bool = False,
             seed: Optional[int] = None) -> Tuple[List[Any], Stats]:
    """Ordena e devolve (nova_lista, Stats). Nao modifica arr.

    s                 testemunhas por elemento (None = n^(2/3))
    w                 largura da janela        (None = n^(2/3))
    shared_witnesses  True usa amostra compartilhada e torna o metodo estavel
    seed              semente propria; None usa o gerador global do modulo
                      random, de modo que random.seed(x) a montante torna a
                      execucao reprodutivel
    """
    st = Stats()
    n = len(arr)

    if n <= 1:                        # casos limite N = 0 e N = 1
        return list(arr), st

    if s is None:
        s = default_s(n)
    if w is None:
        w = default_w(n)
    st.s, st.w = s, max(2, min(w, n))

    rng = random if seed is None else random.Random(seed)

    if s > 0:
        if shared_witnesses:
            b = _phase1_shared(list(arr), s, rng, st)
        else:
            b = _phase1_independent(list(arr), s, rng, st)
    else:
        b = list(arr)

    _phase2(b, w, st)
    return b, st


def sanfona_sort(arr: List[Any],
                 w: Optional[int] = None) -> Tuple[List[Any], Stats]:
    """Somente a Fase 2, sem sondagem.

    Existe para evidenciar que a corretude do metodo nao depende da Fase 1:
    esta funcao ordena qualquer entrada sozinha.
    """
    st = Stats()
    b = list(arr)
    n = len(b)
    if n <= 1:
        return b, st
    if w is None:
        w = default_w(n)
    st.w = max(2, min(w, n))
    _phase2(b, w, st)
    return b, st


def my_authorial_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """Interface exigida pelo TP1: (lista_ordenada, comparacoes, movimentacoes)."""
    out, st = osj_sort(arr)
    return out, st.comparisons, st.moves


def my_authorial_sort_stable(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """Variante estavel (testemunhas compartilhadas), mesma interface."""
    out, st = osj_sort(arr, shared_witnesses=True)
    return out, st.comparisons, st.moves


# ---------------------------------------------------------------------------
# Utilitarios de analise (nunca usados pelo algoritmo)
# ---------------------------------------------------------------------------

def inversions(a: List[Any]) -> int:
    """Inv(A) por forca bruta, O(n^2).

    E a funcao potencial da prova de termino. Existe apenas na analise: o
    algoritmo nunca a calcula, porque calcula-la custaria mais caro do que
    desfazer a desordem que ela mede.
    """
    n = len(a)
    total = 0
    for i in range(n):
        ai = a[i]
        for j in range(i + 1, n):
            if ai > a[j]:
                total += 1
    return total


def max_displacement(a: List[Any]) -> int:
    """Dis(A): maior distancia entre a posicao atual de um elemento e a
    posicao que ele ocupara no vetor ordenado."""
    n = len(a)
    if n == 0:
        return 0
    order = sorted(range(n), key=lambda i: (a[i], i))
    final = [0] * n
    for rank, i in enumerate(order):
        final[i] = rank
    return max(abs(i - final[i]) for i in range(n))


def max_left_displacement(a: List[Any]) -> int:
    """Dis_esq(A): maior deslocamento a ESQUERDA, isto e, o maior valor de
    (posicao atual - posto correto) entre os elementos que estao a direita do
    proprio posto. Zero significa vetor ordenado.

    E a grandeza do lema do avanco (Secao 4.2): o lema vale para a esquerda,
    nao para a direita. Existe apenas na analise, como inversions()."""
    n = len(a)
    if n == 0:
        return 0
    order = sorted(range(n), key=lambda i: (a[i], i))
    final = [0] * n
    for rank, i in enumerate(order):
        final[i] = rank
    return max(max(i - final[i] for i in range(n)), 0)
