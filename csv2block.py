#!/usr/bin/env python
# coding: utf-8

import os
import csv
from FunDefs import SetBlockRight,SetBlockLeft,GenKeyDic

inpath=''
filename='notes.csv'
namespace='gnrate'
outpath='data/'+namespace+'/functions/'

speed=4 # X T/note
BPos=['21','5','-25'] # [X,Y,Z] of actor_21



f=open(inpath+filename)
f_csv=csv.reader(f)
data={}  #data{XJ:{offset:[note]}}
i=0
for row in f_csv:
    if row[0]!='':  #new XJ
        i+=1
        data[i]={}
    offset=int(row[1])
    data[i][offset]=[]
    for note in row[2:]:
        if note!='':
            data[i][offset].append(int(note))


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
        Str_TP='execute at @s run tp ~'+str(16*speed+2)+' ~ ~'+'6'+'\n'
    else:
        Str_TP='execute at @s run tp ~-'+str(16*speed+2)+' ~ ~'+'4'+'\n'
    bfer+=Str_setXJ+Str_TP
AllXJ.write(bfer)
AllXJ.close()
