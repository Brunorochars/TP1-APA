# OSJ — Ordenação por Sondagem e Janelas

**Trabalho Prático 1 — Análise e Projeto de Algoritmos**
Aluno: Bruno da Silva Rocha

---

## Resumo

O **OSJ** é um método de ordenação autoral construído sobre uma separação deliberada de responsabilidades entre duas fases:

- **Fase 1 — Sondagem:** cada elemento estima o próprio posto final consultando `s` "testemunhas" sorteadas do vetor e salta direto para a posição estimada. É uma fase puramente **heurística e aleatorizada**: ela pode errar.
- **Fase 2 — Sanfona:** uma janela de largura `w` varre o vetor com passo `w/2`, ordenando por inserção cada trecho coberto, até uma varredura inteira ocorrer sem nenhuma movimentação. É a fase **determinística** que ordena qualquer entrada sozinha.

A tese central do projeto é que **a Fase 1 não pode errar de modo fatal, apenas de modo caro**. Toda a corretude mora na Fase 2; a Fase 1 responde só pelo desempenho. Isso permite empregar uma heurística agressiva e aleatória sem qualquer risco de saída incorreta.

Com os parâmetros equilibrados em `s = w = Θ(n^{2/3})`, o custo esperado é **Θ(n^{5/3})** — uma classe intermediária entre `n log n` e `n²`. O expoente empírico medido foi **1,59**, contra **1,667** previsto pela dedução.

---

## Como executar

```bash
uv sync                              # monta o ambiente a partir do uv.lock

cd python
uv run python test_osj.py -v         # suíte completa: 42 testes
uv run python student_template.py    # interface exigida pelo enunciado
uv run python exemplo_didatico.py    # exemplo numérico passo a passo
uv run python scaling_osj.py         # medição do expoente de escalabilidade
uv run python benchmark_osj.py       # benchmark completo + gráficos em ../resultados/
```

O algoritmo e a suíte de testes **não têm dependência alguma** além da biblioteca
padrão: `python test_osj.py` roda num Python 3.11 limpo, sem `uv`. O ambiente
existe por causa do `matplotlib`, usado só na geração dos gráficos — e o
`uv.lock` fixa as versões exatas para que as medições relatadas aqui se
reproduzam.

---

## 1. Concepção e raciocínio projetual

### 1.1 A intuição

Os métodos clássicos por comparação descobrem a posição de um elemento **comparando-o repetidamente com os outros**. O Insertion Sort desliza cada elemento até seu lugar; o Selection Sort varre o resto do vetor para achar o mínimo. Em todos, a informação sobre "onde este elemento deve ficar" é construída aos poucos, por contato direto.

A pergunta que originou o OSJ foi: **e se cada elemento pudesse estimar sua posição final por amostragem, sem falar com todo mundo?**

A metáfora é uma eleição com pesquisa de boca de urna. Para saber sua colocação exata num grupo de mil pessoas, você precisaria comparar-se com as 999 restantes. Mas se você perguntar a **quarenta pessoas sorteadas** quantas são menores que você e trinta responderem que sim, você conclui com boa confiança que está por volta do percentil 75 — e pode ir direto para lá. A estimativa não é exata, mas custa 40 perguntas em vez de 999, e o erro é **quantificável**.

Daí vem a Fase 1. E daí vem imediatamente o problema: o vetor resultante fica *quase* ordenado, não ordenado. Alguém precisa consertar os erros residuais.

### 1.2 O reparo: por que janelas, e por que sobrepostas

O conserto precisa ser **local**, porque os erros são locais: a sondagem não teleporta um elemento para o outro extremo do vetor, ela o coloca perto do lugar certo. Um reparo que reexamine o vetor inteiro desperdiçaria a informação que a Fase 1 comprou.

Daí a metáfora da sanfona: uma janela de largura `w` percorre o vetor como uma onda, alisando localmente o que passa embaixo dela, e repete o movimento até que uma passada inteira não encontre mais nada para alisar.

A decisão de projeto mais importante do método está no **passo** dessa janela. Se as janelas forem disjuntas (passo `w`), o processo adquire **pontos fixos espúrios** — estados estáveis que não são o vetor ordenado:

```
A = [3, 4, 1, 2],  w = 2,  passo = 2

  janela [0:2] = [3, 4]  →  já ordenada, nada acontece
  janela [2:4] = [1, 2]  →  já ordenada, nada acontece
  nenhuma movimentação → o algoritmo encerra

  Saída: [3, 4, 1, 2]   ← ERRADO
```

Não é um azar isolado: `[4,5,6,1,2,3]` com `w=3` falha do mesmo modo, e a construção se generaliza para qualquer bloco internamente ordenado na posição errada — é uma família infinita de falhas.

Com **passo `w/2`**, as janelas se sobrepõem e todo par de posições vizinhas `(k, k+1)` passa a estar contido em alguma janela. Isso elimina todos os pontos fixos exceto um:

> **O único ponto fixo do processo com janelas sobrepostas é o vetor ordenado.**

Essa é a razão de o algoritmo funcionar, e o contraexemplo acima está codificado como teste automatizado em `test_osj.py::TestTheory::test_disjoint_windows_have_spurious_fixed_points`.

### 1.3 A separação de responsabilidades

