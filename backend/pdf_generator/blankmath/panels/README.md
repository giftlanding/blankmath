# Problem Panels

Panels are fixed-size render targets for worksheet problems.

The PDF page renderer owns the page-level structure:

- header image
- body grid
- pagination
- answer key page

The panel package owns problem-level rendering:

- panel dimensions and padding
- choosing the panel renderer for a generated problem
- drawing problem numbers, operands, operators, blanks, and answer lines
- standalone panel preview rendering

This keeps visual problem design separate from worksheet generation and page
pagination. A panel can be rendered by itself for inspection before it is
placed into the worksheet grid.

Current panels:

- `VerticalArithmeticPanel`: right-aligns operands, places the operator beside
  the second operand, and draws a horizontal answer line.
- `LongDivisionPanel`: lays out the divisor, dividend, quotient line, and
  handwriting-sized work rows for standard division problems.
- `DistributivePropertyPanel`: lays out a rewritten multiplication expression
  plus guided partial-product and final-combination blanks.
- fallback paragraph panel: used for horizontal problems and unsupported vertical
  prompt shapes.

The next panel types should be added as separate modules in this package, such
as `horizontal_arithmetic.py` or `comparison.py`, rather than adding drawing
logic back into `renderer.py`.

## AI Visual Checks

Panel layout changes should be checked visually before they are committed. The
goal is to inspect the fixed-size panel itself, not only the full worksheet page.

Generate preview images:

```sh
PYTHONPATH=/tmp/blankmath-backend-deps python3 backend/tools/render_panel_previews.py
```

The script writes PNG files to:

```text
/tmp/blankmath-panel-previews/
```

Current preview samples:

- `vertical-23x25.png`
- `long-division-120-div-12.png`
- `distributive-property-600x99.png`

After generating previews, use the AI image-reading tool to open each PNG and
check:

- the problem number is visually separate from the math problem;
- operands are aligned by place value;
- the operator is clearly separated from the operands;
- the main answer line is easy to see;
- there is enough blank vertical space for a child to work;
- multi-step problems such as `23 x 25` have at least three handwriting-sized
  work rows below the main answer line;
- no text, operator, or line overlaps;
- the panel still looks balanced inside its fixed-size box.

If a preview fails visual inspection, adjust the panel renderer or dimensions,
regenerate the PNGs, and inspect again before committing.

Also run the backend tests and a PDF smoke render:

```sh
python3 -m unittest discover -s backend/tests
PYTHONPATH=/tmp/blankmath-backend-deps:backend/pdf_generator python3 -c 'from blankmath.generators import Problem; from blankmath.renderer import render_pdf; problems=[Problem("23 x 25 = ?", "575") for _ in range(16)]; pdf=render_pdf("Multiplication", problems, 20, False, "vertical"); print(pdf[:5], len(pdf))'
```
