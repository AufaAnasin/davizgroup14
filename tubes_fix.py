import pandas as pd
import numpy as np
from datetime import datetime
from bokeh.io import output_file, output_notebook,curdoc
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool,CategoricalColorMapper,Div
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import Select
from bokeh.models import DateRangeSlider

#open the dataset
dataset = pd.read_csv('covid19_indonesia.csv')
dataset = dataset[['Date','Location','New Cases','New Deaths', 'New Recovered', 'New Active Cases', 'Total Cases', 'Total Deaths', 'Total Recovered', 'Total Active Cases']]

# set Index and changing the date
dataset['Date'] = pd.to_datetime(dataset.Date)
dataset.set_index('Date', inplace=True)

#Filtered the dataset
dataset = dataset[dataset.index < datetime.strptime('2021-05-01', '%Y-%M-%d')]

# Define the range date
dateRange = (dataset.index.min(), dataset.index.max())

# New Case Figure
new_cases_figure = figure(plot_width=700,plot_height=800,x_axis_label='Date',x_axis_type='datetime',
            y_axis_label='Total',title='New Cases Each Day')

new_cases_source = ColumnDataSource(data={
    'x'                 :dataset.index.unique()[0:-1], 
    'y'                 :dataset.loc[dataset.Location == 'Indonesia' , 'New Cases'],
    'total_active_case' :dataset.loc[dataset.Location == 'Indonesia', 'Total Active Cases'],
    'total_cases'       :dataset.loc[dataset.Location == 'Indonesia', 'Total Cases'],
    'total_recovered'   :dataset.loc[dataset.Location == 'Indonesia', 'Total Recovered'],
    'total_deaths'      :dataset.loc[dataset.Location == 'Indonesia', 'Total Deaths'],
})

new_cases_figure.line(x='x',y='y',source=new_cases_source,color='#FFA500')

new_cases_figure.add_tools(HoverTool(tooltips=[
    ('Value','@y'),
    ('Total Recovered', '@total_recovered'), 
    ('Total Deaths', '@total_deaths'),
    ('Active Cases','@total_active_case'),
    ('Total Cases','@total_cases'),
]))

# New Recover Figure
new_recovered_figure = figure(plot_width=700,plot_height=800,x_axis_label='Date',x_axis_type='datetime',
            y_axis_label='Total',title='New Recovered Each Day')

new_recovered_source = ColumnDataSource(data={
    'x'                 :dataset.index.unique()[0:-1], 
    'y'                 :dataset.loc[dataset.Location == 'Indonesia' , 'New Recovered'],
    'total_active_case' :dataset.loc[dataset.Location == 'Indonesia', 'Total Active Cases'],
    'total_cases'       :dataset.loc[dataset.Location == 'Indonesia', 'Total Cases'],
    'total_recovered'   :dataset.loc[dataset.Location == 'Indonesia', 'Total Recovered'],
    'total_deaths'      :dataset.loc[dataset.Location == 'Indonesia', 'Total Deaths'],
})

new_recovered_figure.line(x='x',y='y',source=new_recovered_source,color='#11ba41')
    
total_recovered_tooltips = [
    ('Value','@y'),
    ('Active Cases','@total_active_case'),
    ('Total Cases','@total_cases'),
]

new_recovered_figure.add_tools(HoverTool(tooltips=[
    ('Value','@y'),
    ('Total Recovered', '@total_recovered'), 
    ('Total Deaths', '@total_deaths'),
    ('Active Cases','@total_active_case'),
    ('Total Cases','@total_cases'),
]))

# New Deaths Figure
new_deaths_figure = figure(plot_width=700,plot_height=800,x_axis_label='Date',x_axis_type='datetime',
            y_axis_label='Total',title='New Deaths Each Day')

