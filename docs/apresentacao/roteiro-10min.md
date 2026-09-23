# Roteiro de apresentação — OSJ (10 min, duas pessoas)

**Bruno da Silva Rocha · Pietro M. Prauchner**

Versão curta e dividida do [`roteiro.md`](./roteiro.md). Os slides serão refeitos a
partir deste arquivo, então **nada aqui vem dos slides antigos**: cada afirmação e
cada número foi conferido no código (`python/osj.py`, `python/test_osj.py`), na
saída de `python/exemplo_didatico.py` ou nas tabelas versionadas em `resultados/`.
A coluna **Fonte** diz onde conferir.

> **Quem é A e quem é B** fica a critério da dupla. A divisão foi feita para que
> cada um fale ~5 min e defenda uma metade inteira: **A** fica com *o que o
> algoritmo faz e por que está certo*; **B** com *quanto custa, como foi medido e
> o que é autoral*.

---

## Cronometragem

| # | Bloco | Quem | Tempo | Acumulado |
|---:|---|:---:|---:|---:|
| 1 | Abertura e ideia | A | 0:40 | 0:40 |
| 2 | Duas fases, duas responsabilidades | A | 1:00 | 1:40 |
| 3 | Por que o passo é `w/2` | A | 1:00 | 2:40 |
| 4 | Exemplo numérico | A | 1:20 | 4:00 |
| 5 | Corretude: término e ponto fixo | A | 0:50 | **4:50** |
| 6 | De onde vem o `n^{5/3}` | B | 1:15 | 6:05 |
| 7 | Lema do avanço e pior caso | B | 0:50 | 6:55 |
| 8 | O que os experimentos mostram | B | 1:15 | 8:10 |
| 9 | O que é autoral (e o que não é) | B | 0:45 | 8:55 |
| 10 | Testes, autoria e fechamento | B | 0:55 | **9:50** |

A: 4min50 · B: 5min00 · total **9min50**. A conta usa ~130 palavras por minuto;
os textos entre aspas estão dimensionados para isso. Se precisar cortar, os blocos
**7** e **9** encolhem para uma frase cada (−1 min) sem quebrar a linha do
argumento. Os blocos **2** e **3** não se cortam: são a tese do trabalho.

---

## Apresentador A — o algoritmo e a corretude (≈ 4min50)

### 1 · Abertura e ideia — 0:40

> "O nosso método se chama OSJ, Ordenação por Sondagem e Janelas. A ideia vem de
> uma pesquisa de boca de urna: ninguém pergunta a todo mundo; você pergunta a uma
> amostra e estima o resultado. No OSJ, cada elemento faz isso — consulta alguns
> outros elementos sorteados e estima em que posição deveria estar. Isso deixa o
> vetor *quase* ordenado. O resto da apresentação é sobre esse *quase*."

| Afirmação | Fonte |
|---|---|
| Cada elemento consulta `s` testemunhas sorteadas e conta quantas são menores | `osj.py::_phase1_independent` |

### 2 · Duas fases, duas responsabilidades — 1:00

> "O algoritmo tem duas fases. A primeira, a **Sondagem**, é aleatória e **pode
> errar**. Ela conta quantas das `s` testemunhas são menores, e usa a fração
> `c/s` para jogar o elemento numa posição estimada. A segunda, a **Sanfona**, é
> determinística: uma janela de largura `w` percorre o vetor ordenando cada trecho
> por inserção, e repete até uma varredura inteira sem mover nada.
>
> A decisão de projeto é esta: a Fase 1 responde só pelo **desempenho**; a Fase 2
> responde sozinha pela **corretude**. E isso não fica só no argumento. A função
> `sanfona_sort` é o algoritmo sem a Fase 1, e passa em todos os cenários
> obrigatórios. E há um teste que sabota a Sondagem com uma única testemunha e
> ainda exige saída perfeita."

| Afirmação | Fonte |
|---|---|
| Posição estimada `= (c·(n−1)) // s` | `osj.py:206` |
| Fase 2 repete até uma varredura sem movimentação | `osj.py::_phase2` |
| `sanfona_sort` passa nos 10 cenários obrigatórios | `test_osj.py::TestSanfonaOnly` |
| Sondagem sabotada com `s = 1`, saída ainda correta | `test_osj.py::test_correctness_does_not_depend_on_phase1` |

### 3 · Por que o passo é `w/2` — 1:00

> "Um detalhe decide se o algoritmo está certo: a janela anda **meia largura** por
> vez, e não uma largura inteira. Vejam por quê. Pegue `[3, 4, 1, 2]` com `w = 2`
> e janelas que não se sobrepõem: a primeira janela é `[3, 4]`, já ordenada; a
> segunda é `[1, 2]`, já ordenada. Nada se move, o algoritmo para, e a saída está
> **errada**. O `4` e o `1` nunca estiveram na mesma janela.
>
> Com passo `w/2`, todo par de vizinhos cai em alguma janela. Então, quando uma
> varredura termina sem mover nada, cada elemento é menor ou igual ao seguinte, e
> o vetor está ordenado. Isso é **corretude**, não otimização. Também está no
> código como teste, e `[4,5,6,1,2,3]` com `w = 3` mostra que não é um caso isolado,
> é uma família inteira de falhas."

| Afirmação | Fonte |
|---|---|
| `step = max(1, w // 2)` e última janela encostada em `n − w` | `osj.py:158-162` |
| Versão disjunta para em `[3,4,1,2]` e em `[4,5,6,1,2,3]`; sobreposta ordena | `test_osj.py::test_disjoint_windows_have_spurious_fixed_points` |

### 4 · Exemplo numérico — 1:20

Entrada de 12 elementos, `s = 4`, `w = 4`, passo 2 (saída de `exemplo_didatico.py`).

> "Um exemplo real, com 12 números. Depois da Sondagem o vetor está bem melhor: as
> inversões, os pares fora de ordem, caem de **24 para 16**. Mas olhem o `54`:
> ele sorteou as testemunhas `88, 96, 96 e 54`, nenhuma menor que ele, estimou
> zero e foi para a **posição 0**, antes do `42`, que foi para a posição 2. A
> Sondagem errou feio aqui. E não importa: a Sanfona precisa de **duas varreduras**
> para ordenar, e de uma terceira que não move nada, que é o sinal de parada.
>
> Um número para guardar: a Fase 2 fez exatamente **16 trocas de vizinhos**, e o
> vetor que ela recebeu tinha exatamente **16 inversões**. Não é coincidência, é
> o próximo slide."

| Afirmação | Fonte |
|---|---|
| Inv 24 → 16 após a Fase 1; deslocamento máximo 7 → 6 | saída de `exemplo_didatico.py` |
| `54` sorteia `[88, 96, 96, 54]`, `c = 0`, vai para a posição 0 | idem |
| Passada 1 → Inv = 2; passada 2 → Inv = 0; passada 3 sem movimentação | idem |
| 16 trocas de vizinhos = Inv após a Fase 1 = 16; totais 106 comparações, 118 movimentações | idem |

### 5 · Corretude: término e ponto fixo — 0:50

> "A corretude tem duas partes. **Término:** a inserção dentro da janela só troca
> elementos **vizinhos**, e cada troca de vizinhos fora de ordem desfaz exatamente
> **uma** inversão. O número de inversões é inteiro, nunca negativo e começa em no
> máximo `n(n−1)/2`, então o algoritmo não roda para sempre. O 16 = 16 do exemplo
> é esse argumento visto na prática, e a suíte confere essa igualdade de forma
> exata em quatro tipos de entrada. **Ponto fixo:** pelo slide anterior, quando o
> algoritmo para, o vetor está ordenado.
>
> Até aqui: o que o algoritmo faz e por que está certo. O [B] mostra agora quanto
> ele custa."

| Afirmação | Fonte |
|---|---|
| Comparação estrita `a[j] > key`, só desloca uma casa | `osj.py::_insertion_window` |
| `shifts == Inv(A₀)` exato em aleatório, reverso, ordenado e com repetidos | `test_osj.py::test_potential_function_bound_on_swaps` |
| O algoritmo nunca calcula `Inv`; `inversions()` é só instrumentação | `osj.py:42-44`, `osj.py::inversions` |

---

## Apresentador B — custo, evidência e autoria (≈ 5min00)

### 6 · De onde vem o `n^{5/3}` — 1:15

> "O custo tem duas parcelas que puxam em sentidos opostos. A Sondagem faz
> exatamente `n·s` comparações: mais testemunhas, mais caro. Mas o erro da
> estimativa cai com `1/√s`, então o deslocamento que sobra é da ordem de `n/√s`.
> A janela precisa ser desse tamanho, e cada varredura custa por volta de `n·w`.
> Somando: `T(s) ≈ n·s + n²/√s`.
>
> Derivando e igualando a zero: `n − ½·n²·s^{−3/2} = 0`, então `s` é da ordem de
> `n^{2/3}`. E `T = n·n^{2/3} = n^{5/3}`. O ótimo fica onde **as duas fases custam
> o mesmo**, e é por isso que o código usa `s` e `w` iguais, os dois `n^{2/3}`.
>
> Por que `Θ` e não só `O`: as `n·s` comparações da Sondagem acontecem em **toda**
> execução, sem olhar a entrada. Isso dá a cota inferior de graça."

