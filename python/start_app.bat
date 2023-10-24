@echo off
py -m pip install -r ./python/requirements.txt
python -m bokeh serve ./python/prog.py