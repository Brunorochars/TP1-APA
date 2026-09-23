# Roteiro de apresentação — OSJ

**Bruno da Silva Rocha · Pietro M. Prauchner**

Roteiro da defesa oral do TP1. Os slides estão em [`slides.html`](./slides.html);
cada slide carrega este mesmo roteiro como **nota do apresentador**, visível pela
tecla `N` ou pelo botão *Notas*. Este arquivo é a versão para estudar antes; as
notas embutidas são a versão para consultar durante.

> **Orçamento de texto.** Os slides carregam só o que precisa ser lido à distância;
> o detalhamento — provas passo a passo, números secundários, respostas a
> perguntas prováveis — vive nas **notas do apresentador** (`N`) e neste arquivo.
> Se a arguição descer ao detalhe, a resposta está na nota daquele slide.

**Navegação nos slides:** `→` / `espaço` avança, `←` volta, `Home` / `End` vão aos
extremos, `N` liga as notas do apresentador, `F` entra e sai da tela cheia. Cada
slide ocupa a tela inteira e se ajusta sozinho se o conteúdo não couber.

---

## O que a banca está avaliando

A ponderação do enunciado decide onde gastar o tempo. Não é distribuição uniforme
entre os slides:

| Critério | Peso | Slides que o atendem |
|---|---:|---|
| Raciocínio projetual e originalidade | **30%** | 2, 3, 5, 15 |
| Análise teórica de complexidade | **25%** | 7, 8, 9, 10, 11, 12, 13 |
| Corretude e validação experimental | **25%** | 16, 17, 18, 19 |
| Qualidade da documentação e defesa | 10% | todos — clareza, pseudocódigo, gráficos |
| Declaração de autoria e pensamento crítico | 10% | 15, 18, 20, 21 |

Consequência prática: os slides **3** (a separação de responsabilidades) e **5** (o
contraexemplo do passo `w`) são os dois de maior retorno, porque sustentam os 30%
de originalidade *e* preparam os 25% de análise. Se o tempo apertar, é dos slides
7, 8 e 14 que se corta — não desses dois.

> **Regra de ouro do enunciado**, a ter na ponta da língua: *"um algoritmo
> quadrático com uma análise brilhante vale muito mais do que um algoritmo rápido
> cuja lógica o autor não saiba explicar."* Ela é a resposta a qualquer variação de
> "mas o Merge Sort é mais rápido".

---

## Cronometragem

Duas versões do mesmo roteiro. A coluna **20 min** é a completa; a **12 min** é a
que se usa se a turma estiver atrasada.

| # | Slide | 20 min | 12 min |
|---:|---|---:|---:|
| 1 | Título | 0:40 | 0:30 |
| 2 | A pergunta que originou o método | 1:30 | 1:00 |
| 3 | **Duas fases, duas responsabilidades** | 2:00 | 1:30 |
| 4 | Pseudocódigo | 1:30 | 0:45 |
| 5 | **Por que o passo é `w/2`** | 2:00 | 1:30 |
| 6 | Exemplo numérico | 2:00 | 1:00 |
| 7 | Corretude — término | 2:00 | — |
| 8 | Corretude — ponto fixo | 1:30 | 0:45 |
| 9 | Análise da Fase 1 | 2:00 | 0:45 |
| 10 | **Lema do avanço** | 2:30 | 1:00 |
| 11 | **De onde vem o 5/3** | 2:00 | 1:30 |
| 12 | Pior caso | 1:30 | — |
| 13 | Quadro-resumo | 1:30 | 0:30 |
| 14 | Comparação com a literatura | 2:00 | 0:45 |
| 15 | **Originalidade / Sample Sort** | 2:30 | 1:00 |
| 16 | Escalabilidade log-log | 2:00 | 1:00 |
| 17 | O nicho | 2:00 | 0:45 |
| 18 | **Insensibilidade à distribuição** | 2:00 | 1:00 |
| 19 | 44 testes | 1:30 | 0:45 |
| 20 | Limitações | 1:30 | — |
| 21 | Declaração de autoria e IA | 1:30 | 1:00 |
| 22 | Encerramento | 0:40 | 0:30 |

Na versão de 12 min, os slides 7, 12 e 20 são **passados sem falar** (ficam
disponíveis para pergunta). Não se apagam: a existência da prova de término no
material é parte do que se está entregando.

---

## O roteiro, slide a slide

### 1 · Título — 0:40

> "O método se chama OSJ, Ordenação por Sondagem e Janelas. Ele tem duas fases, e a
> ideia central do projeto está na relação entre elas: a primeira é aleatorizada e
> **pode errar**; a segunda é determinística e é a única responsável pela corretude.
> Isso me deixa usar uma heurística agressiva sem nenhum risco de saída errada."