| Afirmação | Fonte |
|---|---|
| Fase 1 custa `n·s` comparações, incondicionalmente | `osj.py:198-205` (docstring: "Custo: n*s") |
| Desvio do estimador `O(1/√s)` → deslocamento `O(n/√s)` → `s = Θ(n^{2/3})` | docstring de `osj.py::default_s` |
| `w` na ordem do deslocamento, `= n^{2/3}` | `osj.py::default_w` |

### 7 · Lema do avanço e pior caso — 0:50

> "Uma lacuna que encontramos na revisão: a análise dependia de que cada varredura
> empurra os elementos atrasados pelo menos meia janela para a esquerda, e isso
> não estava provado. Viramos isso num lema, com prova, e ele depende de duas
> coisas do código: a sobreposição das janelas **e** a varredura da esquerda para
> a direita. A suíte mede isso varredura a varredura.
>
> A consequência é o pior caso: no máximo uns `2n/w` varreduras, cada uma de custo
> `n·w`, então `O(n²)`, o mesmo teto do Insertion Sort. Sem o lema, o único limite
> provado dava `O(n³)`."

| Afirmação | Fonte |
|---|---|
| A ordem crescente dos inícios é premissa do lema | docstring de `osj.py::_sweep` |
| Cada varredura reduz o deslocamento à esquerda em ≥ `w/2` (reverso e sondagem sabotada, `w ∈ {4, 9, 16, 40}`) | `test_osj.py::test_each_sweep_advances_half_a_window` |
| `P ≤ 2n/w + 2`; observado entre 1,4 e 1,95 × `n/w` | `test_osj.py::test_passes_are_bounded_by_the_advance_lemma` |

### 8 · O que os experimentos mostram — 1:15

> "Três resultados. **Primeiro, o expoente.** Num gráfico log-log a inclinação é o
> expoente. Até `N = 10 mil`, as comparações dão **1,64** e o tempo dá **1,68**,
> contra 1,667 previsto. O tempo é uma medida independente da nossa contagem, e
> concorda. E a Fase 2 fecha em 3 a 5 varreduras em toda a faixa, como a análise
> prevê.
>
> **Segundo, o nicho.** Com `N = 1000` aleatório o OSJ faz 130 mil comparações; o
> Insertion faz 248 mil; o Merge, 9 mil. O OSJ fica entre os quadráticos e os
> `n log n`, onde a conta disse que ficaria. Ele não compete com o Merge, e não
> tentamos que competisse.
>
> **Terceiro, e isto é uma limitação:** com `N = 2000`, o vetor já ordenado custa
> 398 mil comparações e o invertido 409 mil, só **3%** de diferença. O OSJ não
> aproveita entrada fácil, porque a Sondagem é paga sempre. O mesmo dado mostra o
> lado bom: a cota vale para qualquer entrada, não só em média."

| Afirmação | Fonte |
|---|---|
| Expoente 1,6408 (comparações) e 1,6778 (tempo), `N` de 250 a 10.000 | `resultados/escalabilidade_osj.csv` |
| 3,4 a 5,2 varreduras médias, de `N = 250` a `N = 10⁴` | idem, coluna `varreduras` |
| `N = 1000`, random: OSJ 129.729 · Insertion 248.229 · Merge 8.709 comparações | `resultados/benchmark_osj.md` |
| `N = 2000`: sorted 397.562 · random 402.550 · reverse 409.441 (≈ 3%) | idem |

### 9 · O que é autoral (e o que não é) — 0:45

> "O código tem uma segunda variante, em que todos os elementos consultam a
> **mesma** amostra de testemunhas. Ela é bem mais rápida, expoente 1,17 contra
> 1,59, e ainda é estável. Investigamos o porquê. Com amostra comum, a posição
> estimada passa a crescer junto com o valor, e isso é exatamente a fase de
> distribuição do **Sample Sort**, um algoritmo conhecido. Então a variante rápida
> é a **menos** autoral, e está declarada como adaptação.
>
> A contribuição é a variante independente, em que a estimativa **não** acompanha
> o valor. O exemplo mostrou isso: o 54 foi parar antes do 42."

| Afirmação | Fonte |
|---|---|
| Variante compartilhada: amostra ordenada única + busca binária → estimativa monótona no valor | `osj.py::_phase1_shared` |
| Expoente de comparações 1,169 (compartilhada) vs 1,591 (independente), `N ≤ 2000` | `resultados/benchmark_osj.md`, tabela de expoentes |
| A entrega usa a variante independente | `student_template.py:25` → `osj.my_authorial_sort` |
| Não-monotonicidade: `54 → 0`, `42 → 2` | saída de `exemplo_didatico.py` |

### 10 · Testes, autoria e fechamento — 0:55

