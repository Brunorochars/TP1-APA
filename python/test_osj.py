"""
Suite de testes do OSJ - Ordenacao por Sondagem e Janelas
=========================================================

Cobre tres niveis:

  1. CONFORMIDADE  - reaproveita os cenarios obrigatorios de test_suite.py
                     (o mixin do proprio pacote da disciplina), aplicados as
                     duas variantes do algoritmo e a Fase 2 isolada.

  2. PROPRIEDADES  - estabilidade, e a evidencia de que a corretude nao
                     depende da Fase 1.

  3. TEORIA        - verificacao experimental das afirmacoes da analise:
                     o limite n(n-1)/2 da funcao potencial, e o
                     contraexemplo que justifica a sobreposicao das janelas.

Execucao:  python test_osj.py -v
"""

import random
import unittest
from typing import Any, List, Tuple

from test_suite import BaseSortMixin          # cenarios obrigatorios do pacote
from osj import (
    Stats,
    inversions,
    max_displacement,
    max_left_displacement,
    my_authorial_sort,
    my_authorial_sort_stable,
    osj_sort,
    sanfona_sort,
)


# ===========================================================================
# 1. CONFORMIDADE COM A SUITE OBRIGATORIA
# ===========================================================================

def _sanfona_only(arr):
    out, st = sanfona_sort(arr)
    return out, st.comparisons, st.moves


class TestOSJ(unittest.TestCase, BaseSortMixin):
    """OSJ completo, variante de testemunhas independentes."""
    sort_fn = staticmethod(my_authorial_sort)
    name = "OSJ (testemunhas independentes)"


class TestOSJStable(unittest.TestCase, BaseSortMixin):
    """OSJ completo, variante de testemunhas compartilhadas (estavel)."""
    sort_fn = staticmethod(my_authorial_sort_stable)
    name = "OSJ (testemunhas compartilhadas)"


class TestSanfonaOnly(unittest.TestCase, BaseSortMixin):
    """Fase 2 isolada. Passar aqui e a evidencia experimental de que toda a
    corretude do metodo mora na Sanfona, e nenhuma na Sondagem."""
    sort_fn = staticmethod(_sanfona_only)
    name = "Sanfona isolada (Fase 2 sem Fase 1)"


# ===========================================================================
# 2. PROPRIEDADES DO ALGORITMO
# ===========================================================================

class Item:
    """Elemento com chave e etiqueta. A comparacao usa SO a chave, de modo
    que a etiqueta revela se a ordem original entre chaves iguais sobreviveu."""

    __slots__ = ("key", "tag")

    def __init__(self, key: int, tag: int) -> None:
        self.key = key
        self.tag = tag

    def __lt__(self, other): return self.key < other.key
    def __gt__(self, other): return self.key > other.key
    def __le__(self, other): return self.key <= other.key
    def __ge__(self, other): return self.key >= other.key
    def __eq__(self, other): return self.key == other.key
    def __hash__(self): return hash(self.key)
    def __repr__(self): return "Item({0},{1})".format(self.key, self.tag)


def _labelled(keys: List[int]) -> List[Item]:
    return [Item(k, t) for t, k in enumerate(keys)]


def _signature(items: List[Item]) -> List[Tuple[int, int]]:
    return [(it.key, it.tag) for it in items]


