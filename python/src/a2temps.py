#Imports
import pandas as pd
import numpy as np

from python.src.Utils import *
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, Div, Slider, Range1d, PrintfTickFormatter, CustomJSTickFormatter, CustomJS, InlineStyleSheet, Button, CustomJS, SetValue, TabPanel, Tabs, DatetimeTickFormatter, Legend, LegendItem, Whisker
from bokeh.layouts import column, row


# Dataframe
df = pd.read_csv("./python/all_cities.csv")
cities = ['adelaide', 'brisbane', 'darwin', 'hobart', 'melbourne', 'perth', 'sydney']
df['date'] = pd.to_datetime(df['date'])

# Init Bokeh
#output_notebook()

# Single scatterplot for Perth 2012-2022
def Perth9amTempatures():
    # Get the 9am temperatures for Perth
    perth_temps = df[df['city'] == 'perth'][['date', '9amTemp']].reset_index(drop=True)

    perth9amScatterData = ColumnDataSource(data=dict(
        x=perth_temps.date,
        y=perth_temps['9amTemp'],
    ))

    # Plot the scatter plot for Perth
    plot = figure(height=600, width=800, x_axis_label='Date', y_axis_label='Temperature (°C)',
                  title='Perth 9am Temperatures')

    xmin, xmax = GetMinMax(perth_temps['date'])
    ymin, ymax = GetMinMax(perth_temps['9amTemp'])

    plot.circle(source=perth9amScatterData, size=8, color='blue', legend_label='Perth 9am Temperature')
    plot.x_range.start = xmin
    plot.x_range.end = xmax
    plot.y_range.start = ymin
    plot.y_range.end = ymax

    plot.xaxis.major_label_orientation = 'horizontal'
    # plot.xaxis.ticker.desired_num_ticks = 15
    plot.xaxis.formatter = DatetimeTickFormatter(days='%d', months="%m", years='%Y')
    # Show the plot
    return row(plot)


# Scatter plots for each state from 2012-2022
# Takes a long time to load
def Selectable9amTempScatterPlot(city: str):
    # Get the 9am temperatures
    cityTemps = df[df['city'] == city][['date', '9amTemp']]
    cityTempsData = ColumnDataSource(data={
        'date': cityTemps.date,
        '9amTemp': cityTemps['9amTemp']
    })

    xmin, xmax = GetMinMax(cityTemps['date'])
    ymin, ymax = GetMinMax(cityTemps['9amTemp'])

    # Plot the scatter plot
    plot = figure(height=600, width=800, x_axis_label='Date', y_axis_label='Temperature (°C)',
                  title=f'{city.capitalize()} 9am Temperatures')
    plot.circle(x='date', y='9amTemp', source=cityTempsData, size=8, color='blue', legend_label=f'{city.capitalize()} 9am Temperature')

    plot.x_range.start = xmin
    plot.x_range.end = xmax
    plot.y_range.start = ymin
    plot.y_range.end = ymax

    plot.xaxis.major_label_orientation = 'horizontal'
    plot.xaxis.formatter = DatetimeTickFormatter(days='%d', months="%m", years='%Y')
    return row(plot)


