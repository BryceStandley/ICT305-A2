#Imports

import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, Div, Slider, Range1d, PrintfTickFormatter, CustomJSTickFormatter, CustomJS, InlineStyleSheet, Button, CustomJS, SetValue, TabPanel, Tabs, DatetimeTickFormatter, Legend, LegendItem
from bokeh.layouts import column, row
import os

main_dir = os.path.dirname(__file__)
dataset_file_path = os.path.join(main_dir, 'res', '305data.csv')

#Read in data
df = pd.read_csv(dataset_file_path)

# Convert the date column to datetime with the correct format
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Sort data by date
df = df.sort_values(by='Date')

#Shows min and max for each day across January 2021
# Filter data for January 2021
january_data = df[(df['Date'].dt.year == 2021) & (df['Date'].dt.month == 1)]

#Bokeh
minJanSource= ColumnDataSource(data={
    'x': january_data.Date,
    'y': january_data['Minimum temperature (°C)'],
})
maxJanSource= ColumnDataSource(data={
    'x': january_data.Date,
    'y': january_data['Maximum temperature (°C)']
})

janTemps = figure(height=600, width=800)
janTemps.xaxis.axis_label = 'Date'
janTemps.yaxis.axis_label = 'Temperature (°C)'
janTemps.title = 'Perth Min & Max Temperatures in January 2021'
janTemps.line(source=minJanSource, color='blue', legend_label ='Min Temp')
janTemps.line(source=maxJanSource, color='red', legend_label ='Max Temp')

janTemps.legend.location= 'top_right'

janTemps.xaxis[0].formatter = DatetimeTickFormatter()

#Specify Year and Month using 2 sliders.
#Generates graph with min and max
#Does not work for data beyond August of 2023

#bokeh

# Create sliders
monthly_plot_year_slider = Slider(start=2008, end=2023, step=1, value=2021, title='Year')
monthly_plot_month_slider = Slider(start=1, end=12, step=1, value=1, title='Month')

# Create generate plot button
monthly_plot_button = Button(label="Generate Plot", button_type='default')

# Filter data
setupData = df[(df['Date'].dt.year == 2021) & (df['Date'].dt.month == 1)]
setup_monthly_data = setupData.loc[:,('Date', 'Minimum temperature (°C)', 'Maximum temperature (°C)')]
setup_monthly_data.columns = ['Date', 'minTemp', 'maxTemp']

minS = ColumnDataSource(data={'x': setup_monthly_data.Date, 'y' : setup_monthly_data.minTemp})
maxS = ColumnDataSource(data={'x': setup_monthly_data.Date, 'y' : setup_monthly_data.maxTemp})

temp_plot = figure(height=600, width=800)
temp_plot.xaxis.axis_label = 'Date'
temp_plot.yaxis.axis_label = 'Temperature (°C)'
temp_plot.title = 'Perth Min & Max Temperatures in {month}'
temp_plot.line(source=minS, color='blue', legend_label ='Min Temp')
temp_plot.line(source=maxS, color='red', legend_label ='Max Temp')

temp_plot.legend.location= 'top_right'
temp_plot.xaxis.formatter = DatetimeTickFormatter(days='%d', months="%m", years='&Y')
temp_plot.xaxis.major_label_orientation = 'horizontal'
temp_plot.xaxis.major_label_orientation = 45  # Rotate by 45 degrees


# func for plot
def plot_monthly_data_bokeh(event = None):
    
    year = monthly_plot_year_slider.value
    month = monthly_plot_month_slider.value
    
    # Filter data
    data = df[(df['Date'].dt.year == year) & (df['Date'].dt.month == month)]
    monthly_data = data.loc[:,('Date', 'Minimum temperature (°C)', 'Maximum temperature (°C)')]
    monthly_data.columns = ['Date', 'minTemp', 'maxTemp']
    
    # Skip empty months
    if len(monthly_data) == 0:
        return
    
    minTempSource ={
        'x' : monthly_data.Date,
        'y' : monthly_data.minTemp,
    }
    
    maxTempSource = {
        'x' : monthly_data.Date,
        'y' : monthly_data.maxTemp,
    }
    
    minS.data = minTempSource
    maxS.data = maxTempSource
    temp_plot.title.text = 'Perth Min & Max Temperatures in {month}'.format(month = monthly_data.iloc[0]["Date"].strftime("%B %Y"))

# func for button click
monthly_plot_button.on_click(plot_monthly_data_bokeh)

plot_monthly_data_bokeh()

