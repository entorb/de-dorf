"""Use Streamlit AppTest."""
# ruff: noqa: D103, INP001

import sys
import warnings
from pathlib import Path

from streamlit.testing.v1 import AppTest

warnings.filterwarnings("ignore", message=".*streamlit.runtime.scriptrunner_utils.*")

sys.path.insert(0, (Path(__file__).parent.parent / "src").as_posix())


def run_and_assert_no_problems(at: AppTest) -> None:
    at.run(timeout=60)
    assert not at.exception
    assert not at.error
    assert not at.warning


def test_app() -> None:
    p = Path("src/app.py")
    at = AppTest.from_file(p)
    run_and_assert_no_problems(at)

    at.session_state["sel_compact"] = True
    run_and_assert_no_problems(at)
