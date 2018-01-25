import pickle
from FPaths import EXCEL_PATH, DBPATH
import xlwings as xw
import datetime
import time

if __name__ == "__main__":
    wb = xw.Book(EXCEL_PATH)
    sht = wb.sheets['Overview']
    while True:
        try: 
            with open(DBPATH, 'ab') as _f:
                while True:
                    tries = 0
                    try:
                        tab = sht.range('B14:G24').value
                        break
                    except Exception, e:
                        print("Error in reading overview table : %s"%e)
                        
                        if tries == 4:
                            break
                        tries += 1
                outdic ={
                    'ts' : datetime.datetime.now(),
                    'data': tab
                } 
                pickle.dump(outdic, _f)
                print "Data save at %s"%datetime.datetime.now()
        except Exception, e:
            print "Error in dumping : %s"%e
        finally:
            time.sleep(180)

