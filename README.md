# The Archipelago of the East

A procedural travelogue by **J K Hoffman**, inspired by *The Deserts of the West*
by **Martin O'Leary**. The repository is named **RandomTravelogue**.

Generate fictional island maps, names, travel descriptions, and a complete PDF
with Python 3.9 or newer.

## Install and run

Install dependencies using the same Python interpreter you use to run the project:

```powershell
python -m pip install -r requirements.txt
python generate.py novel -n 1
```

Open **`novel/novel.pdf`** after the completion message. The directory argument
selects the output folder. The `-n` option selects the number of maps and
accompanying chapters, with a minimum of 1 and a default of 100.

```powershell
python generate.py novel -n 10
python generate.py my-travelogue -n 3
```

The second example creates `my-travelogue/novel.pdf`. The PDF filename remains
`novel.pdf` regardless of the output folder or the title in `frame.tex`.

## Islands and fresh generation

- Each map starts with one to five island footprints, allowing a single large
  island or several smaller islands.
- Island sizes, orientations, elongation, and coastline shapes vary.
  Placement reserves water between footprints and fits their coastlines
  within a 10% margin around the map.
- Erosion shapes the interiors while preserving the island footprints.
- Each connected landmass receives at least one named city that becomes a
  regional capital and a stop on the narrated route.
- Travel descriptions use the generated places and journey between stops.
  Names and vocabulary come from a generated fictional language.
- Every run creates fresh maps, names, and descriptions and rebuilds the PDF.
  Saved map data is overwritten for the requested chapters.

If you rerun with fewer maps, older numbered directories can remain in the output
folder. The new PDF includes only the chapters requested for that run.

## Output files

Each numbered chapter directory, starting with `00`, contains these files.

| File | Contents |
| --- | --- |
| `map.png` | Labeled map with cities, regions, terrain, and travel route |
| `map.md` | Chapter heading and city descriptions |
| `map.pickle` | Compressed snapshot of the generated map object |

The output folder also contains `novel.pdf` and `contents.tex`. The latter is
a legacy LaTeX index. Automatic PDF export reads the PNG and Markdown files
directly. Saved map snapshots are not reused during the next run.

## PDF and opening pages

The command also writes `novel/novel.pdf`, starting with the title page and
epigraph from `frame.tex`, followed by the maps and travel descriptions.
PDF export uses Matplotlib and requires no additional packages. If you use Make,
`make novel COUNT=1` runs the same one-map example.

Set `NOVEL=my-travelogue` in the Make command to change its output folder.

Edit the title, author, and date fields in `frame.tex` to customize the opening
page. The current values are shown below.

```tex
\title{The Archipelago of the East}
\author{J K Hoffman}
\date{Inspired by The Deserts of the West by Martin O'Leary}
```

The exporter reads the epigraph between the title page and `\mainmatter`,
including the attribution inside `flushright`. Preserve this structure when
editing the file.

The PDF uses 6-by-9-inch pages. Its title page and epigraph precede each map and
its paginated travel text. The exporter interprets the current `frame.tex`
structure with Matplotlib. LaTeX fonts, spacing, and arbitrary commands are not
applied. Markdown city headings become bold text, and inline emphasis markers
are removed.

The PDF metadata title currently remains `RandomTravelogue`, even when the
visible title page uses the book title from `frame.tex`.

## Dependencies and development

The required packages are Click, NumPy, SciPy, and Matplotlib. Automatic PDF
generation requires neither Pandoc nor a LaTeX installation.

The optional interactive grammar tool (`python pretty.py test`) requires
`pyreadline3` on Windows. Terrain noise is implemented with NumPy and does not
require the `noise` package or C++ build tools.

The optional placeholder grammar text is also built in, so `loremipsum` is
no longer required.

| File | Role |
| --- | --- |
| `generate.py` | Command-line entry point and automatic PDF export |
| `terrain.py` | Terrain, erosion, cities, territories, routing, and map drawing |
| `coherent_noise.py` | Seeded gradient noise implemented with NumPy |
| `describe.py` | Fresh map generation and travel chapter writing |
| `language.py` | Fictional language, vocabulary, and place names |
| `description.grammar` | Travel description templates |
| `grammar.py` and `parsecom.py` | Template engine and parser |
| `book_pdf.py` | Opening pages, map pages, and paginated travel text |
| `frame.tex` | Book title, author, inspiration credit, and epigraph |
| `pretty.py` | Grammar inspection and interactive development commands |

Run the existing noise tests with `python -m unittest test_coherent_noise`.
These check seed repeatability and continuity across lattice boundaries.
They do not validate full map generation or PDF layout.

Grammar inspection commands include `python pretty.py grammar`,
`python pretty.py orphans`, and `python pretty.py graph`.

Python execution and PDF rendering have not been verified in the editing
environment. The Python 3.14 installation reported during development is on
the user's machine.

## Credits and license

The original project and code are credited to Martin O'Leary. This adaptation
uses the title and author above and retains the Borges epigraph attributed to
*Del rigor en la ciencia*. The code is distributed under the MIT License in
[LICENSE.md](LICENSE.md).
