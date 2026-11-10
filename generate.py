import click
import describe
from book_pdf import write_book

template = r"""
\begin{figure}[t]
\includegraphics[width=0.9\textwidth]{%02d/map.png}
\end{figure}
\input{%02d/map}
"""

@click.command()
@click.argument("directory")
@click.option("-n", default=100, type=click.IntRange(min=1))
def main(directory, n):
    describe.do_novel(directory, n)
    with open(directory + "/contents.tex", "w") as f:
        for i in range(n):
            f.write(template % (i,i))
    click.echo(f"Created {write_book(directory, n)}")

if __name__ == '__main__':
    main()
