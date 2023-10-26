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