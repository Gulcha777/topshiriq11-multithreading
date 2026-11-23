import faulthandler
import io
import queue
import threading
import time


def run_producer_consumer(total_items: int = 12, queue_capacity: int = 4) -> list[str]:
    blocking_queue: queue.Queue[str | None] = queue.Queue(maxsize=queue_capacity)
    processed: list[str] = []

    def producer() -> None:
        for i in range(1, total_items + 1):
            blocking_queue.put(f"task-{i:02d}")
            time.sleep(0.002)
        blocking_queue.put(None)

    def consumer() -> None:
        while True:
            item = blocking_queue.get()
            if item is None:
                blocking_queue.task_done()
                break
            processed.append(item)
            blocking_queue.task_done()

    p = threading.Thread(target=producer, name="Producer-Thread")
    c = threading.Thread(target=consumer, name="Consumer-Thread")
    p.start()
    c.start()
    p.join()
    c.join()
    return processed


def capture_deadlock_thread_dump() -> dict:
    lock_a = threading.Lock()
    lock_b = threading.Lock()
    t1_acquired_a = threading.Event()
    t2_acquired_b = threading.Event()
    release_event = threading.Event()

    def worker_t1() -> None:
        with lock_a:
            t1_acquired_a.set()
            t2_acquired_b.wait(timeout=1.0)
            got_b = lock_b.acquire(timeout=0.35)
            if got_b:
                lock_b.release()
            release_event.wait(timeout=0.5)

    def worker_t2() -> None:
        t1_acquired_a.wait(timeout=1.0)
        with lock_b:
            t2_acquired_b.set()
            got_a = lock_a.acquire(timeout=0.35)
            if got_a:
                lock_a.release()
            release_event.wait(timeout=0.5)

    t1 = threading.Thread(target=worker_t1, name="Deadlock-T1")
    t2 = threading.Thread(target=worker_t2, name="Deadlock-T2")
    t1.start()
    t2.start()
    time.sleep(0.08)

    dump_buf = io.StringIO()
    faulthandler.dump_traceback(file=dump_buf, all_threads=True)
    raw_dump = dump_buf.getvalue()

    release_event.set()
    t1.join()
    t2.join()
    return {"deadlock_detected": "worker_t1" in raw_dump and "worker_t2" in raw_dump, "dump_preview": raw_dump[:900]}


def run_deadlock_fixed_ordered() -> list[str]:
    lock_a = threading.Lock()
    lock_b = threading.Lock()
    completed: list[str] = []

    def ordered_worker(worker_name: str) -> None:
        with lock_a:
            with lock_b:
                completed.append(worker_name)

    t1 = threading.Thread(target=ordered_worker, args=("Safe-T1",), name="Safe-T1")
    t2 = threading.Thread(target=ordered_worker, args=("Safe-T2",), name="Safe-T2")
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return completed
