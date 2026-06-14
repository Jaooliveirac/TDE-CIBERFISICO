Parte 1 - Jantar dos Filosofos

Nesta parte foi feita uma simulacao simples do problema do jantar dos filosofos usando threading do Python.

A mesa tem 5 filosofos e 5 garfos. Cada filosofo alterna entre pensar, ficar com fome e comer. Para comer, ele precisa pegar dois garfos: o da esquerda e o da direita. Como os garfos sao compartilhados com os vizinhos, aparece o problema de concorrencia.

Arquivos

jantar_filosofos_ingenua.py: versão que mostra o risco de deadlock.
jantar_filosofos_corrigido.py: versão corrigida usando hierarquia de recursos.

Versao ingenua

Na versao ingenua, todos fazem a mesma coisa:

1. pegam o garfo da esquerda;
2. esperam um pouco;
3. tentam pegar o garfo da direita.

O problema e que pode acontecer de todos pegarem o garfo da esquerda ao mesmo tempo. Ai cada um fica segurando um garfo e esperando o garfo do vizinho. Ninguem consegue continuar, que e a situacao de deadlock.

No codigo eu usei acquire(timeout=...) na hora de pegar o segundo garfo. Assim o programa nao trava para sempre no terminal, mas ainda da para ver nos logs a situacao acontecendo.

Exemplo:

[Filosofo 0] pegou garfo esquerdo (0)
[Filosofo 1] pegou garfo esquerdo (1)
[Filosofo 2] pegou garfo esquerdo (2)
[Filosofo 0] tentando pegar garfo direito (1)
[Filosofo 0] nao conseguiu pegar o garfo direito (deadlock)

Condicoes de Coffman

Na versao ingenua aparecem as quatro condicoes:

1. Exclusao mutua: um garfo nao pode ser usado por dois filosofos ao mesmo tempo.
2. Manter e esperar: o filosofo segura um garfo enquanto espera o outro.
3. Nao preempcao: um filosofo nao pode tomar o garfo de outro a forca.
4. Espera circular: cada filosofo pode ficar esperando o garfo que esta com o proximo.

Com essas quatro condicoes juntas, o deadlock pode acontecer.

Versao corrigida

Na versao corrigida foi usada hierarquia de recursos.

Cada garfo tem um numero de 0 a 4. O filosofo calcula quais sao seus dois garfos e sempre pega primeiro o garfo de menor numero. Depois pega o de maior numero.

Para o filosofo p:

garfo_esquerda = p
garfo_direita = (p + 1) % N

primeiro = min(garfo_esquerda, garfo_direita)
segundo = max(garfo_esquerda, garfo_direita)

Depois ele faz:

pensar()
estado = "com fome"
pegar primeiro
pegar segundo
estado = "comendo"
comer()
liberar segundo
liberar primeiro
estado = "pensando"

Essa ordem quebra a espera circular, porque todos passam a respeitar uma ordem unica para pegar os recursos. Entao a condicao de Coffman negada pela solucao foi a espera circular.

Progresso e inanicacao

A solucao corrigida evita deadlock porque nao deixa formar um ciclo de espera entre os filosofos.

Na simulacao, cada filosofo executa 3 ciclos. Tambem foram usados tempos pequenos e aleatorios para pensar e comer, entao os filosofos nao tentam sempre pegar os garfos no mesmo instante. Depois de comer, cada um libera os dois garfos corretamente.

Com isso, na execucao do programa todos conseguem comer e terminar. Para uma justica ainda mais forte em um sistema real, daria para adicionar uma fila ou um semaforo justo, mas para esta simulacao a combinacao de hierarquia, liberacao correta e tempos alternados garante progresso e evita inanicacao na pratica.

Como executar

Entrar na pasta:

cd parte1-filosofos

Rodar a versao ingenua:

python jantar_filosofos_ingenua.py

Rodar a versao corrigida:

python jantar_filosofos_corrigido.py

Logs

A versao ingenua deve mostrar filosofos pegando o garfo esquerdo e depois falhando ao tentar pegar o direito.

A versao corrigida deve terminar com:

Versao corrigida finalizada normalmente.
