import threading
import time


T = 8
M = 200000

contador = 0


def tarefa():
    global contador

    for _ in range(M):
        valor_atual = contador
        time.sleep(0)
        contador = valor_atual + 1


def executar():
    global contador

    contador = 0
    valor_esperado = T * M
    threads = []

    for indice in range(T):
        thread = threading.Thread(target=tarefa, name=f"thread-{indice}")
        threads.append(thread)

    inicio = time.perf_counter()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    tempo = time.perf_counter() - inicio
    perdidos = valor_esperado - contador

    print("\n=== Versao sem sincronizacao ===")
    print(f"Threads: {T}")
    print(f"Incrementos por thread: {M}")
    print(f"Valor esperado: {valor_esperado}")
    print(f"Valor obtido: {contador}")
    print(f"Incrementos perdidos: {perdidos}")
    print(f"Tempo: {tempo:.2f} segundos")

    return {
        "versao": "Sem sincronizacao",
        "esperado": valor_esperado,
        "obtido": contador,
        "perdidos": perdidos,
        "tempo": tempo,
    }


if __name__ == "__main__":
    executar()
