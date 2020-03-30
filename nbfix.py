#!/usr/bin/env python
# https://gist.github.com/fbattello/c617e4928c37f3f934d14b90f9cc22fb
# Fix IPython notebook files generated by vscode
# Failed validating 'additionalProperties' in markdown_cell : https://github.com/microsoft/vscode-python/issues/8772

"""
usage:

python nbfix.py index.ipynb
python nbfix.py "chapter*.ipynb"
python nbfix.py "intro*.ipynb" "chapter*.ipynb" "appendix*.ipynb"
"""

import io
import os
import sys

import nbformat
from pathlib import Path

def fix_notebooks(filenames):
    for fname in filenames:
        with io.open(fname, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
            nbformat.write(nb, fname+".bak") # comment this line for no backup
            [cell.pop(k, None) for k in ['outputs', 'execution_count'] for cell in nb.cells if cell['cell_type']=='markdown']
            nbformat.write(nb, fname) # override origin notebook

if __name__ == '__main__':
    notebooks_glob = sys.argv[1:] # notebook filenames with wildcards
    if not notebooks_glob:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
 
    notebooks = []
    for notebook_glob in notebooks_glob:
        _notebooks = [f.name for f in Path().glob(notebook_glob)]
        notebooks.extend(_notebooks)

    fix_notebooks(notebooks)