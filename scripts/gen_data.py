#!/usr/bin/env python3
"""Convert data/*.tsv|csv into web/data.js so the site works offline via file://."""

import csv
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT = ROOT / "web" / "data.js"

md_link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def md_to_html(src: str) -> str:
    """Render the small markdown subset used by Weitere_Zahlen.md."""
    src = html.escape(src, quote=False)
    src = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", src)
    src = md_link_re.sub(r'<a href="\2">\1</a>', src)

    out: list[str] = []
    in_list = False
    for raw in src.strip().split("\n"):
        line = raw.rstrip()
        if line.startswith("* "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{line[2:]}</li>")
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        if not line:
            continue
        m = re.match(r"(#{1,6})\s+(.*)", line)
        if m:
            level = len(m.group(1))
            out.append(f"<h{level}>{m.group(2)}</h{level}>")
        else:
            out.append(f"<p>{line}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def read_population() -> dict[int, int]:
    """Year -> inhabitants."""
    with (DATA_DIR / "population.tsv").open(encoding="utf-8") as fh:
        rows = csv.DictReader(fh, delimiter="\t")
        return {int(r["Jahr"]): int(r["Einwohner"]) for r in rows}


def read_data(pop: dict[int, int]) -> list[dict]:
    """Fill missing Personen/Prozent, keep both as numbers."""
    out: list[dict] = []
    with (DATA_DIR / "data.tsv").open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            d = {
                "Kategorie": r["Kategorie"],
                "Titel": r["Titel"],
                "Personen": None,
                "Prozent": None,
                "Jahr": int(r["Jahr"]),
                "Kommentar": r["Kommentar"],
                "Quelle": r["Quelle"],
            }
            if r["Personen"]:
                d["Personen"] = int(r["Personen"])
                d["Prozent"] = round(100 * d["Personen"] / pop[d["Jahr"]], 1)
            else:
                d["Prozent"] = float(r["Prozent"])
                d["Personen"] = int(round(d["Prozent"] * 0.01 * pop[d["Jahr"]], 0))
            out.append(d)
    return out


def read_countries() -> tuple[list[dict], list[dict], int]:
    """Return (countries, continents, world population)."""
    with (DATA_DIR / "countries.tsv").open(encoding="utf-8") as fh:
        countries = [
            {
                "Kontinent": r["Kontinent"],
                "Land": r["Land"],
                "Einwohner": int(r["Einwohner"]),
            }
            for r in csv.DictReader(fh, delimiter="\t")
        ]
    countries.sort(key=lambda c: c["Einwohner"], reverse=True)

    by_continent: dict[str, int] = {}
    for c in countries:
        by_continent[c["Kontinent"]] = (
            by_continent.get(c["Kontinent"], 0) + c["Einwohner"]
        )
    continents = [
        {"Kontinent": k, "Einwohner": v}
        for k, v in sorted(by_continent.items(), key=lambda kv: kv[1], reverse=True)
    ]
    world_population = sum(c["Einwohner"] for c in countries)
    return countries, continents, world_population


def read_flaechennutzung() -> list[dict]:
    """Compute percent share, drop total row."""
    with (DATA_DIR / "flaechennutzung.csv").open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter=";"))
    total = float(rows[-1]["qkm"])
    return [
        {
            "Kategorie1": r["Kategorie 1"],
            "Kategorie2": r["Kategorie 2"],
            "Was": r["Was"],
            "qkm": float(r["qkm"]),
            "Prozent": round(100 * float(r["qkm"]) / total, 2),
        }
        for r in rows[:-1]
    ]


def read_weitere_zahlen() -> str:
    """Weitere_Zahlen.md -> html, dropping the '# Title' line."""
    cont = (ROOT / "Weitere_Zahlen.md").read_text(encoding="utf-8").split("\n", 1)[1]
    return md_to_html(cont)


def main() -> None:
    """Write web/data.js (window.DATA) instead of data.json so fetch is not needed."""
    population = read_population()
    countries, continents, world_population = read_countries()
    data = {
        "population": population,
        "data": read_data(population),
        "countries": countries,
        "continents": continents,
        "world_population": world_population,
        "flaechennutzung": read_flaechennutzung(),
        "weitere_zahlen": read_weitere_zahlen(),
    }
    OUT.write_text(
        "window.DATA = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