> "A validação são **44 testes**: os 10 cenários obrigatórios rodando contra as
> duas variantes *e* contra a Sanfona sozinha, mais testes de propriedade e testes
> que conferem a teoria: a igualdade trocas = inversões, o contraexemplo do passo
> `w` e o lema do avanço. Se um teorema do relatório estiver errado, a suíte quebra.
>
> Sobre autoria: usamos o Claude, da Anthropic. A implementação e a redação estão
> declaradas como da ferramenta. A escolha da direção do método, as duas ideias
> centrais da prova de término e as correções da revisão, como o lema do avanço e
> o pior caso, são nossas. Está tudo no relatório, seção 8.
>
> Para fechar, uma frase: **a fase que pode errar nunca é a fase que decide a
> corretude.**"

| Afirmação | Fonte |
|---|---|
| 44 testes = 3 × 10 obrigatórios + 7 de propriedade + 7 de teoria | `test_osj.py` (`uv run python test_osj.py -v`) |
| Papéis da ferramenta e dos alunos, e as correções de 09/09/2026 | `README.md` §8 (não é código; a declaração de autoria só existe ali) |

---

## Perguntas prováveis

Quem responde é quem apresentou o bloco. Respostas em uma linha, com onde mostrar
no código se pedirem.

| Pergunta | Quem | Resposta | Mostrar |
|---|:---:|---|---|
| Como garante corretude se é aleatório? | A | A Fase 1 não garante nada; a Fase 2 ordena sozinha. | `sanfona_sort`, `osj.py:291` |
| Por que o passo não pode ser `w`? | A | Janelas disjuntas param em estado errado: `[3,4,1,2]`. | `osj.py:158` e o teste de janelas disjuntas |
| Por que existe a passada 3 do exemplo? | A | O sinal de parada é "não moveu nada", custo `O(1)`. Saber que já está ordenado exigiria calcular `Inv`, que custa mais que ordenar. | `osj.py::_phase2` |
| É estável? | A | A variante independente não: chaves iguais podem receber estimativas diferentes. A compartilhada é. | docstrings de `_phase1_independent` e `_phase1_shared` |
| Por que o Insertion é mais rápido em tempo com `N = 1000`, se o OSJ compara menos? | B | 16,6 ms contra 23,9 ms: o OSJ tem mais sobrecarga por operação em Python (sorteio, baldes). Em comparações ele já ganha (130 mil contra 248 mil), e o expoente menor faz a vantagem crescer com `N`. | `resultados/benchmark_osj.md` |
| É caso médio como no Quick Sort? | B | Não. A média é sobre o sorteio do algoritmo, e vale para toda entrada; os 3% entre distribuições medem isso. | `benchmark_osj.md`, `N = 2000` |
| Isso não é Sample Sort / Learned Sort? | B | A variante compartilhada é Sample Sort, e está declarada. A independente não tem mapa monótono valor → posição. | `_phase1_shared` × `_phase1_independent` |
| Por que parou em `N = 10⁴`? | B | ~1,2 s por execução, 5 repetições; o expoente já estabilizou. | `escalabilidade_osj.csv` |
| Quanto espaço usa? | B | `Θ(n)`: a Fase 1 monta `n` baldes. | `osj.py:196` |
| Os números se reproduzem? | B | `random.seed(42)`, `uv.lock` versionado, `resultados/` versionado. | `benchmark_osj.py`, `scaling_osj.py` |

---

## Para quem for montar os slides novos

Um slide por bloco (10 slides). O que cada um precisa mostrar, e só isso:

| # | Conteúdo visual |
|---:|---|
| 1 | Nome do método, nomes da dupla, a frase das duas fases |
| 2 | Duas caixas lado a lado: Sondagem (aleatória, desempenho) e Sanfona (determinística, corretude) |
| 3 | `[3, 4, 1, 2]` com janelas disjuntas (para errado) × sobrepostas (ordena) |
| 4 | O vetor antes e depois da Fase 1, com o `54` destacado; as três passadas; o `16 = 16` |
| 5 | Uma linha: "cada troca de vizinhos desfaz 1 inversão" + `≤ n(n−1)/2` |
| 6 | `T(s) = n·s + n²/√s`, a derivada e `s* = n^{2/3}` → `n^{5/3}` |
| 7 | "≥ `w/2` por varredura" → `O(n/w)` varreduras × `O(n·w)` = `O(n²)` |
| 8 | Gráfico log-log (`resultados/escalabilidade_loglog.png`) + os três números de `N = 2000` |
| 9 | Variante compartilhada (monótona = Sample Sort) × independente (54 antes do 42) |
| 10 | "44 testes", uma linha de autoria, e a frase final |

---

## Checklist antes de apresentar

- [ ] `cd python && uv run python test_osj.py` na máquina da apresentação: **44/44**
- [ ] Ensaiar cronometrando, cada um a sua metade: A em ≤ 5:00, B em ≤ 5:00
- [ ] Ensaiar a passagem do bloco 5 para o 6 (é a única troca de apresentador)
- [ ] Ter `python/osj.py` e `README.md` abertos em abas, para a arguição
