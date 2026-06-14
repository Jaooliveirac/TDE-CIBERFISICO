import threading
import time


T = 8
M = 200000

contador = 0


def tarefa(semaforo):
    global contador

    for _ in range(M):
        semaforo.acquire()
        try:
            contador = contador + 1
        finally:
            semaforo.release()


def executar():
    global contador

    contador = 0
    valor_esperado = T * M
    semaforo = threading.Semaphore(1)
    threads = []

    for indice in range(T):
        thread = threading.Thread(
            target=tarefa,
            args=(semaforo,),
            name=f"thread-{indice}",
        )
        threads.append(thread)

    inicio = time.perf_counter()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    tempo = time.perf_counter() - inicio
    perdidos = valor_esperado - contador

    print("\n=== Versao com semaforo ===")
    print(f"Threads: {T}")
    print(f"Incrementos por thread: {M}")
    print(f"Valor esperado: {valor_esperado}")
    print(f"Valor obtido: {contador}")
    print(f"Incrementos perdidos: {perdidos}")
    print(f"Tempo: {tempo:.2f} segundos")

    return {
        "versao": "Com semaforo",
        "esperado": valor_esperado,
        "obtido": contador,
        "perdidos": perdidos,
        "tempo": tempo,
    }


if __name__ == "__main__":
    executar()
