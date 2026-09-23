# Issue tracker: GitHub

As issues e PRDs deste repositório vivem como **issues do GitHub**, em
`Brunorochars/TP1-APA`. Use o `gh` CLI para todas as operações — ele infere o
repositório a partir do `git remote`, então basta rodar de dentro do clone.

## Receitas

- **Criar issue**: `gh issue create --title "..." --body-file corpo.md`
- **Ler issue**: `gh issue view <número> --comments`
- **Listar issues**:
  ```bash
  gh issue list --state open --json number,title,body,labels,comments \
    --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'
  ```
  com os filtros `--label` / `--state` que o caso pedir.
- **Comentar**: `gh issue comment <número> --body-file comentario.md`
- **Aplicar / remover label**: `gh issue edit <número> --add-label "..."` /
  `--remove-label "..."`
- **Fechar**: `gh issue close <número> --comment "..."`

## Quando uma skill diz "publique no issue tracker"

Crie uma issue no GitHub.

## Quando uma skill diz "busque o ticket relevante"

Rode `gh issue view <número> --comments`.

## Notas específicas deste repositório

- **O repositório é do grupo** (`Brunorochars/TP1-APA`), não pessoal. Criar
  issues, labels ou comentários é visível para os outros integrantes — trate como
  ação externa, não como rascunho local.
- **Corpos multilinha vão por arquivo ou heredoc**, nunca por here-string do
  PowerShell dentro da tool `Bash`. Prefira `--body-file arquivo.md`; se for
  heredoc, `<<'EOF'`. Um erro de sintaxe aqui não falha — ele publica o texto
  errado e segue calado.
- **Não há issues abertas hoje.** O tracker foi configurado antes do primeiro uso.