# Display graph
monthly_Plot_layout = column(row(monthly_plot_year_slider, monthly_plot_month_slider, monthly_plot_button), temp_plot)

#Months averaged and shown across 12 months(Jan->Feb)
#Slider to select what year
#DOES NOT WORK FOR 2023
#Bokeh
monthly_temp_plot_yearly_data = df[df['Date'].dt.year == 2021]
monthly_averages = monthly_temp_plot_yearly_data.loc[:,('Date', 'Minimum temperature (°C)', 'Maximum temperature (°C)')]
monthly_averages.columns = ['Date', 'minTemp', 'maxTemp']
monthly_averages = monthly_averages.groupby(monthly_averages.Date.dt.month)[['minTemp', 'maxTemp']].mean()

# Month names
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

minMonthlyTempSource = ColumnDataSource(data={
    'x' : monthly_averages.index,
    'y' : monthly_averages.minTemp,
})

maxMonthlyTempSource = ColumnDataSource(data={
    'x' : monthly_averages.index,
    'y' : monthly_averages.maxTemp,
})

monthly_temp_plot = figure(height=600, width=800, x_range=(1,12))
monthly_temp_plot.xaxis.axis_label = 'Month'
monthly_temp_plot.yaxis.axis_label = 'Temperature (°C)'
monthly_temp_plot.title = 'Perth Average Min & Max Temperatures in {year}'.format(year = 2021)
monthly_temp_plot.line(source=minMonthlyTempSource, color='blue', legend_label ='Avg Min Temp')
monthly_temp_plot.line(source=maxMonthlyTempSource, color='red', legend_label ='Avg Max Temp')

monthly_temp_plot.legend.location= 'top_right'
monthly_temp_plot.xaxis.formatter = CustomJSTickFormatter(code="""
    var month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return month_names[tick - 1];
""")
monthly_temp_plot.xaxis.major_label_orientation = 'horizontal'
monthly_temp_plot.xaxis.major_label_orientation = 45  # Rotate by 45 degrees
monthly_temp_plot.xaxis.ticker.desired_num_ticks = 12

# Create slider
monthly_temp_plot_year_slider = Slider(start=2008, end=2023, step=1, value=2021, title='Year')

def update_plot(att, old, new):
    year = monthly_temp_plot_year_slider.value    
    
    data = df[df['Date'].dt.year == year]
    
    averages = data.loc[:,('Date', 'Minimum temperature (°C)', 'Maximum temperature (°C)')]
    averages.columns = ['Date', 'minTemp', 'maxTemp']
    averages = averages.groupby(averages.Date.dt.month)[['minTemp', 'maxTemp']].mean()
    
    new_min_data = {
        'x' : averages.index,
        'y' : averages.minTemp,
    }
    
    new_max_data = {
        'x' : averages.index,
        'y' : averages.maxTemp,
    }
    
    monthly_temp_plot.title.text = "Perth Yearly Average Temperatures for {year}".format(year = year)
    minMonthlyTempSource.data = new_min_data
    maxMonthlyTempSource.data = new_max_data
    

monthly_temp_plot_year_slider.on_change('value', update_plot)

monthly_avg_temp_layout = column(row(monthly_temp_plot_year_slider), monthly_temp_plot)


#Compare the monthly averages across a year of 2 years.
#Slider to choose the 2 years, one shown with triangles other shown with circles

#DOES NOT WORK FOR 2023

#Might need to move each of the sliders for it to generate the first plot

# Bokeh

# Create sliders for selecting the years
temp_year1_slider = Slider(start=2008, end=2023, step=1, value=2021, title='Year 1')
temp_year2_slider = Slider(start=2008, end=2023, step=1, value=2022, title='Year 2')

# Filter data
setupData_year1 = df[df['Date'].dt.year == temp_year1_slider.value]
setupData_year2 = df[df['Date'].dt.year == temp_year2_slider.value]

#Year 1 Avg Data
setup_year1_monthly_avg_data = setupData_year1.loc[:,('Date', 'Minimum temperature (°C)', 'Maximum temperature (°C)')]
setup_year1_monthly_avg_data.columns = ['Date', 'minTemp', 'maxTemp']
setup_year1_monthly_avg_data = setup_year1_monthly_avg_data.groupby(setup_year1_monthly_avg_data['Date'].dt.month)[['minTemp', 'maxTemp']].mean()

