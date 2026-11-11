# Roteiro do teste com usuários

Mínimo de **5 pessoas de fora do grupo**. Cada sessão leva uns 10 minutos.

## Antes de começar (ler para a pessoa)

> "Vamos testar um assistente sobre documentos. Quem está sendo testado é o sistema, não você.
> **Não digite nenhum dado seu de verdade** (CPF, nome, telefone). Não vamos anotar seu nome:
> você vai ser só P1, P2, P3..."

**O que NÃO anotar:** nome, idade exata, telefone, e-mail, foto ou gravação do rosto. Anotar só o código (P1, P2...), o tempo, se acertou e as notas.

## As 3 tarefas

Cronometrar do momento em que a pessoa termina de ler a tarefa até ela falar a resposta. Pode usar o menu ou escrever.

| Tarefa | O que pedir | Resposta certa (fichas) |
|---|---|---|
| T1 | "Você perdeu seu RG. Descubra o que precisa levar para tirar a segunda via." | Certidão de nascimento ou casamento, comprovante de residência dos últimos 90 dias e declaração de extravio (assinada no balcão; BO não é exigido na perda). FC-01 |
| T2 | "Descubra quanto custa e em quanto tempo sai a certidão de nascimento pelo portal." | R$ 49,00, em 3 dias úteis, em PDF. FC-05 |
| T3 | "Descubra se dá para ir à Central num sábado." | Não; segunda a sexta, das 8h às 17h. FC-07 |

## Questionário (depois das 3 tarefas)

Notas de 1 (discordo totalmente) a 5 (concordo totalmente):

1. Foi fácil encontrar a informação que eu procurava.
2. As respostas estavam em uma linguagem fácil de entender.
3. Eu confiaria nas orientações para saber o que levar ao atendimento.
4. Ficou claro de onde vinha a informação (ficha e data).
5. Eu usaria o assistente de novo.

Anotar tudo em `resultados.csv` e rodar `python testes_usuarios/indicadores.py`.