new_deaths_figure_source = ColumnDataSource(data={
    'x'                 :dataset.index.unique()[0:-1], 
    'y'                 :dataset.loc[dataset.Location == 'Indonesia' , 'New Deaths'],
    'total_active_case' :dataset.loc[dataset.Location == 'Indonesia', 'Total Active Cases'],
    'total_cases'       :dataset.loc[dataset.Location == 'Indonesia', 'Total Cases'],
    'total_recovered'   :dataset.loc[dataset.Location == 'Indonesia', 'Total Recovered'],
    'total_deaths'      :dataset.loc[dataset.Location == 'Indonesia', 'Total Deaths'],
})

new_deaths_figure.line(x='x',y='y',source=new_deaths_figure_source,color='#c21d30')

new_deaths_figure.add_tools(HoverTool(tooltips=[
    ('Value','@y'),
    ('Total Recovered', '@total_recovered'), 
    ('Total Deaths', '@total_deaths'),
    ('Active Cases','@total_active_case'),
    ('Total Cases','@total_cases'),
]))
group_dataset = dataset.groupby(by='Location').sum()

x = ['Total Cases', 'Total Deaths', 'Total Recovered', 'Total Active Cases']
y = group_dataset.loc['Indonesia', ['Total Cases', 'Total Deaths', 'Total Recovered', 'Total Active Cases']].to_list()

total_cases = figure(x_range=x, toolbar_location=None, tools="",title='All Time Statistics', plot_width=700, plot_height=800, y_axis_label='Total')

total_cases_source = ColumnDataSource(data={
    'x' :x, 
    'y' :y,
    'color' : ('#2311bf','#c21d30', '#11ba41', '#FFA500')
})

total_cases.vbar(x='x', top='y',source=total_cases_source,legend_field="x", color='color',width=0.9)

total_cases.add_tools(HoverTool(tooltips=[
    ('Value','@y'),
]))

# Make Dropdown
dropdown_location = Select(
    options=[str(x) for x in np.sort(dataset['Location'].unique())],
    value = 'Indonesia',
    title = 'Location'
)
dropdown_location1 = Select(
    options=[str(x) for x in np.sort(dataset['Location'].unique())],
    value = 'Indonesia',
    title = 'Location'
)
dropdown_location2 = Select(
    options=[str(x) for x in np.sort(dataset['Location'].unique())],
    value = 'Indonesia',
    title = 'Location'
)
dropdown_location3 = Select(
    options=[str(x) for x in np.sort(dataset['Location'].unique())],
    value = 'Indonesia',
    title = 'Location'
)

# Make Slider
slider = DateRangeSlider(start = dateRange[0], end = dateRange[1], value=dateRange)
slider1 = DateRangeSlider(start = dateRange[0], end = dateRange[1], value=dateRange)
slider2 = DateRangeSlider(start = dateRange[0], end = dateRange[1], value=dateRange)
slider3 = DateRangeSlider(start = dateRange[0], end = dateRange[1], value=dateRange)

# Layout
layout = row(column(dropdown_location, slider), new_cases_figure)
layout1 = row(column(dropdown_location1, slider1), new_recovered_figure)
layout2 = row(column(dropdown_location2, slider2), new_deaths_figure)
layout3 = row(column(dropdown_location3, slider3), total_cases)

# Panel
panel = Panel(child=layout, title='New Case')
panel1 = Panel(child=layout1, title='New Recovered')
panel2 = Panel(child=layout2, title='New Deaths')
panel3 = Panel(child=layout3, title='Statistics')
tabs = Tabs(tabs=[panel, panel1, panel2, panel3])

