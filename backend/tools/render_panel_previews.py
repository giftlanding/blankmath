from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pdf_generator"))

from reportlab.lib.styles import getSampleStyleSheet

from blankmath.panels.preview import render_panel_png
from blankmath.panels.problem import problem_panel


SAMPLES = [
    ("vertical-23x25.png", 1, "23 x 25 = ?", "vertical"),
    ("vertical-120-div-12.png", 2, "120 / 12 = ?", "vertical"),
]


def main() -> None:
    output_dir = Path("/tmp/blankmath-panel-previews")
    output_dir.mkdir(parents=True, exist_ok=True)
    style = getSampleStyleSheet()["Normal"]

    for filename, problem_number, prompt, layout in SAMPLES:
        panel = problem_panel(problem_number, prompt, style, layout)
        output_path = output_dir / filename
        render_panel_png(panel, output_path)
        print(output_path)


if __name__ == "__main__":
    main()
