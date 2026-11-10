"""Render the generated maps and chapters as a single PDF."""

from pathlib import Path
import re
from tempfile import NamedTemporaryFile
from textwrap import wrap

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
from matplotlib.image import imread


def write_front_matter(pdf):
    frame = Path(__file__).with_name("frame.tex").read_text(encoding="utf-8")
    title = re.search(r"^\\title\{([^}]*)\}", frame, re.MULTILINE)[1]
    author = re.search(r"^\\author\{([^}]*)\}", frame, re.MULTILINE)[1]
    date = re.search(r"^\\date\{([^}]*)\}", frame, re.MULTILINE)[1]
    opening = frame.split(r"\end{titlingpage}", 1)[1].split(r"\mainmatter", 1)[0]
    quote, attribution = opening.split(r"\begin{flushright}", 1)
    quote = re.sub(r"\\(?:clearpage|vspace\{[^}]*\})", "", quote)
    attribution = attribution.split(r"\end{flushright}", 1)[0]
    attribution = re.sub(r"\\textit\{([^}]*)\}", r"\1", attribution).strip()

    figure = Figure(figsize=(6, 9))
    for y, text, size in ((0.66, title, 22), (0.58, author, 14), (0.51, date, 11)):
        figure.text(0.5, y, text, ha="center", fontsize=size, parse_math=False)
    pdf.savefig(figure)

    figure = Figure(figsize=(6, 9))
    for row, line in enumerate(wrap(" ".join(quote.split()), 58)):
        figure.text(0.08, 0.78 - row * 0.021, line, fontsize=10,
                    fontfamily="DejaVu Sans Mono", parse_math=False)
    figure.text(0.92, 0.40, attribution, ha="right", fontsize=10, parse_math=False)
    pdf.savefig(figure)


def write_book(directory, count):
    directory = Path(directory)
    destination = directory / "novel.pdf"
    with NamedTemporaryFile(dir=directory, suffix=".pdf", delete=False) as stream:
        temporary = Path(stream.name)
    try:
        with PdfPages(temporary, metadata={"Title": "RandomTravelogue"}) as pdf:
            write_front_matter(pdf)
            for index in range(count):
                chapter = directory / f"{index:02d}"
                title, _, body = (chapter / "map.md").read_text(
                    encoding="utf-8"
                ).partition("\n")
                figure = Figure(figsize=(6, 9))
                figure.text(0.5, 0.9, title.removeprefix("# "), ha="center",
                            fontsize=16, parse_math=False)
                axes = figure.add_axes([0.08, 0.18, 0.84, 0.65])
                axes.imshow(imread(chapter / "map.png"))
                axes.set_axis_off()
                pdf.savefig(figure)

                lines = []
                for paragraph in body.strip().split("\n\n"):
                    for line in paragraph.splitlines():
                        heading = line.startswith("## ")
                        content = line.removeprefix("## ").replace("*", "")
                        lines.extend((text, heading) for text in wrap(content, 58))
                    lines.append(("", False))

                for start in range(0, len(lines), 40):
                    figure = Figure(figsize=(6, 9))
                    for row, (line, heading) in enumerate(lines[start:start + 40]):
                        figure.text(0.08, 0.92 - row * 0.021, line,
                                    fontsize=10, fontfamily="DejaVu Sans Mono",
                                    fontweight="bold" if heading else "normal",
                                    parse_math=False)
                    pdf.savefig(figure)
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination
