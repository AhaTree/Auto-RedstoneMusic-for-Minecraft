from struct import unpack

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
        print('meta event,type=',MetaEvent_Type,end=' ,')
        MetaEvent_Len=parse_time(f)
#        print('length=',MetaEvent_Len,end=' ,')

        if MetaEvent_Type==b'\x2F':
#            print('end of track')
            Event_Data['TFlag']=0
            return Event_Data

        elif MetaEvent_Type==b'\x51':
            Speed=unpack('>I',b'\x00'+f.read(3))[0]
            Event_Data['Track_Speed']=Speed
#            print('\n')
            print('Track speed=',Event_Data['Track_Speed'],'us per quarter note')
            return Event_Data

        elif MetaEvent_Type==b'\x04':
            MetaEvent_Data=f.read(MetaEvent_Len)
            print('instrument:',MetaEvent_Data)

        else:
            MetaEvent_Data=f.read(MetaEvent_Len)
#            print('other meta event,data=',MetaEvent_Data)
            return Event_Data  
    else:
        Event_Type=unpack('B',Event_Status)[0]>>4
#        print('Event type=',Event_Type,end=' ,')

        if Event_Type==9:
            Event_Channel=(unpack('B',Event_Status)[0]&15)+1
            Event_Data['Event_Type']='press'
            Event_Data['Event_Channel']=Event_Channel
            Note=unpack('B',f.read(1))[0]
            Strength=unpack('B',f.read(1))[0]
            Event_Data['Note']=Note
#            print('press key:',Note,' channel: ',Event_Channel,' ,strength=',Strength)
            return Event_Data

        elif Event_Type==8:
            Event_Data['Event_Type']='leave'
            Note=unpack('B',f.read(1))[0]
            Strength=unpack('B',f.read(1))[0]
#            print('leave key:',Note,' ,strength=',Strength)
            return Event_Data

        elif Event_Type==int('B',16): #change controller
            controller=unpack('B',f.read(1))[0]
#            print('Change controller into ',controller,end=' ,')
            controller_para=unpack('B',f.read(1))[0]
#            print('para=',controller_para)
            Event_Data['Event_Type']='change controller'
            return Event_Data

        elif Event_Type==int('C',16): #change instrument
            instrument=unpack('B',f.read(1))[0]
            print('Change instrument into ',instrument)
            Event_Data['Event_Type']='change instrument'
            return Event_Data

        elif Event_Type==int('D',16): #change pressure
#            print('IDK:',f.read(1))
            Event_Data['Event_Type']='DX'
            return Event_Data

        else:
            Event_Data['Event_Type']='else'
#            print('other event,data=',f.read(2))
            return Event_Data
    raise Exception('Parse event didn\'t end well!!')
