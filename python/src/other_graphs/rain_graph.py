import pandas as pd
import datetime
from ..Utils import GetMinMax
from bokeh.plotting import figure
from bokeh.models import Range1d, PrintfTickFormatter,HoverTool, TabPanel
from bokeh.layouts import column, row

def CreateRainHoverTool():
    return HoverTool(tooltips=[('Day', '@x'), ('Rainfall', '@rain{%smm}'),('Sunshine', '@sun{%s hours}'), ('Evaporation', '@evap{%smm}')], formatters={
        '@y' : 'printf',
        '@evap' : 'printf',
        '@sun' : 'printf',
    })