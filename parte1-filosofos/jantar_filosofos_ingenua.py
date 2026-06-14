import random
import threading
import time


N = 5
TEMPO_TIMEOUT = 1.5


def registrar(filosofo, mensagem):
    print(f"[Filosofo {filosofo}] {mensagem}", flush=True)


def pensar(filosofo):
    registrar(filosofo, "pensando")
    time.sleep(random.uniform(0.2, 0.5))


def comer(filosofo):
    registrar(filosofo, "comendo")
    time.sleep(random.uniform(0.2, 0.5))


def filosofo_ingenuo(indice, garfos, barreira_inicio):
    garfo_esquerda = indice
    garfo_direita = (indice + 1) % N

    pensar(indice)
    registrar(indice, "com fome")
    barreira_inicio.wait()

    garfos[garfo_esquerda].acquire()
    registrar(indice, f"pegou garfo esquerdo ({garfo_esquerda})")

    # Esse sleep ajuda a mostrar o problema na pratica.
    time.sleep(0.3)

    registrar(indice, f"tentando pegar garfo direito ({garfo_direita})")
    pegou_direita = garfos[garfo_direita].acquire(timeout=TEMPO_TIMEOUT)

    if not pegou_direita:
        registrar(
            indice,
            "nao conseguiu pegar o garfo direito (deadlock)",
        )
        garfos[garfo_esquerda].release()
        registrar(indice, "liberou garfo esquerdo")
        return

    try:
        registrar(indice, f"pegou garfo direito ({garfo_direita})")
        comer(indice)
    finally:
        garfos[garfo_direita].release()
        garfos[garfo_esquerda].release()
        registrar(indice, "liberou garfos")


def criar_garfos():
    return [threading.Lock() for _ in range(N)]


def executar_versao_ingenua():
    print("\n=== Versao ingenua: risco de deadlock ===\n", flush=True)
    garfos = criar_garfos()
    barreira_inicio = threading.Barrier(N)
    threads = []

    for indice in range(N):
        thread = threading.Thread(
            target=filosofo_ingenuo,
            args=(indice, garfos, barreira_inicio),
            name=f"filosofo-ingenuo-{indice}",
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(
        "\nFim da versao ingenua. Quando todos seguram um garfo e esperam "
        "o outro, o deadlock pode acontecer.\n",
        flush=True,
    )


if __name__ == "__main__":
    executar_versao_ingenua()
