# ruff: noqa: D100 D103 INP001 PLR2004
import csv
from pathlib import Path


def test_data_columns() -> None:
    with Path("data/data.tsv").open(mode="r", encoding="utf-8") as fh:
        csv_reader = csv.DictReader(fh, delimiter="\t")
        for row in csv_reader:
            assert len(row) == 7, len(row)


def test_data_no_whitespaces() -> None:
    with Path("data/data.tsv").open(mode="r", encoding="utf-8") as fh:
        csv_reader = csv.DictReader(fh, delimiter="\t")
        for row in csv_reader:
            for col in row:
                assert row[col] == row[col].strip(), f"'{row[col]}'"


def test_data_percent_or_pop() -> None:
    """Ensure that either Personen or Prozent are entered."""
    with Path("data/data.tsv").open(mode="r", encoding="utf-8") as fh:
        csv_reader = csv.DictReader(fh, delimiter="\t")
        for row in csv_reader:
            if row["Personen"] != "":
                assert row["Prozent"] == "", row["Prozent"]
                assert int(row["Personen"]) > 0, row["Personen"]
                assert int(row["Personen"]) < 100_000_000, row["Personen"]
            if row["Prozent"] != "":
                assert row["Personen"] == "", row["Personen"]
                assert float(row["Prozent"]) > 0, row["Prozent"]


def test_pop_no_whitespaces() -> None:
    with Path("data/population.tsv").open(mode="r", encoding="utf-8") as fh:
        csv_reader = csv.DictReader(fh, delimiter="\t")
        for row in csv_reader:
            for col in row:
                assert row[col] == row[col].strip(), f"'{row[col]}'"
                assert int(row[col]) > 0, row[col]


def test_pop_data_for_all_years() -> None:
    with Path("data/population.tsv").open(mode="r", encoding="utf-8") as fh:
        csv_reader = csv.DictReader(fh, delimiter="\t")
        d = {}
        for row in csv_reader:
            d[int(row["Jahr"])] = int(row["Einwohner"])

    with Path("data/data.tsv").open(mode="r", encoding="utf-8") as fh:
        csv_reader = csv.DictReader(fh, delimiter="\t")
        for row in csv_reader:
            assert int(row["Jahr"]) in d, row["Jahr"]
