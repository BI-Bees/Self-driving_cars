import os
import csv
from bokeh.plotting import figure, output_file, show, ColumnDataSource

# This method reads the first two rows (years and accidents) in a file (url given as param) and returns lists containing the data
def getDataFromFile(url):
    filename = os.path.basename(url)

    # Reading the file
    with open(filename) as f:
        reader = csv.reader(f)

        years = next(reader)
        accidents = next(reader)

        # Convert data to int
        years = list(map(int, years))
        accidents = list(map(int, accidents))

    return years, accidents

# This method creates a bar chart of the given data, saves it and shows it as a HTML-file
def createBarChart(years, accidents, area, y_max):
    source = ColumnDataSource(data=dict(
        x=years,
        y=accidents
    ))

    # used to show exact data when user hovers over a specific point
    TOOLTIPS = [
        ("År", "$x{0}"),
        ("Uheld", "@y")
    ]

    # create a new plot with a title and axis labels
    p = figure(title="FÆRDSELSUHELD MED PERSONSKADE I " + area.upper() + " FRA ÅR 2000-2017",
               x_axis_label='Årstal', y_axis_label='Antal Uheld', y_range=[0, y_max], tooltips=TOOLTIPS)
    p.xaxis.ticker = years

    # create bar
    p.vbar(x='x', top='y', source=source, width=0.9)

    # output to static HTML file
    output_file("bar_chart_" + area.lower() + ".html", title='Uheld ' + area)

    # show the results
    show(p)

# This method reads the first two rows (years and accidents) in all files (urls given as param) and returns a dictionary containing data from the files
def getDataFromFiles(urls):
    dataFromAllFiles = {}

    for area, url in urls.items():
        filename = os.path.basename(url)

        # Reading the file
        with open(filename) as f:
            reader = csv.reader(f)

            # Read and save next to rows
            years = next(reader)
            accidents = next(reader)

            # Convert data to int
            years = list(map(int, years))
            accidents = list(map(int, accidents))
            dataFromAllFiles[area] = [years, accidents]

    return dataFromAllFiles

# This method creates a line chart with two lines, saves it and shows it as a HTML-file
def createLineChartCphAalb(data):
    TOOLTIPS = [
        ("År", "$x{0}"),
        ("Uheld", "@y")
    ]

    # create a new plot with a title and axis labels
    p = figure(title="FÆRDSELSUHELD MED PERSONSKADE I KØBENHAVN/ÅLBORG FRA ÅR 2000-2017",
               x_axis_label='Årstal', y_axis_label='Antal Uheld', tooltips=TOOLTIPS, y_range=[0, 800])
    p.xaxis.ticker = data['Ålborg'][0]

    # add a line renderer with legend and line thickness
    p.line(data['Ålborg'][0], data['Ålborg'][1], legend="Ålborg", line_width=3)
    p.circle(data['Ålborg'][0], data['Ålborg'][1],
             legend='Ålborg', fill_color="white", size=8)

    p.line(data['København'][0], data['København'][1],
           legend="København", line_width=3, color="firebrick")
    p.circle(data['København'][0], data['København'][1],
             legend='København', fill_color="white", size=8, color="navy")

    # hide line when user clicks on the name of the line
    p.legend.click_policy = "hide"

    # output to static HTML file
    output_file("line_chart_cph_aalb.html", title='Uheld KBH & AALB')

    # show the results
    show(p)


# method call with path to csv-file
years, accidents = getDataFromFile('uheld_dk.csv')
createBarChart(years, accidents, 'Danmark', 8000)

years, accidents = getDataFromFile('uheld_kbh.csv')
createBarChart(years, accidents, 'København', 800)

years, accidents = getDataFromFile('uheld_aalb.csv')
createBarChart(years, accidents, 'Ålborg', 400)

# method call with name of area and paths to csv-files
data = getDataFromFiles({'Ålborg':'uheld_aalb.csv', 'København':'uheld_kbh.csv'})
createLineChartCphAalb(data)
