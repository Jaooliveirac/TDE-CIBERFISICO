Parte 2 - Threads e Semaforos

Nesta parte foi feita uma simulacao de varias threads mexendo no mesmo contador.

A ideia e mostrar primeiro o problema sem sincronizacao, onde as threads acessam o contador ao mesmo tempo e alguns incrementos se perdem. Depois o mesmo teste e feito usando um semaforo binario, deixando apenas uma thread por vez alterar o contador.

Arquivos

contador_sem_sincronizacao.py: versao sem protecao, usada para mostrar a perda de incrementos.
contador_com_semaforo.py: versao corrigida com semaforo binario.

Parametros usados

T = 8 threads
M = 200000 incrementos por thread
Valor esperado = 1600000

O que e uma condicao de corrida

Condicao de corrida acontece quando duas ou mais threads acessam o mesmo recurso compartilhado ao mesmo tempo, e o resultado depende da ordem em que elas executam.

No caso do contador, a operacao contador = contador + 1 parece uma coisa so, mas na pratica tem etapas:

1. ler o valor atual;
2. somar 1;
3. gravar o novo valor.

Se duas threads leem o mesmo valor antes de uma gravar, as duas podem escrever o mesmo resultado. Assim um incremento acaba apagando o outro.

Versao sem sincronizacao

Na versao sem sincronizacao, todas as threads usam o mesmo contador global e nenhuma protecao e usada.

O incremento foi separado assim:

valor_atual = contador
time.sleep(0)
contador = valor_atual + 1

O time.sleep(0) foi colocado para facilitar a troca de contexto entre as threads. Isso ajuda a mostrar a corrida em Python, porque o GIL pode esconder o problema quando o incremento e simples demais.

Versao com semaforo

Na versao corrigida foi usado threading.Semaphore(1).

Como o semaforo comeca com apenas uma permissao, ele funciona como semaforo binario. Apenas uma thread por vez entra na parte critica.

A parte critica e o trecho onde o contador e incrementado.

O codigo usa try/finally para garantir que o semaforo seja liberado mesmo se acontecer algum erro dentro da parte critica.

Pseudocodigo

Globais:

contador = 0
semaforo = Semaforo(1)

Versao sem sincronizacao:

para cada thread:
    para i de 1 ate M:
        valor_atual = contador
        contador = valor_atual + 1

Versao com semaforo:

para cada thread:
    para i de 1 ate M:
        semaforo.adquirir()
        try:
            contador = contador + 1
        finally:
            semaforo.liberar()

Programa principal:

iniciar T threads
esperar todas terminarem
imprimir valor esperado
imprimir valor obtido
imprimir incrementos perdidos
imprimir tempo de execucao

Resultados

Execucao | Versao | Valor esperado | Valor obtido | Incrementos perdidos | Tempo
1 | Sem sincronizacao | 1600000 | 200327 | 1399673 | 2.85s
2 | Sem sincronizacao | 1600000 | 200459 | 1399541 | 3.28s
3 | Sem sincronizacao | 1600000 | 200192 | 1399808 | 3.30s
1 | Com semaforo | 1600000 | 1600000 | 0 | 2.16s
2 | Com semaforo | 1600000 | 1600000 | 0 | 2.17s
3 | Com semaforo | 1600000 | 1600000 | 0 | 2.10s

Discussao dos resultados

A versao sem sincronizacao perde incrementos porque varias threads podem ler o mesmo valor antigo do contador. Quando elas gravam o novo valor, uma escrita pode sobrescrever a outra.

A versao com semaforo da o valor correto porque so uma thread por vez executa a parte critica. Assim cada incremento termina antes de outra thread mexer no contador.

O custo disso e desempenho. A versao sem sincronizacao pode parecer mais rapida ou mais solta, mas o resultado final fica errado. A versao com semaforo pode demorar mais, porque as threads precisam esperar sua vez, mas o resultado fica correto.

Sobre justica, o Semaphore do Python nao garante uma fila FIFO perfeita. Mesmo assim, neste experimento todas as threads terminam e o valor final fica certo.

Sobre visibilidade e ordenacao, em Java existe a garantia de happens-before entre o release de uma thread e o acquire de outra. Em Python, as primitivas do threading funcionam como barreiras praticas de sincronizacao, fazendo com que a parte critica seja acessada de forma ordenada neste experimento.

Como executar

Entrar na pasta:

cd parte2-semaforo

Rodar a versao sem sincronizacao:

python contador_sem_sincronizacao.py

Rodar a versao com semaforo:

python contador_com_semaforo.py
