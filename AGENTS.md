# AGENTS.md

German statistics scaled to a village of 2000. Data in `data/*` -> [scripts/gen_data.py](scripts/gen_data.py) -> `web/data.js` (vanilla JS, no build).

## Data

- `data/data.tsv`: each row has `Personen` (int) OR `Prozent` (float, `.`); the other is derived from `data/population.tsv`. Also `countries.tsv`, `flaechennutzung.csv` (`;`-delimited), [Weitere_Zahlen.md](Weitere_Zahlen.md) (converted to HTML, `# Title` dropped).
- After editing any `data/` file: `uv run python scripts/gen_data.py` rewrites `web/data.js` (gitignored, so it must be regenerated before local viewing via `file://` or deploy). CI regenerates it to catch data errors.

## Commands (from repo root)

- Setup: `uv sync`
- Checks: `scripts/run_checks.sh` runs all checks (ruff, prek, rumdl, cspell, biome, pytest). `scripts/update.sh` refreshes deps, then runs checks.
- Deploy: `scripts/deploy.sh` -> ruff, regenerate `data.js`, rsync `web/` to `entorb.net` (needs SSH).

## Gotchas

- CI gates (`.github/workflows/check.yml`): prek, rumdl, cspell, biome, `ruff format --check`, `ruff check --no-fix`, regenerate `data.js`, `pytest tests/`.
- `ruff.toml` selects ALL rules; line length 88, LF endings.
- cspell checks German + English; new words -> `cspell-words.txt` (kept sorted by prek). `data/*` excluded.
- rumdl disables only MD013.
- Frontend: plain JS, tab-indented, checked with Biome (`scripts/chk_biome.sh`). UI text stays German.
- Only `scripts/gen_data.py` is unit-tested; `tests/` import it via `sys.path` hack.
