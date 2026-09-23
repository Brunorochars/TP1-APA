# Grill — conformidade com o enunciado

Sessão de grill sobre a entrega do TP1 confrontada com `docs/Enunciado.md`:
cenários obrigatórios, métricas exigidas, itens do relatório e critérios de
rejeito.

Início: 2026-09-09 10:51

**P:** O enunciado pede escalabilidade em `N = 10, 10², 10³, 10⁴, …`, mas 10⁴ não
aparece em nenhum experimento (benchmark para em 2000, escalabilidade em 8000).
Estender tudo, deixar como está, ou estender só o eixo barato e declarar o teto?

**R:** Seguir a recomendação: levar `scaling_osj.py` a `N = 10⁴`, manter o
benchmark comparativo em 2000 e declarar no §6.1 o porquê do teto (os
quadráticos instrumentados em 10⁴ custariam ~10⁸ comparações). Regeneração de
`resultados/` e atualização das tabelas como sub-tarefa própria.

**P:** Vale implementar o mesmo algoritmo em C para comparar as duas linguagens
no relatório? É válido? Compensa?

**R:** (ver resposta abaixo — decisão registrada na sequência)

**R (C):** Não portar. O port mede o fator constante do interpretador, não o
algoritmo — eixo que o enunciado desvaloriza explicitamente, e que não pontua em
nenhum dos cinco critérios. Além disso dobraria a superfície de risco de
incorretude (duas implementações podendo divergir na suíte obrigatória). O
conteúdo intelectual do port entra de graça como um parágrafo no §6.1: contagens
de operações são invariantes da linguagem, tempo absoluto não é. A restrição de
`code-conventions.md` ("trilha C++ fora de escopo") permanece válida.

**P:** "Repetições estatísticas" está cumprido pela metade: `TRIALS = 3` e só a
média, sem dispersão. Subir para 5 com desvio-padrão, manter 3 declarando a
limitação, ou 10 com mediana?

**R:** Subir para 5 repetições, com desvio-padrão registrado no tempo.

**P:** A §4.2 sustenta o `n^{5/3}` inteiro num lema de meia linha e sem prova
("cada varredura reduz o deslocamento máximo em pelo menos `w/2`"). O argumento
real depende da sobreposição *mais* a ordem esquerda→direita das janelas, e da
assimetria entre mover-se à esquerda (limitado pela janela) e à direita
(cascateia). Provar e medir, provar só, ou rebaixar a hipótese declarada?

**R:** Provar o lema e medir também. A ordem esquerda→direita como parte do
argumento era novidade para o autor — razão extra para o relatório explicitá-la
(risco de arguição).

**P:** O pior caso `O(n²)` da §4.4 não é derivado, e a justificativa citada
(corolário `Inv ≤ n(n−1)/2`) limita trocas, não comparações. Com o único limite
provado para `P` (o do término, `P ≤ n(n−1)/2`), o pior caso de comparações seria
`O(n³)` — pior que Bubble. O `O(n²)` exige `P = O(n/w) = O(n^{1/3})`, que vem do
lema do avanço. Derivar explicitamente ou só corrigir a justificativa da célula?

**R:** Derivar. O autor não tinha essa dedução. Consequências registradas: o lema
do avanço sustenta o pior caso, não só o caso médio; e no pior caso o OSJ
degenera para o Insertion mais o overhead `Θ(ns)`, com o termo dominante vindo
das trocas — material para a §5.2.

**P:** "Caso médio `Θ(n^{5/3})`" não diz sobre o que a média é tomada, mistura o
regime do deslocamento típico com o de Hoeffding (`√log n` maior), e o `Θ` não é
conectado à sua cota inferior (o `Θ(ns)` incondicional da Fase 1). Fixar os
regimes num parágrafo de convenções, ou rebaixar Hoeffding a rodapé?

**R:** Seguir a recomendação (parágrafo de regimes e convenções abrindo a §4, com
as duas afirmações lado a lado no quadro-resumo). E reivindicar
`E[T] = Θ(n^{5/3})` **para toda entrada** — esperança sobre a aleatoriedade da
sondagem, corroborada pela insensibilidade à distribuição medida na §6.4.

**P:** A §8 traz um aviso dizendo que a seção não reflete o processo real e deixa
"Modificações realizadas" — um dos cinco itens obrigatórios — como TODO, o que
cai no critério de rejeito por ausência da declaração. Preencher a partir do log
desta sessão, ou o aluno escreve com as próprias palavras?

