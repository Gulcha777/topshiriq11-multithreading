from pathlib import Path
from app.vazifa1_race_condition import run_locked_counter, run_unsafe_counter
from app.vazifa2_threadpool_files import benchmark_files
from app.vazifa3_producer_consumer_deadlock import (
    capture_deadlock_thread_dump,
    run_deadlock_fixed_ordered,
    run_producer_consumer,
)


def test_locked_counter_reaches_exact_million():
    assert run_locked_counter(10, 100_000) == 1_000_000


def test_unsafe_counter_shows_race_condition():
    val = run_unsafe_counter(10, 100_000)
    assert val <= 1_000_000


def test_threadpool_faster_than_sequential(tmp_path: Path):
    res = benchmark_files(folder=tmp_path / "files", max_workers=8)
    assert res["files_count"] == 100
    assert res["parallel_sec"] < res["sequential_sec"]


def test_producer_consumer_and_deadlock_fix():
    items = run_producer_consumer(10)
    assert len(items) == 10
    dump = capture_deadlock_thread_dump()
    assert dump["deadlock_detected"] is True
    assert run_deadlock_fixed_ordered() == ["Safe-T1", "Safe-T2"]
