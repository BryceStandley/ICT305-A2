# Imports
from temp_graphs_a1 import *
from a2temps import *
from bokeh.io import curdoc
from Utils import *
import os

main_dir = os.path.dirname(__file__)

titleDivFilePath = os.path.join(main_dir, 'res', 'titleDiv.html')

# Load title HTML file
with open(titleDivFilePath, 'r', encoding='utf-8') as f:
    titleDivContents = f.read()

dataset_file_path = os.path.join(main_dir, 'res', 'all_cities.csv')

df_trim = pd.read_csv(dataset_file_path)
df_trim['date'] = pd.to_datetime(df_trim['date'])

# Default values
default_capital = "perth"
default_sub_capital = 'sydney'
default_year = min(df_trim.year[df_trim.city == default_capital])
default_month = min(df_trim.month[df_trim.year == default_year])

default_temp_capital = 'perth'

# Default Data trimmed to default values
data = df_trim[
    (df_trim['year'] == default_year) & (df_trim['month'] == default_month) & (df_trim['city'] == default_capital)]
data2 = df_trim[
    (df_trim['year'] == default_year) & (df_trim['month'] == default_month) & (df_trim['city'] == default_sub_capital)]
data3 = df_trim[(df_trim['city'] == default_temp_capital)]

#Define Temp scatter and box plot functions



# Setup plot source data and build plots
trimmedMainSourceData = ColumnDataSource(data={
    'x': data.day,
    'evap': data.evap,
    'rain': data.rain,
    'sun': data.sun,
    'city': data.city
})

trimmedSubSourceData = ColumnDataSource(data={
    'x': data2.day,
    'evap': data2.evap,
    'rain': data2.rain,
    'sun': data2.sun,
    'city': data2.city
})

trimmedTempSourceData = ColumnDataSource(data={
    'date': data3.date,
    'year': data3.year,
    '9amTemp': data3['9amTemp']
})

# Default selected cities
currentlySelectedMainCapital = default_capital
currentlySelectedSubCapital = default_sub_capital
currentlySelectedTempCapital = default_temp_capital

# Default Evaporation, Rain and Sunshine plots
evapPlot = CreateLinePlot(
    currentlySelectedMainCapital.capitalize() + ' vs ' + currentlySelectedSubCapital.capitalize() + " Evaporation in {month} {year}",
    df_trim, trimmedMainSourceData, trimmedSubSourceData, default_month,
    default_year, "x", "evap", "Day of the Month", "Evaporation", '%smm')
rainPlot = CreateLinePlot(
    currentlySelectedMainCapital.capitalize() + ' vs ' + currentlySelectedSubCapital.capitalize() + " Rainfall in {month} {year}",
    df_trim, trimmedMainSourceData, trimmedSubSourceData, default_month, default_year,
    "x", "rain", "Day of the Month", "Rainfall", '%smm')
sunPlot = CreateLinePlot(
    currentlySelectedMainCapital.capitalize() + ' vs ' + currentlySelectedSubCapital.capitalize() + " Sunshine in {month} {year}",
    df_trim, trimmedMainSourceData, trimmedSubSourceData, default_month, default_year,
    "x", "sun", "Day of the Month", "Sunshine", '%s hours')




# Plot Layouts
year_slider = Slider(start=min(df_trim.year), end=max(df_trim.year), step=1, value=default_year, title='Year')
month_slider = Slider(start=min(df_trim.month[(df_trim.year == year_slider.value) & (df_trim.city == default_capital)]),
                      end=max(df_trim.month[(df_trim.year == year_slider.value) & (df_trim.city == default_capital)]),
                      step=1,
                      value=min(df_trim.month[(df_trim.year == year_slider.value) & (df_trim.city == default_capital)]),
                      title='Month')

cityNames = [('Perth', 'perth'), ('Adelaide', "adelaide"), ('Brisbane', "brisbane"), ('Darwin', "darwin"),
             ('Hobart', "hobart"), ('Melbourne', "melbourne"), ('Sydney', "sydney")]
