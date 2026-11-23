# Topshiriq №11 (M11 + A11): Ko'p oqimli dasturlash (Multithreading)

**Talaba:** Xamroyeva Gulruh  
**Guruh:** 1-1DIM-24  
**GitHub repozitoriy:** https://github.com/Gulcha777/topshiriq11-multithreading

---

## Loyiha tuzilmasi

- `app/vazifa1_race_condition.py` — 10 ta oqim × 100 000 marta hisoblagich: race condition va `threading.Lock` yechimi
- `app/vazifa2_threadpool_files.py` — `ThreadPoolExecutor` yordamida 100 ta faylni parallel qayta ishlash va ketma-ket vaqt bilan solishtirish
- `app/vazifa3_producer_consumer_deadlock.py` — `queue.Queue` (BlockingQueue) Producer–Consumer, deadlock, `faulthandler` thread dump tahlili va Lock tartibi (`Lock A -> Lock B`) yechimi
- `app/demo_flow.py` — Barcha vazifalarni ishga tushirib natijani ko'rsatuvchi demo skript
- `tests/test_multithreading.py` — `pytest` testlari
- `docs/deadlock_diagram.png` — Deadlock stsenariysi va Lock tartibi blok-sxemasi
