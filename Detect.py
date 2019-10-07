import csv
import os
from CSV_FunDef import ReadSCV

data={}#data={XJ:{offset:{remain:{note}}}}
for i in range(1,4):
    f=open('LBF_T'+str(i)+'_Channel1.csv')
    f_csv=csv.reader(f)
    next(f_csv)
    for row in f_csv:
        [xj,offset,remain,note]=row
        xj=int(xj)
        offset=int(offset)
        remain=int(remain)
        note=int(note)
        if not xj in data:
            data[xj]={}
        if not offset in data[xj]:
            data[xj][offset]={}
        if not remain in data[xj][offset]:
            data[xj][offset][remain]={}
        if note in data[xj][offset][remain]:
            print(i,row)
        else:
             data[xj][offset][remain][note]=1
    f.close()
