# Parâmetros da sondagem e da janela em `Θ(n^{2/3})`

As duas fases do OSJ têm custos que se movem em direções opostas quando `s`
(testemunhas por elemento) cresce: a Fase 1 custa `n·s`, e mais testemunhas
significam estimativas melhores, portanto deslocamento residual menor e janela
`w` menor na Fase 2. Escolhemos `s = w = Θ(n^{2/3})`, o ponto em que as duas
fases se equilibram, o que dá custo total esperado `Θ(n^{5/3})`.

A dedução: o desvio-padrão do estimador de posto é `O(1/√s)`, logo o
deslocamento típico após a Fase 1 é `O(n/√s)`. Igualar o custo da Fase 1 (`n·s`)
ao da Fase 2 (da ordem de `n·w` com `w` na ordem do deslocamento) leva a
`s = Θ(n^{2/3})`.

## Considered Options

- **`s` menor (ex. `n^{1/2}`)** — Fase 1 mais barata, mas deslocamento residual
  maior e janela mais larga; a Fase 2 passa a dominar.
- **`s` maior (ex. `n^{3/4}`)** — estimativas melhores, mas o ganho na Fase 2 é
  anulado pelo custo da própria sondagem. Há uma barreira estrutural aqui:
  nenhum `s` faz o OSJ alcançar `n log n`.
- **`s` adaptativo a uma medida de desordem** — recuperaria o melhor caso `Θ(n)`,
  hoje ausente. Não implementado; registrado como trabalho futuro.

## Consequências

- Reverter a escolha invalida a análise assintótica e **todas** as tabelas do
  relatório — é a decisão mais caramente acoplada à entrega.
- O expoente empírico medido foi **1,59**, abaixo dos 1,667 previstos. A cota
  `D ≤ 2εn` de Hoeffding é folgada, e o deslocamento real fica bem abaixo do
  previsto; uma análise via estatísticas de ordem daria um expoente ótimo
  ligeiramente diferente.
- Os parâmetros são configuráveis (`osj_sort(arr, s=..., w=...)`), mas os padrões
  de `default_s`/`default_w` são o que o relatório analisa.
