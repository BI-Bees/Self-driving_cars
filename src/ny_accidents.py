import os
import csv
import pandas as pd
from collections import Counter
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge

df = None

# This method reads a csv-file (url given as param) and saves it as a (global) dataframe
def saveDataFromFileAsDataframe(url):
    filename = os.path.basename(url)
    global df
    df = pd.read_csv(filename)

# This method calculates top 10 vehicle makes involved in car crashes and returns a dictionary containing data about vehicle makes, years, and amount of car crashes
def getDictWithAccidentData():
    years = df['Year'].unique()

    years = [str(year) for year in years]
    vehicle_makes = df['Vehicle Make'].dropna()

    top_vecicle_makes = {}
    for make in vehicle_makes:
        if make in top_vecicle_makes:
            top_vecicle_makes[make] += 1
        else:
            top_vecicle_makes[make] = 1
    top_vecicle_makes = dict(Counter(top_vecicle_makes).most_common(10))

    data = {'top_vecicle_makes': [*top_vecicle_makes]}

    for year in years:
        data[year] = []
        for make in top_vecicle_makes:
            data[year].append(df[(df['Year'] == int(year)) & (
                df['Vehicle Make'] == make)].count()['Vehicle Make'])
    return data

# This method creates a bar chart of the given data, saves it and shows it as a HTML-file
def createBarChartVehicleMakes(data):
    source = ColumnDataSource(data=data)

    TOOLTIPS = [
        ("År", "$name"),
        ("Uheld", "@$name"),
        ("Mærke", "@top_vecicle_makes")
    ]

    p = figure(x_range=data['top_vecicle_makes'], plot_height=500, title="TOP 10 BILMÆRKER MED FLEST FÆRDSELSUHELD I NEW YORK",
               x_axis_label='Bilmærke', y_axis_label='Antal Uheld', tooltips=TOOLTIPS)

    p.vbar(x=dodge('top_vecicle_makes', -0.25, range=p.x_range), top='2014', width=0.2, source=source,
           color="#c9d9d3", legend=value("2014"), name="2014")

    p.vbar(x=dodge('top_vecicle_makes',  0.0,  range=p.x_range), top='2015', width=0.2, source=source,
           color="#718dbf", legend=value("2015"), name="2015")

    p.vbar(x=dodge('top_vecicle_makes',  0.25, range=p.x_range), top='2016', width=0.2, source=source,
           color="#e84d60", legend=value("2016"), name="2016")

    p.legend.click_policy = "hide"
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "horizontal"

    output_file("bar_chart_ny.html", title='Uheld NY')

    show(p)

# This method finds all car crashes and returns lists containing in which years the accidents happened and the amount of the accidents
def getListsWithAllCarsData():
    years = [2014, 2015, 2016]
    accidents = []

    for year in years:
        accidents.append(
            df.loc[df['Year'] == year].count()['Year'])

    return years, accidents

# This method finds all accidents with self-driving cars involved and returns lists containing in which years the accidents happened and the amount of the accidents
def getListsWithSelfDrivingCarsData():
    years = [2014, 2015, 2016]
    electric_car_accidents = df.loc[df['Fuel Type'] == 'Electric']
    accidents = []

    for year in years:
        accidents.append(
            electric_car_accidents.loc[df['Year'] == year].count()['Year'])

    return years, accidents

# This method creates a bar chart with the given data, saves it and shows it as a HTML-file
def createBarChart(years, accidents, title, y_range):
    source = ColumnDataSource(data=dict(
        x=years,
        y=accidents
    ))

    TOOLTIPS = [
        ("År", "$x{0}"),
        ("Uheld", "@y")
    ]

    # create a new plot with a title and axis labels
    p = figure(title=title.split('#')[1], x_axis_label='Årstal',
               y_axis_label='Antal Uheld', y_range=y_range, tooltips=TOOLTIPS)
    p.xaxis.ticker = years

    p.vbar(x='x', top='y', source=source, width=0.5, color="blue")

    output_file("bar_chart_" + title.split('#')[0] + ".html", title='Uheld NY')

    show(p)


# path to csv-file containing data
url = 'crashes_ny.csv'
saveDataFromFileAsDataframe(url)

# method calls
years, accidents = getListsWithSelfDrivingCarsData()
createBarChart(years, accidents,
               "self#FÆRDSELSUHELD MED SELVKØRENDE BILER INVOLVERET (NEW YORK)", [0, 400])
years, accidents = getListsWithAllCarsData()
createBarChart(years, accidents,
               "all#ALLE FÆRDSELSUHELD I NEW YORK FRA ÅR 2014-2016", [500000, 575000])

data = getDictWithAccidentData()
createBarChartVehicleMakes(data)

# This is only made for testing
# print("TOYOTA")
# print(df[(df["Year"] == 2014) & (df["Vehicle Make"] == "TOYOT")].count()["Vehicle Make"])
# print(df[(df["Year"] == 2015) & (df["Vehicle Make"] == "TOYOT")].count()["Vehicle Make"])
# print(df[(df["Year"] == 2016) & (df["Vehicle Make"] == "TOYOT")].count()["Vehicle Make"])
# print("-------------------------------------")
# print("FORD")
# print(df[(df["Year"] == 2014) & (df["Vehicle Make"] == "FORD")].count()["Vehicle Make"])
# print(df[(df["Year"] == 2015) & (df["Vehicle Make"] == "FORD")].count()["Vehicle Make"])
# print(df[(df["Year"] == 2016) & (df["Vehicle Make"] == "FORD")].count()["Vehicle Make"])
# print("-------------------------------------")
# print("HONDA")
# print(df[(df["Year"] == 2014) & (df["Vehicle Make"] == "HONDA")].count()["Vehicle Make"])
# print(df[(df["Year"] == 2015) & (df["Vehicle Make"] == "HONDA")].count()["Vehicle Make"])
# print(df[(df["Year"] == 2016) & (df["Vehicle Make"] == "HONDA")].count()["Vehicle Make"])
# print("-------------------------------------")
# print("CHEVR")
# print(df[(df["Year"] == 2014) & (df["Vehicle Make"] == "CHEVR")].count()["Vehicle Make"])
# print(df[(df["Year"] == 2015) & (df["Vehicle Make"] == "CHEVR")].count()["Vehicle Make"])
# print(df[(df["Year"] == 2016) & (df["Vehicle Make"] == "CHEVR")].count()["Vehicle Make"])
# print("-------------------------------------")
# print("NISSA")
# print(df[(df["Year"] == 2014) & (df["Vehicle Make"] == "NISSA")].count()["Vehicle Make"])
# print(df[(df["Year"] == 2015) & (df["Vehicle Make"] == "NISSA")].count()["Vehicle Make"])
# print(df[(df["Year"] == 2016) & (df["Vehicle Make"] == "NISSA")].count()["Vehicle Make"])