cityDropdownMain = Dropdown(label="Capital City 1", button_type="success", menu=cityNames)
cityDropdownSub = Dropdown(label="Capital City 2", button_type="primary", menu=cityNames)
cityTempsDropdown = Dropdown(label="Capital City", button_type="warning", menu=cityNames)

tempData = df_trim[df_trim['city'] == currentlySelectedTempCapital][['date', 'year', '9amTemp']]
tempScatterPlotData = ColumnDataSource(data={
    'date': tempData.date,
    '9amTemp': tempData['9amTemp'],
    'year': tempData.year
})
tempBoxPlotData = []
def boxplot_data_update():
    global tempBoxPlotData
    qmin, q1, q2, q3, qmax = df_trim[(df_trim['city'] == currentlySelectedTempCapital)]['9amTemp'].quantile([0, 0.25, 0.5, 0.75, 1])

    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr

    out = (df_trim[(df_trim['city'] == currentlySelectedTempCapital)]['9amTemp'] > upper) | (df_trim[(df_trim['city'] == currentlySelectedTempCapital)]['9amTemp'] < lower)

    #outlier = []
    #if not out.empty:
    #    outlier = list(out.values)

    upper = min(qmax, upper)
    lower = max(qmin, lower)

    hbar_height = (qmax - qmin) / 500

    tempBoxPlotData = ColumnDataSource(
        data=dict(x=['Temperature (°C)'], upper=[upper], lower=[lower], q1=[q1], q2=[q2], q3=[q3], hbar_height=[hbar_height]))


def boxplot_data():
    global tempBoxPlotData
    qmin, q1, q2, q3, qmax = df_trim[(df_trim['city'] == currentlySelectedTempCapital)]['9amTemp'].quantile([0, 0.25, 0.5, 0.75, 1])

    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr

    out = (df_trim[(df_trim['city'] == currentlySelectedTempCapital)]['9amTemp'] > upper) | (df_trim[(df_trim['city'] == currentlySelectedTempCapital)]['9amTemp'] < lower)

    #outlier = []
    #if not out.empty:
    #    outlier = list(out.values)

    upper = min(qmax, upper)
    lower = max(qmin, lower)

    hbar_height = (qmax - qmin) / 500

    newData = {
        'x': 'Temperature (°C)',
        'upper': upper,
        'lower': lower,
        'q1': q1,
        'q2': q2,
        'q3': q3,
        'hbar_height': hbar_height
    }
    tempBoxPlotData.data = dict(newData)

tempScatterPlot = Selectable9amTempScatterPlot(currentlySelectedTempCapital, trimmedTempSourceData)
boxplot_data_update()
tempBoxPlot = Selectable9amTempsBoxPlot(currentlySelectedTempCapital, tempBoxPlotData)
tempBoxPlot2Y = Selectable9amTempBoxPlot2Years(currentlySelectedTempCapital)


# Creating the hover tools for the plot
evapPlot.add_tools(CreateLinePlotHoverTool(('Evaporation', '@evap{%smm}'),
                                           [('Rainfall', '@rain{%smm}'), ('Sunshine', '@sun{%s hours}'),
                                            ('City', '@city')]))
rainPlot.add_tools(CreateLinePlotHoverTool(('Rainfall', '@rain{%smm}'),
                                           [('Evaporation', '@evap{%smm}'), ('Sunshine', '@sun{%s hours}'),
                                            ('City', '@city')]))
sunPlot.add_tools(CreateLinePlotHoverTool(('Sunshine', '@sun{%s hours}'),
                                          [('Rainfall', '@rain{%smm}'), ('Evaporation', '@evap{%smm}'),
                                           ('City', '@city')]))