# Perth boxplot 2008-2023
def Perth9amTempsBoxPlot():
    # Get all 9am temperatures from PerthDF
    perth_temperatures = df[df['city'] == 'perth'][['date', '9amTemp']].reset_index(drop=True)

    qmin, q1, q2, q3, qmax = perth_temperatures['9amTemp'].quantile([0, 0.25, 0.5, 0.75, 1])

    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr
    mean = perth_temperatures['9amTemp'].mean()

    out = perth_temperatures[(perth_temperatures['9amTemp'] > upper) | (perth_temperatures['9amTemp'] < lower)]

    outlier = []
    if not out.empty:
        outlier = list(out.values)

    upper = min(qmax, upper)
    lower = max(qmin, lower)

    hbar_height = (qmax - qmin) / 500

    # Create a box plot
    plot = figure(height=600, width=800, title='Perth Temperature at 9am (°C) from 2008 to 2023',
                  background_fill_color="#eaefef", y_axis_label='Temperature (°C)', x_range=['Temperature (°C)'])

    plot.segment(['Temperature (°C)'], upper, ['Temperature (°C)'], q3, line_color='black')
    plot.segment(['Temperature (°C)'], lower, ['Temperature (°C)'], q1, line_color='black')

    plot.vbar(['Temperature (°C)'], 0.7, q2, q3, line_color='black')
    plot.vbar(['Temperature (°C)'], 0.7, q1, q2, line_color='black')

    plot.rect(['Temperature (°C)'], lower, 0.2, hbar_height, line_color='black')
    plot.rect(['Temperature (°C)'], upper, 0.2, hbar_height, line_color='black')

    if not out.empty:
        plot.circle(['Temperature (°C)'] * len(outlier), outlier, size=6, fill_alpha=0.6)

    plot.y_range.start = lower - 5
    plot.y_range.end = upper + 5

    return row(plot)


def Selectable9amTempsBoxPlot(city: str):
    # Get all 9am temperatures from PerthDF
    cityTemps = df[df['city'] == city][['date', '9amTemp']].reset_index(drop=True)

    #data = pd.DataFrame(columnData.data)

    qmin, q1, q2, q3, qmax = cityTemps['9amTemp'].quantile([0, 0.25, 0.5, 0.75, 1])

    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr
    mean = cityTemps['9amTemp'].mean()

    out = cityTemps[(cityTemps['9amTemp'] > upper) | (cityTemps['9amTemp'] < lower)]

    outlier = []
    if not out.empty:
        outlier = list(out.values)

    upper = min(qmax, upper)
    lower = max(qmin, lower)

    hbar_height = (qmax - qmin) / 500

    # Create a box plot
    plot = figure(height=600, width=800, title=f'{city.capitalize()} Temperature at 9am (°C) from 2008 to 2023',
                  background_fill_color="#eaefef", y_axis_label='Temperature (°C)', x_range=['Temperature (°C)'])

    plot.segment(['Temperature (°C)'], upper, ['Temperature (°C)'], q3, line_color='black')
    plot.segment(['Temperature (°C)'], lower, ['Temperature (°C)'], q1, line_color='black')

    plot.vbar(['Temperature (°C)'], 0.7, q2, q3, line_color='black')
    plot.vbar(['Temperature (°C)'], 0.7, q1, q2, line_color='black')

    plot.rect(['Temperature (°C)'], lower, 0.2, hbar_height, line_color='black')
    plot.rect(['Temperature (°C)'], upper, 0.2, hbar_height, line_color='black')

    if not out.empty:
        plot.circle(['Temperature (°C)'] * len(outlier), outlier, size=6, fill_alpha=0.6)

    plot.y_range.start = lower - 5
    plot.y_range.end = upper + 5

    return row(plot)


# Box plot for 2012 perth and 2022 perth

