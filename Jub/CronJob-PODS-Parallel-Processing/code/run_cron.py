import pathlib
import os
import re
import time
from datetime import datetime, date, timedelta

def run():
    #today = date.today().strftime('%d%m%Y')
    today = "05052021"
    print(today)
    getfiles = list(pathlib.Path(os.getcwd()+"/data/").glob('*_'+today+'.csv'))
    if len(getfiles) > 0:
        for file in getfiles:
            print(len(getfiles))
            time.sleep(30)
            fname = os.path.basename(file)
            fname1 = os.path.splitext(fname)[0]
            fres = re.split('_', fname1)
            print(fres)
            rename_csv(os.getcwd()+'/data/', fres[0]+'_'+fres[1], fres[0]+'_'+fres[1],'prog')
    else:
        print("No more files to read")        
        

def rename_csv(file_path,recent_file_name,actual_file_name,file_sufix):
        os.rename(file_path + recent_file_name +'.csv',file_path + actual_file_name + '_' + file_sufix + '.csv')        
        
if __name__ == "__main__":
    run()            