def update_plots(yearValue, monthValue, capitalMain, capitalSub):
    global trimmedMainSourceData, evapPlot, rainPlot, sunPlot
    # Check if all cities are being plotted
    d = df_trim[(df_trim['year'] == yearValue) & (df_trim['month'] == monthValue) & (
            df_trim['city'] == capitalMain)].reset_index(drop=True)
    d2 = df_trim[(df_trim['year'] == yearValue) & (df_trim['month'] == monthValue) & (
            df_trim['city'] == capitalSub)].reset_index(drop=True)
    # Only update the data of the plot if there's data to use
    if not d.empty or d2.empty:
        newData1 = {
            'x': d.day,
            'evap': d.evap,
            'rain': d.rain,
            'sun': d.sun,
            'city': d.city
        }

        newData2 = {
            'x': d2.day,
            'evap': d2.evap,
            'rain': d2.rain,
            'sun': d2.sun,
            'city': d2.city
        }

        trimmedMainSourceData.data = dict(newData1)
        trimmedSubSourceData.data = dict(newData2)

        yEvapmin, yEvapmax = GetMinMax(d['evap'])
        yRainmin, yRainmax = GetMinMax(d['rain'])
        ySunmin, ySunmax = GetMinMax(d['sun'])

        if not capitalMain == 'all':
            evapPlot.y_range.start = yEvapmin - 1
            evapPlot.y_range.end = yEvapmax + 5
            rainPlot.y_range.start = yRainmin - 1
            rainPlot.y_range.end = yRainmax + 5
            sunPlot.y_range.start = ySunmin - 1
            sunPlot.y_range.end = ySunmax + 5
    else:
        newData1 = {
            'x': [0],
            'evap': [0],
            'rain': [0],
            'sun': [0],
            'city': currentlySelectedMainCapital
        }

        trimmedMainSourceData.data = dict(newData1)
        trimmedSubSourceData.data = dict(newData1)

    evapPlot.title.text = capitalMain.capitalize() + ' vs ' + capitalSub.capitalize() + " Evaporation in {month} {year}".format(
        month=datetime.datetime.strptime(str(monthValue), '%m').strftime('%B'), year=yearValue)
    rainPlot.title.text = capitalMain.capitalize() + ' vs ' + capitalSub.capitalize() + " Rainfall in {month} {year}".format(
        month=datetime.datetime.strptime(str(monthValue), '%m').strftime('%B'), year=yearValue)
    sunPlot.title.text = capitalMain.capitalize() + ' vs ' + capitalSub.capitalize() + " Sunshine in {month} {year}".format(
        month=datetime.datetime.strptime(str(monthValue), '%m').strftime('%B'), year=yearValue)


def slidersOnChange(attr, old, new):
    global year_slider, month_slider, currentlySelectedMainCapital, currentlySelectedSubCapital
    clampSliders()
    update_plots(year_slider.value, month_slider.value, currentlySelectedMainCapital, currentlySelectedSubCapital)


def capitalMainDropdownOnClick(event):
    global year_slider, month_slider, currentlySelectedMainCapital, currentlySelectedSubCapital
    currentlySelectedMainCapital = event.item
    clampSliders()
    update_plots(year_slider.value, month_slider.value, currentlySelectedMainCapital, currentlySelectedSubCapital)


def capitalSubDropdownOnClick(event):
    global year_slider, month_slider, currentlySelectedMainCapital, currentlySelectedSubCapital
    currentlySelectedSubCapital = event.item
    clampSliders()
    update_plots(year_slider.value, month_slider.value, currentlySelectedMainCapital, currentlySelectedSubCapital)

def cityTempDropdownOnClick(event):
    global currentlySelectedTempCapital, tempScatterPlot, tempBoxPlot, tempBoxPlot2Y
    currentlySelectedTempCapital = event.item

    d = df_trim[(df_trim['city'] == currentlySelectedTempCapital)]

    newData = {
        'date': d.date,
        'year': d.year,
        '9amTemp': d['9amTemp']
    }

    trimmedTempSourceData.data = dict(newData)
    tempScatterPlot.title.text = f'{currentlySelectedTempCapital.capitalize()} 9am Temperatures'

    boxplot_data()



