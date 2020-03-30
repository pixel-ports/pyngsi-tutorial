#!/bin/bash
python nbmerge.py "chapter*.ipynb" > pyngsi-tutorial.ipynb
jupyter nbconvert --to html_toc pyngsi-tutorial.ipynb
rm -f pyngsi-tutorial.ipynb