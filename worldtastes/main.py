"""
Created January 6th, 2018
Program: Visualizes various countries' music preferences for acousticness, danceability, energy, and valence.
@author: Charles Zhang
"""

from bokeh.io import curdoc
import datetime
import pandas as pd
import math
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column, widgetbox, row
from bokeh.models import CustomJS, ColumnDataSource, HoverTool, Range1d, Tool
from bokeh.models.widgets import Slider, Div, Select, RangeSlider, MultiSelect, DataTable, TableColumn, TextInput, DateRangeSlider, Paragraph, DatePicker
from bokeh.models.annotations import Title
from os.path import join, dirname
from bokeh.core.properties import field

master_data = pd.read_csv(join(dirname(__file__), '/Input/worldtastes_data.csv'))
master_df = pd.DataFrame(master_data)

mask = (master_df['days'] == 1)
curr_df = master_df[mask]
curr_df = curr_df.rename(columns = {'valence_avg_10' : 'x', 'energy_avg_10':'y'})

country_dict = {'Argentina':'ar','Australia':'au','Austria':'at','Belgium':'be','Bolivia':'bo','Brazil':'br','Bulgaria':'bg',
                'Canada':'ca','Chile':'cl','Colombia':'co','Costa Rica':'cr','Cyprus':'cy',
                'Czech Republic':'cz','Denmark':'dk','Dominican Republic':'do','Ecuador':'ec','Estonia':'ee','Finland':'fi',
                'France':'fr','Germany':'de','Global':'global','Greece':'gr','Guatemala':'gt','Honduras':'hn','Hong Kong':'hk','Hungary':'hu',
                'Iceland':'is','Indonesia':'id','Ireland':'ie','Italy':'it','Japan':'jp','Latvia':'lv','Lithuania':'lt','Luxembourg':'lu',
                'Malaysia':'my','Malta':'mt','Mexico':'mx','Monaco':'mc','Netherlands':'nl','New Zealand':'nz','Nicaragua':'ni',
                'Norway':'no','Panama':'pa','Paraguay':'py','Peru':'pe','Philippines':'ph','Poland':'pl','Portugal':'pt',
                'El Salvador':'sv','Singapore':'sg','Slovakia':'sk','Sweden':'se','Switzerland':'ch','Taiwan':'tw','Thailand':'th','Turkey':'tr','United States':'us','United Kingdom':'gb',
                'Uruguay':'uy'}
# param number of days into 2017
# returns date in this format: e.g. January 27, 2017
desc = Div(text=open(join(dirname(__file__), 'description.html')).read(), width=800)
def convertDate (days):
    convertedDate = str(datetime.datetime(2017, 1, 1) + datetime.timedelta(days - 1))[:10]
    year, month, day = convertedDate.split('-')
    months = {'01' : 'January', '02':'February', '03': 'March', '04':'April', '05':'May', '06':'June', '07':'July',
              '08':'August','09':'September','10':'October','11':'November','12':'December'}
    stringDate =  months[month] + ' ' + str(day) + ', ' + str(year)
    return stringDate


def get_dataset(src):
    master_df = src
    return ColumnDataSource(data=src)

def make_plot(source):
    """
    Plot number of streams against value of audio features
    Reverse the axis for p_values so smaller values are on the right.
    """

    hover = HoverTool(tooltips="""
    <div>
        <div>
            <span style="font-size: 12px; color: #2F2F2F; font-weight: bold;">Country:</span>
            <span style="font-size: 10px; color: #2F2F2F;">@country_name</span>
        </div>
        <div>
            <span style="font-size: 12px; color: #2F2F2F; font-weight: bold;">Avg. Top 10 Streams:</span>
            <span style="font-size: 10px; color: #2F2F2F;">@streams_avg_10{000,000,000}</span>
        </div>
        <div>
            <span style="font-size: 12px; color: #2F2F2F; font-weight: bold;">X-Value:</span>
            <span style="font-size: 10px; color: #2F2F2F;">@x</span>
        </div>
        <div>
            <span style="font-size: 12px; color: #2F2F2F; font-weight: bold;">Y-Value:</span>
            <span style="font-size: 10px; color: #2F2F2F;">@y</span>
        </div>
    </div>
    """)

    p = figure(plot_width=1000, plot_height=600,
               x_axis_label="Valence", y_axis_label="Energy", tools=[hover],
               x_range=(0.3, 0.92), y_range = (0.4,0.92))
    p.yaxis[0].formatter.use_scientific=False

    # Format text
    p.title.text_font_size = "36pt"
    p.title.align = "center"
    # p.title.text_color = "#DFDEDE"
    p.xaxis.axis_label_text_font_size = "18pt"
    p.xaxis.axis_label_text_font_style = "bold"
    p.yaxis.axis_label_text_font_size = "18pt"
    p.yaxis.axis_label_text_font_style = "bold"
    p.xaxis.major_label_text_font_size = "14pt"
    p.xaxis.major_label_text_font_style = "normal"
    p.yaxis.major_label_text_font_size = "14pt"
    p.yaxis.major_label_text_font_style = "normal"
    p.xaxis.minor_tick_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.toolbar.logo = None
    p.toolbar_location = None

    # Format dots on graph
    r = p.circle(x="x", y="y", source=source,
             size="size_10", color="color", alpha=0.7, legend=field("continent"))
    glyph = r.glyph
    glyph.line_color = "white"
    glyph.line_width = .75
    return p