def clampSliders():
    global year_slider, month_slider, currentlySelectedMainCapital, df_trim
    # Get the new max year for the currently selected city
    if (currentlySelectedMainCapital == 'all'):
        yMin, yMax = GetMinMax(df_trim.year)
    else:
        yMin, yMax = GetMinMax(df_trim.year[df_trim.city == currentlySelectedMainCapital])
    # Clamp the year value incase the selected value is outside the range
    year_slider.value = clamp(year_slider.value, yMin, yMax)
    # Set new min and max year values
    year_slider.start = yMin
    year_slider.end = yMax
    # Get the new max month for the currently selected city
    if (currentlySelectedMainCapital == 'all'):
        mMin, mMax = GetMinMax(df_trim.month[(df_trim.year == year_slider.value)])
    else:
        mMin, mMax = GetMinMax(
            df_trim.month[(df_trim.city == currentlySelectedMainCapital) & (df_trim.year == year_slider.value)])
    # Set new min and max month values
    month_slider.start = mMin
    month_slider.end = mMax
    # Clamp the month value incase the selected value is outside the range
    month_slider.value = clamp(month_slider.value, mMin, mMax)


year_slider.on_change('value', slidersOnChange)
month_slider.on_change('value', slidersOnChange)
cityDropdownMain.on_click(capitalMainDropdownOnClick)
cityDropdownSub.on_click(capitalSubDropdownOnClick)
cityTempsDropdown.on_click(cityTempDropdownOnClick)

titleDiv = Div(text=titleDivContents)

# Temperature Graphs

# TODO - Make temperatures have sub-tabs
janTempsTab = TabPanel(child=janTemps, title='Min/Max')
monthlyPlotTempsTab = TabPanel(child=monthly_Plot_layout, title='Monthly')
monthlyAvgPlotTempsTab = TabPanel(child=monthly_avg_temp_layout, title='Monthly Avg Temp')
temp_YearOverYear_plotTempsTab = TabPanel(child=temp_YearOverYear_plot_layout, title='Year vs Year')
monthly_MinMax_plot_layoutTempsTab = TabPanel(child=monthly_MinMax_plot_layout, title='Monthly Min/Max')
yearly_MinMax_plot_layoutTempsTab = TabPanel(child=yearly_MinMax_plot_layout, title='Yearly Min/Max')

# TODO: Update to use a dropdown to select the city
selectable9amScatterTempTab = TabPanel(child=column(row(cityTempsDropdown), tempScatterPlot), title='9am Scatter')
selectable9amBoxplotTempTab = TabPanel(child=column(row(cityTempsDropdown), tempBoxPlot), title='9am Box')
selectable9amBoxplot2YearsTempTab = TabPanel(child=column(row(cityTempsDropdown), tempBoxPlot2Y),
                                             title='9am Box Year vs Year')

perthTempsTab = TabPanel(child=Tabs(tabs=[janTempsTab, monthlyPlotTempsTab, monthlyAvgPlotTempsTab,
                                          temp_YearOverYear_plotTempsTab, monthly_MinMax_plot_layoutTempsTab,
                                          yearly_MinMax_plot_layoutTempsTab]), title='Perth - A1')

tempTabs = TabPanel(child=Tabs(tabs=[perthTempsTab, selectable9amScatterTempTab, selectable9amBoxplotTempTab,
                                     selectable9amBoxplot2YearsTempTab], margin=(10, 0, 0, 0)),
                    title='Temperature')

evapTab = CreateGraphTabPanel(cityDropdownMain, cityDropdownSub, year_slider, month_slider, evapPlot, "Evaporation")
rainTab = CreateGraphTabPanel(cityDropdownMain, cityDropdownSub, year_slider, month_slider, rainPlot, "Rainfall")
sunTab = CreateGraphTabPanel(cityDropdownMain, cityDropdownSub, year_slider, month_slider, sunPlot, "Sunshine")

layout = CreatePageLayout(titleItem=titleDiv, pageTabItems=[tempTabs, evapTab, rainTab, sunTab], align="center",
                          margin=(50, 0, 50, 50))

curdoc().add_root(layout)
curdoc().theme = 'dark_minimal'
curdoc().title = "ICT305 Assignment 2 - Pink Fluffy Unicorns"