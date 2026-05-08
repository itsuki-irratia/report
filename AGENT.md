# AGENT.md — Itsuki Irratia Report System

Full context for an AI agent to understand and work on this project without reading source files.

---

## What this project does

Analytics reporting tool for **Itsuki Irratia**, a Basque-language web radio station. It parses Caddy/Icecast server access logs (JSON format), computes listener statistics, generates SVG charts, and produces a Markdown + PDF report. Output is in **Basque (Euskara)**.

---

## Stack

- **Language**: Python 3
- **Dependencies**: `requests`, `pandas`, `matplotlib`
- **External tools** (must be installed separately): `pandoc`, `weasyprint`
- **Geolocation API**: `ip-api.com` (free, no key required, rate-limited)
- **PDF styling**: `md.css` (DejaVu Sans Mono font)

---

## Project layout

```
/home/projects/report/
├── main.py          # Orchestrator: runs the full pipeline, writes report/
├── filter.py        # Pre-processing: filters log lines by date range
├── VisitsDay.py     # Chart: hourly connections/uniques for one day
├── VisitsMonth.py   # Chart: daily connections/uniques for one month
├── Geos.py          # Chart: horizontal bars for city/region/country
├── Devices.py       # Chart: horizontal bars for device/browser breakdown
├── lib/
│   ├── common.py    # CLI arg parsing, timestamp <-> string conversions
│   ├── log.py       # Log parsing, validation, filtering
│   ├── visit.py     # Connection counting, unique IPs, duration math
│   ├── report.py    # Report class: data aggregation with caching
│   ├── device.py    # User-agent -> device label (regex)
│   ├── app.py       # User-agent -> app label (Instagram/FB/WhatsApp/Telegram)
│   ├── geo.py       # IP -> city/region/country via ip-api.com + cache
│   └── md.py        # Markdown string builders for report sections
├── build/           # Generated SVG charts (gitignored)
├── report/          # Generated .md and .pdf reports (gitignored)
├── md.css           # PDF stylesheet
└── requirements.txt # requests, pandas, matplotlib
```

---

## Typical workflow

```bash
# 1. Deduplicate raw Caddy/Icecast log
uniq access.log access-uniq.log

# 2. Filter to desired date range
python3 filter.py \
  --log-file="access-uniq.log" \
  --since="2025-10-01 00:00:00" \
  --until="2025-10-31 23:59:59" > 2025-10.log

# 3. Generate report
python3 main.py \
  --log-file="2025-10.log" \
  --since="2025-10-01 00:00:00" \
  --until="2025-10-31 23:59:59"
```

Outputs: `report/2025-10-01.md` and `report/2025-10-01.pdf`

---

## Input log format

Caddy server logs — each line is a JSON object:

```json
{
  "ts": 1727784000.123,
  "request": {
    "remote_ip": "1.2.3.4",
    "uri": "/itsuki.ogg",
    "headers": { "User-Agent": ["Mozilla/5.0 ..."] }
  },
  "duration": 42.5,
  "status": 200
}
```

Key fields used: `ts`, `request.remote_ip`, `request.uri`, `request.headers.User-Agent[0]`, `duration`, `status`.

---

## Log filtering rules (`lib/log.py`)

A log entry is **accepted** only if ALL of these pass:

| Rule | Detail |
|---|---|
| URI allowed | must match `/itsuki\.(ogg\|mp3\|opus\|aac)` |
| Status | must be `200` |
| IP not local | excludes `192.168.*` |
| User-Agent not blocked | blocks: `Go-http-client`, `curl`, `Lavf`, `GuzzleHttp` |

---

## Data pipeline

```
filter.py            →  date-range filtered .log file
Log.getLines()       →  parse JSON, convert ts to datetime
Log.getByDates()     →  apply validation rules above
Report.get()         →  aggregate: connections, uniques, duration, devices, geos
VisitsDay/Month.py   →  matplotlib SVG charts
Geos.py / Devices.py →  matplotlib SVG charts
md.py                →  markdown string assembly
main.py              →  write .md, run pandoc+weasyprint → .pdf
```

---

## Core classes and functions

### `lib/common.py`
- `getArguments()` — parses `--key=value` CLI args into dict
- `getTimestamp(item)` — extracts int timestamp from log entry
- `getTimestampFromDateString(ds)` — `"YYYY-MM-DD HH:MM:SS"` → Unix timestamp (timezone: **Europe/Madrid**)
- `getDateStringFromTimestamp(ts)` — reverse

