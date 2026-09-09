# OSJ — Ordenação por Sondagem e Janelas

Glossário do domínio do TP1 de APA: o método de ordenação autoral OSJ, suas duas
fases e as grandezas usadas na análise de complexidade e na instrumentação
experimental.

Ponte entre o termo de domínio (pt-BR, usado no relatório) e o identificador no
código (inglês). Decisões e seus porquês em [`docs/adr/`](./docs/adr/).

## Language

### Grandezas de custo e de desordem

**Comparação**:
Confronto entre duas chaves do vetor. Unidade de custo contada em `comparisons`,
na mesma convenção de `classical.py`, para que o OSJ possa ser comparado com os
baselines em pé de igualdade.

**Movimentação**:
Qualquer leitura ou gravação de chave contabilizada pela convenção de
`classical.py` — inclui a leitura da chave, cada deslocação de uma casa e a
gravação final. Contada em `moves`.
_Avoid_: movimento, operação

**Troca de vizinhos**:
Mover um elemento uma única casa, trocando-o com o vizinho adjacente. É a
operação elementar da prova de término: cada troca de vizinhos fora de ordem
reduz `Inv(A)` em exatamente 1. Contada em `shifts`.
_Avoid_: deslocamento, shift, troca

**Deslocamento**:
Distância entre a posição atual de um elemento e o seu posto correto — uma
medida de **estado** (o quanto o vetor está desordenado), nunca de ação. É a
grandeza que dimensiona a janela: com `s = n^{2/3}` o deslocamento típico após a
Sondagem é `Θ(n^{2/3})`, e é daí que sai `w`. Medida por `max_displacement()`.
_Avoid_: troca de vizinhos, shift

**Inversão**:
Par de posições fora de ordem no vetor. `Inv(A)` é grandeza **da análise, não do
algoritmo**: nada no caminho de execução a calcula. `inversions()` existe apenas
para instrumentação experimental.

**Varredura**:
Uma passagem completa da janela por todo o vetor, cobrindo todas as posições
iniciais. Contada em `passes`. A Sanfona repete varreduras até que uma delas
ocorra sem nenhuma troca de vizinhos.
_Avoid_: passada, iteração, rodada

### O método e suas fases

**OSJ** (Ordenação por Sondagem e Janelas):
O método autoral inteiro: uma Sondagem heurística seguida de uma Sanfona
determinística. Sozinho, "OSJ" designa a variante de **sondagem independente** —
é dela que a tese `Θ(n^{5/3})` fala.

**Sondagem**:
Fase 1. Cada elemento estima o próprio posto consultando testemunhas sorteadas e
é depositado na posição estimada. Fase heurística e aleatorizada: responde pelo
desempenho, nunca pela corretude — pode errar de modo caro, nunca de modo fatal.
_Avoid_: amostragem, estimativa, fase probabilística

**Sanfona**:
Fase 2. A janela varre o vetor repetidamente, ordenando por inserção cada trecho
coberto, até uma varredura sem trocas de vizinhos. Fase determinística onde mora
toda a corretude do método: ordena qualquer entrada sozinha (`sanfona_sort`).
_Avoid_: reparo, polimento, fase de conserto

**Testemunha**:
Elemento sorteado do vetor com o qual outro elemento se compara para estimar o
próprio posto. A quantidade de testemunhas por elemento é `s`.
_Avoid_: amostra, pivô, referência

**Posto**:
A posição que um elemento ocupa no vetor ordenado. A Sondagem produz uma
*estimativa* de posto; o posto verdadeiro só existe ao final.
_Avoid_: rank, índice, colocação

**Janela**:
Trecho contíguo de largura `w` ordenado por inserção de uma vez pela Sanfona.

**Passo**:
Distância entre os inícios de duas janelas consecutivas. É sempre `w/2`: janelas
sobrepostas garantem que todo par de posições vizinhas caia dentro de alguma
janela.

**Ponto fixo espúrio**:
Estado em que uma varredura inteira não move nada mas o vetor não está ordenado.
Existe quando as janelas são disjuntas (passo `w`) e é o que o passo `w/2`
elimina — com sobreposição, o único ponto fixo é o vetor ordenado.

### Variantes da Sondagem

**Sondagem independente**:
Cada elemento sorteia as próprias testemunhas. Os erros de estimativa são
independentes entre elementos, o que sustenta a análise probabilística limpa.
Custo `n·s`. Não preserva estabilidade: chaves iguais podem receber estimativas
diferentes.

**Sondagem compartilhada**:
Todos os elementos consultam a mesma amostra ordenada de testemunhas, por busca
binária. Chaves iguais caem sempre no mesmo balde, o que torna o método inteiro
estável, e o custo por elemento cai de `s` para `log₂ s`. Mede-se melhor
(expoente 1,19 contra 1,59), mas por um motivo que a desqualifica como
contribuição: com amostra comum o mapa valor→posição fica **monótono**, e a fase
passa a ser a distribuição do Sample Sort. É mantida no código como termo de
comparação e como variante estável, declarada explicitamente como adaptação de
técnica conhecida.
_Avoid_: OSJ estável, variante estável

> As duas variantes diferem em quatro eixos — estabilidade, independência dos
> erros, custo da Fase 1 (`n·s` contra `n·log₂ s`) e **originalidade**. O último
> é o decisivo: é por ele que o OSJ é a variante independente. Nomear pelo
> mecanismo evita citar só uma das consequências.

**Monotonicidade do mapa valor→posição**:
Propriedade de a posição estimada ser função monótona do valor da chave. Ocorre
com sondagem compartilhada e **não** ocorre com sondagem independente. É o
critério que separa o OSJ da distribuição do Sample Sort: sem monotonicidade, a
Fase 1 não ordena globalmente entre baldes, e a desordem que sobra para a Sanfona
não é apenas intra-balde.

**DPES** (Dual-Pivot Extremes Sieve Sort):
Algoritmo autoral de referência **fornecido pela disciplina** (`authorial.py`),
usado como baseline de comparação. Não é contribuição deste trabalho.

**Balde**:
Uma das `n` posições de destino em que a Sondagem deposita os elementos segundo a
estimativa de posto. Concatenar os baldes em ordem produz o vetor quase ordenado
que a Sanfona recebe.
_Avoid_: bucket, cesto, slot
