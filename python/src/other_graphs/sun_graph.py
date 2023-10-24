import pandas as pd
import datetime
from ..Utils import GetMinMax
from bokeh.plotting import figure
from bokeh.models import Range1d, PrintfTickFormatter, HoverTool, TabPanel
from bokeh.layouts import column, row

def CreateSunHoverTool():
    return HoverTool(tooltips=[('Day', '@x'), ('Sunshine', '@sun{%s hours}'), ('Evaporation', '@evap{%smm}'), ('Rainfall', '@rain{%smm}')], formatters={
        '@y' : 'printf',
        '@rain' : 'printf',
        '@evap' : 'printf',
    })