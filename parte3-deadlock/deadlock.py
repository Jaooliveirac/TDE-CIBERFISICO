import threading
import time
import os

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()

def thread_1_func():
    with LOCK_A:
        print("[Thread 1]: Adquiriu LOCK_A. Aguardando LOCK_B")
        time.sleep(0.05)  
        
        with LOCK_B:
            print("[Thread 1]: Adquiriu LOCK_B! Concluiu seção crítica")

def thread_2_func():
    with LOCK_B:
        print("[Thread 2]: Adquiriu LOCK_B. Aguardando LOCK_A")
        time.sleep(0.05)  
        
        with LOCK_A:
            print("[Thread 2]: Adquiriu LOCK_A! Concluiu seção crítica")

if __name__ == "__main__":
    print(f"PID do Processo: {os.getpid()}")
    print("Iniciando simulação de Deadlock\n")

    t1 = threading.Thread(target=thread_1_func, name="Thread-1")
    t2 = threading.Thread(target=thread_2_func, name="Thread-2")

    t1.start()
    t2.start()
    t1.join()
    t2.join()