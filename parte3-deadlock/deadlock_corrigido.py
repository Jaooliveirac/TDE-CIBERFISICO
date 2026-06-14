import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()

def thread_1_func():
    
    with LOCK_A:
        print("[Thread 1]: Adquiriu LOCK_A. Aguardando LOCK_B")
        time.sleep(0.05)
        
        with LOCK_B:
            print("[Thread 1]: Adquiriu LOCK_B! Seção crítica executada com sucesso")

def thread_2_func():
    
    with LOCK_A:  
        print("[Thread 2]: Adquiriu LOCK_A. Aguardando LOCK_B")
        time.sleep(0.05)
        
        with LOCK_B:
            print("[Thread 2]: Adquiriu LOCK_B! Seção crítica executada com sucesso")

if __name__ == "__main__":
    print("Iniciando simulação CORRIGIDA (Hierarquia de Recursos)\n")

    t1 = threading.Thread(target=thread_1_func, name="Thread-1")
    t2 = threading.Thread(target=thread_2_func, name="Thread-2")

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
    print("\nPrograma finalizado com sucesso (sem deadlocks)!")