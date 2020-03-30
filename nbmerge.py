#!/usr/bin/env python
# https://gist.github.com/fbattello/5b5d26824ac443aae84f38a0ea818d80
# updated version of fperez version : https://gist.github.com/fperez/e2bbc0a208e82e450f69
# from an initial work from minrk : https://github.com/ipython/ipython-in-depth/blob/master/tools/nbmerge.py

"""
usage:

python nbmerge.py "chapter*.ipynb" > merged.ipynb
python nbmerge.py "intro*.ipynb" "chapter*.ipynb" "appendix*.ipynb" > merged.ipynb
"""

import io
import os
import sys

import nbformat
from pathlib import Path

BREAKINGPAGE = nbformat.v4.new_markdown_cell(r'<div style="page-break-after: always; visibility: hidden">\pagebreak</div>')

def merge_notebooks(filenames):
    merged = None
    for fname in filenames:
        with io.open(fname, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
            # vscode fix
            [cell.pop(k, None) for k in ['outputs', 'execution_count'] for cell in nb.cells if cell['cell_type']=='markdown']
        nb.cells.append(BREAKINGPAGE) # add page break after each chapter   
        if merged is None:
            merged = nb
        else:
            merged.cells.extend(nb.cells)
    if not hasattr(merged.metadata, 'name'):
        merged.metadata.name = ''
    merged.metadata.name += "_merged"
    print(nbformat.writes(merged))

if __name__ == '__main__':
    notebooks_glob = sys.argv[1:] # notebook filenames with wildcards
    if not notebooks_glob:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
 
    notebooks = []
    for notebook_glob in notebooks_glob:
        _notebooks = sorted([f.name for f in Path().glob(notebook_glob)])
        notebooks.extend(_notebooks)

    merge_notebooks(notebooks)