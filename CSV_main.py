#!/usr/bin/env python
# coding: utf-8

import os
import csv
from CSV_FunDef import SetBlockRight,SetBlockLeft,ReadSCV

inpath='mic/'
TRACK='3'
filename='XTDM_T'+TRACK+'.csv'
namespace='track'+TRACK
outpath='data/track'+TRACK+'/functions/'


BPos=['21','5','-25'] # [X,Y,Z] of actor_21



f=open(inpath+filename)
f_csv=csv.reader(f)
speed=int(next(f_csv)[0])# X T/note

data={}  #data={XJ:{offset:{remain:[note]}}}

data=ReadSCV(f_csv)

i=100
for xj in range(1,i+1): 
    bfer='say '+'Track '+TRACK+' XJ '+str(xj)+' done\n'
    if xj in data:
        XJ=data[xj]  
        # print(XJ)
        
        for offset in XJ:  #XJ={offset:{remain:[note]}}
            NOTES=XJ[offset]  #NOTES={remain:[note]}
            bfer+=SetBlockRight(int(offset),NOTES,speed,BPos)
    output=open(outpath+'xj'+str(xj)+'.mcfunction','w+')
    #print(bfer)
    output.write(bfer)
    output.close()

AllXJ=open(outpath+'allxj.mcfunction','w+')
bfer=''
for k in range(1,i+1):
    Str_setXJ='execute at @s run function '+namespace+':xj'+str(k)+'\n'
    Str_Clear='execute at @s run fill ~1 ~1 ~ ~'+str(16*speed)+' ~4 ~1 minecraft:air replace\n'
    if k%2!=0: 
        Str_TP='execute at @s run tp ~'+str(16*speed)+' ~ ~'+''+'\n'
    else:
        Str_TP='execute at @s run tp ~-'+str(16*speed)+' ~ ~'+'3'+'\n'
    bfer+=Str_Clear+Str_setXJ+Str_TP
AllXJ.write(bfer)
AllXJ.close()
print('CSV to function: END')