| | responsabilidade | pode falhar? | consequência de falhar |
| :--- | :--- | :--- | :--- |
| **Fase 1** | desempenho | sim, é aleatória | a Fase 2 fica mais cara |
| **Fase 2** | corretude | não, é determinística | — |

Consequência prática: a aleatoriedade da sondagem **nunca** produz saída errada. Para tornar isso verificável e não apenas argumentável, o código expõe `sanfona_sort()` — o algoritmo *sem* a Fase 1 — e a suíte de testes roda **todos os cenários obrigatórios contra ela**, além de um teste que sabota deliberadamente a sondagem (`s = 1`, uma única testemunha) e confirma que a saída continua perfeita.

---

## 2. Especificação formal

### 2.1 Pseudocódigo

```
ALGORITMO OSJ(A, s, w)
  Entrada: vetor A de n elementos comparáveis; s ≥ 1; w ≥ 2
  Saída:   permutação ordenada de A

  se n ≤ 1 então devolva A                      // casos limite N=0 e N=1

  ─── FASE 1: SONDAGEM ────────────────────────────────────────────
  para i ← 0 até n−1 faça
      c ← 0
      repita s vezes
          j ← inteiro aleatório uniforme em [0, n−1]
          se A[j] < A[i] então c ← c + 1
      p̂[i] ← ⌊ (c / s) · (n−1) ⌋                // posição estimada
  B ← distribuição estável de A pelos valores de p̂   // resolve colisões

  ─── FASE 2: SANFONA ─────────────────────────────────────────────
  w ← max(2, min(w, n))                          // janela nunca excede o vetor
  passo ← ⌊w / 2⌋
  inícios ← { 0, passo, 2·passo, … } ∪ { n − w } // a última encosta na borda

  repita
      movimentou ← falso
      para cada p em inícios faça
          se INSERÇÃO(B, p, p+w) moveu algo então movimentou ← verdadeiro
      até movimentou = falso

  devolva B
```

A rotina `INSERÇÃO` é a ordenação por inserção clássica restrita ao intervalo, com comparação estrita (`B[j] > chave`), o que a torna estável e — crucialmente para a análise — faz com que **só troque elementos vizinhos**.

### 2.2 Exemplo numérico passo a passo

Entrada com 12 elementos, `s = 4`, `w = 4`. O rastro abaixo é a saída real de `exemplo_didatico.py`, não uma ilustração idealizada.

```
Entrada  : [42, 7, 19, 88, 3, 61, 25, 54, 12, 77, 33, 96]
Ordenado : [3, 7, 12, 19, 25, 33, 42, 54, 61, 77, 88, 96]
Inv(A) inicial = 24   |   deslocamento máximo = 7
```

**Fase 1 — cada elemento consulta 4 testemunhas:**

```
  valor |        testemunhas sorteadas |   c |    c/s |  posição
  ------------------------------------------------------------------
     42 |             [54, 19, 96, 77] |   1 |    1/4 |        2
      7 |              [3, 88, 96, 25] |   1 |    1/4 |        2
     19 |              [96, 3, 12, 88] |   2 |    2/4 |        5
     88 |             [33, 96, 54, 61] |   3 |    3/4 |        8
      3 |             [25, 12, 96, 77] |   0 |    0/4 |        0
     61 |              [88, 3, 12, 96] |   2 |    2/4 |        5
     25 |              [61, 12, 7, 96] |   2 |    2/4 |        5
     54 |             [88, 96, 96, 54] |   0 |    0/4 |        0
     12 |             [96, 33, 19, 12] |   0 |    0/4 |        0
     77 |             [88, 25, 42, 61] |   3 |    3/4 |        8
     33 |              [33, 25, 54, 7] |   2 |    2/4 |        5
     96 |             [96, 96, 19, 61] |   2 |    2/4 |        5

  Vetor após a Fase 1: [3, 54, 12, 42, 7, 19, 61, 25, 33, 96, 88, 77]
  Inv(A) = 16 (era 24)   |   deslocamento máximo = 6 (era 7)
```

Repare no elemento `54`, que sorteou `[88, 96, 96, 54]` e não encontrou nenhuma testemunha menor: estimou `c/s = 0` e foi parar na posição 0. **A Fase 1 errou feio com ele** — e o algoritmo continua correto, porque a Fase 2 conserta.

**Fase 2 — janelas de largura 4 com passo 2:**

```
  Passada 1:
    janela [ 0: 4]  [3, 54, 12, 42]  -> [3, 12, 42, 54]     <- ordenou
    janela [ 2: 6]  [42, 54, 7, 19]  -> [7, 19, 42, 54]     <- ordenou
    janela [ 4: 8]  [42, 54, 61, 25] -> [25, 42, 54, 61]    <- ordenou
    janela [ 6:10]  [54, 61, 33, 96] -> [33, 54, 61, 96]    <- ordenou
    janela [ 8:12]  [61, 96, 88, 77] -> [61, 77, 88, 96]    <- ordenou
    estado: [3, 12, 7, 19, 25, 42, 33, 54, 61, 77, 88, 96]   Inv = 2

  Passada 2:
    janela [ 0: 4]  [3, 12, 7, 19]   -> [3, 7, 12, 19]      <- ordenou
    janela [ 2: 6]  [12, 19, 25, 42] -> [12, 19, 25, 42]
    janela [ 4: 8]  [25, 42, 33, 54] -> [25, 33, 42, 54]    <- ordenou
    janela [ 6:10]  [42, 54, 61, 77] -> [42, 54, 61, 77]
    janela [ 8:12]  [61, 77, 88, 96] -> [61, 77, 88, 96]
    estado: [3, 7, 12, 19, 25, 33, 42, 54, 61, 77, 88, 96]   Inv = 0

  Passada 3:
    (nenhuma janela move nada) -> PONTO FIXO, encerra

Saída: [3, 7, 12, 19, 25, 33, 42, 54, 61, 77, 88, 96]
Totais: 106 comparações, 118 movimentações, 16 trocas de vizinhos, 3 passadas
```