Não adiantar números. O `5/3` é do slide 11.

### 2 · A pergunta que originou o método — 1:30

Contar a metáfora da boca de urna **antes** de qualquer notação. Se a plateia
entender "pesquisa de boca de urna", a Fase 1 já está entendida.

Terminar exatamente na frase *"fica quase ordenado, não ordenado"* — é o gancho do
próximo slide. Não resolver o problema aqui.

### 3 · Duas fases, duas responsabilidades — 2:00 ⭐

Slide a defender com mais convicção. A pergunta previsível é *"como você garante
corretude se a primeira fase é aleatória?"*. A resposta está desenhada: **ela não
garante**. A Fase 2 garante, e ela é determinística.

Prova executável, se cobrarem: `sanfona_sort()` é o algoritmo sem a Fase 1, e a
suíte roda *todos* os cenários obrigatórios contra ela. Há também um teste que
sabota a Sondagem com `s = 1` — uma única testemunha — e ainda exige saída perfeita.

### 4 · Pseudocódigo — 1:30

Ler os dois blocos rápido, sem soletrar linha por linha. Sublinhar duas coisas:

1. `passo ← ⌊w/2⌋`, destacado, porque é o próximo slide;
2. a comparação estrita, que faz a inserção **só trocar vizinhos** — e é isso que a
   prova de término vai consumir.

*Se perguntarem por que o último início é `n−w`:* para a janela final encostar na
borda direita; senão as últimas posições ficam descobertas e o argumento de
cobertura quebra.

### 5 · Por que o passo é `w/2` — 2:00 ⭐

Andar o vetor `[3,4,1,2]` com o dedo. Com passo 2: as duas janelas estão ordenadas
*por dentro*, nada se move, o critério de parada dispara, e a saída está errada. O
par (4,1) nunca coexistiu numa janela.

Dizer explicitamente: **isto é corretude, não desempenho.** E que está codificado
como teste automatizado — o teste exige que a versão disjunta *falhe* e que a
sobreposta acerte (`test_disjoint_windows_have_spurious_fixed_points`).

### 6 · Exemplo numérico — 2:00

Dois pontos a extrair, e só dois:

- **O `54`** — apontar para ele. Sorteou `[88,96,96,54]`, não achou nenhuma
  testemunha menor, estimou `c/s = 0` e foi para a posição 0. É a demonstração
  concreta de que a Fase 1 erra, e de que errar não compromete nada.
- **Os dois 16 iguais** — 16 trocas de vizinhos e `Inv = 16`. Preparam o corolário
  do próximo slide.

*Se perguntarem por que a passada 3 existe:* o sinal de parada é `movimentou`,
custo `O(1)`. Detectar o ponto fixo sem varrer exigiria calcular `Inv`, que custa
mais que desfazer a desordem que ele mede.

### 7 · Corretude — término — 2:00

Não recitar os quatro passos. Dizer o argumento inteiro em uma frase — *"existe uma
grandeza inteira, não-negativa, que cai de exatamente 1 a cada movimentação; então
não há execução infinita"* — e gastar o tempo no **por que a adjacência importa**,
que é a parte que um avaliador testa: uma troca a distância `d` alteraria até
`2d − 1` pares de uma vez, e o efeito sobre o potencial deixaria de ser unitário.

Fecha o gancho do slide 6: os dois 16 são o corolário. `Inv` é grandeza *da
análise*, não do algoritmo — o código não a calcula em lugar nenhum.

### 8 · Corretude — ponto fixo — 1:30

A conta `k + 2 − w ≤ p ≤ k` vale ser escrita no ar: é o argumento de cobertura, e
reaparece duas vezes — aqui, e como Passo 1 do lema do avanço.

*Se perguntarem por que não usar o passo máximo `w−1`:* a corretude sobrevive, mas
a convergência piora; `w/2` compra meia janela de avanço garantido por varredura,
que é o que o lema entrega.

### 9 · Análise da Fase 1 — 2:00

Distinguir com clareza os dois instrumentos — é onde a análise ganha ou perde nota:

- a **variância** dá o erro *típico* `O(n/√s)` e sustenta o regime de esperança;
- **Hoeffding + cota da união** dá o erro *simultâneo para todos os n* e cobra um
  fator `√log n` por isso.

*Se perguntarem por que a esperança não precisa de Hoeffding:* porque
`Inv ≤ Σ dᵢ` é uma **soma**, e linearidade da esperança basta. Máximo precisaria de
concentração; soma não.

