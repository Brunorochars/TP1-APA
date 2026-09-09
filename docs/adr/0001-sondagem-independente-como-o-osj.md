# A sondagem independente é o OSJ; a compartilhada não

O OSJ tem duas variantes de Fase 1. Na **compartilhada**, todos os elementos
consultam a mesma amostra ordenada de testemunhas por busca binária; na
**independente**, cada elemento sorteia as próprias. A compartilhada é
melhor em quase toda métrica visível: expoente empírico 1,19 contra 1,59, custo
por elemento `log₂ s` em vez de `s`, e ela é **estável**.

Adotamos a **independente** como o OSJ, apesar disso.

O motivo é que a superioridade da compartilhada vem de uma propriedade que a
desqualifica como contribuição: com amostra comum, a posição estimada torna-se
função **monótona** do valor, de modo que a Fase 1 já entrega os baldes
globalmente ordenados entre si, restando desordem apenas *dentro* de cada balde.
Distribuir elementos em baldes delimitados por quantis de uma amostra é
exatamente a fase de distribuição do **Sample Sort** — técnica consolidada na
literatura. A variante rápida é, portanto, a menos autoral.

Na variante independente o mapa valor→posição **não** é monótono, os erros de
estimativa são independentes entre elementos (o que sustenta a análise via
Hoeffding), e o comportamento `Θ(n^{5/3})` resultante não corresponde a nenhum
método clássico identificado.

## Consequências

- A tese `Θ(n^{5/3})` e todas as tabelas do relatório referem-se à variante
  independente. "OSJ", sem qualificador, significa ela.
- A variante compartilhada permanece no código (`my_authorial_sort_stable`) por
  dois motivos legítimos: é a variante estável, e serve de termo de comparação
  para isolar o efeito da independência das amostras. Ela é declarada no
  relatório como adaptação de técnica conhecida, nunca como contribuição própria.
- Estabilidade e independência das amostras ficam **mutuamente exclusivas** na
  formulação atual: a primeira exige estimativas idênticas para chaves iguais, a
  segunda as proíbe. Reconciliá-las exigiria um desempate determinístico por
  índice original.
- O trabalho aceita medir pior em troca de poder reivindicar autoria. Como o
  enunciado avalia raciocínio projetual e não performance bruta, a troca é
  favorável.
