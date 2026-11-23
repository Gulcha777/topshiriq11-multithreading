import hashlib
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def prepare_sample_files(folder: Path, count: int = 100) -> list[Path]:
    folder.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for i in range(1, count + 1):
        p = folder / f"file_{i:03d}.txt"
        if not p.exists():
            p.write_text(f"Topshiriq 11 test fayli #{i}\nMa'lumot qatori A\nMa'lumot qatori B\n", encoding="utf-8")
        paths.append(p)
    return paths


def process_single_file(path: Path) -> str:
    data = path.read_text(encoding="utf-8")
    digest = hashlib.sha256(data.encode("utf-8")).hexdigest()
    time.sleep(0.002)
    return digest[:16]


def benchmark_files(folder: Path = Path("docs/sample_files"), max_workers: int = 8) -> dict[str, float]:
    files = prepare_sample_files(folder, 100)

    t0 = time.perf_counter()
    seq_results = [process_single_file(p) for p in files]
    seq_sec = time.perf_counter() - t0

    t1 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        par_results = list(executor.map(process_single_file, files))
    par_sec = time.perf_counter() - t1

    assert seq_results == par_results
    speedup = seq_sec / par_sec if par_sec > 0 else 1.0
    return {
        "files_count": len(files),
        "workers": max_workers,
        "sequential_sec": seq_sec,
        "parallel_sec": par_sec,
        "speedup": speedup,
    }