def Perth9amTempBoxPlot2Years():
    # Get all 9am temperatures from PerthDF
    perth2012temperatures = df[(df['city'] == 'perth') & (df['year'] == 2012)][['date', '9amTemp']].reset_index(
        drop=True)
    perth2022temperatures = df[(df['city'] == 'perth') & (df['year'] == 2022)][['date', '9amTemp']].reset_index(
        drop=True)

    qminY1, q1Y1, q2Y1, q3Y1, qmaxY1 = perth2012temperatures['9amTemp'].quantile([0, 0.25, 0.5, 0.75, 1])
    iqrY1 = q3Y1 - q1Y1
    upperY1 = q3Y1 + 1.5 * iqrY1
    lowerY1 = q1Y1 - 1.5 * iqrY1
    outY1 = perth2012temperatures[
        (perth2012temperatures['9amTemp'] > upperY1) | (perth2012temperatures['9amTemp'] < lowerY1)]
    outlierY1 = []
    if not outY1.empty:
        outlierY1 = list(outY1.values)
    upperY1 = min(qmaxY1, upperY1)
    lowerY1 = max(qminY1, lowerY1)
    hbar_heightY1 = (qmaxY1 - qminY1) / 500

    qminY2, q1Y2, q2Y2, q3Y2, qmaxY2 = perth2022temperatures['9amTemp'].quantile([0, 0.25, 0.5, 0.75, 1])
    iqrY2 = q3Y2 - q1Y2
    upperY2 = q3Y2 + 1.5 * iqrY2
    lowerY2 = q1Y2 - 1.5 * iqrY2
    outY2 = perth2022temperatures[
        (perth2022temperatures['9amTemp'] > upperY2) | (perth2022temperatures['9amTemp'] < lowerY2)]
    outlierY2 = []
    if not outY2.empty:
        outlierY2 = list(outY2.values)
    upperY2 = min(qmaxY2, upperY2)
    lowerY2 = max(qminY2, lowerY2)
    hbar_heightY2 = (qmaxY2 - qminY2) / 500

    xAxisNameY1 = 'Temperature (°C) 2012'
    xAxisNameY2 = 'Temperature (°C) 2022'

    # Create a box plot
    # Year 1
    plot = figure(height=600, width=800, title='Perth Temperature at 9am (°C) in 2012 and 2022',
                  background_fill_color="#eaefef", y_axis_label='Temperature (°C)', x_range=[xAxisNameY1, xAxisNameY2])
    plot.segment([xAxisNameY1], upperY1, [xAxisNameY1], q3Y1, line_color='black')
    plot.segment([xAxisNameY1], lowerY1, [xAxisNameY1], q1Y1, line_color='black')

    plot.vbar([xAxisNameY1], 0.7, q2Y1, q3Y1, color='blue', line_color='black')
    plot.vbar([xAxisNameY1], 0.7, q1Y1, q2Y1, color='blue', line_color='black')

    plot.rect([xAxisNameY1], lowerY1, 0.2, hbar_heightY1, color='blue', line_color='black')
    plot.rect([xAxisNameY1], upperY1, 0.2, hbar_heightY1, color='blue', line_color='black')

    if not outY1.empty:
        plot.circle([xAxisNameY1] * len(outlierY1), outlierY1, size=6, fill_alpha=0.6)

    # Year 2
    plot.segment([xAxisNameY2], upperY2, [xAxisNameY2], q3Y2, line_color='black')
    plot.segment([xAxisNameY2], lowerY2, [xAxisNameY2], q1Y2, line_color='black')

    plot.vbar([xAxisNameY2], 0.7, q2Y2, q3Y2, color='red', line_color='black')
    plot.vbar([xAxisNameY2], 0.7, q1Y2, q2Y2, color='red', line_color='black')

    plot.rect([xAxisNameY2], lowerY2, 0.2, hbar_heightY2, color='red', line_color='black')
    plot.rect([xAxisNameY2], upperY2, 0.2, hbar_heightY2, color='red', line_color='black')

    if not outY2.empty:
        plot.circle([xAxisNameY2] * len(outlierY2), outlierY2, size=6, fill_alpha=0.6)

    plot.y_range.start = min(lowerY1 - 5, lowerY2 - 5)
    plot.y_range.end = max(upperY1 + 5, upperY2 + 5)

    return row(plot)


