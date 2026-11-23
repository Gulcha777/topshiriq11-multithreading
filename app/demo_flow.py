from app.vazifa1_race_condition import run_locked_counter, run_unsafe_counter
from app.vazifa2_threadpool_files import benchmark_files
from app.vazifa3_producer_consumer_deadlock import (
    capture_deadlock_thread_dump,
    run_deadlock_fixed_ordered,
    run_producer_consumer,
)


def main() -> None:
    print("=== 1-VAZIFA: RACE CONDITION VA LOCK ===")
    unsafe_val = run_unsafe_counter()
    locked_val = run_locked_counter()
    print("Kutilgan natija : 1,000,000")
    print(f"Lock'siz (Race) : {unsafe_val:,}")
    print(f"Lock bilan      : {locked_val:,}")

    print("\n=== 2-VAZIFA: THREADPOOL (100 TA FAYL) ===")
    bench = benchmark_files()
    print(f"Ketma-ket (1 oqim)     : {bench['sequential_sec']:.4f} s")
    print(f"ThreadPool (8 worker)  : {bench['parallel_sec']:.4f} s ({bench['speedup']:.2f}x tezroq)")

    print("\n=== 3-VAZIFA: PRODUCER-CONSUMER VA DEADLOCK YECHIMI ===")
    items = run_producer_consumer(12)
    dump_info = capture_deadlock_thread_dump()
    fixed = run_deadlock_fixed_ordered()
    print(f"Producer-Consumer qayta ishladi: {len(items)} ta element")
    print(f"Thread dump deadlock aniqlandi : {dump_info['deadlock_detected']}")
    print(f"Lock tartibi (A -> B) yechimi  : {fixed}")


if __name__ == "__main__":
    main()