def update_new_cases(attr, old, new) : 
    [start, end] = slider.value
    start_date = datetime.fromtimestamp(start/1000.0)
    end_date = datetime.fromtimestamp(end/1000.0)

    new_location = str(dropdown_location.value)

    filter_dataset = dataset[(dataset.index >= start_date) & (dataset.index <= end_date)]
    
    new_data = {
        'x'                 :filter_dataset.index.unique(), 
        'y'                 :filter_dataset.loc[filter_dataset.Location == new_location , 'New Cases'],
        'total_active_case' :filter_dataset.loc[filter_dataset.Location == new_location, 'Total Active Cases'],
        'total_cases'       :filter_dataset.loc[filter_dataset.Location == new_location, 'Total Cases'],
        'total_recovered'   :filter_dataset.loc[filter_dataset.Location == new_location, 'Total Recovered'],
        'total_deaths'      :filter_dataset.loc[filter_dataset.Location == new_location, 'Total Deaths'],
    }
    
    new_cases_source.data = new_data

def update_new_recovered(attr, old, new) : 
    [start, end] = slider1.value
    start_date = datetime.fromtimestamp(start/1000.0)
    end_date = datetime.fromtimestamp(end/1000.0)

    new_location = str(dropdown_location1.value)

    filter_dataset = dataset[(dataset.index >= start_date) & (dataset.index <= end_date)]
    
    new_data = {
        'x'                 :filter_dataset.index.unique(), 
        'y'                 :filter_dataset.loc[filter_dataset.Location == new_location , 'New Recovered'],
        'total_active_case' :filter_dataset.loc[filter_dataset.Location == new_location, 'Total Active Cases'],
        'total_cases'       :filter_dataset.loc[filter_dataset.Location == new_location, 'Total Cases'],
        'total_recovered'   :filter_dataset.loc[filter_dataset.Location == new_location, 'Total Recovered'],
        'total_deaths'      :filter_dataset.loc[filter_dataset.Location == new_location, 'Total Deaths'],
    }
    
    new_recovered_source.data = new_data

def update_new_deaths(attr, old, new) : 
    [start, end] = slider2.value
    start_date = datetime.fromtimestamp(start/1000.0)
    end_date = datetime.fromtimestamp(end/1000.0)

    new_location = str(dropdown_location2.value)
    
    filter_dataset = dataset[(dataset.index >= start_date) & (dataset.index <= end_date)]
    
    new_data = {
        'x'                 :filter_dataset.index.unique(), 
        'y'                 :filter_dataset.loc[filter_dataset.Location == new_location , 'New Deaths'],
        'total_active_case' :filter_dataset.loc[filter_dataset.Location == new_location, 'Total Active Cases'],
        'total_cases'       :filter_dataset.loc[filter_dataset.Location == new_location, 'Total Cases'],
        'total_recovered'   :filter_dataset.loc[filter_dataset.Location == new_location, 'Total Recovered'],
        'total_deaths'      :filter_dataset.loc[filter_dataset.Location == new_location, 'Total Deaths'],
    }
    
    new_deaths_figure_source.data = new_data

def update_total_cases(attr, old, new) : 
    [start, end] = slider3.value
    start_date = datetime.fromtimestamp(start/1000.0)
    end_date = datetime.fromtimestamp(end/1000.0)

    new_location = str(dropdown_location3.value)

    filter_dataset = dataset[(dataset.index >= start_date) & (dataset.index <= end_date)]
    filter_group_dataset = filter_dataset.groupby(by='Location').sum()

    x = ['Total Cases', 'Total Deaths', 'Total Recovered', 'Total Active Cases']
    y = filter_group_dataset.loc[new_location, ['Total Cases', 'Total Deaths', 'Total Recovered', 'Total Active Cases']].to_list()

    new_data = {
        'x' :x, 
        'y' :y,
        'color' : ('#2311bf','#c21d30', '#11ba41', '#FFA500')
    }
    
    total_cases_source.data = new_data

dropdown_location.on_change('value', update_new_cases)
dropdown_location1.on_change('value', update_new_recovered)
dropdown_location2.on_change('value', update_new_deaths)
dropdown_location3.on_change('value', update_total_cases)

slider.on_change('value', update_new_cases)
slider1.on_change('value', update_new_recovered)
slider2.on_change('value', update_new_deaths)
slider3.on_change('value', update_total_cases)

curdoc().add_root(tabs)