def Selectable9amTempBoxPlot2Years(city: str):
    # Get all 9am temperatures from PerthDF
    y1 = min(df[(df['city'] == city)]['year'])
    # y1 = min(columnData.data['year'])
    y2 = max(df[(df['city'] == city)]['year'])
    #y2 = max(columnData.data['year'])

    #data = pd.DataFrame(columnData.data)

    #temperaturesY1 = data[(data['year'] == y1)][['date', '9amTemp']].reset_index(drop=True)
    temperaturesY1 = df[(df['year'] == y1)][['date', '9amTemp']].reset_index(drop=True)
    #temperaturesY2 = data[(data['year'] == y2)][['date', '9amTemp']].reset_index(drop=True)
    temperaturesY2 = df[(df['year'] == y2)][['date', '9amTemp']].reset_index(drop=True)

    qminY1, q1Y1, q2Y1, q3Y1, qmaxY1 = temperaturesY1['9amTemp'].quantile([0, 0.25, 0.5, 0.75, 1])
    iqrY1 = q3Y1 - q1Y1
    upperY1 = q3Y1 + 1.5 * iqrY1
    lowerY1 = q1Y1 - 1.5 * iqrY1
    outY1 = temperaturesY1[(temperaturesY1['9amTemp'] > upperY1) | (temperaturesY1['9amTemp'] < lowerY1)]
    outlierY1 = []
    if not outY1.empty:
        outlierY1 = list(outY1.values)
    upperY1 = min(qmaxY1, upperY1)
    lowerY1 = max(qminY1, lowerY1)
    hbar_heightY1 = (qmaxY1 - qminY1) / 500

    qminY2, q1Y2, q2Y2, q3Y2, qmaxY2 = temperaturesY2['9amTemp'].quantile([0, 0.25, 0.5, 0.75, 1])
    iqrY2 = q3Y2 - q1Y2
    upperY2 = q3Y2 + 1.5 * iqrY2
    lowerY2 = q1Y2 - 1.5 * iqrY2
    outY2 = temperaturesY2[(temperaturesY2['9amTemp'] > upperY2) | (temperaturesY2['9amTemp'] < lowerY2)]
    outlierY2 = []
    if not outY2.empty:
        outlierY2 = list(outY2.values)
    upperY2 = min(qmaxY2, upperY2)
    lowerY2 = max(qminY2, lowerY2)
    hbar_heightY2 = (qmaxY2 - qminY2) / 500

    xAxisNameY1 = 'Temperature (°C) 2012'
    xAxisNameY2 = 'Temperature (°C) 2022'

    # Create a box plot
    # Year 1
    plot = figure(height=600, width=800, title=f'{city.capitalize()} Temperature at 9am (°C) in {y1} and {y2}',
                  background_fill_color="#eaefef", y_axis_label='Temperature (°C)', x_range=[xAxisNameY1, xAxisNameY2])
    plot.segment([xAxisNameY1], upperY1, [xAxisNameY1], q3Y1, line_color='black')
    plot.segment([xAxisNameY1], lowerY1, [xAxisNameY1], q1Y1, line_color='black')

    plot.vbar([xAxisNameY1], 0.7, q2Y1, q3Y1, color='blue', line_color='black')
    plot.vbar([xAxisNameY1], 0.7, q1Y1, q2Y1, color='blue', line_color='black')

    plot.rect([xAxisNameY1], lowerY1, 0.2, hbar_heightY1, color='blue', line_color='black')
    plot.rect([xAxisNameY1], upperY1, 0.2, hbar_heightY1, color='blue', line_color='black')

    if not outY1.empty:
        plot.circle([xAxisNameY1] * len(outlierY1), outlierY1, size=6, fill_alpha=0.6)

    # Year 2
    plot.segment([xAxisNameY2], upperY2, [xAxisNameY2], q3Y2, line_color='black')
    plot.segment([xAxisNameY2], lowerY2, [xAxisNameY2], q1Y2, line_color='black')

    plot.vbar([xAxisNameY2], 0.7, q2Y2, q3Y2, color='red', line_color='black')
    plot.vbar([xAxisNameY2], 0.7, q1Y2, q2Y2, color='red', line_color='black')

    plot.rect([xAxisNameY2], lowerY2, 0.2, hbar_heightY2, color='red', line_color='black')
    plot.rect([xAxisNameY2], upperY2, 0.2, hbar_heightY2, color='red', line_color='black')

    if not outY2.empty:
        plot.circle([xAxisNameY2] * len(outlierY2), outlierY2, size=6, fill_alpha=0.6)

    plot.y_range.start = min(lowerY1 - 5, lowerY2 - 5)
    plot.y_range.end = max(upperY1 + 5, upperY2 + 5)

    return row(plot)