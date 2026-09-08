"""
TRABALHO PRATICO 1 (TP1)
Disciplina: Analise e Projetos de Algoritmos (APA)
Aluno: Bruno da Silva Rocha

Algoritmo autoral: OSJ - Ordenacao por Sondagem e Janelas.
A implementacao, a documentacao do raciocinio projetual e a prova de termino
estao em osj.py. Este arquivo cumpre a interface exigida pelo enunciado.

Resumo do metodo:
  Fase 1 (Sondagem)  - cada elemento estima seu posto final consultando s
                       testemunhas sorteadas e salta para a posicao estimada.
                       Fase heuristica: pode errar sem comprometer a corretude.
  Fase 2 (Sanfona)   - janela de largura w varre o vetor com passo w/2,
                       ordenando por insercao cada trecho, ate uma passada
                       sem movimentacao. Esta fase sozinha ordena qualquer
                       entrada: e nela que mora toda a corretude.

Execute test_osj.py para a suite completa (42 testes).
"""

from typing import Any, List, Tuple
import unittest

from osj import my_authorial_sort as _osj


def my_authorial_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """OSJ - Ordenacao por Sondagem e Janelas.

    Retorno: (lista_ordenada, total_comparacoes, total_movimentacoes)
    """
    return _osj(arr)


# =============================================================================
# SUITE DE TESTES AUTOMATICA DE VALIDACAO
# =============================================================================
class TestStudentAuthorialSort(unittest.TestCase):
    def assert_sorted(self, original: List, result: List):
        self.assertEqual(len(result), len(original), "Tamanho divergente!")
        self.assertEqual(sorted(original), result, "A lista nao foi ordenada corretamente!")

    def test_empty(self):
        res, _, _ = my_authorial_sort([])
        self.assert_sorted([], res)

    def test_single(self):
        res, _, _ = my_authorial_sort([99])
        self.assert_sorted([99], res)

    def test_sorted(self):
        data = list(range(100))
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_reverse(self):
        data = list(range(100, 0, -1))
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_identical(self):
        data = [5] * 50
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_random(self):
        import random
        random.seed(42)
        data = [random.randint(-1000, 1000) for _ in range(200)]
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)


if __name__ == "__main__":
    print("Executando testes unitarios no algoritmo autoral OSJ...")
    unittest.main(verbosity=2)