#Year 2 Avg Data
setup_year2_monthly_avg_data = setupData_year2.loc[:,('Date', 'Minimum temperature (°C)', 'Maximum temperature (°C)')]
setup_year2_monthly_avg_data.columns = ['Date', 'minTemp', 'maxTemp']
setup_year2_monthly_avg_data = setup_year2_monthly_avg_data.groupby(setup_year2_monthly_avg_data['Date'].dt.month)[['minTemp', 'maxTemp']].mean()

minSY1 = ColumnDataSource(data={'x': setup_year1_monthly_avg_data.index, 'y' : setup_year1_monthly_avg_data.minTemp})
maxSY1 = ColumnDataSource(data={'x': setup_year1_monthly_avg_data.index, 'y' : setup_year1_monthly_avg_data.maxTemp})

minSY2 = ColumnDataSource(data={'x': setup_year2_monthly_avg_data.index, 'y' : setup_year2_monthly_avg_data.minTemp})
maxSY2 = ColumnDataSource(data={'x': setup_year2_monthly_avg_data.index, 'y' : setup_year2_monthly_avg_data.maxTemp})

temp_YearOverYear_plot = figure(height=600, width=800)
temp_YearOverYear_plot.xaxis.axis_label = 'Month'
temp_YearOverYear_plot.yaxis.axis_label = 'Temperature (°C)'
temp_YearOverYear_plot.title = 'Perth Yearly Average Temperatures for {year1} and {year2}'.format(year1 = temp_year1_slider.value, year2 = temp_year2_slider.value)


minY1_line = temp_YearOverYear_plot.line(source=minSY1, color='blue')
minY1_cross = temp_YearOverYear_plot.cross(source=minSY1, color='blue', size=18, angle=45)
maxY1_line = temp_YearOverYear_plot.line(source=maxSY1, color='red')
maxY1_cross = temp_YearOverYear_plot.cross(source=maxSY1, color='red', size=18, angle=45)

minY2_line = temp_YearOverYear_plot.line(source=minSY2, color='blue')
minY2_circle = temp_YearOverYear_plot.circle(source=minSY2, color='blue', fill_color='blue', size=8)
maxY2_line = temp_YearOverYear_plot.line(source=maxSY2, color='red',)
maxY2_circle = temp_YearOverYear_plot.circle(source=maxSY2, color='red', fill_color='red', size=8)

legend = Legend(items=[
    LegendItem(index=0, label='Min Temp {year1}'.format(year1 = temp_year1_slider.value), renderers=[minY1_line, minY1_cross]),
    LegendItem(index=1, label='Max Temp {year1}'.format(year1 = temp_year1_slider.value), renderers=[maxY1_line, maxY1_cross]),
    LegendItem(index=2, label='Min Temp {year2}'.format(year2 = temp_year2_slider.value), renderers=[minY2_line, minY2_circle]),
    LegendItem(index=3, label='Max Temp {year2}'.format(year2 = temp_year2_slider.value), renderers=[maxY2_line, maxY2_circle]),
], location="top_right")
temp_YearOverYear_plot.add_layout(legend)

temp_YearOverYear_plot.xaxis.formatter = CustomJSTickFormatter(code="""
    var month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return month_names[tick - 1];
    """)
temp_YearOverYear_plot.xaxis.major_label_orientation = 'horizontal'
temp_YearOverYear_plot.xaxis.major_label_orientation = 45  # Rotate by 45 degrees
temp_YearOverYear_plot.xaxis.ticker.desired_num_ticks = 12

