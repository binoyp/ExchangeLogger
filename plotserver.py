import pickle
import numpy as np
import sys
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox, column, row
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider, TextInput
from bokeh.models import ColumnDataSource

from bokeh.plotting import figure, curdoc

_hdr = ['LTC/ETH',
        'OMG/ETH',
        'QTUM/ETH',
        'XRP/ETH',
        'BCH/ETH',
        'ETH/BTC',
        'LTC/BTC',
        'OMG/BTC',
        'QTUM/BTC',
        'XRP/BTC',
        'BCH/BTC'
        ]

headers = {k: v for v, k in enumerate(_hdr, 1)}

titles = {
    0: 'Conversion 1 - In coins',
    1: 'Conversion 1 - In Rupees',
    2: 'Conversion 1 - In \%',
    3: 'Conversion 2 - In coins',
    4: 'Conversion 2 - In Rupees',
    5: 'Conversion 2 - In \%'

}

source = ColumnDataSource(
    data=dict(x=[], y=[], color=[]))

curr = Select(title="Currency:", value=_hdr[0], options=_hdr)
col = Select(title="Column:", value="0", options=[
             str(v) for v in titles.keys()])
dbinput = TextInput(
    title="Path", value=r"D:\AdMarenDrive\Admaren Shared\Arbitrage\cryptodata_nikhil_30.bin")
btn = Button(label="Plot", button_type="success")

filterval = Slider(title="Filter", start=-5000, end=5000, value=-500, step=1)
p = figure(x_axis_type='datetime', plot_width=900, plot_height=700, title="")
p.circle(x="x", y="y", source=source, size=7, color="color", line_color=None)

def getData(k, colno, limitval, dbpath):
    print(colno, limitval, k)
    with open(dbpath, 'rb') as _f:
        i = 0

        arrdata = []
        xdata = []
        while True:
            try:
                d = pickle.load(_f, encoding='bytes')

                curarr = np.array(d[b'data'])
                xdata.append(d[b'ts'])
                # print(d[b'ts'])
                try:
                    arrdata.append(curarr[headers[k], :])
                except BaseException as e:
                    print("Error in loading")

            except EOFError:
                break
        final_array = np.array(arrdata)
        xdata = np.array(xdata)
        fx = xdata[final_array[:, colno] > limitval]
        fy = final_array[:, colno][final_array[:, colno] > limitval]
        return fx, fy


def update():
    dbpath = dbinput.value
    currency = curr.value
    colno = int(col.value)
    limitval = float(filterval.value)
    fx, fy = getData(currency, colno, limitval, dbpath)
    p.title.text = titles[colno]
    source.data =dict(
        x=fx,
        y=fy,
        color=np.where(fy > 0, "orange", "red"),
    )



btn.on_click(update)
col0 = column(curr, col, dbinput, btn, filterval)
r0 = row(col0, p)
curdoc().add_root(r0)
