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
pagination. A vertical arithmetic panel can be rendered by itself for inspection
before it is placed into the worksheet grid.

Current panels:

- `VerticalArithmeticPanel`: right-aligns operands, places the operator beside
  the second operand, and draws a horizontal answer line.
- fallback paragraph panel: used for horizontal problems and unsupported vertical
  prompt shapes.

The next panel types should be added as separate modules in this package, such
as `horizontal_arithmetic.py` or `comparison.py`, rather than adding drawing
logic back into `renderer.py`.
