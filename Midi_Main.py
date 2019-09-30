import os
import csv
from struct import unpack
from Midi_FunDef import parse_event,parse_time

inpath='MidTest/'
outpath='Function Test/'
filename='XTDM_T1'
f=open(inpath+filename+'.mid',mode='rb')
result=open(outpath+filename+'.csv','w+',newline='')
Result=csv.writer(result)
Result.writerow(['','Speed','############','*'])

H_MThd=f.read(4)
if H_MThd!=b'MThd':
    raise Exception('This is not a mid file!')
H_06=unpack('>I',f.read(4))[0]
H_Track_fmt=unpack('>H',f.read(2))[0]
H_Track_num=unpack('>H',f.read(2))[0]
H_BscTick=unpack('>H',f.read(2))[0]
Tick_Per_XJ=H_BscTick*4
Tick_Per_Note=H_BscTick/4
Tick_Speed=0
print('Track format: ',H_Track_fmt)
print('Track number: ',H_Track_num)
print('Basic tick: ',H_BscTick,' ticks per 1/4 note')

for Track_Num in range(H_Track_num):
#    print('Track',Track_Num+1)
    Track_Head = f.read(4)
    if Track_Head != b'MTrk':
        if Track_Head != b'':
            print('Track head is:')
            print(Track_Head)
            raise Exception('not a midi file!')
        else:
            print('No more tracks')
            break
    Track_Length=unpack('>I',f.read(4))[0]
#    print('Track length= ',Track_Length)
    Track_Flag=1
    Key_DeltaTime=0
    Key_TotalTime=0
    while Track_Flag:
        Chunk_DeltaTime=parse_time(f)
        Key_TotalTime+=Chunk_DeltaTime
        Key_DeltaTime+=Chunk_DeltaTime
        Event_Data=parse_event(f)
        if 'Track_Speed' in Event_Data:
            Tick_Speed=Event_Data['Track_Speed']
        if Event_Data['Event_Type']=='press':
            Key_PresentXJ=(Key_TotalTime//Tick_Per_XJ)+1
            Key_Offset_Tick=(Key_TotalTime%Tick_Per_XJ)
            Key_Offset_Note=int(Key_Offset_Tick//Tick_Per_Note)+1
            Key_Offset_Remain=int(Key_Offset_Tick%Tick_Per_Note)
            Note=Event_Data['Note']
            #print('present XJ:',Key_PresentXJ,end=' ,')
            #print('offset:',Key_Offset_Note,end=' ,')
            #print('remain: ',Key_Offset_Remain,end=' ,')
            #print('Note:',Note)
            Note_Present=[Key_PresentXJ,Key_Offset_Note,Key_Offset_Remain,Note]
            Result.writerow(Note_Present)
            Key_DeltaTime=0
        Track_Flag=Event_Data['TFlag']
    print('Track',Track_Num+1,' done')
result.seek(0)
Result.writerow([str(Tick_Speed)])
result.close()

print('END')