Note a **passada 3**: ela não muda nada, mas é obrigatória. É ela que *constata* o ponto fixo. O algoritmo não pode saber que terminou sem gastar uma varredura confirmando.

E note a coincidência que não é coincidência: **16 trocas de vizinhos** e `Inv = 16` ao início da Fase 2. A seção seguinte explica por quê.

---

## 3. Corretude

### 3.1 Término

> **Teorema.** A Fase 2 termina após um número finito de passadas, para qualquer entrada e qualquer `w ≥ 2`.

Define-se a **função potencial**

$$\mathrm{Inv}(A) = \#\{(i,j) : i < j \text{ e } A[i] > A[j]\}$$

o número de pares fora de ordem. Trata-se de uma grandeza **da análise, não do algoritmo**: ela não é calculada em lugar nenhum do código, e calculá-la custaria mais caro do que desfazer a desordem que ela mede. O algoritmo usa em seu lugar o sinal barato `movimentou`, de custo `O(1)`.

**Passo 1.** `Inv(A)` é um inteiro não-negativo: é a cardinalidade de um conjunto finito de pares.

**Passo 2.** Cada movimentação elementar reduz `Inv(A)` em **exatamente 1**. A inserção dentro da janela só troca posições **vizinhas** `k` e `k+1`, e apenas quando `A[k] > A[k+1]`. O par `(k, k+1)` deixa de ser inversão: −1. Qualquer outro par envolve um elemento numa posição `m ∉ {k, k+1}`, que não se move; se `m < k` ele precedia ambos e continua precedendo, se `m > k+1` ele sucedia ambos e continua sucedendo, e **não existe posição estritamente entre `k` e `k+1`**. Como nem os valores nem a ordem posicional relativa desses pares mudaram, seus status são preservados.

> A adjacência é essencial. Uma troca a distância `d` alteraria até `2d − 1` pares de uma vez, e o efeito sobre o potencial deixaria de ser unitário e previsível.

**Passo 3.** Inicialmente `Inv(A) ≤ n(n−1)/2`, pois esse é o número total de pares, e o máximo é atingido exatamente pelo **vetor estritamente reverso** — que é, não por acaso, o cenário de estresse da suíte obrigatória.

**Passo 4.** Toda passada que não encerra o laço executa ao menos uma movimentação, logo reduz `Inv(A)` em ao menos 1. Se houvesse infinitas passadas com movimentação, `Inv(A)` se tornaria negativo, contradizendo o Passo 1. Logo ocorrem no máximo `n(n−1)/2` passadas com movimentação, e a passada seguinte encerra o laço. ∎

> **Corolário (fórmula fechada para movimentações).** Como cada troca desfaz exatamente uma inversão e nenhuma inversão é criada, o número total de trocas de vizinhos em toda a execução é **exatamente `Inv(A₀)`**, onde `A₀` é o vetor no início da Fase 2 — e portanto no máximo `n(n−1)/2 = O(n²)`.

Isso é verificado experimentalmente como **igualdade exata**, não apenas como limite, em `test_osj.py::TestTheory::test_potential_function_bound_on_swaps`.

### 3.2 Corretude no ponto fixo

> **Teorema.** Se uma passada completa não produz nenhuma movimentação, o vetor está ordenado.

**Prova.** Nenhuma movimentação na passada inteira significa que **nada se moveu**, logo todas as janelas estavam simultaneamente ordenadas no início da passada e assim permaneceram. (Essa simultaneidade é o ponto delicado: numa passada comum, ordenar uma janela pode desarrumar a região de sobreposição da anterior. A preocupação desaparece exatamente quando não há movimentação.)

Tome agora um par de posições vizinhas `(k, k+1)` qualquer. Uma janela iniciada em `p` cobre `[p, p+w−1]`, portanto contém o par se e somente se `p ≤ k` e `p + w − 1 ≥ k + 1`, isto é

$$k + 2 - w \;\le\; p \;\le\; k$$

um intervalo de comprimento `w − 1`. Como os inícios de janela são múltiplos de `⌊w/2⌋ ≤ w − 1` (para `w ≥ 2`), sempre existe um início dentro desse intervalo, complementado pela janela final encostada na borda direita. Logo **todo par vizinho está contido em alguma janela**, que estava ordenada, donde `A[k] ≤ A[k+1]` para todo `k`. Um vetor cujos pares vizinhos estão todos em ordem está ordenado. ∎

O intervalo de comprimento `w − 1` mostra que o passo máximo admissível é `w − 1`; a escolha `w/2` é conservadora e favorece a convergência em menos passadas.

