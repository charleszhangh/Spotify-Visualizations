"""
Created January 6th, 2018
Program: Visualizes Spotify's Top 200 Viral Charts in listed countries.
@author: Charles Zhang
"""

from bokeh.io import curdoc, show, output_notebook
import datetime
import pandas as pd
import math
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column, widgetbox, row
from bokeh.models import CustomJS, ColumnDataSource, HoverTool, Range1d
from bokeh.models.widgets import Slider, Div, Select, RangeSlider, MultiSelect, DataTable, TableColumn, TextInput, DateRangeSlider, Paragraph, DatePicker
from bokeh.models.annotations import Title
from jinja2 import Template
from bokeh.resources import CDN
from bokeh.embed import server_document, components
from bokeh.server.server import Server
from bokeh.client import push_session
from os.path import join, dirname


#convert data from CSV
DIR_INPUT = "01_Input/"
DIR_OUTPUT = "02_Output/"
#master_data = pd.read_csv(DIR_OUTPUT + "complete_data2.csv",encoding="ISO-8859-1")
#master_data = pd.read_csv(join(dirname(__file__), 'input/top200charts_data.csv'),encoding="ISO-8859-1")

desc = Div(text=open(join(dirname(__file__), 'description.html')).read(), width=800)
abr_dict = ['ar', 'au', 'at', 'be', 'bo', 'br','bg','ca', 'cl', 'co', 'cr', 'cy','cz', 'dk', 'do', 'ec', 'ee', 'es',
                'fi','fr', 'de', 'global', 'gr', 'gt','hn', 'hk', 'hu','is', 'id', 'ie', 'it', 'jp', 'lv','lt',
                'my',  'mx',  'nl','nz', 'no', 'pa', 'py', 'pe', 'ph', 'pl','pt','sv', 'sg', 'sk', 'se',
                'ch','tw', 'tr', 'us', 'gb','uy']
country_dfs_dict = {}

def addCountryDf(abr):
    file_name = 'input/' + abr + '_data.csv'
    country_data = pd.read_csv(join(dirname(__file__), file_name), encoding="ISO-8859-1")
    country_df = pd.DataFrame(country_data)
    country_dfs_dict[abr] = country_df

#country_dfs_dict = dict(country_dfs_list)

addCountryDf('us')
master_df = country_dfs_dict.get('us')

def createPlot():
    #master_df = pd.DataFrame(master_data)

    mask = (master_df['days'] == 1)
    curr_df = master_df[mask]
    curr_df = curr_df.rename(columns = {'valence' : 'x'})

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
                <span style="font-size: 12px; color: #2F2F2F; font-weight: bold;">Song Name:</span>
                <span style="font-size: 10px; color: #2F2F2F;">@track_name</span>
            </div>
            <div>
                <span style="font-size: 12px; color: #2F2F2F; font-weight: bold;">Artist:</span>
                <span style="font-size: 10px; color: #2F2F2F;">@artist</span>
            </div>
            <div>
                <span style="font-size: 12px; color: #2F2F2F; font-weight: bold;">Position:</span>
                <span style="font-size: 10px; color: #2F2F2F;">@position</span>
            </div>
            <div>
                <span style="font-size: 12px; color: #2F2F2F; font-weight: bold;">Streams:</span>
                <span style="font-size: 10px; color: #2F2F2F;">@streams{000,000,000}</span>
            </div>
        </div>
        """)

        p = figure(plot_width=1000, plot_height=600,
                   x_axis_label="Valence", y_axis_label="Streams", tools=[hover],
                   x_range=(0.0, 1.0), y_range = (0,1500000))
        p.yaxis[0].formatter.use_scientific=False

        # Format text
        p.title.text_font_size = "36pt"
        p.title.align = "center"
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
        r = p.circle(x="x", y="streams", source=source,
                 size="size", color="color", alpha=0.7, legend="")
        glyph = r.glyph
        glyph.line_color = "white"
        glyph.line_width = .75

        return p

    #event handlers below makes changes to Slider values
    def update_data(attrname, old, new):
        days = date_slider.value
        audio_feature = af_select.value
        l_audio_feature = audio_feature.lower()

        country = country_select.value
        country_abr = country_dict.get(country)
        if (country_abr not in country_dfs_dict):
            addCountryDf(country_abr)
        #artist_text_list = text_input.value.split(',')

        str_date = convertDate(days)
        date_text.text = str_date
        master_df = country_dfs_dict.get(country_abr)
        mask = (master_df['days'] == days)
        new_df = master_df[mask]
        new_df = new_df.rename(columns={l_audio_feature: 'x'})
        new_df = new_df.reset_index(drop=True)
        streams_max = new_df.loc[1,'country_max']
        ceiling = streams_max + streams_max/10.0
        plot.xaxis.axis_label = audio_feature
        plot.y_range.end = ceiling

        #new_df.loc[new_df['artist'].isin(artist_text_list), ['color']] = '#C1107F'
        new_source = get_dataset(new_df)
        source.data.update(new_source.data)

    # creates Sliders
    date_slider = Slider(start=1, end=229, value=1, step=1, title="Days",)
    date_text = Paragraph(text="January 01, 2017", width = 200, height = 10)

    af_select = Select(title="Audio Feature:", value = "Valence", options=["Acousticness","Danceability","Energy","Valence"])

    country_select = Select(title="Country:", value = "United States", options=['Global','United States','United Kingdom','Argentina','Australia',
                                                'Austria','Belgium','Bolivia','Brazil',
                    'Canada','Chile','Colombia','Costa Rica',
                    'Czech Republic','Denmark','Dominican Republic','Ecuador','Estonia','Finland',
                    'France','Germany','Greece','Guatemala','Honduras','Hong Kong','Hungary',
                    'Iceland','Indonesia','Ireland','Italy','Japan','Latvia','Lithuania',
                    'Malaysia','Mexico','Netherlands','New Zealand',
                    'Norway','Panama','Paraguay','Peru','Philippines','Poland','Portugal',
                    'El Salvador','Singapore','Slovakia','Sweden','Switzerland','Taiwan','Turkey',
                    'Uruguay'])

    # creates text input for fund name
    text_input = TextInput(value="", title="Track Artists:")

    source = get_dataset(curr_df)

    plot = make_plot(source)

    for w in [date_slider]:
        w.on_change('value', update_data)
    #
    for w in [af_select]:
        w.on_change('value', update_data)

    for w in [country_select]:
        w.on_change('value', update_data)

    input_widgets = column(widgetbox(date_text),widgetbox(date_slider, sizing_mode = "scale_width"), widgetbox(country_select),widgetbox(af_select))
    layout = row(input_widgets,plot)
    page = column(desc, layout)
    curdoc().add_root(page)
    curdoc().title = "spotify_visualizer"
createPlot()
