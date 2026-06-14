import random
import threading
import time


N = 5
CICLOS = 3


def registrar(filosofo, mensagem):
    print(f"[Filosofo {filosofo}] {mensagem}", flush=True)


def pensar(filosofo):
    registrar(filosofo, "pensando")
    time.sleep(random.uniform(0.2, 0.5))


def comer(filosofo):
    registrar(filosofo, "comendo")
    time.sleep(random.uniform(0.2, 0.5))


def filosofo_corrigido(indice, garfos, ciclos):
    garfo_esquerda = indice
    garfo_direita = (indice + 1) % N
    primeiro = min(garfo_esquerda, garfo_direita)
    segundo = max(garfo_esquerda, garfo_direita)

    for ciclo in range(1, ciclos + 1):
        registrar(indice, f"iniciando ciclo {ciclo}")
        pensar(indice)
        registrar(indice, "com fome")

        registrar(indice, f"tentando pegar primeiro garfo ({primeiro})")
        garfos[primeiro].acquire()
        registrar(indice, f"pegou primeiro garfo ({primeiro})")

        registrar(indice, f"tentando pegar segundo garfo ({segundo})")
        garfos[segundo].acquire()
        registrar(indice, f"pegou segundo garfo ({segundo})")

        try:
            comer(indice)
        finally:
            garfos[segundo].release()
            registrar(indice, f"liberou segundo garfo ({segundo})")
            garfos[primeiro].release()
            registrar(indice, f"liberou primeiro garfo ({primeiro})")

        time.sleep(random.uniform(0.05, 0.2))

    registrar(indice, "terminou todos os ciclos")


def criar_garfos():
    return [threading.Lock() for _ in range(N)]


def executar_versao_corrigida():
    print("\n=== Versao corrigida: hierarquia de recursos ===\n", flush=True)
    garfos = criar_garfos()
    threads = []

    for indice in range(N):
        thread = threading.Thread(
            target=filosofo_corrigido,
            args=(indice, garfos, CICLOS),
            name=f"filosofo-corrigido-{indice}",
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("\nVersao corrigida finalizada normalmente.\n", flush=True)


if __name__ == "__main__":
    executar_versao_corrigida()
