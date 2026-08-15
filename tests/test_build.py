"""Tests for scripts/gen_data.py output."""

import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, (Path(__file__).parent.parent / "scripts").as_posix())

import gen_data


def test_md_to_html() -> None:
    src = "# Title\n\n### Demo\n\n* eins\n* zwei [Link](https://x.de)\n"
    out = gen_data.md_to_html(src.split("\n", 1)[1])
    assert "<h3>Demo</h3>" in out
    assert "<ul>" in out
    assert "<li>eins</li>" in out
    assert '<a href="https://x.de">Link</a>' in out


def test_read_data() -> None:
    pop = gen_data.read_population()
    data = gen_data.read_data(pop)
    for r in data:
        assert r["Personen"] > 0
        assert r["Prozent"] >= 0

    auslaender = next(r for r in data if r["Titel"] == "Ausländeranteil")
    assert auslaender["Personen"] == 12_324_195
    assert (
        abs(auslaender["Prozent"] - round(100 * auslaender["Personen"] / pop[2022], 1))
        < 0.001
    )

    miete = next(r for r in data if r["Titel"] == "Wohnen zur Miete")
    assert miete["Prozent"] == 52.4
    assert miete["Personen"] == 43_730_968


def test_read_countries() -> None:
    countries, continents, world = gen_data.read_countries()
    assert world == sum(c["Einwohner"] for c in countries)
    assert sum(c["Einwohner"] for c in continents) == world
    for a, b in itertools.pairwise(countries):
        assert a["Einwohner"] >= b["Einwohner"]


def test_read_flaechennutzung() -> None:
    out = gen_data.read_flaechennutzung()
    assert out
    assert 0 <= out[0]["Prozent"] <= 100
    assert abs(out[0]["Prozent"] - 33934.02 / 357682.93 * 100) < 0.01
    for r in out:
        assert "Kategorie1" in r
        assert "qkm" in r


def test_main_writes_json() -> None:
    out_path = gen_data.OUT
    backup = out_path.read_text(encoding="utf-8") if out_path.exists() else None
    try:
        gen_data.main()
        cont = out_path.read_text(encoding="utf-8")
        data = json.loads(cont.removeprefix("window.DATA = ").removesuffix(";\n"))
        assert data["data"]
        assert data["countries"]
        assert data["weitere_zahlen"].startswith("<")
    finally:
        if backup is None:
            out_path.unlink(missing_ok=True)
        else:
            out_path.write_text(backup, encoding="utf-8")
