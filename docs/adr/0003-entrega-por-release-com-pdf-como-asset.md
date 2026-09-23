# A entrega é uma release com tag, e o PDF do relatório é asset, não arquivo versionado

O relatório é o `README.md` — fonte única, em Markdown, que o enunciado aceita
explicitamente (Opção A: "PDF / Markdown"). Mas ele usa `$$…$$` em profusão
(Hoeffding, a otimização de `s`, a função potencial): renderiza no GitHub e em
editores com KaTeX, e vira texto cru num visualizador de Markdown comum. Se a
entrega chegar como arquivo em vez de link, a matemática não abre.

A entrega, portanto, é uma **release com tag** no repositório, com o PDF do
relatório anexado como **asset** — gerado a partir do `README.md` daquela tag,
nunca commitado.

## Considered Options

- **PDF versionado no repositório** — obsoleto na primeira edição do README, e
  nada garante que o binário corresponda ao Markdown ao lado dele. Um leitor que
  abrir o PDF não tem como saber se está lendo a versão atual.
- **Um `relatorio.md` separado do `README.md`** — duas fontes que divergem no
  primeiro ajuste. Rejeitado: o `README.md` *é* o relatório.
- **Só o link do repositório, sem PDF** — depende do renderizador do avaliador.
- **Release com PDF como asset** — adotado. A tag prende o PDF a um estado
  imutável do relatório, e o tarball automático já leva código e suíte, que o
  enunciado exige junto.

## Consequências

- O PDF é **derivado**, não fonte: reconstruído a cada release a partir do
  `README.md` da tag (`pandoc README.md -o TP1-OSJ.pdf -V geometry:margin=2cm
  --toc`; `pdflatex` via MiKTeX tipografa a matemática). Fallback sem toolchain:
  imprimir para PDF a página renderizada do GitHub na tag.
- Duas verificações **visuais** são obrigatórias antes de publicar o asset, e não
  são automatizáveis por asserção: as tabelas de 5 colunas (§5.3, §6.3) estouram
  a largura da página em LaTeX, e os links relativos (`resultados/*.csv`) não
  resolvem dentro de um PDF — no build devem ser reescritos para a URL da tag.
- Isso é **assimétrico** em relação a `resultados/`, que é versionado de
  propósito, e a assimetria é deliberada: `resultados/` é evidência primária
  citada pelo texto; o PDF é uma renderização do próprio texto.
- As *release notes* carregam a receita de reprodução (`uv sync`, os comandos de
  execução, a semente fixa, o `uv.lock`) — é a resposta ao critério de rejeito
  por irreprodutibilidade, colocada onde o avaliador vai olhar.
- A release sai de `main`, o que torna o merge `dev → main` parte do ritual de
  entrega.
