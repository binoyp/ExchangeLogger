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
        k = 'OMG/ETH'  # change here for various currencies
        colno = 0 # choose column
    with open(r"D:\AdMarenDrive\Admaren Shared\Arbitrage\exceldata.bin", 'rb') as _f:
        i = 0
        
        arrdata = []
        xdata = []
        while True:
            try:
                d = pickle.load(_f)
                curarr = np.array(d['data'])
                xdata.append(d['ts'])
                # print curarr[headers[k], :]
                try:
                    arrdata.append(curarr[headers[k], :])
                except Exception,e:
                    print("Error %s with:\n\t%s"%(e,d))

            except EOFError:
                break
        final_array = np.array(arrdata)
        xdata = np.array(xdata)

        fx = xdata[np.abs(final_array[:, colno]) < 1e5]
        fy = final_array[:, colno][np.abs(final_array[:, colno]) < 1e5]
        plt.plot(fx, fy, 'r-o')

        plt.title(k + '- ' + titles[colno])
        plt.tight_layout()
        plt.grid(1)
        plt.show()
