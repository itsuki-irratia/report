#!/bin/bash
python 3 -m venv venv
source venv/bin/activate.fish
python3 main.py --log-file="2025-09.log" --since="2025-09-01 00:00:00" --until="2025-09-30 23:59:59"
python3 main.py --log-file="2025-10.log" --since="2025-10-01 00:00:00" --until="2025-10-31 23:59:59"
python3 main.py --log-file="2025-11.log" --since="2025-11-01 00:00:00" --until="2025-11-30 23:59:59"
python3 main.py --log-file="2025-12.log" --since="2025-12-01 00:00:00" --until="2025-12-31 23:59:59"
python3 main.py --log-file="2026-01.log" --since="2026-01-01 00:00:00" --until="2026-01-31 23:59:59"
python3 main.py --log-file="2026-02.log" --since="2026-02-01 00:00:00" --until="2026-02-28 23:59:59"
python3 main.py --log-file="2026-03.log" --since="2026-03-01 00:00:00" --until="2026-03-31 23:59:59"
python3 main.py --log-file="2026-04.log" --since="2026-04-01 00:00:00" --until="2026-04-30 23:59:59"
python3 main.py --log-file="2026-05.log" --since="2026-05-01 00:00:00" --until="2026-05-31 23:59:59"
