def ReadSCV(f):
    data={}    #data={XJ:{offset:{remain:[note]}}}
    for row in f:
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
            data[xj][offset][remain]=[]
        data[xj][offset][remain].append(note)
    return data

def GenKeyDic():
    basekey1=['1','1#','2','2#','3','4','4#','5','5#','6','6#','7']
    basekey2=['','2b','','3b','4b','3#','5b','','6b','','7b','']
    KeyDic={'-46':21,'-46#':22,'-47b':22,'-47':23,'-47#':24}
    for i in range(-3,4):
        for k in range(12):
            KeyDic[( '' if i==0 else str(i) )+basekey1[k]]=60+i*12+k
            if basekey2[k]!='':
                KeyDic[( '' if i==0 else str(i) )+basekey2[k]]=60+i*12+k
        KeyDic[( '' if i==0 else str(i) )+'7#']=60+(i+1)*12
    return KeyDic


def SetBlock(BPOS,SPOS,Cflag):  #DURM
    
    stb="setblock"
    B_Pos=" ~"+BPOS[0]+" ~"+BPOS[1]+" ~"+BPOS[2]
    B_ID=r" minecraft:"+( "chain_" if Cflag else "" )+"command_block[facing=up]"
    B_Cmd1=r"{TrackOutput:0,Command:'"
    B_Cmd2=r"'"+( ",auto:1" if Cflag else "" )+"}"

    if SPOS[0]=='59':
        S_Pos=r'summon minecraft:falling_block 60 15 7 {BlockState:{Name:"minecraft:redstone_block"},Time:1s,Motion:[-1.4,0.6,-2.0]}'
    elif SPOS[0]=='60':
        S_Pos=r'summon minecraft:falling_block 60 15 7 {BlockState:{Name:"minecraft:redstone_block"},Time:1s,Motion:[0.18,0.5,-1.9]}'
    elif SPOS[0]=='61':
        S_Pos=r'summon minecraft:falling_block 60 15 7 {BlockState:{Name:"minecraft:redstone_block"},Time:1s,Motion:[2.0,0.6,-2.0]}'
    else:
        raise Exception('not a drum track!')
    
    bufer=stb+B_Pos+B_ID+B_Cmd1+S_Pos+B_Cmd2+'\n'

    return bufer

'''
def SetBlock(BPOS,SPOS,Cflag):  #PIANO
    
    stb="setblock"
    B_Pos=" ~"+BPOS[0]+" ~"+BPOS[1]+" ~"+BPOS[2]
    B_ID=r" minecraft:"+( "chain_" if Cflag else "" )+"command_block[facing=up]"
    B_Cmd1=r"{TrackOutput:0,Command:'setblock"
    S_Pos=" "+SPOS[0]+" "+SPOS[1]+" "+SPOS[2]
    B_Cmd2=r" minecraft:redstone_block'"+( ",auto:1" if Cflag else "" )+"}"
    
    bufer=stb+B_Pos+B_ID+B_Cmd1+S_Pos+B_Cmd2+'\n'
    return bufer
'''


def SetBlock_DoubleLine(offset,OFFSET,speed,BPos):  #OFFSET={remain:[notes]}
    
    bufer=''
    for remain in OFFSET:
        
        NOTES=OFFSET[remain]
        Kcount=len(NOTES) # key number
        pos=(offset-1)*speed+remain
        Height=0

        for k in range(Kcount):

            [px,py,pz]=['','1','']
            note=NOTES[k]
            px=str(pos)
            if pos%2==0:
                pz='1'
            if Height:
                py=str(Height+1)
            
            BPOS=[str(abs(note)),BPos[1],BPos[2]]       
            bufer+=SetBlock([px,py,pz],BPOS,bool(Height))
            Height+=1
            
    return bufer

def SetBlock_SingleLine(offset,OFFSET,speed,BPos):  #OFFSET={remain:[notes]}
    
    if len(OFFSET)>1:
        raise Exception('Not suitable for single line!')
    bufer=''
    NOTES=OFFSET[1]
    Kcount=len(NOTES) # key number
    Height=0

    for k in range(Kcount):

        [px,py,pz]=['','1','']
        note=NOTES[k]
        px=str(2*offset-1)
        if Height:
            py=str(Height+1)
        
        BPOS=[str(abs(note)),BPos[1],BPos[2]]       
        bufer+=SetBlock([px,py,pz],BPOS,bool(Height))
        Height+=1
        
    return bufer

def SetBlockLeft(offset,OFFSET,speed,BPos):  #abandoned function, only when S shape
     
    bufer=''
    for remain in OFFSET:
        
        NOTES=OFFSET[remain]
        Kcount=len(NOTES) # key number
        pos=(offset-1)*speed+remain
        Height=0

        for k in range(Kcount):

            [px,py,pz]=['','1','']
            note=NOTES[k]
            px=str(-pos)
            if pos%2==0:
                pz='-1'
            if Height:
                py=str(Height+1)
            
            BPOS=[str(abs(note)),BPos[1],BPos[2]]       
            bufer+=SetBlock([px,py,pz],BPOS,bool(Height))
            Height+=1
            
    return bufer