# Function to generate and display the plot for the selected years
def plot_selected_years(att, old, new):
    
    year1 = temp_year1_slider.value
    year2 = temp_year2_slider.value
    
    # Filter data 
    year1_data = df[df['Date'].dt.year == year1]
    year2_data = df[df['Date'].dt.year == year2]
    
    #Year 1 Avg Data
    year1_monthly_avg_data = year1_data[['Date', 'Minimum temperature (°C)', 'Maximum temperature (°C)']]
    year1_monthly_avg_data.columns = ['Date', 'minTemp', 'maxTemp']
    year1_monthly_avg_data = year1_monthly_avg_data.groupby(year1_monthly_avg_data['Date'].dt.month)[['minTemp', 'maxTemp']].mean()
    
    #Year 2 Avg Data
    year2_monthly_avg_data = year2_data[['Date', 'Minimum temperature (°C)', 'Maximum temperature (°C)']]
    year2_monthly_avg_data.columns = ['Date', 'minTemp', 'maxTemp']
    year2_monthly_avg_data = year2_monthly_avg_data.groupby(year2_monthly_avg_data['Date'].dt.month)[['minTemp', 'maxTemp']].mean()
    
    new_y1_min_data = {
        'x' : year1_monthly_avg_data.index,
        'y' : year1_monthly_avg_data.minTemp
    }
    new_y1_max_data = {
        'x' : year1_monthly_avg_data.index,
        'y' : year1_monthly_avg_data.maxTemp
    }
    
    new_y2_min_data = {
        'x' : year2_monthly_avg_data.index,
        'y' : year2_monthly_avg_data.minTemp
    }
    new_y2_max_data = {
        'x' : year2_monthly_avg_data.index,
        'y' : year2_monthly_avg_data.maxTemp
    }
    
    minSY1.data = new_y1_min_data
    maxSY1.data = new_y1_max_data
    minSY2.data = new_y2_min_data
    maxSY2.data = new_y2_max_data
    temp_YearOverYear_plot.title.text = "Perth Yearly Average Temperatures for {year1} and {year2}".format(year1 = year1, year2 = year2)
    legendItems = legend.items
    legendItems[0] = LegendItem(label='Min Temp {year1}'.format(year1 = year1), renderers=[minY1_line, minY1_cross] )
    legendItems[1] = LegendItem(label='Max Temp {year1}'.format(year1 = year1), renderers=[maxY1_line, maxY1_cross] )
    legendItems[2] = LegendItem(label='Min Temp {year2}'.format(year2 = year2), renderers=[minY2_line, minY2_circle] )
    legendItems[3] = LegendItem(label='Max Temp {year2}'.format(year2 = year2), renderers=[maxY2_line, maxY2_circle] )
    legend.update(items = legendItems)

# Observe the slider values and call the update function
temp_year1_slider.on_change('value', plot_selected_years)
temp_year2_slider.on_change('value', plot_selected_years)

temp_YearOverYear_plot_layout = column(row(temp_year1_slider, temp_year2_slider), temp_YearOverYear_plot)


# Plot min/max for each month for every year.
df_trim_minmax = df.loc[:,('Date', 'Minimum temperature (°C)', 'Maximum temperature (°C)')]
df_trim_minmax['year'] = df['Date'].dt.year
df_trim_minmax['month'] = df['Date'].dt.month

df_trim_minmax['minTemp'] = df_trim_minmax.groupby(['year','month'])['Minimum temperature (°C)'].transform('min')
df_trim_minmax['maxTemp'] = df_trim_minmax.groupby(['year','month'])['Maximum temperature (°C)'].transform('max')

# Step 2: Filter for date values
minTempRows = df_trim_minmax[df_trim_minmax['Minimum temperature (°C)'] == df_trim_minmax['minTemp']]
maxTempRows = df_trim_minmax[df_trim_minmax['Maximum temperature (°C)'] == df_trim_minmax['maxTemp']]

monthly_MinMax_data = minTempRows.merge(maxTempRows, how="right")
# Create the figure
monthly_MinMax_plot = figure(height=600, width=800)

# Update axes labels and title
monthly_MinMax_plot.title = 'Perth Min & Max Temperatures Per Month'
monthly_MinMax_plot.xaxis.axis_label = 'Year'
monthly_MinMax_plot.yaxis.axis_label = 'Temperature (°C)'

monthly_MinMax_minSource = ColumnDataSource(data={
    'x' : monthly_MinMax_data.index,
    'y' : monthly_MinMax_data.minTemp,
    'year' : monthly_MinMax_data.year,
    'month' : monthly_MinMax_data.month,
    'date' : monthly_MinMax_data.Date
})
monthly_MinMax_maxSource = ColumnDataSource(data={
    'x' : monthly_MinMax_data.index,
    'y' : monthly_MinMax_data.maxTemp,
    'year' : monthly_MinMax_data.year,
    'month' : monthly_MinMax_data.month,
    'date' : monthly_MinMax_data.Date
})

monthly_min_scatter = monthly_MinMax_plot.scatter(source=monthly_MinMax_minSource, size=8, marker='triangle', color='blue')
monthly_min_line = monthly_MinMax_plot.line(source=monthly_MinMax_minSource, line_width=1, line_dash=[4,4], color='blue')

monthly_max_scatter = monthly_MinMax_plot.scatter(source=monthly_MinMax_maxSource, size=8, marker='circle', color='red')
monthly_max_line = monthly_MinMax_plot.line(source=monthly_MinMax_maxSource, line_width=1, line_dash=[4,4], color='red')

