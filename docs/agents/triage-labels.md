# Labels de triagem

As skills falam em cinco papéis canônicos de triagem. Esta tabela mapeia cada
papel para a string de label realmente usada no tracker deste repositório.

| Papel (em mattpocock/skills) | Label neste repositório | Significado |
| ---------------------------- | ----------------------- | ----------- |
| `needs-triage`               | `needs-triage`          | Precisa de avaliação do mantenedor |
| `needs-info`                 | `needs-info`            | Aguardando informação do relator |
| `ready-for-agent`            | `ready-for-agent`       | Totalmente especificada, pronta para um agente AFK |
| `ready-for-human`            | `ready-for-human`       | Exige implementação humana |
| `wontfix`                    | `wontfix`               | Não será feita |

Quando uma skill mencionar um papel (ex.: "aplique a label de pronto para AFK"),
use a string da coluna do meio.

## Estado no repositório

As cinco labels **existem** em `Brunorochars/TP1-APA`:

- `wontfix` já vinha do conjunto padrão do GitHub.
- `needs-triage`, `needs-info`, `ready-for-agent` e `ready-for-human` foram
  criadas na sessão de adoção do repositório.

Não há renomeação: o grupo não tinha nomenclatura própria de triagem, só os
labels padrão do GitHub, então não havia com o que colidir. Para mudar o
vocabulário, edite a coluna do meio — as skills leem daqui, não de uma lista
fixa.
