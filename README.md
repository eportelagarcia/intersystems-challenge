# Gaia DR3 Epoch Photometry — Variable Star Detector

Processes Gaia DR3 epoch photometry data to identify astronomical objects with significant flux variability (>100% change) across BP and RP bands.

## How It Works

1. **Input**: 20 gzipped CSV files in `data/in/` containing epoch photometry from Gaia DR3. Each row represents one star with time-series flux measurements packed as arrays.

2. **Processing**: For each star, the script:
   - Parses the `bp_flux` and `rp_flux` observation arrays
   - Filters out NaN/invalid values
   - Computes min and max flux for each band
   - Calculates percentage change: `((max - min) / min) × 100`
   - Keeps the larger of BP vs RP percentage change

3. **Output**: `data/out/result.csv` containing only stars where percentage change exceeds 100%, with columns: `source_id, bp_min_flux, bp_max_flux, rp_min_flux, rp_max_flux, percentage_change`

The heavy lifting is done in Python (`src/process.py`) using `multiprocessing.Pool` to process all 20 files in parallel. The IRIS routine (`src/RunScript.mac`) serves as the entry point and timer.

## Installation

Import the RunScript.mac file
Import the process.py file

## Running

```bash
docker-compose exec iris iris session iris -U USER
```

Then in the IRIS terminal:

```
USER> do ^RunScript
```

The script will process all input files and write results to `data/out/result.csv`.

## Project Structure

```
src/
  RunScript.mac   — Entry point (Cache ObjectScript routine)
  process.py      — Data processing (Python, stdlib only)
data/
  in/             — Input CSV files (gzipped)
  out/            — Output results (generated)
```