### 10 · Lema do avanço — 2:30 ⭐

Este lema entrou depois: na primeira versão a afirmação "cada varredura reduz o
deslocamento em `w/2`" sustentava toda a análise **sem estar provada**. Vale dizer
isso na defesa — é revisão crítica própria, e pontua.

A **redução 0/1** é o truque a vender: pintando de 1 os `m` menores, todo 1 precede
todo 0, e ordenar uma janela equivale a *compactar seus 1s à esquerda*. Logo nenhum
1 anda para a direita, e `R_m` é não-crescente. Se o tempo apertar, apresentar só a
redução e o resultado, e oferecer os quatro passos se perguntarem.

**Peso da consequência, que é o que se defende:** sem o lema, o único limite de
varreduras provado é `P ≤ n(n−1)/2` (do término), que daria `O(n³)` — colocando o
OSJ *abaixo do Bubble Sort*. O lema é o que separa um limite honesto de um limite
constrangedor.

*Se perguntarem pelo lado direito:* o enunciado simétrico é **falso**. Em `[2,3,0,1]`
com `w = 2` o elemento `2` precisa avançar duas posições à direita e a varredura
inteira o deixa onde estava. A garantia é do lado esquerdo — e `Dis_esq = 0` já
implica vetor ordenado, que é o lado de que a análise precisa.

### 11 · De onde vem o 5/3 — 2:00 ⭐

Fazer a derivada no ar, devagar. É o cálculo que os 25% de análise mais recompensam,
e é curto: `n − ½n²s^{−3/2} = 0 ⟹ s^{3/2} = n/2 ⟹ s* = Θ(n^{2/3})`.

Frisar a leitura estrutural: **o ótimo é onde as duas fases custam o mesmo.** Isso é
o que explica por que `s` e `w` coincidem em `n^{2/3}`.

*Se perguntarem sobre o `Θ` (pergunta boa e provável):* a cota **inferior** é
própria e incondicional, e vem da Fase 1 — ela faz `n·s` comparações sem olhar para
nada, logo `T ≥ Ω(n^{5/3})` em *toda* execução, não só em esperança. É isso que
fecha o `Θ`; a soma de `Θ` com `O` sozinha daria só um `O`.

### 12 · Pior caso — 1:30

A derivação também nasceu de revisão: a justificativa original do `O(n²)` estava
**errada** — citava o corolário do potencial, que limita *trocas*, não comparações.
Dizer isso é ponto no critério de pensamento crítico.

A frase que se lembra: **"no pior caso o OSJ é o Insertion Sort mais o troco"** — as
trocas de vizinhos somam `Inv(A₀)`, exatamente o que o Insertion pagaria sobre o
mesmo vetor, e sobre isso o OSJ acumula `Θ(n·s)` de sondagem desperdiçada.

### 13 · Quadro-resumo — 1:30

Não ler a tabela. Deixar no ar e narrar três linhas: melhor caso (a limitação
honesta), caso médio (a reivindicação), pior caso (o que se suporta).

O parágrafo final é o ponto mais sofisticado do trabalho, e responde *"então é caso
médio como no Quick Sort?"*. **Não.** A esperança é sobre a moeda do algoritmo, não
sobre uma distribuição de entradas — o que a licencia é que `Xᵢ ~ Binomial(s, pᵢ)`
depende só do **posto**, e a família dos postos é `{0,…,n−1}` seja qual for a
permutação recebida. E a §6.4 mede exatamente isso: 3% de espalhamento entre a
entrada mais favorável e a mais hostil.

### 14 · Comparação com a literatura — 2:00

O enunciado exige tabela + discussão contra ≥ 2 clássicos; aqui há quatro mais o
Shell. **Não ler os quatro cartões** — escolher dois:

- **Insertion**, porque o OSJ o *contém* (com `w = n` a Fase 2 é uma inserção sobre
  o vetor inteiro) — é a comparação estruturalmente mais reveladora;
- **Quick**, porque contrasta o papel da aleatoriedade, que é a tese do trabalho.

Deixar o Shell para o slide 15 se houver pergunta sobre originalidade.

### 15 · Originalidade / Sample Sort — 2:30 ⭐

Slide que vale nos dois critérios de 10% e protege contra o critério de rejeito por
plágio. Apresentar como escolha deliberada:

> "Encontrei uma variante mais rápida — testemunhas compartilhadas, expoente 1,17
> contra 1,59. Investiguei por que, descobri que quando a amostra é comum a posição
> estimada vira função **monótona** do valor, e que isso é precisamente a fase de
> distribuição do Sample Sort. Então **a variante rápida é a menos autoral**, e ela
> está declarada como adaptação de técnica conhecida, não como contribuição própria."

