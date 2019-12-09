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
        'state': current.state_abbr,
        'elec_score': current.elec_score,
        'gas_score': current.gas_score,
        'num_establishments': current.num_establishments,
        'elec_1kdollars': current.elec_1kdollars,
        'elec_mwh': current.elec_mwh,
        'gas_1kdollars': current.gas_1kdollars,
        'gas_mcf': current.gas_mcf,
        'elec_lb_ghg': current.elec_lb_ghg,
        'gas_lb_ghg': current.gas_lb_ghg,
        'elec_bin_group': current.elec_bin_group,
        'gas_bin_group': current.gas_bin_group,
    }

def exportIndustrialCSV(df, source):
    button = Button(label="Export Industrial Data CSV: Download", button_type="success")
    button.callback = CustomJS(args=dict(source=source), code=open(join(dirname(__file__), "download_industrial.js")).read())

    columns=[
        TableColumn(field='city', title='City'),
        TableColumn(field='state', title='State'),
        TableColumn(field='elec_score', title='Electric Score', formatter=NumberFormatter(format="0,0.0000")),
        TableColumn(field='gas_score', title='Natural-Gas Score', formatter=NumberFormatter(format="0,0.0000")),
        TableColumn(field='num_establishments', title='Number of Establishments'),
        TableColumn(field='elec_1kdollars', title='Electric 1k Dollars'),
        TableColumn(field='elec_mwh', title='Electric Megawatt Hours'),
        TableColumn(field='gas_1kdollars', title='Natural Gas 1k Dollars'),
        TableColumn(field='gas_mcf', title='Natural Gas MCF'),
        TableColumn(field='elec_lb_ghg', title='Electric lb GHG'),
        TableColumn(field='gas_lb_ghg', title='Natural Gas lb GHG'),
        TableColumn(field='elec_bin_group', title='Electric Usage'),
        TableColumn(field='gas_bin_group', title='Natural Gas Usage'),
    ]
    data_table = DataTable(source=source, columns=columns, fit_columns=False, width=1200, height=800)
    controls = widgetbox(button, data_table)
    layout = row(controls)
    update(df, source)
    output_file('export_industrial_csv.html', title='Export CSV')
    show(layout)

if __name__ == "__main__":
    df = pd.read_csv(join(dirname(__file__), 'cleaned_energy_industrial.csv'))
    source = ColumnDataSource(data=dict())
    exportIndustrialCSV(df, source)