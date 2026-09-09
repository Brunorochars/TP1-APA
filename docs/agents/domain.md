# Docs de domínio

Como as skills de engenharia devem consumir a documentação de domínio deste
repositório ao explorar o código.

## Antes de explorar, leia

- **`CONTEXT.md`** na raiz — o glossário do domínio do OSJ.
- **`docs/adr/`** — os ADRs que tocam a área em que você vai trabalhar.

Não existe `CONTEXT-MAP.md`: este é um repositório **single-context**.

## Estrutura

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-sondagem-independente-como-o-osj.md
│   └── 0002-parametros-em-n-elevado-a-dois-tercos.md
└── python/
```

## Use o vocabulário do glossário

Quando sua saída nomear um conceito do domínio — título de issue, proposta de
refatoração, hipótese, nome de teste — use o termo como o `CONTEXT.md` o define.
Não derive para sinônimos que o glossário lista como a evitar.

O caso mais fácil de errar neste projeto: **"deslocamento"** é a distância entre
um elemento e o seu posto correto (um *estado*, o que `max_displacement()` mede).
A *ação* de mover um elemento uma casa é **"troca de vizinhos"** (`shifts`).
Trocar os dois torna a dedução de `w` incompreensível.

Se o conceito que você precisa ainda não está no glossário, isso é um sinal: ou
você está inventando linguagem que o projeto não usa (reconsidere), ou existe uma
lacuna real (anote para o `/grill-with-docs`).

## Sinalize conflito com ADR

Se sua saída contradiz um ADR existente, diga isso explicitamente em vez de
sobrescrever em silêncio:

> _Contradiz o ADR-0001 (sondagem independente como o OSJ) — mas vale reabrir
> porque…_

Atenção especial ao **ADR-0001**: ele fixa a variante de sondagem independente
como o OSJ, apesar de a compartilhada medir melhor. Propostas de "otimizar a Fase
1" adotando a amostra compartilhada não são melhorias — elas atingem a alegação
de autoria do trabalho.