O **Learned Sort** é o vizinho mais próximo — a descrição dos próprios autores
("aproximar a posição de saída de cada chave por um modelo e depois aplicar um
algoritmo determinístico que funciona bem em vetores quase ordenados") é a mesma
decomposição. Reconhecer a filiação em voz alta, e reivindicar só a
**não-monotonicidade**.

*Se perguntarem "então isso já existe?":* a busca por métodos que estimem posto por
comparação contra testemunhas sorteadas **independentemente por elemento** não
retornou correspondência. É um resultado negativo, não prova de inexistência — e
está declarado como tal no relatório.

### 16 · Escalabilidade log-log — 2:00

Explicar a leitura log-log **antes** de mostrar números: reta, inclinação =
expoente. Depois o argumento de convergência: 1,591 em `N ≤ 2000`, 1,641 em
`N ≤ 10⁴` — *anda na direção do 1,667*, e isso é o comportamento esperado de termos
de ordem inferior perdendo peso, não uma discrepância.

Ponto forte a não perder: o expoente do **tempo** (1,678) é um eixo *independente
das contagens*. Se a convenção de contagem estivesse inflando algo, o tempo não
seguiria.

*Se perguntarem por que parou em `10⁴`:* uma execução leva ~1,2 s, ~6 s para as 5
repetições, e a dobra seguinte custaria ~3× isso. O ajuste já estabilizou; a
distância remanescente é de termos de ordem inferior, não de expoente.

### 17 · O nicho — 2:00

A reta dos expoentes é o gráfico a defender: mostra que a classe `n^{5/3}` não é um
número arbitrário, é uma faixa que os clássicos **não ocupam**, e o OSJ cai nela por
dedução, não por ajuste.

Antecipar a objeção honesta — *"então é pior que Merge e Quick"*. Sim, e o relatório
diz isso na §5.2: o OSJ não compete com o Merge, nem pretende. Aqui entra a regra de
ouro do enunciado.

### 18 · Insensibilidade à distribuição — 2:00 ⭐

Apresentar o achado **desfavorável antes** da leitura favorável, nunca o contrário.
A ordem importa: quem abre com a desculpa parece estar se defendendo; quem abre com
a limitação e depois mostra que o mesmo dado sustenta a cota parece dominar o
próprio trabalho.

Frase de ligação: *"o mesmo número que mostra que o OSJ não é adaptativo é o número
que mostra que a cota vale uniformemente."*

⚠️ **Cuidado com os N:** o gráfico do slide é `N = 1000` (126,5k / 129,7k / 131,9k,
≈4% de espalhamento). Os 3% citados na §6.4 são de `N = 2000`
(397.562 / 402.550 / 409.441). Não trocar um pelo outro sob pergunta.

### 19 · 44 testes — 1:30

Vale nos 25% de validação e é o critério de rejeito mais direto. Duas coisas a dizer
bem:

1. A suíte obrigatória roda contra a **Sanfona isolada** também. Isso é o que
   transforma a tese do slide 3 de argumento em verificação.
2. Há testes de **teoria**: a identidade `trocas = Inv(A₀)` é checada como
   *igualdade exata* em quatro distribuições, e o lema do avanço é medido varredura a
   varredura pelo seam `_sweep`. Se um teorema do relatório estiver errado, a suíte
   quebra.

*Reprodutibilidade, se perguntarem:* `random.seed(42)`, `uv.lock` versionado fixando
as 13 transitivas, e `resultados/` versionado como evidência primária. O algoritmo é
stdlib-puro — roda em qualquer Python 3.11 limpo, sem instalar nada.

### 20 · Limitações — 1:30

Não pedir desculpa por nenhuma. Apresentar cada uma com o **caminho de ataque** ao
lado — é o que distingue "sei que tem um problema" de "sei o que faria".

A folga do Hoeffding é a mais sofisticada de admitir: reconhece que a própria prova é
conservadora (`D ≤ 2εn` é frouxa) e nomeia a ferramenta que a apertaria
(estatísticas de ordem em vez de união sobre Hoeffding). Se sobrar tempo, é aqui que
se gasta.

### 21 · Declaração de autoria e IA — 1:30

**Obrigatória, e a ausência é critério de rejeito.** Não passar rápido por medo: a
declaração é *exigida*, e uma declaração detalhada e honesta pontua nos 10%. Uma
declaração vaga é o que penaliza.

O que carrega o slide é a coluna das **modificações determinadas na revisão** de
09/09/2026: cinco intervenções de conteúdo, três delas corrigindo erros técnicos
reais na análise (lema não provado, pior caso mal justificado, regimes
probabilísticos misturados). Isso é a evidência de domínio, e é o antídoto direto
para o critério de rejeito por "desconhecimento substancial da solução".

*Se perguntarem "quanto disso é seu?":* a tabela do §8 não infla o papel do aluno —
a implementação e a redação estão declaradas como da ferramenta; a concepção, a
escolha de direção entre cinco candidatas, as duas peças da prova de término e as
cinco correções estão declaradas como do aluno. **A defesa oral é a prova**, e é por
isso que o roteiro pesa nos slides 3, 5, 10 e 11.

### 22 · Encerramento — 0:40

Três frases, e parar. Não recapitular a apresentação inteira.

A frase para deixar no ar, se houver só uma:

> **"A fase que pode errar nunca é a fase que decide a corretude."**

---

## Mapa de arguição

Perguntas prováveis e onde está a resposta. Vale decorar esta tabela — ela é o
seguro contra o critério de rejeito por desconhecimento.

| Pergunta | Slide | Resposta em uma linha |
|---|:---:|---|
| Como garante corretude se é aleatório? | 3 | A Fase 1 não garante nada. A Fase 2 é determinística e ordena sozinha — `sanfona_sort()` prova isso executando. |
| Por que o passo não pode ser `w`? | 5 | Janelas disjuntas criam pontos fixos espúrios: `[3,4,1,2]` sai errado. Família infinita de falhas. |
| Isso não é Shell Sort? | 14 | Shell opera em elementos *distantes* com incremento decrescente; a Sanfona em blocos *contíguos* com `w` fixo até o ponto fixo. Filiação reconhecida. |
| Isso não é Sample Sort / Learned Sort? | 15 | Aqueles têm mapa valor→posição **monótono**; a Sondagem independente não. Por isso a desordem residual é global, e por isso a Fase 2 não pode ser ordenação por balde. |
| De onde vem o `5/3`? | 11 | Equilibrar `Θ(ns)` com `O(n²/√s)`: a derivada dá `s* = Θ(n^{2/3})`, e `T = Θ(n·s) = Θ(n^{5/3})`. |
| Por que é `Θ` e não só `O`? | 11 | A cota inferior é incondicional e vem da Fase 1: `n·s` comparações em *toda* execução. |
| É caso médio como no Quick Sort? | 13 | Não — é esperança sobre a moeda do algoritmo, válida para *toda* entrada, porque a distribuição do erro depende só do posto. |
| Por que o pior caso é `O(n²)`? | 12 | `P = O(n/w)` pelo lema do avanço + `Inv ≤ n(n−1)/2` pelo potencial. Sem o lema seria `O(n³)`. |
| Por que não é adaptativo? | 18, 20 | A Sondagem é incondicional: paga `n·s` mesmo no vetor ordenado. Limitação admitida, com caminho de correção. |
| O Merge Sort não é melhor? | 17 | É, assintoticamente, e o relatório diz isso. Performance bruta não é o critério do enunciado. |
| Por que Python e não C++? | — | Recusa fundamentada e registrada: o port mediria o fator constante do interpretador — eixo que o enunciado desvaloriza — ao custo de duplicar a superfície de risco de incorretude. Contagens de operações são invariantes da linguagem; tempo absoluto não. |
| Por que os quadráticos param em `N = 1000`? | 17 | Já fazem ~2·10⁶ comparações em `N = 2000`; o regime quadrático está inequívoco (2,03 · 2,02 · 1,96). Medir mais longe reconfirma um fato assentado. |
| Como sei que os números se reproduzem? | 19 | `random.seed(42)`, `uv.lock` versionado, `resultados/` versionado, e verificação contra `sorted()` em cada execução. |

---

## Checklist antes de apresentar

- [ ] `uv run python test_osj.py` — confirmar **44/44** no dia, na máquina que vai apresentar
- [ ] Abrir `slides.html` no navegador, entrar em **tela cheia** (`F`) e testar `→`, `←` e `N` uma vez
- [ ] Conferir a tela cheia **no projetor da sala**, não só no monitor — é onde a altura muda
- [ ] Decidir a versão do relógio (20 min ou 12 min) e marcar mentalmente os cortes (7, 12, 20)
- [ ] Ter `README.md` aberto numa aba — é o relatório, e a arguição pode pedir uma seção específica
- [ ] Ter `python/osj.py` aberto noutra aba — se pedirem para mostrar o código do passo `w/2`
- [ ] Ensaiar em voz alta os slides **3, 5, 10 e 11**. São 8min30 dos 20, e é onde a nota está.
