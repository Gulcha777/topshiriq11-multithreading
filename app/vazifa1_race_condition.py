import threading
import time


def run_unsafe_counter(num_threads: int = 10, increments_per_thread: int = 100_000) -> int:
    shared_counter = [0]

    def worker() -> None:
        for _ in range(increments_per_thread):
            current = shared_counter[0]
            if _ % 500 == 0:
                time.sleep(0)
            shared_counter[0] = current + 1

    threads = [threading.Thread(target=worker, name=f"Unsafe-{i+1}") for i in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return shared_counter[0]


def run_locked_counter(num_threads: int = 10, increments_per_thread: int = 100_000) -> int:
    shared_counter = [0]
    lock = threading.Lock()

    def worker() -> None:
        for _ in range(increments_per_thread):
            with lock:
                shared_counter[0] += 1

    threads = [threading.Thread(target=worker, name=f"Locked-{i+1}") for i in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return shared_counter[0]