#event handlers below makes changes to Slider values
def update_data(attrname, old, new):
    days = date_slider.value
    x_value = x_select.value
    y_value = y_select.value

    x_header = x_value.lower() + "_avg_10"
    y_header = y_value.lower() + "_avg_10"

    str_date = convertDate(days)
    date_text.text = str_date

    mask = (master_df['days'] == days)
    new_df = master_df[mask]
    new_df = new_df.rename(columns={x_header: 'x', y_header: 'y'})

    x_start = 0
    x_end = 0
    y_start = 0
    y_end = 0
    if (x_value == "Acousticness"):
        x_start = 0.0
        x_end = 0.52
    elif  (x_value == "Danceability"):
        x_start = .5
        x_end = 0.92
    elif (x_value == "Energy"):
        x_start = .4
        x_end = 0.92
    elif (x_value == "Valence"):
        x_start = .3
        x_end = 0.92
        
    if (y_value == "Acousticness"):
        y_start = 0.0
        y_end = 0.52
    elif  (y_value == "Danceability"):
        y_start = 0.5
        y_end = 0.92
    elif (y_value == "Energy"):
        y_start = .4
        y_end = 0.92
    elif (y_value == "Valence"):
        y_start = .3
        y_end = 0.92

    plot.x_range.start = x_start
    plot.x_range.end = x_end
    plot.y_range.start = y_start
    plot.y_range.end = y_end

    plot.xaxis.axis_label = x_value
    plot.yaxis.axis_label = y_value
    new_source = get_dataset(new_df)
    source.data.update(new_source.data)

# creates Sliders and Selectors
date_slider = Slider(start=1, end=229, value=1, step=1, title="Days")

date_text = Paragraph(text="January 01, 2017", width = 200, height = 10)

x_select = Select(title="X-Axis:", value = "Valence", options=["Acousticness","Danceability","Energy","Valence"])
y_select = Select(title="Y-Axis:", value = "Energy", options=["Acousticness","Danceability","Energy","Valence"])

country_select = Select(title="Country:", value = "Argentina", options=['Global','United States','United Kingdom','Argentina','Australia',
                                            'Austria','Belgium','Bolivia','Brazil','Bulgaria',
                'Canada','Chile','Colombia','Costa Rica','Cyprus',
                'Czech Republic','Denmark','Dominican Republic','Ecuador','Estonia','Finland',
                'France','Germany','Greece','Guatemala','Honduras','Hong Kong','Hungary',
                'Iceland','Indonesia','Ireland','Italy','Japan','Latvia','Lithuania','Luxembourg',
                'Malaysia','Malta','Mexico','Monaco','Netherlands','New Zealand','Nicaragua',
                'Norway','Panama','Paraguay','Peru','Philippines','Poland','Portugal',
                'El Salvador','Singapore','Slovakia','Sweden','Switzerland','Taiwan','Thailand','Turkey',
                'Uruguay'])


source = get_dataset(curr_df)

plot = make_plot(source)

for w in [date_slider]:
    w.on_change('value', update_data)
#
for w in [x_select]:
    w.on_change('value', update_data)

for w in [y_select]:
    w.on_change('value', update_data)

for w in [country_select]:
    w.on_change('value', update_data)


input_widgets = column(widgetbox(date_text),widgetbox(date_slider, sizing_mode = "scale_width"),
                       widgetbox(x_select),widgetbox(y_select))
layout = row(input_widgets,plot)
final_layout = column(desc, layout)

curdoc().add_root(final_layout)
curdoc().title = "worldtastes"