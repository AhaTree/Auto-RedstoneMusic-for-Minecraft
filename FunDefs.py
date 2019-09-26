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

def SetBlock(BPOS,SPOS,Cflag):
    
    stb="setblock"
    B_Pos=" ~"+BPOS[0]+" ~"+BPOS[1]+" ~"+BPOS[2]
    B_ID=r" minecraft:"+( "chain_" if Cflag else "" )+"command_block[facing=up]"
    B_Cmd1=r"{TrackOutput:0,Command:'setblock"
    S_Pos=" "+SPOS[0]+" "+SPOS[1]+" "+SPOS[2]
    B_Cmd2=r" minecraft:redstone_block'"+( ",auto:1" if Cflag else "" )+"}"
    
    bufer=stb+B_Pos+B_ID+B_Cmd1+S_Pos+B_Cmd2+'\n'
    return bufer

def SetBlockRight(offset,NOTES,speed,BPos):
    
    bufer=''
    Kcount=len(NOTES) # key number
    pos=(offset-1)*speed+1
    Height=0
    for k in range(Kcount):

        [px,py,pz]=['','1','']
        note=NOTES[k]
        if note<0:
            pos+=1
            Height=0
        px=str(pos)
        if pos%2==0:
            pz='1'
        if Height:
            py=str(Height+1)
        
        BPOS=[str(abs(note)),BPos[1],BPos[2]]       
        bufer+=SetBlock([px,py,pz],BPOS,bool(Height))
        Height+=1
        
    return bufer

def SetBlockLeft(offset,NOTES,speed,BPos):
      
    bufer=''
    Kcount=len(NOTES) # key number
    pos=(offset-1)*speed+1
    Height=0
    for k in range(Kcount):

        [px,py,pz]=['','1','']
        note=NOTES[k]
        if note<0:
            pos+=1
            Height=0
        px=str(-pos)
        if pos%2==0:
            pz='-1'
        if Height:
            py=str(Height+1)

        
        BPOS=[str(abs(note)),BPos[1],BPos[2]]       
        bufer+=SetBlock([px,py,pz],BPOS,bool(Height))
        Height+=1

    return bufer