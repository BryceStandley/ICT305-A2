# Imports
from temps import *
from src.Utils import *
from src.a2temps import *
from bokeh.io import curdoc

# Load title HTML file
with open('./python/src/titleDiv.html', 'r', encoding='utf-8') as f:
    titleDivContents = f.read()

# Code used to load and combine the different csv files into a single csv
'''
# Define the folder path
folder_path = "./python/ICT305_States"

# Create DFs
adelaideDF = pd.read_csv(os.path.join(folder_path, "Adelaide.csv"), encoding='latin1')
brisbaneDF = pd.read_csv(os.path.join(folder_path, "Brisbane.csv"), encoding='latin1')
darwinDF = pd.read_csv(os.path.join(folder_path, "Darwin.csv"), encoding='latin1')
hobartDF = pd.read_csv(os.path.join(folder_path, "Hobart.csv"), encoding='latin1')
perthDF = pd.read_csv(os.path.join(folder_path, "Perth.csv"), encoding='latin1')
melbourneDF = pd.read_csv(os.path.join(folder_path, "Melbourne.csv"), encoding='latin1')
sydneyDF = pd.read_csv(os.path.join(folder_path, "Sydney.csv"), encoding='latin1')

# Rename columns because they have garbage ascii characters in their names
new_columns = {
    'ï»¿Date': 'Date',
    'Minimum temperature (ÃÂ°C)': 'Min Temperature (°C)',
    'Maximum temperature (ÃÂ°C)': 'Max Temperature (°C)',
    'Rainfall (mm)': 'Rainfall (mm)',
    'Evaporation (mm)': 'Evaporation (mm)',
    'Sunshine (hours)': 'Sunshine (hours)',
    'Direction of maximum wind gust ': 'Max Wind Gust Direction',
    'Speed of maximum wind gust (km/h)': 'Max Wind Gust Speed (km/h)',
    'Time of maximum wind gust': 'Time of Max Wind Gust',
    '9am Temperature (ÃÂ°C)': '9am Temperature (°C)',
    '9am relative humidity (%)': '9am Relative Humidity (%)',
    '9am cloud amount (oktas)': '9am Cloud Amount (oktas)',
    '9am wind direction': '9am Wind Direction',
    '9am wind speed (km/h)': '9am Wind Speed (km/h)',
    '9am MSL pressure (hPa)': '9am MSL Pressure (hPa)',
    '3pm Temperature (ÃÂ°C)': '3pm Temperature (°C)',
    '3pm relative humidity (%)': '3pm Relative Humidity (%)',
    '3pm cloud amount (oktas)': '3pm Cloud Amount (oktas)',
    '3pm wind direction': '3pm Wind Direction',
    '3pm wind speed (km/h)': '3pm Wind Speed (km/h)',
    '3pm MSL pressure (hPa)': '3pm MSL Pressure (hPa)'
}

# Rename columns in each DataFrame
adelaideDF = adelaideDF.rename(columns=new_columns)
brisbaneDF = brisbaneDF.rename(columns=new_columns)
darwinDF = darwinDF.rename(columns=new_columns)
hobartDF = hobartDF.rename(columns=new_columns)
perthDF = perthDF.rename(columns=new_columns)
melbourneDF = melbourneDF.rename(columns=new_columns)
sydneyDF = sydneyDF.rename(columns=new_columns)
# Adding the City to each frame
adelaideDF.insert(1, "city", "adelaide")
brisbaneDF.insert(1, "city", "brisbane")
darwinDF.insert(1, "city", "darwin")
hobartDF.insert(1, "city", "hobart")
perthDF.insert(1, "city", "perth")
melbourneDF.insert(1, "city", "melbourne")
sydneyDF.insert(1, "city", "sydney")

# Grouping the data
dataframes = [adelaideDF, brisbaneDF, darwinDF, hobartDF, melbourneDF, perthDF, sydneyDF]
all_cities_df = pd.concat(dataframes)

# Pre-process and update the dates of the dataframe to be the correct format
all_cities_df["Date"] = pd.to_datetime(all_cities_df["Date"], format='%d/%m/%Y')

# Pre-processing Data
# Add day, month and year columns
all_cities_df['day'] = all_cities_df['Date'].dt.day
all_cities_df['month'] = all_cities_df['Date'].dt.month
all_cities_df['year'] = all_cities_df['Date'].dt.year

# Trim Data
df_trim = all_cities_df.loc[:, ('Date', 'city', 'day', 'month', 'year', 'Evaporation (mm)', 'Rainfall (mm)',
                                'Sunshine (hours)', 'Min Temperature (°C)', 'Max Temperature (°C)',
                                'Max Wind Gust Direction',
                                'Max Wind Gust Speed (km/h)', 'Time of Max Wind Gust', '9am Temperature (°C)',
                                '9am Relative Humidity (%)',
                                '9am Cloud Amount (oktas)', '9am Wind Direction', '9am Wind Speed (km/h)',
                                '9am MSL Pressure (hPa)',
                                '3pm Temperature (°C)', '3pm Relative Humidity (%)', '3pm Cloud Amount (oktas)',
                                '3pm Wind Direction',
                                '3pm Wind Speed (km/h)', '3pm MSL Pressure (hPa)')]

df_trim.columns = ['date', 'city', 'day', 'month', 'year', 'evap', 'rain', 'sun', 'minTemp', 'maxTemp',
                   'maxWindGustDir', 'maxWindGustSpeed', 'maxWindGustTime', '9amTemp', '9amRelHum', '9amClouds',
                   '9amWindDir', '9amWindSpeed', '9amMSL', '3pmTemp', '3pmRelHumid', '3pmClouds', '3pmWindDir',
                   '3pmWindSpeed', '3pmMSL']

df_trim.fillna(value=0.0, inplace=True)
df_trim.to_csv(path_or_buf="./all_cities.csv")
'''