class TestProperties(unittest.TestCase):

    def test_correctness_does_not_depend_on_phase1(self):
        """A Fase 1 pode ser sabotada sem afetar a saida.

        Com s = 1 a estimativa de posto e praticamente ruido: uma unica
        testemunha. A saida deve continuar perfeitamente ordenada, apenas
        mais cara. E o teste empirico da separacao de responsabilidades.
        """
        random.seed(7)
        for n in (2, 3, 17, 100, 400):
            data = [random.randint(-500, 500) for _ in range(n)]
            out, st = osj_sort(data, s=1)
            self.assertEqual(out, sorted(data),
                             "falhou com sondagem degenerada, n={0}".format(n))

    def test_stable_variant_preserves_order_of_equal_keys(self):
        """Testemunhas compartilhadas => chaves iguais recebem a mesma
        estimativa => mesmo balde => ordem original preservada.
        Combinado com a insercao estrita da Fase 2, o metodo e estavel."""
        random.seed(11)
        keys = [random.choice([3, 1, 4, 1, 5]) for _ in range(300)]
        data = _labelled(keys)
        out, _ = osj_sort(data, shared_witnesses=True)
        expected = sorted(data, key=lambda it: it.key)   # sorted e estavel
        self.assertEqual(_signature(out), _signature(expected))

    def test_independent_variant_sorts_but_is_not_guaranteed_stable(self):
        """A variante independente ordena corretamente; a estabilidade nao e
        garantida e nao e reivindicada. O teste afirma apenas o que e
        verdadeiro: as chaves saem ordenadas."""
        random.seed(13)
        keys = [random.choice([3, 1, 4, 1, 5]) for _ in range(300)]
        data = _labelled(keys)
        out, _ = osj_sort(data, shared_witnesses=False)
        self.assertEqual([it.key for it in out], sorted(keys))

    def test_input_is_not_mutated(self):
        original = [5, 2, 9, 1, 5, 6]
        copy = list(original)
        my_authorial_sort(original)
        self.assertEqual(original, copy)

    def test_edge_cases(self):
        for data in ([], [42], [1, 1], [2, 1], [1, 2]):
            out, _, _ = my_authorial_sort(data)
            self.assertEqual(out, sorted(data), "falhou em {0}".format(data))

    def test_randomised_stress_many_seeds(self):
        """Corretude sob muitas execucoes independentes. Como a Fase 1 e
        aleatoria, repetir e o unico jeito honesto de testar."""
        for trial in range(60):
            random.seed(trial)
            n = random.randint(0, 120)
            data = [random.randint(-50, 50) for _ in range(n)]
            out, _, _ = my_authorial_sort(data)
            self.assertEqual(out, sorted(data),
                             "falhou no trial {0}, n={1}".format(trial, n))

    def test_various_window_widths(self):
        """O metodo deve ordenar para qualquer w >= 2, nao so para o w padrao.
        Isso confirma que a corretude vem da sobreposicao, nao da largura."""
        random.seed(17)
        data = [random.randint(0, 999) for _ in range(200)]
        for w in (2, 3, 4, 7, 16, 50, 199, 200, 500):
            out, _ = sanfona_sort(data, w=w)
            self.assertEqual(out, sorted(data), "falhou com w={0}".format(w))


# ===========================================================================
# 3. VERIFICACAO EXPERIMENTAL DA TEORIA
# ===========================================================================

def _disjoint_window_sort(arr: List[Any], w: int) -> List[Any]:
    """Variante DEFEITUOSA, com passo w em vez de w/2 (janelas disjuntas).

    Nao faz parte do algoritmo. Existe apenas para materializar, em codigo
    executavel, o contraexemplo que justifica a sobreposicao.
    """
    a = list(arr)
    n = len(a)
    if n < 2:
        return a
    w = max(2, min(w, n))
    starts = list(range(0, n - w + 1, w))
    if starts[-1] != n - w:
        starts.append(n - w)
    while True:
        moved = False
        for p in starts:
            for i in range(p + 1, p + w):
                key = a[i]
                j = i - 1
                while j >= p and a[j] > key:
                    a[j + 1] = a[j]
                    j -= 1
                    moved = True
                a[j + 1] = key
        if not moved:
            return a


