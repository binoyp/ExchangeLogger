import pickle, sys
import matplotlib.pyplot as plt
import numpy as np
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

if __name__ == "__main__":

    if len(sys.argv) == 3:
        k = sys.argv[1]
        colno = int(sys.argv[2])

    else:
        k = 'BCH/BTC'
        colno = 1
    with open('cryptodata.bin', 'rb') as _f:
        i = 0
        
        arrdata = []
        xdata = []
        while True:
            try:
                d = pickle.load(_f)
                curarr = np.array(d['data'])
                xdata.append(d['ts'])
                # print curarr[headers[k], :]
                arrdata.append(curarr[headers[k], :])

            except EOFError:
                break
        final_array = np.array(arrdata)
        xdata = np.array(xdata)

        fx = xdata[np.abs(final_array[:, colno]) < 1e6]
        fy = final_array[:, colno][np.abs(final_array[:, colno]) < 1e6]
        plt.plot(fx, fy, 'r-o')

        plt.title(k + '- ' + titles[colno])
        plt.tight_layout()
        plt.grid(1)
        plt.show()
