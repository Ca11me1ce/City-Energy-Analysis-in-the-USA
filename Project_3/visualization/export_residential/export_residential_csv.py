from os.path import dirname, join

import pandas as pd

from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import RangeSlider, Button, DataTable, TableColumn, NumberFormatter
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show, ColumnDataSource

def update(df, source):
    current=df.dropna()
    #source.data is used for downloading with js file
    source.data = {
        'city': current.city,
        'state': current.state_id,
        'housing_units': current.housing_units,
        'total_pop': current.total_pop,
        'elec_1kdollars': current.elec_1kdollars,
        'elec_mwh': current.elec_mwh,
        'gas_1kdollars': current.gas_1kdollars,
        'gas_mcf': current.gas_mcf,
        'elec_lb_ghg': current.elec_lb_ghg,
        'gas_lb_ghg': current.gas_lb_ghg,
    }

def exportResidentialCSV(df, source):
    button = Button(label="Export Residential Data CSV: Download", button_type="success")
    button.callback = CustomJS(args=dict(source=source), code=open(join(dirname(__file__), "download_residential.js")).read())

    columns=[
        TableColumn(field='city', title='City'),
        TableColumn(field='state', title='State'),
        TableColumn(field='housing_units', title='Housing Units'),
        TableColumn(field='total_pop', title='Total Population'),
        TableColumn(field='elec_1kdollars', title='Electric 1k Dollars'),
        TableColumn(field='elec_mwh', title='Electric Megawatt Hours'),
        TableColumn(field='gas_1kdollars', title='Natural Gas 1k Dollars'),
        TableColumn(field='gas_mcf', title='Natural Gas MCF'),
        TableColumn(field='elec_lb_ghg', title='Electric lb GHG'),
        TableColumn(field='gas_lb_ghg', title='Natural Gas lb GHG'),
    ]
    data_table = DataTable(source=source, columns=columns, fit_columns=False, width=1200, height=800)
    controls = widgetbox(button, data_table)
    layout = row(controls)
    update(df, source)
    output_file('export_residential_csv.html', title='Export CSV')
    show(layout)

if __name__ == "__main__":
    df = pd.read_csv(join(dirname(__file__), 'cleaned_residential.csv'))
    source = ColumnDataSource(data=dict())
    exportResidentialCSV(df, source)