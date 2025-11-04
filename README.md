# itsuki-report

itsuki irratiaren bisiten erreporte sistema

# remove duplicate entries
```
uniq access.log access-uniq.log
```

# filter log
```
python3 filter.py --log-file="access-uniq.log" --since="2025-10-01 00:00:00" --until="2025-10-31 23:59:59" > 2025-10.log
```

# create report
```
python3 main.py --log-file="2025-10.log" --since="2025-10-01 00:00:00" --until="2025-10-31 23:59:59"
```