monthly_MinMax_plot.xaxis.major_label_orientation = 'horizontal'
monthly_MinMax_plot.xaxis.ticker.desired_num_ticks = 15

year_starts = monthly_MinMax_data[monthly_MinMax_data['month'] == 1].index
monthly_MinMax_plot.xaxis.major_label_overrides = {x: str(monthly_MinMax_data['year'][x]) for x in monthly_MinMax_data.index}

#TODO - Add Date back into hover
minTemp_Hover = HoverTool(tooltips=[('Year', '@year'), ('Month', '@month'), ('Date', '@date{%d/%m/%Y}'), ('Min Temp', '@y{0.0} °C')], formatters={
    '@month' : 'printf',
    '@year' : 'printf',
    '@date' : 'datetime',
}, renderers=[monthly_min_scatter, monthly_min_line])
monthly_MinMax_plot.add_tools(minTemp_Hover)

maxTemp_Hover = HoverTool(tooltips=[('Year', '@year'), ('Month', '@month'), ('Date', '@date{%d/%m/%Y}'), ('Max Temp', '@y{0.0} °C')], formatters={
    '@month' : 'printf',
    '@year' : 'printf',
    '@date' : 'datetime',
}, renderers=[monthly_max_scatter, monthly_max_line])
monthly_MinMax_plot.add_tools(maxTemp_Hover)


monthly_MinMax_plot_layout = row(monthly_MinMax_plot)

# Highest and lowest point for each year all on one plot
# Step 1: Obtain the highest and lowest temperature of each year
df_trim = df.loc[:,('Date', 'Minimum temperature (°C)', 'Maximum temperature (°C)')]
df_trim['year'] = df['Date'].dt.year
df_trim['minTemp'] = df_trim.groupby('year')['Minimum temperature (°C)'].transform('min')
df_trim['maxTemp'] = df_trim.groupby('year')['Maximum temperature (°C)'].transform('max')

# Step 2: Filter for date values
minRows = df_trim[df_trim['Minimum temperature (°C)'] == df_trim['minTemp']]
maxRows = df_trim[df_trim['Maximum temperature (°C)'] == df_trim['maxTemp']]

# Create the figure
yearly_MinMax_plot = figure(height=600, width=800)

# Update axes labels and title
yearly_MinMax_plot.title = 'Perth Min & Max Temperatures Per Year'
yearly_MinMax_plot.xaxis.axis_label = 'Year'
yearly_MinMax_plot.yaxis.axis_label = 'Temperature (°C)'

yearly_MinMax_minSource = ColumnDataSource(data={
    'x' : minRows.year,
    'y' : minRows.minTemp,
    'year' : minRows.year,
    'date' : minRows.Date
})
yearly_MinMax_maxSource = ColumnDataSource(data={
    'x' : maxRows.year,
    'y' : maxRows.maxTemp,
    'year' : maxRows.year,
    'date' : maxRows.Date
})


yearly_min_circle = yearly_MinMax_plot.circle(source=yearly_MinMax_minSource, size=8, color='blue', legend_label='Min Temp')
yearly_min_line = yearly_MinMax_plot.line(source=yearly_MinMax_minSource, line_width=1, line_dash=[4,4], color='blue', legend_label='Min Temp')

yearly_max_circle = yearly_MinMax_plot.circle(source=yearly_MinMax_maxSource, size=8, color='red', legend_label='Max Temp')
yearly_max_line = yearly_MinMax_plot.line(source=yearly_MinMax_maxSource, line_width=1, line_dash=[4,4], color='red', legend_label='Max Temp')

yearly_MinMax_plot.xaxis.major_label_orientation = 'horizontal'
yearly_MinMax_plot.xaxis.ticker.desired_num_ticks = 15

yearly_minTemp_Hover = HoverTool(tooltips=[('Date', '@date{%d/%m/%Y}'), ('Min Temp', '@y{0.0} °C')], formatters={
    '@date' : 'datetime',
}, renderers=[yearly_min_circle, yearly_min_line])
yearly_MinMax_plot.add_tools(yearly_minTemp_Hover)

yearly_maxTemp_Hover = HoverTool(tooltips=[('Date', '@date{%d/%m/%Y}'), ('Max Temp', '@y{0.0} °C')], formatters={
    '@date' : 'datetime',
}, renderers=[yearly_max_circle, yearly_max_line])
yearly_MinMax_plot.add_tools(yearly_maxTemp_Hover)


yearly_MinMax_plot_layout = row(yearly_MinMax_plot)