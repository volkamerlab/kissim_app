r"""
This script takes all notebooks and renders the first markdown cell
of the notebook to the corresponding README.md in the containing folder.
Usage
-----
.. code-block::
    % python devtools/regenerate_readmes.py --output README.md \
        notebooks/comparison/
"""


def first_markdown_cell(path):
    import nbformat

    nb = nbformat.read(path, nbformat.NO_CONVERT)
    cell = nb.cells[0]
    if cell["cell_type"] == "markdown":
        yield cell["source"]


def parse_cli():
    from argparse import ArgumentParser

    p = ArgumentParser()
    p.add_argument("notebook_folder", type=str)
    p.add_argument("--output", type=str, default=None)
    return p.parse_args()


def main():
    from pathlib import Path

    args = parse_cli()

    notebook_folder = Path(args.notebook_folder)

    # Collect notebook names and notebook's first cell contents for all notebooks in folder
    nbcontents = []
    for notebook_file in notebook_folder.glob("*.ipynb"):
        nbcontent = "\n\n\n".join(list(first_markdown_cell(notebook_file)))
        if not nbcontent.strip():  # empty results
            nbcontent = "> This talktorial is still under development"
        nbcontents.append(f"## `{notebook_file.name}`\n\n##{nbcontent}")
    nbcontents = "\n\n\n".join(nbcontents)

    if args.output:
        with open(notebook_folder / args.output, "w") as f:
            f.write(nbcontents + "\n")
    else:
        print(nbcontents)


if __name__ == "__main__":
    main()