class TestTheory(unittest.TestCase):

    def test_disjoint_windows_have_spurious_fixed_points(self):
        """Justificativa do passo w/2.

        Com janelas disjuntas o processo para num estado que nao e o vetor
        ordenado. [3,4,1,2] com w=2 e o menor contraexemplo; [4,5,6,1,2,3]
        com w=3 mostra que nao e um azar isolado, e sim uma familia.
        """
        for data, w in (([3, 4, 1, 2], 2), ([4, 5, 6, 1, 2, 3], 3)):
            defeituoso = _disjoint_window_sort(data, w)
            self.assertNotEqual(defeituoso, sorted(data),
                                "o contraexemplo deveria falhar: {0}".format(data))
            self.assertEqual(defeituoso, data,
                             "o estado deveria ser um ponto fixo: {0}".format(data))

            correto, _ = sanfona_sort(data, w=w)     # passo w/2
            self.assertEqual(correto, sorted(data),
                             "com sobreposicao deveria ordenar: {0}".format(data))

    def test_potential_function_bound_on_swaps(self):
        """Corolario da prova de termino: o total de trocas de vizinhos em
        toda a execucao e no maximo Inv(A) inicial, e portanto no maximo
        n(n-1)/2. Verificado inclusive no pior caso (vetor reverso)."""
        random.seed(19)
        casos = {
            "aleatorio": [random.randint(0, 999) for _ in range(150)],
            "reverso": list(range(150, 0, -1)),
            "ordenado": list(range(150)),
            "repetidos": [random.choice([1, 2, 3]) for _ in range(150)],
        }
        for nome, data in casos.items():
            n = len(data)
            inv0 = inversions(data)
            out, st = sanfona_sort(data)
            self.assertEqual(out, sorted(data))
            self.assertLessEqual(st.shifts, n * (n - 1) // 2,
                                 "limite n(n-1)/2 violado em {0}".format(nome))
            self.assertEqual(st.shifts, inv0,
                             "cada troca de vizinhos deve desfazer exatamente "
                             "uma inversao, portanto o total de trocas deve "
                             "igualar Inv(A) inicial; falhou em {0}".format(nome))

    def test_reverse_vector_maximises_the_potential(self):
        """O cenario de estresse da suite obrigatoria e exatamente o vetor
        que maximiza a funcao potencial da analise."""
        for n in (2, 5, 10, 40):
            self.assertEqual(inversions(list(range(n, 0, -1))), n * (n - 1) // 2)

    def test_sorted_input_terminates_in_a_single_pass(self):
        """Melhor caso da Fase 2: nenhuma movimentacao, uma unica varredura."""
        data = list(range(500))
        out, st = sanfona_sort(data)
        self.assertEqual(out, data)
        self.assertEqual(st.passes, 1)
        self.assertEqual(st.shifts, 0)

    def test_phase1_reduces_displacement(self):
        """A Fase 1 deve entregar a Fase 2 um vetor com deslocamento maximo
        muito menor que o do vetor original. E a razao de ela existir."""
        random.seed(23)
        n = 900
        data = list(range(n, 0, -1))          # deslocamento maximo ~ n
        antes = max_displacement(data)
        st = Stats()
        from osj import _phase1_independent, default_s
        depois_vec = _phase1_independent(list(data), default_s(n), random, st)
        depois = max_displacement(depois_vec)
        self.assertLess(depois, antes / 4.0,
                        "a sondagem deveria reduzir substancialmente o "
                        "deslocamento: antes={0}, depois={1}".format(antes, depois))

    def test_each_sweep_advances_half_a_window(self):
        """Lema do avanco (Secao 4.2 do relatorio).

        Enquanto o deslocamento a esquerda exceder w/2, cada varredura o
        reduz em pelo menos w/2; a varredura que encerra a Fase 2 fecha em
        zero. Dirige uma varredura por vez pela funcao privada _sweep, porque
        o laco ate o ponto fixo tornaria o estado intermediario inobservavel.
        Mais de uma largura de janela, para nao verificar coincidencia de w.
        """
        from osj import _phase1_independent, _sweep

        random.seed(29)
        n = 240
        sabotada = _phase1_independent(
            [random.randint(0, 999) for _ in range(n)], 1, random, Stats())
        casos = {
            "reverso": list(range(n, 0, -1)),
            "sondagem sabotada com s=1": sabotada,
        }

        for nome, data in casos.items():
            for w in (4, 9, 16, 40):
                passo = w // 2
                a = list(data)
                st = Stats()
                antes = max_left_displacement(a)
                while True:
                    movimentou = _sweep(a, w, st)
                    depois = max_left_displacement(a)
                    if antes > passo:
                        self.assertLessEqual(
                            depois, antes - passo,
                            "lema do avanco (Sec. 4.2) violado: uma varredura "
                            "deveria reduzir o deslocamento a esquerda em pelo "
                            "menos w/2={0}, mas foi de {1} para {2} em '{3}' "
                            "com w={4}".format(passo, antes, depois, nome, w))
                    antes = depois
                    if not movimentou:
                        break
                self.assertEqual(
                    antes, 0,
                    "a varredura sem troca de vizinhos deveria fechar o "
                    "deslocamento a esquerda em zero (Sec. 3.2); sobrou {0} "
                    "em '{1}' com w={2}".format(antes, nome, w))
                self.assertEqual(a, sorted(data),
                                 "'{0}' com w={1}".format(nome, w))

    def test_passes_are_bounded_by_the_advance_lemma(self):
        """Limite de varreduras que sustenta o pior caso (Secao 4.3).

        O lema do avanco da P <= ceil(Dis_esq / floor(w/2)) + 1, e como
        Dis_esq < n isso vale P <= 2n/w + 2. Aqui a Sondagem e sabotada com
        s = 1 para entregar a Fase 2 um vetor quase maximamente desordenado
        sem depender de sorte, e a constante usada na asserticao e 4 - o
        dobro da que o lema prova, para nao transformar variacao amostral em
        falha. Observado nesta suite: entre 1,4 e 1,95 vezes n/w.

        Usa o contador publico Stats.passes apos ordenacao completa, como o
        teste do melhor caso ja faz.
        """
        constante = 4.0
        for n in (200, 400, 800, 1600, 3000):
            random.seed(31)
            data = [random.randint(0, 10 * n) for _ in range(n)]
            out, st = osj_sort(data, s=1)
            self.assertEqual(out, sorted(data), "n={0}".format(n))
            limite = constante * n / st.w + 2
            self.assertLessEqual(
                st.passes, limite,
                "o pior caso O(n^2) da Secao 4.3 depende de P = O(n/w) pelo "
                "lema do avanco; com n={0} e w={1} isso da no maximo {2:.1f} "
                "varreduras, mas foram {3}".format(n, st.w, limite, st.passes))


if __name__ == "__main__":
    unittest.main(verbosity=2)
