# Parte 3 — Deadlock

Nesta parte foi feita uma simulação direta de deadlock usando duas threads e dois locks compartilhados no Python.

O objetivo é ver na prática como a inversão na ordem de pedido de recursos trava o sistema e como resolver isso com uma regra de prioridade.

Arquivos

deadlock.py: versão que trava o terminal.

deadlock_corrigido.py: versão corrigida.

Versão que trava:

Na versão que trava, as duas threads tentam pegar os mesmos dois locks (LOCK_A e LOCK_B), mas em ordens cruzadas:

Thread 1: pega o LOCK_A, dorme 50ms, e tenta pegar o LOCK_B.

Thread 2: pega o LOCK_B, dorme 50ms, e tenta pegar o LOCK_A.

O uso do time.sleep garante que as duas threads rodem juntas. O problema é que a Thread 1 fica segurando o lock A e esperando o B, enquanto a Thread 2 fica segurando o lock B e esperando o A. Nenhuma solta o que tem e nenhuma consegue avançar, travando o terminal.

Exemplo nos logs (o terminal trava aqui):

PID do Processo: 21836
Iniciando simulação de Deadlock

[Thread 1]: Adquiriu LOCK_A. Aguardando LOCK_B
[Thread 2]: Adquiriu LOCK_B. Aguardando LOCK_A

Condições de Coffman

Na versão que trava, as quatro condições acontecem ao mesmo tempo:

Exclusão mútua: um lock só pode ser segurado por uma thread de cada vez.

Manter e esperar: a Thread 1 segura o lock A enquanto espera o lock B (e a Thread 2 faz o inverso).

Não preempção: o sistema não tira o lock de uma thread à força para dar para a outra.

Espera circular: a Thread 1 espera pela Thread 2, que por sua vez está esperando pela Thread 1, fechando um ciclo.

Versão corrigida:

Na versão corrigida, todas as threads devem pegar o LOCK_A primeiro e o LOCK_B depois.

Esquema lógico:
Thread 1 e Thread 2:
adquirir(LOCK_A)
adquirir(LOCK_B)

seção crítica
liberar(LOCK_B)
liberar(LOCK_A)

Essa mudança simples quebra a espera circular (a quarta condição de Coffman). Se a Thread 1 pegar o LOCK_A primeiro, a Thread 2 vai ficar parada logo no início esperando o LOCK_A liberar, sem chegar a tocar no LOCK_B. Isso elimina qualquer chance de criar um ciclo de espera.

Progresso:

Com a correção, o programa flui sem interrupções. Uma thread faz todo o seu trabalho, libera os dois locks e só então a próxima thread entra e faz o dela.

Logs da versão corrigida:

Iniciando simulação CORRIGIDA (Hierarquia de Recursos)...

[Thread 1]: Adquiriu LOCK_A. Aguardando LOCK_B...
[Thread 1]: Adquiriu LOCK_B! Seção crítica executada com sucesso.
[Thread 2]: Adquiriu LOCK_A. Aguardando LOCK_B...
[Thread 2]: Adquiriu LOCK_B! Seção crítica executada com sucesso.

Programa finalizado com sucesso (sem deadlocks)!

Como executar

Entrar na pasta:
cd parte3-deadlock

Rodar a versão que trava:
python deadlock.py

Rodar a versão corrigida:
python deadlock_corrigido.py
