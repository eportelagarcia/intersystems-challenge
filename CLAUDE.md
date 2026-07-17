# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

InterSystems IRIS programming challenge template. The task: read CSV files from `data/in/`, process the data, write output to `data/out/`, optimized for speed. The entry point is `src/RunScript.mac` — a Cache ObjectScript (COS) routine executed via `do ^RunScript` in the IRIS terminal.

## Language

All application code is **Cache ObjectScript** (`.mac` files). This is MUMPS-derived — uses `Set`, `Write`, `Do`, `$ZHOROLOG` for timing, `#;` for comments, dot-syntax method calls (`##class(Package.Class).Method()`). The namespace is `USER`.

## Build & Run

```bash
# Build and start the IRIS container
docker-compose up --build -d

# Open IRIS terminal
docker-compose exec iris iris session iris -U USER

# Run the script (this is how the challenge is evaluated)
USER> do ^RunScript

# Rebuild from scratch (no cache)
docker compose build --no-cache --progress=plain
```

## Architecture

- `src/RunScript.mac` — The only application source file. All challenge logic goes here.
- `data/in/*.csv.gz` — Input: 20 gzipped EpochPhotometry CSV files.
- `data/out/` — Output directory (created by your code).
- `Dockerfile` — Builds on `intersystems/iris-community:latest-em`, copies source, runs `iris.script` during build.
- `iris.script` — Build-time IRIS commands: disables password expiry, enables CallIn for Embedded Python.
- `merge.cpf` — Creates a `TEMP_DATA` database and enables `%Service_CallIn`.
- `docker-compose.yml` — Mounts repo at `/home/irisowner/dev`, exposes ports 1972 (SuperServer), 52773 (web), 53773.

## Key Details

- The container mounts the repo to `/home/irisowner/dev` — file paths in COS use this base.
- Embedded Python is available (`PYTHON_PATH=/usr/irissys/bin/`). You can call Python from COS if needed.
- Default credentials: `_SYSTEM` / `SYS`.
- CI runs `docker build` with `TESTS=1` build arg on push/PR to main/master.
- A `TEMP_DATA` database is provisioned via `merge.cpf` for scratch storage.