df_trim = pd.read_csv("./python/all_cities.csv")

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

# Plot Setup
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

currentlySelectedMainCapital = default_capital
currentlySelectedSubCapital = default_sub_capital
currentlySelectedTempCapital = default_temp_capital

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

tempData = df_trim[df_trim['city'] == currentlySelectedTempCapital][['date','year', '9amTemp']]
tempScatterPlotData = ColumnDataSource(data={
    'date': tempData.date,
    '9amTemp': tempData['9amTemp'],
    'year': tempData.year
})

tempScatterPlot = Selectable9amTempScatterPlot(currentlySelectedTempCapital)
tempBoxPlot = Selectable9amTempsBoxPlot(currentlySelectedTempCapital)
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

    newData = dict(
        x=tempData.date,
        y=tempData['9amTemp'],
        year=tempData.year
    )

    tempScatterPlotData.data = newData
    tempScatterPlot = Selectable9amTempScatterPlot(currentlySelectedTempCapital)
    tempBoxPlot = Selectable9amTempsBoxPlot(currentlySelectedTempCapital)
    tempBoxPlot2Y = Selectable9amTempBoxPlot2Years(currentlySelectedTempCapital)


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
selectable9amScatterTempTab = TabPanel(child=column(row(cityTempsDropdown),tempScatterPlot), title='9am Scatter')
selectable9amBoxplotTempTab = TabPanel(child=column(row(cityTempsDropdown),tempBoxPlot), title='9am Box')
selectable9amBoxplot2YearsTempTab = TabPanel(child=column(row(cityTempsDropdown),tempBoxPlot2Y),
                                             title='9am Box Year vs Year')

perthTempsTab = TabPanel(child=Tabs(tabs=[janTempsTab, monthlyPlotTempsTab, monthlyAvgPlotTempsTab,
                                          temp_YearOverYear_plotTempsTab,monthly_MinMax_plot_layoutTempsTab,
                                          yearly_MinMax_plot_layoutTempsTab]), title='Perth - A1')

tempTabs = TabPanel(child=Tabs(tabs=[perthTempsTab, selectable9amScatterTempTab,selectable9amBoxplotTempTab,
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
