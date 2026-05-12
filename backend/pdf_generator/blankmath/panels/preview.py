from io import BytesIO

from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate


def render_panel_pdf(panel, width: float = 2 * inch, height: float = 1.5 * inch) -> bytes:
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=(width, height),
        rightMargin=0,
        leftMargin=0,
        topMargin=0,
        bottomMargin=0,
    )
    document.build([panel])
    return buffer.getvalue()
