import os

outpath='../data/gnrate/functions/'


volum1='0.4'
volum2='0.5'
def GenCommand():
    data=r'fill 21 ~ ~ 108 ~ ~ minecraft:air'+'\n'
    for i in range(21,109):
        si=str(i)
        if i<60:
            data=data+r'setblock '+si+r" ~ ~ minecraft:command_block[facing=up]{Command:'execute at @a run playsound minecraft:aha.piano"+si+r" record @a ~ ~ ~ "+volum1+r"'} "+"\n"
        else:
            data=data+r'setblock '+si+r" ~ ~ minecraft:command_block[facing=up]{Command:'execute at @a run playsound minecraft:aha.piano"+si+r" record @a ~ ~ ~ "+volum2+r"'} "+"\n"
    return data

f=open(outpath+'setnotes_lit.mcfunction',mode='w+')
data=GenCommand()
f.write(data)
f.close()
print('output done')