### `lib/log.py`
- `getLines(log_file)` — read file, return list of normalized log dicts
- `prepareLog(log, output_mode)` — adds `dt`, `uri`, `remote_ip`, `user_agent`, `duration`, `device`, `app`, `geo` fields
- `getByDates(logs, since, until, output_mode)` — main filter (see rules above)
- `getUniquesByDates(...)` — same but deduplicates by IP

### `lib/visit.py`
- `getConnections(logs)` — count audio requests
- `getUniques(logs)` — list unique IPs
- `countUnique(logs)` — count unique IPs
- `getOgg(logs)` / `getMp3(logs)` — count by codec (OGG/OPUS vs MP3/AAC)
- `getDuration(logs)` — total listen seconds
- `duration2Human(s)` — `{hours, minutes, seconds}` dict

### `lib/report.py — Report class`
- `get(since, until, output_mode)` — returns dict; `output_mode` controls what's included:
  - `'basic'`: connections, unique, duration, since, until
  - `'devices'`: + device breakdown
  - `'apps'`: + app breakdown
  - `'geos'`: + city/region/country breakdown
  - `'full'`: all of the above
- Caches parsed logs internally to avoid re-parsing

### `lib/device.py`
Regex-based detection from user agent string. Labels:
`ios`, `Android`, `bot`, `Firefox`, `Chrome`, `Safari`, `WhatsApp`, `Facebook`, `RadioGarden`, `Go-http-client`, `lavf`, `web / other`

### `lib/app.py`
Social app detection: `instagram`, `facebook`, `whatsapp`, `telegram`, `web / other`

### `lib/geo.py`
- Calls `ip-api.com` REST API per unique IP
- Caches results in `lib/geo.cache.json` (gitignored)
- Handles 429 rate-limit with exponential backoff
- **Special mapping**: `Navarre` and `Basque Country` → `Euskal Herria`
- Region name translations to Basque: `Nafarroa`, `Euskal Autonomi Erkidegoa`
- `getCities(logs)` / `getRegions(logs)` / `getCountries(logs)` — aggregate unique IPs per location

### `lib/md.py`
- `intro()` — describes log architecture (Caddy + Icecast)
- `visistsMonth(since, month_data, duration_data, image, width)` — monthly section
- `visistsDay(since, day_data, image, width)` — per-day section
- `notes(...)` — explains unique visitor math:
  - Sum of daily uniques ≠ monthly unique total
  - Returning visitors = daily_unique_sum − monthly_unique

---

## Charts

All charts saved as SVG to `build/`:

| Script | Output file | Content |
|---|---|---|
| `VisitsDay.py` | `visits-day-{date}.svg` | Hourly connections + unique visitors |
| `VisitsMonth.py` | `visits-month-{date}.svg` | Daily connections + unique visitors |
| `Geos.py` | `geos-{type}-{date}.svg` | Horizontal bars: city/region/country |
| `Devices.py` | `devices-{date}.svg` | Horizontal bars: device breakdown |

Chart sizing for Geos/Devices is dynamic: height scales with number of items.

---

## Unique visitor accounting

Daily uniques are counted per day. A listener who tunes in on multiple days is counted once per day but only once in the monthly total. The report's `notes()` section explains this:

```
returning_visitors = sum(daily_uniques) - monthly_unique_total
```

---

## Timezone

All timestamps are interpreted in **Europe/Madrid** (CET/CEST). This was changed from GMT in a past commit — important if debugging timestamp edge cases.

---

## Language

Report text is in **Basque (Euskara)**. Location names use Basque forms: `Euskal Herria`, `Nafarroa`, `Bilbo`, etc. Do not replace with Spanish equivalents.

---

## Known design decisions

- **GuzzleHttp blocked**: PHP HTTP client used by some bots; added to blocklist after it was found polluting stats.
- **`uniq` pre-processing**: Raw Caddy logs can contain duplicate lines; the workflow requires running `uniq` before filtering.
- **SVG over PNG**: Charts were migrated from PNG to SVG for better quality in PDF output.
- **ip-api.com cache**: `lib/geo.cache.json` is persistent across runs and gitignored. Delete it to force fresh geo lookups.
- **pandoc + weasyprint**: PDF generation is a two-step external process triggered from `main.py`. Both must be installed on the system.

---

## What's gitignored

- `build/*` — generated SVG charts
- `report/*` — generated reports
- `*.log` — input log files
- `*.json` — includes the geo cache
- `lib/__pycache__`, `*.pyc`
- `venv/`
