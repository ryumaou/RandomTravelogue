# RandomTravelogue

Generate island maps and accompanying travel descriptions with Python 3.

Install dependencies using the same Python interpreter you use to run the project:

```powershell
python -m pip install -r requirements.txt
python generate.py novel -n 1
```

Each run generates fresh island maps and descriptions. The numbered output
directories receive new `map.png`, `map.md`, and `map.pickle` files for the
requested chapters. Increase `-n` to generate more maps.

The command also writes `novel/novel.pdf`, starting with the title page and
epigraph from `frame.tex`, followed by the maps and travel descriptions.
PDF export uses Matplotlib and requires no additional packages. If you use Make,
`make novel COUNT=1` runs the same one-map example.

The optional interactive grammar tool (`python pretty.py test`) requires
`pyreadline3` on Windows. Terrain noise is implemented with NumPy and does not
require the `noise` package or C++ build tools.
