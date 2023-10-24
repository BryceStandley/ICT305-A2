from bokeh.models import Range1d, PrintfTickFormatter, HoverTool, TabPanel, Slider, UIElement, Div, Tabs, Dropdown, ColumnDataSource
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.palettes import inferno
import datetime
import itertools

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def GetMinMax(dataFrameColumn):
    return min(dataFrameColumn), max(dataFrameColumn)

def CreateGraphTabPanel(capitalMainDropdown: Dropdown, capitalSubDropdown: Dropdown, yearSlider: Slider, monthSlider: Slider, plot: figure, plotTitle: str) -> TabPanel:
    return TabPanel(child=column(capitalMainDropdown, capitalSubDropdown, row(yearSlider, monthSlider), column(plot)), title=plotTitle)

def CreatePageLayout(titleItem: Div, pageTabItems : list[UIElement], align: str, margin: any) -> row:
    return row(column(titleItem, Tabs(tabs=pageTabItems), align=align, margin=margin))

def CreateLinePlotHoverTool(yaxis: tuple, additionalHoverInfo: list[tuple: str]):
    return HoverTool(tooltips=[('Day', '@x'), yaxis, *additionalHoverInfo], formatters={
        yaxis[1].split('{')[0] : 'printf',
        additionalHoverInfo[0][1].split('{')[0] : 'printf',
        additionalHoverInfo[1][1].split('{')[0] : 'printf',
        additionalHoverInfo[2][1].split('{')[0] : 'printf',
    })

def CreateLinePlot(plotTitle: str, dataframe, trimmedMainSourceData, trimmedSubSourceData, month, year, xAxisKey: str, yAxisKey: str, xAxisLabel: str, yAxisLabel: str):
    plot = figure(height=600, width=1000)
    plot.title = plotTitle.format(
        month=datetime.datetime.strptime(str(month), '%m').strftime('%B'), year=year)
    plot.title_location = 'above'
    #plot.line(x=trimmeddataSource.data[xAxisKey], y=trimmeddataSource.data[yAxisKey])
    plot.line(x=xAxisKey, y=yAxisKey, source=trimmedMainSourceData, color="red")
    plot.line(x=xAxisKey, y=yAxisKey, source=trimmedSubSourceData, color="blue")
    #plot.circle(x=trimmeddataSource.data[xAxisKey], y=trimmeddataSource.data[yAxisKey], fill_color="white", size=6)
    plot.circle(x=xAxisKey, y=yAxisKey, source=trimmedMainSourceData, fill_color="red", size=6)
    plot.circle(x=xAxisKey, y=yAxisKey, source=trimmedSubSourceData, fill_color="blue", size=6)

    xmin, xmax = GetMinMax(dataframe['day'])
    ymin, ymax = GetMinMax(dataframe[yAxisKey])

    # Set range for X and Y and limit the plot to the min and max
    plot.x_range = Range1d(xmin, xmax, bounds=(xmin, xmax))
    plot.y_range = Range1d(ymin - 1, ymax + 1, bounds=(ymin - 1, ymax + 1))
    plot.yaxis[0].formatter = PrintfTickFormatter(format='%smm')
    plot.xaxis.axis_label = xAxisLabel
    plot.yaxis.axis_label = yAxisLabel
    plot.visible = True
    return plot
