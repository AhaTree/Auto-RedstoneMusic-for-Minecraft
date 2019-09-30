#!/usr/bin/env python
# coding: utf-8

import os
import csv
from CSV_FunDef import SetBlockRight,SetBlockLeft,ReadSCV

inpath='Function Test/'
filename='XTDM_T1.csv'
namespace='gnrate'
outpath='Function Test/data/'+namespace+'/functions/'


BPos=['21','5','-25'] # [X,Y,Z] of actor_21



f=open(inpath+filename)
f_csv=csv.reader(f)
MS_Per_Offset=int(next(f_csv)[0])/4/1000
MTick_Per_Offset=round(MS_Per_Offset/50)
speed=MTick_Per_Offset # X T/note
next(f_csv)


data={}  #data={XJ:{offset:{remain:[note]}}}

data=ReadSCV(f_csv)

i=len(data)
for xj in range(1,i+1):
    XJ=data[xj]
    # print(XJ)
    bfer=''

    for offset in XJ:
        NOTES=XJ[offset]
        bfer+=( SetBlockRight(offset,NOTES,speed,BPos) if xj%2!=0 else SetBlockLeft(offset,NOTES,speed,BPos) )
    output=open(outpath+'XJ'+str(xj)+'.mcfunction','w+')
    #print(bfer)
    output.write(bfer)
    output.close()

AllXJ=open(outpath+'allxj.mcfunction','w+')
bfer=''
for k in range(1,i+1):
    Str_setXJ='execute at @s run function '+namespace+':xj'+str(k)+'\n'
    if k%2!=0: 
        Str_Clear='execute at @s run fill ~1 ~1 ~ ~'+str(16*speed)+' ~4 ~1 minecraft:air replace\n'
        Str_TP='execute at @s run tp ~'+str(16*speed+2)+' ~ ~'+'6'+'\n'
    else:
        Str_Clear='execute at @s run fill ~-1 ~1 ~ ~-'+str(16*speed)+' ~4 ~-1 minecraft:air replace\n'
        Str_TP='execute at @s run tp ~-'+str(16*speed+2)+' ~ ~'+'4'+'\n'
    bfer+=Str_Clear+Str_setXJ+Str_TP
AllXJ.write(bfer)
AllXJ.close()
print('END')