---

## 4. Análise assintótica

### 4.1 Fase 1 — análise probabilística

Seja `r_i` o posto verdadeiro de `A[i]` (número de elementos estritamente menores) e `p_i = r_i / n`. Cada testemunha é sorteada uniformemente, logo

$$X_i \sim \mathrm{Binomial}(s,\, p_i), \qquad \hat{p}_i = X_i/s, \qquad \mathbb{E}[\hat{p}_i] = p_i$$

**Custo.** Exatamente `n·s` comparações e `n` movimentações: **Θ(n s)**, independente da entrada.

**Erro típico.** $\mathrm{Var}(\hat p_i) = p_i(1-p_i)/s \le 1/(4s)$, portanto o desvio típico da estimativa é `O(1/√s)` e o deslocamento típico em posições é

$$\mathbb{E}\,|\hat{p}_i - p_i| \cdot n \;=\; O\!\left(\frac{n}{\sqrt{s}}\right)$$

**Erro máximo (alta probabilidade).** Pela desigualdade de Hoeffding,

$$\Pr\big[\,|\hat{p}_i - p_i| \ge \varepsilon\,\big] \;\le\; 2e^{-2s\varepsilon^{2}}$$

Aplicando união sobre os `n` elementos e tomando $\varepsilon = \sqrt{\ln(2n/\delta) / (2s)}$, com probabilidade ao menos `1 − δ` **todas** as estimativas ficam dentro de `ε`.

**Do erro de estimativa ao deslocamento.** Se todas as estimativas estão dentro de `ε`, dois elementos `i` e `j` só podem sair trocados entre si se `|p_j − p_i| ≤ 2ε`. Existem no máximo `2εn` elementos nessa faixa, logo o deslocamento de cada elemento em relação à sua posição verdadeira satisfaz

$$D \;\le\; 2\varepsilon n \;=\; O\!\left(n\sqrt{\frac{\log n}{s}}\right) \quad\text{com alta probabilidade}$$

### 4.2 Fase 2 — custo em função da desordem recebida

Cada janela custa `Θ(w)` comparações de varredura mais uma comparação por deslocamento. Com `2n/w` janelas por passada:

- **comparações por passada:** `Θ(n)` mais os deslocamentos daquela passada;
- **total de deslocamentos em todas as passadas:** exatamente `Inv(A₀)`, pelo corolário da Seção 3.1;
- **número de passadas:** cada passada reduz o deslocamento máximo em pelo menos `w/2`, logo `P = O(D/w + 1)`.

$$T_{\text{Fase 2}} \;=\; \Theta\!\left(n \cdot \Big(\tfrac{D}{w} + 1\Big)\right) \;+\; \mathrm{Inv}(A_0), \qquad \mathrm{Inv}(A_0) = O(nD)$$

### 4.3 Custo total e escolha ótima dos parâmetros

Somando as duas fases e escolhendo `w = Θ(D)` (a janela na ordem do deslocamento que a Fase 1 deixou, de modo que a Fase 2 convirja em `O(1)` passadas):

$$T(n,s) \;=\; \Theta(ns) \;+\; O\!\left(\frac{n^{2}}{\sqrt{s}}\right)$$

O primeiro termo cresce com `s`, o segundo decresce. Derivando em relação a `s` e igualando a zero:

$$n - \tfrac{1}{2}\,n^{2} s^{-3/2} = 0 \;\Longrightarrow\; s^{3/2} = \tfrac{n}{2} \;\Longrightarrow\; \boxed{s^{*} = \Theta\!\left(n^{2/3}\right)}$$

e, substituindo, `w* = Θ(D) = Θ(n / √s*) = Θ(n^{2/3})` também. Ambas as fases ficam então com o mesmo custo:

$$T(n) \;=\; \Theta\!\left(n \cdot n^{2/3}\right) \;=\; \boxed{\Theta\!\left(n^{5/3}\right)}$$

*(A versão com garantia de alta probabilidade carrega um fator `(log n)^{1/3}` adicional, oriundo do `√log n` do limite de Hoeffding.)*

### 4.4 Quadro-resumo

| Propriedade | OSJ | Observação |
| :--- | :--- | :--- |
| **Melhor caso** | `Ω(n^{5/3})` | a Fase 1 **não** é adaptativa: paga `n·s` mesmo com o vetor já ordenado |
| **Caso médio** | `Θ(n^{5/3})` | com `s = w = Θ(n^{2/3})`; confirmado empiricamente (expoente 1,59) |
| **Pior caso** | `O(n²)` | sondagem degenerada; limitado pelo corolário `Inv ≤ n(n−1)/2` |
| **Movimentações** | exatamente `Inv(A₀)` | fórmula fechada, não apenas cota |
| **Espaço auxiliar** | `Θ(n)` | baldes e vetor de saída da Fase 1 |
| **In-place** | não | a Fase 2 isolada **é** in-place, com `O(1)` extra |
| **Estabilidade** | não (variante padrão) | sim na variante de testemunhas compartilhadas — ver §5.2 |
| **Determinismo** | não | aleatorizado, mas **a corretude é determinística** |