**R:** Preencher a partir do log e remover o aviso do topo. Sem inflar a tabela
"Como foi utilizada": a honestidade dela é o que protege os 10% de
transparência, e a autoria substantiva se comprova fazendo (P3/P4) e na arguição.

**P:** A verificação de originalidade cobre Shell e Sample Sort, mas não os
vizinhos publicados mais próximos (ProxmapSort, Flashsort, histogram sort). O
enunciado promete busca semântica, e plágio não-atribuído é nota 0,0. Criar uma
§5.3 nomeando-os, com o diferencial estrutural — e verificar as citações antes?

**R:** Aprovado, com verificação prévia por busca. A busca (set. 2026) confirmou
autoria e mecanismo de ProxmapSort (Standish, ~1987), Flashsort (Neubert,
Dr. Dobb's 1998) e revelou o vizinho mais próximo, ausente da lista original:
**Learned Sort** (Kristo, Vaidya, Çetintemel, Misra, Kraska — SIGMOD 2020), cuja
descrição pelos próprios autores é a mesma decomposição em duas fases. §5.3
escrita com a fronteira estabelecida por propriedade (não-monotonicidade +
comparison-only) em vez de por ausência. Busca por métodos que estimem posto por
comparação contra testemunhas independentes: sem correspondência — resultado
negativo declarado como tal.

**P:** O enunciado separa formato de entrega (Opção A/B) de apresentação oral
(1/3 obrigatório, 2/3 para o bônus). O repositório não trata a segunda. Vai
apresentar o TP1? E a entrega é por link ou por arquivo?

**R:** Não sabe se vai apresentar, mas quer manter a possibilidade — deck não
será montado agora (depende do lema do avanço e da derivação do pior caso).
Proposta do aluno, adotada: entregar via **release** do repositório, mantendo o
relatório em Markdown no repo e anexando a versão PDF à entrega. Ajustes
acordados: sem `relatorio.md` separado (o `README.md` é o relatório); PDF como
asset da tag, nunca commitado; release notes com a receita de reprodução.
Registrado no **ADR-0003**. `pandoc` não está instalado (mas `pdflatex` sim);
verificação visual obrigatória das tabelas largas e dos links relativos.

**P:** O ADR-0001 afirma originalidade por ausência e não conhece o Learned Sort.
Emendar?

**R:** Sim — emenda de duas linhas registrando o vizinho de 2020 e que ele
reforça a decisão em vez de revertê-la. Feito.

**P:** A §8 passou a citar `docs/grills_logs/` como evidência, mas o
`.gitignore:8` (`docs/*`) o exclui — link morto no item obrigatório. Versionar o
log, ou remover a citação?

**R:** Versionar. O log é a única evidência datada de que as decisões de análise
foram do aluno, e o critério do `CLAUDE.md` para versionar é "vale para o grupo".
Feito: `!docs/grills_logs/` no `.gitignore` e a nota de versionamento do
`CLAUDE.md` atualizada. Desconforto reconhecido e aceito: o log mostra também as
lacunas que a ferramenta apontou.

---

## Fecho da sessão

Os oito itens que o enunciado exige do relatório e os cinco critérios de rejeito
foram percorridos. Aplicado nesta sessão: §5.3 (vizinhos publicados, com
citações verificadas), item "Modificações realizadas" da §8, remoção do aviso de
seção provisória, termos *avanço* e direção da *varredura* no `CONTEXT.md`,
ADR-0003, emenda ao ADR-0001, versionamento do log.

Pendente de implementação (decidido, não feito):

1. Lema do avanço provado na §4.2 + teste que mede a queda de `≥ w/2` por
   varredura → verificar: `test_osj.py` passa com o novo teste.
2. Derivação do pior caso `O(n²)` na §4.3 e correção da célula da §4.4 →
   verificar: o `O(n²)` reconstrutível a partir do texto.
3. Parágrafo de regimes e convenções abrindo a §4, com `E[T] = Θ(n^{5/3})` para
   toda entrada e a linha de alta probabilidade no quadro-resumo.
4. `TRIALS = 5` com desvio-padrão do tempo; `scaling_osj.py` até `N = 10⁴`;
   motivo do teto declarado na §6.1 → verificar: `resultados/` regenerado e
   tabelas do README conferidas (sub-tarefa própria, commit separado).
5. Release: merge `dev → main`, tag, PDF via pandoc como asset, release notes com
   a receita de reprodução.
