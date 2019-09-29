import os
import binascii as bn
from struct import unpack
f=open('XTDM.mid',mode='rb')

H_MThd=f.read(4)
if H_MThd!=b'MThd':
    raise Exception('This is not a mid file!')
H_06=unpack('>I',f.read(4))[0]
H_Track_fmt=unpack('>H',f.read(2))[0]
H_Track_num=unpack('>H',f.read(2))[0]
H_BscTick=unpack('>H',f.read(2))[0]
XJ_Per_Tick=H_BscTick*4
Tick_Speed=0
print('Track format: ',H_Track_fmt)
print('Track number: ',H_Track_num)
print('Basic tick: ',H_BscTick,' ticks per 1/4 note')

def parse_time(f):    
    length=0
    buffer=[]
    while True:
        data=unpack('B',f.read(1))[0]
        if data>127:
            buffer.insert(0,data-128)
            length+=1
        else:
            buffer.insert(0,data)
            length+=1
            break
    result=0
    for idx in range(length):
        result+=buffer[idx]*(128**idx)
    return result

def parse_event(f):
    Event_Data={'TFlag':1}
    Event_Status=f.read(1)
#    print('Event status=',Event_Status,end=' ,')
    if Event_Status==b'\xFF':
        # meta event
        Event_Data['Event_Type']='meta event'
        MetaEvent_Type=f.read(1)
#        print('meta event,type=',MetaEvent_Type,end=' ,')
        MetaEvent_Len=parse_time(f)
#        print('length=',MetaEvent_Len,end=' ,')
        if MetaEvent_Type==b'\x2F':
#            print('end of track')
            Event_Data['TFlag']=0
            return Event_Data
        elif MetaEvent_Type==b'\x51':
            Speed=0
            for num in range(MetaEvent_Len):
                Speed+=unpack('B',f.read(1))[0]
            Event_Data['Track_Speed']=Speed
            global Tick_Speed
            Tick_Speed=Speed
#            print('\n')
            print('Track speed=',Event_Data['Track_Speed'])
            return Event_Data
        else:
            MetaEvent_Data=f.read(MetaEvent_Len)
#            print('other meta event,data=',MetaEvent_Data)
            return Event_Data  
    else:
        Event_Type=unpack('B',Event_Status)[0]>>4
#        print('Event type=',Event_Type,end=' ,')
        if Event_Type==9:
            Event_Data['Event_Type']='press'
            Note=unpack('B',f.read(1))[0]
            Strength=unpack('B',f.read(1))[0]
            Event_Data['Note']=Note
#            print('press key:',Note,' ,strength=',Strength)
            return Event_Data
        elif Event_Type==8:
            Event_Data['Event_Type']='leave'
            Note=unpack('B',f.read(1))[0]
            Strength=unpack('B',f.read(1))[0]
#            print('leave key:',Note,' ,strength=',Strength)
            return Event_Data
        elif Event_Type==int('C',16):
#            print('Change instrument into ',f.read(1))
            Event_Data['Event_Type']='change instrument'
            return Event_Data
        elif Event_Type==int('D',16):
#            print('IDK:',f.read(1))
            Event_Data['Event_Type']='DX'
            return Event_Data
        else:
            Event_Data['Event_Type']='else'
            print('other event,data=',f.read(2))
            return Event_Data
    raise Exception('Parse event didn\'t end well!!')

for Track_Num in range(H_Track_num):
    print('Track',Track_Num+1)
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
    print('Track length= ',Track_Length)
    Track_Flag=1
    Key_DeltaTime=0
    Key_TotalTime=0
    while Track_Flag:
        Chunk_DeltaTime=parse_time(f)
        Key_TotalTime+=Chunk_DeltaTime
        Key_DeltaTime+=Chunk_DeltaTime
        Event_Data=parse_event(f)
#        print('Chunk delta time=',Chunk_DeltaTime,end=' ,')
#        print('Event_Data=',Event_Data)
        if Event_Data['Event_Type']=='press':
            Key_PresentXJ=(Key_TotalTime//XJ_Per_Tick)+1
            Key_Offset=(Key_TotalTime%XJ_Per_Tick)
#            print('tataltime:',Key_TotalTime,end=' ,')
            print('present XJ:',Key_PresentXJ,end=' ,')
            print('offset:',Key_Offset,end=' ,')
#            print('deltatime',Key_DeltaTime,end=' ,')
            print('Note:',Event_Data['Note'])
            Key_DeltaTime=0
        
        Track_Flag=Event_Data['TFlag']