O melhor caso merece destaque por ser uma **limitação honesta do projeto**: como a sondagem é incondicional, o OSJ gasta `Θ(n^{5/3})` mesmo num vetor já ordenado, enquanto Insertion e Bubble gastam `Θ(n)`. Os dados experimentais confirmam: 395.932 comparações no vetor ordenado contra 402.358 no aleatório para `N = 2000` — praticamente idênticos. A Seção 7 discute como corrigir isso.

---

## 5. Comparação com a literatura

### 5.1 Tabela comparativa

| Método | Melhor | Médio | Pior | Espaço | Estável | In-place |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Insertion Sort | `Θ(n)` | `Θ(n²)` | `Θ(n²)` | `O(1)` | sim | sim |
| Selection Sort | `Θ(n²)` | `Θ(n²)` | `Θ(n²)` | `O(1)` | não | sim |
| Merge Sort | `Θ(n log n)` | `Θ(n log n)` | `Θ(n log n)` | `O(n)` | sim | não |
| Quick Sort | `Θ(n log n)` | `Θ(n log n)` | `Θ(n²)` | `O(log n)` | não | sim |
| **OSJ** | `Ω(n^{5/3})` | `Θ(n^{5/3})` | `O(n²)` | `Θ(n)` | não | não |

### 5.2 Discussão crítica

**Contra o Insertion Sort.** O OSJ *contém* o Insertion Sort como caso particular: com `w = n`, a Fase 2 vira uma inserção sobre o vetor inteiro. O parâmetro `w` portanto **interpola** entre uma família de comportamentos, e o Insertion é o extremo superior dessa família. A diferença estrutural é que o Insertion paga `Θ(Inv)` comparações sobre o vetor **original**, enquanto o OSJ paga `Θ(n s)` para reduzir `Inv` antes de aplicar o mesmo mecanismo. É uma troca explícita: gastar comparações baratas de amostragem para evitar comparações caras de deslocamento. Nos dados, `N = 2000` aleatório: Insertion faria da ordem de 10⁶ comparações; o OSJ faz 402 mil.

**Contra o Merge Sort.** O Merge é assintoticamente superior (`n log n` contra `n^{5/3}`) e o OSJ não compete com ele — nem pretende. A diferença conceitual é de **onde vem a informação de ordem**: o Merge a constrói recursivamente por fusão, de forma determinística e exata; o OSJ a estima estatisticamente e depois repara o erro. O OSJ troca garantia por localidade: seu reparo é local e in-place, enquanto o Merge exige `O(n)` de espaço em toda fusão.

**Contra o Quick Sort.** Ambos são aleatorizados, mas a aleatoriedade cumpre papéis opostos. No Quick Sort, um pivô ruim degrada o algoritmo a `O(n²)` **e a aleatoriedade participa da estrutura recursiva** que produz o resultado. No OSJ, a aleatoriedade está confinada a uma fase que não pode produzir saída errada: a estrutura que garante o resultado (a Sanfona) é inteiramente determinística. Isso é uma vantagem de projeto em contextos onde a previsibilidade da corretude importa mais que a do tempo.

**Relação com o Shell Sort.** É a comparação mais delicada, e precisa ser explicitada. O Shell Sort também aplica inserções sobre subconjuntos e converge por refinamentos sucessivos. As diferenças estruturais são duas: (i) o Shell opera sobre elementos **distantes** separados por um incremento `h`, ao passo que a Sanfona opera sobre blocos **contíguos**; (ii) a sequência do Shell é **decrescente** (do grosseiro ao fino), enquanto a Sanfona mantém `w` fixo e itera até o ponto fixo. Ainda assim, ambos pertencem à mesma família conceitual de "inserção em subestruturas com convergência iterativa", e essa filiação é reconhecida aqui.

**Relação com o Sample Sort — e um resultado que exige transparência.** A variante do OSJ com **testemunhas compartilhadas** (todos os elementos consultam a mesma amostra) mede-se muito melhor: expoente empírico 1,19 contra 1,59 da variante padrão. A investigação da causa revelou que ela **deixa de ser o algoritmo proposto**: quando a amostra é comum, a posição estimada torna-se uma função **monótona** do valor, de modo que a saída da Fase 1 já está globalmente ordenada *entre* os baldes, restando desordem apenas *dentro* de cada balde. Medição confirmando, para `n = 2000`:

| variante | deslocamento máximo após a Fase 1 | inversões restantes |
| :--- | ---: | ---: |
| testemunhas independentes | 274 | 67.137 |
| testemunhas compartilhadas | 79 | 12.368 |

Distribuir elementos em baldes delimitados por quantis de uma amostra é precisamente a fase de distribuição do **Sample Sort**, técnica consolidada na literatura. Portanto: **a variante rápida é a menos autoral**, e é declarada aqui como adaptação de técnica conhecida, não como contribuição própria. A variante adotada como OSJ é a de **testemunhas independentes**, na qual cada elemento estima seu posto isoladamente, o mapa valor→posição **não** é monótono, e o comportamento resultante `Θ(n^{5/3})` não corresponde a nenhum método clássico identificado. A fronteira com a família de distribuição inteira — e não apenas com o Sample Sort — é estabelecida na §5.3.

A variante compartilhada é mantida no código (`my_authorial_sort_stable`) por dois motivos legítimos: ela é **estável** — chaves iguais recebem estimativa idêntica, caem no mesmo balde e preservam a ordem original, e a inserção estrita da Fase 2 preserva essa ordem — e serve de termo de comparação para isolar o efeito da independência das amostras.

