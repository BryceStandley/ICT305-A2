import pandas as pd
import datetime
from ..Utils import GetMinMax
from bokeh.plotting import figure
from bokeh.models import Range1d, PrintfTickFormatter, HoverTool, TabPanel
from bokeh.layouts import column, row

def CreateEvaporationHoverTool():
    return HoverTool(tooltips=[('Day', '@x'), ('Evaporation', '@evap{%smm}'), ('Rainfall', '@rain{%smm}'), ('Sunshine', '@sun{%s hours}')], formatters={
        '@y' : 'printf',
        '@rain' : 'printf',
        '@sun' : 'printf',
    })