### 5.3 Vizinhos publicados mais próximos

A estrutura "estimar a posição de cada elemento, depositá-lo lá, e concluir com um reparo determinístico" não é nova, e a honestidade exige nomear quem a publicou antes. Os quatro métodos abaixo são os vizinhos mais próximos identificados:

| Método | Como estima a posição | Reparo final | Mapa valor→posição | Exige chave numérica |
| :--- | :--- | :--- | :---: | :---: |
| **ProxmapSort** (Standish, UC Irvine, ~1987) | *map key* aplicada à chave, produzindo um *proximity map* com o início do subarranjo de destino | inserção nos subarranjos | monótono | sim |
| **Flashsort** (Neubert, *Dr. Dobb's*, 1998) | interpolação linear da chave em `[A_min, A_max]` sobre `m` classes | permutação in-place + *straight insertion* | monótono | sim |
| **Sample Sort** | busca binária da chave numa amostra ordenada de separadores | ordenação intra-balde | monótono | não |
| **Learned Sort** (Kristo et al., SIGMOD 2020) | modelo aprendido da **CDF empírica** aproxima a posição de saída de cada chave | algoritmo determinístico bom em vetores quase ordenados (Insertion Sort) | monótono | sim |
| **OSJ** (este trabalho) | comparação contra `s` testemunhas sorteadas **por elemento** | Sanfona: janelas sobrepostas até o ponto fixo | **não monótono** | **não** |

O Learned Sort é o mais próximo de todos, e a descrição dos próprios autores — aproximar a posição de saída de cada chave por um modelo e depois "aplicar um algoritmo determinístico que funciona bem em vetores quase ordenados" — é a mesma decomposição em duas fases proposta aqui. A filiação é reconhecida.

**O que separa o OSJ da família inteira é uma única propriedade: a estimativa não é função monótona do valor.** Todos os métodos acima derivam a posição de uma operação *aritmética sobre a chave* — interpolação, quantil, CDF — e portanto entregam os baldes já globalmente ordenados entre si; são algoritmos de **distribuição**, e a desordem que resta ao reparo é apenas *intra-balde*. Na Sondagem independente cada elemento é comparado com testemunhas próprias, de modo que dois elementos podem receber estimativas em ordem trocada, e a desordem residual é **global**. Três consequências:

1. **A Fase 2 não pode ser uma ordenação por balde.** Como a Fase 1 não ordena entre baldes, o reparo precisa ser uma iteração de ponto fixo sobre o vetor inteiro — é daí que a Sanfona vem, e é por isso que ela não é substituível por "ordenar cada balde".
2. **O OSJ é comparison-only.** Não faz aritmética alguma sobre os valores, e ordena qualquer tipo totalmente ordenado — a suíte exercita inteiros, negativos e ponto flutuante. ProxmapSort, Flashsort e Learned Sort exigem chaves numéricas. (O Sample Sort também é comparison-only; o que o separa do OSJ é a monotonicidade, discutida na §5.2.)
3. **O preço é o expoente.** A família de distribuição atinge comportamento quase linear em dados bem distribuídos; o OSJ fica em `Θ(n^{5/3})`. Essa é a fatura da independência das amostras — e é exatamente a mesma fatura medida na §5.2 entre as duas variantes da Sondagem.

Uma busca por métodos publicados que estimem posto por **comparação contra testemunhas sorteadas independentemente por elemento** (realizada em setembro de 2026, com busca semântica e por palavra-chave) não retornou correspondência. Isso é um resultado negativo, não uma prova de inexistência, e é declarado como tal.

**Onde a Sanfona se situa.** O parâmetro `w` interpola uma família conhecida: com `w = n` a Fase 2 é exatamente o Insertion Sort sobre o vetor inteiro; com `w = 2` ela degenera em varreduras de troca de vizinhos, isto é, uma bolha. A Sanfona é o interior dessa família — larga o suficiente para absorver o deslocamento deixado pela Sondagem, estreita o suficiente para custar `Θ(n)` por varredura.

---

## 6. Resultados experimentais

### 6.1 Metodologia

- 8 algoritmos × 5 distribuições × 7 tamanhos × 3 repetições, com verificação de ordenação em **todas** as execuções.
- Distribuições: `random`, `sorted`, `reverse`, `duplicates`, `almost_sorted`, geradas pelo `generate_dataset` do próprio pacote da disciplina, de modo que os baselines enfrentem exatamente os mesmos vetores.
- Métricas: tempo médio, comparações e movimentações, sob a mesma convenção de contagem de `classical.py`.
- Semente fixa (`random.seed(42)`) para reprodutibilidade.
- Dados brutos em [`resultados/benchmark_osj.csv`](resultados/benchmark_osj.csv); tabelas completas em [`resultados/benchmark_osj.md`](resultados/benchmark_osj.md).

### 6.2 Escalabilidade e verificação do expoente

![Escalabilidade do OSJ](resultados/escalabilidade_loglog.png)

Em escala log-log, `T(n) ~ c·n^k` vira uma reta de inclinação `k`. A curva medida do OSJ acompanha a reta de referência `n^{5/3}` em toda a faixa testada.

| | expoente |
| :--- | ---: |
| Previsto pela análise | **1,667** |
| Medido (comparações, `N` até 2000) | **1,593** |
| Medido (comparações, `N` até 8000) | **1,639** |

A aproximação melhora conforme `N` cresce, como esperado: os termos de ordem inferior perdem peso relativo.

### 6.3 Comparação com os métodos clássicos

![Comparações](resultados/benchmark_comparacoes.png)

![Tempo](resultados/benchmark_tempo.png)

**Expoentes empíricos, distribuição aleatória:**

| Algoritmo | comparações | tempo |
| :--- | ---: | ---: |
| Bubble Sort | 2,032 | 1,890 |
| Selection Sort | 2,021 | 1,803 |
| Insertion Sort | 1,961 | 1,814 |
| **OSJ** | **1,593** | **1,460** |
| DPES (referência) | 1,338 | 1,114 |
| Merge Sort | 1,271 | 0,955 |
| Quick Sort | 1,185 | 1,035 |

**Comparações absolutas, distribuição aleatória:**

| Algoritmo | N=100 | N=500 | N=1000 | N=2000 |
| :--- | ---: | ---: | ---: | ---: |
| Bubble Sort | 4.917 | 124.154 | 498.943 | — |
| Selection Sort | 4.950 | 124.750 | 499.500 | — |
| Insertion Sort | 2.730 | 65.537 | 250.362 | — |
| **OSJ** | 3.247 | 41.701 | 130.455 | 402.358 |
| OSJ estável | 1.019 | 6.779 | 15.334 | 34.190 |
| DPES (referência) | 1.026 | 7.982 | 18.118 | 40.901 |
| Merge Sort | 543 | 3.861 | 8.719 | 19.401 |
| Quick Sort | 969 | 6.263 | 14.013 | 29.670 |

O OSJ ocupa exatamente o nicho previsto pela teoria: nitidamente superior aos quadráticos a partir de `N ≈ 300`, nitidamente inferior aos `n log n`. O cruzamento com o Insertion Sort ocorre cedo justamente porque o termo `n·s` é linear em `n` para `s` fixo, mas o `Inv` do Insertion cresce quadraticamente.

### 6.4 Sensibilidade à distribuição

| Distribuição | Comparações (N=2000) | Leitura |
| :--- | ---: | :--- |
| `sorted` | 395.932 | **quase igual ao aleatório** — a Fase 1 não é adaptativa |
| `random` | 402.358 | caso de referência |
| `reverse` | 410.082 | o "pior caso" clássico praticamente não pesa |

Este é o resultado experimental mais informativo do trabalho, e é **desfavorável ao algoritmo**: o OSJ é quase **insensível à ordem da entrada**. O vetor reverso, que arruína Bubble e Insertion, custa apenas 2% a mais que o aleatório; e o vetor já ordenado, que aqueles resolvem em `Θ(n)`, custa aqui praticamente o mesmo que o caso médio. A explicação é direta: o termo dominante `n·s` da Fase 1 é pago incondicionalmente, e ele não olha para a ordem da entrada.

### 6.5 Validação de corretude

`python test_osj.py` — **42 testes, todos aprovados**:

- Os 10 cenários obrigatórios do `test_suite.py` do pacote da disciplina, aplicados a **três** alvos: OSJ padrão, OSJ estável e a Sanfona isolada.
- Casos limite `N = 0` e `N = 1`, vetor unitário, vetores com todos os elementos idênticos, negativos e ponto flutuante.
- Teste de sabotagem da Fase 1 (`s = 1`) confirmando que a corretude não depende dela.
- Teste de estabilidade com chaves etiquetadas, confirmando a estabilidade da variante compartilhada.
- Teste de robustez a `w` arbitrário (`w ∈ {2, 3, 4, 7, 16, 50, 199, 200, 500}`).
- 60 execuções aleatórias independentes com tamanhos variados.
- Verificação do contraexemplo `[3,4,1,2]`: janelas disjuntas **devem** falhar, janelas sobrepostas **devem** acertar.
- Verificação da identidade `trocas de vizinhos = Inv(A₀)` em quatro distribuições.

---

## 7. Limitações e trabalhos futuros

1. **Ausência de adaptatividade (limitação principal).** A Fase 1 é incondicional. Uma verificação prévia de ordenação em `O(n)`, ou tornar `s` função de uma medida barata de desordem, recuperaria o melhor caso `Θ(n)` sem afetar o caso médio.
2. **Superioridade assintótica dos métodos `n log n`.** `n^{5/3}` é intrinsecamente pior que `n log n`. O ganho de `s` além de `n^{2/3}` é anulado pelo custo da própria sondagem — a barreira é estrutural, não de implementação.
3. **Custo de espaço.** `Θ(n)` na Fase 1. Uma distribuição por permutação cíclica in-place eliminaria os baldes ao custo de perder a estabilidade da distribuição.
4. **Estabilidade não simultânea com independência.** As duas propriedades desejáveis estão em conflito na formulação atual: independência das amostras (que sustenta a análise limpa) e estabilidade (que exige estimativas idênticas para chaves iguais). Um desempate determinístico por índice original poderia reconciliá-las.
5. **Constante do limite de Hoeffding.** A cota `D ≤ 2εn` é folgada; as medições indicam deslocamento real bem abaixo do previsto, sugerindo que uma análise mais fina (via estatísticas de ordem, em vez de união sobre Hoeffding) daria um expoente ótimo ligeiramente diferente.

---

## 8. Declaração de autoria e uso de IA

> **Esta seção deve ser revisada e ajustada pelo aluno para refletir com exatidão o processo real.**

### Ferramenta utilizada

**Claude (Anthropic)**, modelo Opus, em sessão interativa de trabalho conjunto.

### Por que foi utilizada

Como parceiro de discussão técnica para a concepção do mecanismo, para orientação na construção das provas formais, e para acelerar a implementação, a instrumentação experimental e a redação deste documento.

### Como foi utilizada

| Etapa | Papel da ferramenta | Papel do aluno |
| :--- | :--- | :--- |
| Concepção | Apresentou cinco direções candidatas de mecanismo autoral, com análise de viabilidade e risco de originalidade de cada uma | Escolheu a direção (combinação de sondagem amostral com reparo por janelas deslizantes) |
| Prova de término | Conduziu por método socrático: formulou as perguntas, apontou os erros, forneceu contraexemplos; ao final redigiu a prova completa após o aluno ter estabelecido a intuição central | Identificou por conta própria a separação de responsabilidades entre as fases e a observação de que os elementos não movidos preservam suas relações — as duas peças conceituais da prova |
| Contraexemplo do passo `w` | Construiu o vetor `[3,4,1,2]` e o rastro de execução | Solicitou a construção |
| Implementação | Escreveu `osj.py`, `test_osj.py`, `benchmark_osj.py`, `scaling_osj.py` e `exemplo_didatico.py` | Definiu o destino dos arquivos e ratificou as decisões de projeto |
| Análise assintótica | Deduziu a aplicação de Hoeffding, a passagem do erro de estimativa ao deslocamento e a otimização de `s` | — |
| Experimentos | Projetou e executou os benchmarks, investigou a anomalia da variante estável e identificou sua relação com o Sample Sort | — |
| Redação | Redigiu este README | — |

### Modificações realizadas

*(A ser preenchido pelo aluno: quaisquer alterações feitas sobre o material produzido, decisões revertidas ou reescritas.)*

### Como o resultado foi validado

- Suíte de 42 testes automatizados cobrindo todos os cenários obrigatórios do enunciado mais os testes de propriedade e de teoria descritos na §6.5.
- Verificação cruzada de toda saída contra `sorted()` da biblioteca padrão, em cada uma das execuções de benchmark.
- **Confronto quantitativo entre teoria e experimento:** o expoente deduzido analiticamente (5/3 = 1,667) foi confrontado com o expoente medido por ajuste de mínimos quadrados em escala log-log (1,593 a 1,639).
- **Verificação de teorema por instrumentação:** a identidade `trocas de vizinhos = Inv(A₀)`, derivada da prova de término, foi verificada como igualdade exata em quatro distribuições distintas.
- Verificação executável do contraexemplo que justifica a sobreposição das janelas.

### Fontes e técnicas da literatura reconhecidas

- **Desigualdade de Hoeffding** — limite de concentração usado na análise da Fase 1.
- **Sample Sort** — a variante de testemunhas compartilhadas é reconhecida como adaptação dessa técnica, conforme discutido na §5.2.
- **ProxmapSort** (Standish, UC Irvine, ~1987), **Flashsort** (Neubert, *Dr. Dobb's Journal*, fev. 1998) e **Learned Sort** (Kristo, Vaidya, Çetintemel, Misra e Kraska, SIGMOD 2020) — os vizinhos publicados mais próximos da estrutura em duas fases, identificados por busca deliberada de originalidade e discutidos na §5.3. O Learned Sort é o mais próximo: a filiação é reconhecida, e a distinção reivindicada é a não-monotonicidade da estimativa.
- **Shell Sort** — filiação conceitual da Fase 2 à família de inserções em subestruturas, com as diferenças estruturais explicitadas na §5.2.
- **Ordenação adaptativa** — a medida de desordem `Dis(A)` (deslocamento máximo) e a função potencial `Inv(A)` são instrumentos padrão dessa literatura.

---

## 9. Estrutura do repositório

```
TP1-APA/
├── README.md                    este relatório
├── pyproject.toml               dependências (uv): apenas matplotlib
├── uv.lock                      versões exatas, para reprodutibilidade
├── python/
│   ├── osj.py                   ← algoritmo autoral (implementação e documentação)
│   ├── test_osj.py              ← suíte de 42 testes
│   ├── benchmark_osj.py         ← benchmark comparativo e geração de gráficos
│   ├── scaling_osj.py           ← medição do expoente de escalabilidade
│   ├── exemplo_didatico.py      ← exemplo numérico passo a passo
│   ├── student_template.py      ← interface exigida pelo enunciado
│   ├── classical.py             baselines fornecidos pela disciplina
│   ├── authorial.py             DPES de referência (fornecido)
│   ├── benchmark.py             framework fornecido
│   └── test_suite.py            suíte fornecida
└── resultados/
    ├── benchmark_osj.csv        dados brutos
    ├── benchmark_osj.md         tabelas completas
    ├── benchmark_tempo.png
    ├── benchmark_comparacoes.png
    └── escalabilidade_loglog.png
```
