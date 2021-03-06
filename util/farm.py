import random, time

from util import db as silo

def createFarm(owner, name, location, area, visible):
    time_created = int(time.time())
    map = createMap(area, time)
    silo.addFarm(owner, name, location, area, time_created, map, visible)

def createMap(area, time):
    random.seed(time);
    size = int(area**(1/2))
    #print (size)
    map = ''
    for x in range(size):
        row = ",".join(random.choices(['Dirt', 'Rock', 'Tree'], [2, 5, 5], k=size))
        map += row + ";"

    return map[:-1]

def mapArray(strMap):
    map = strMap.split(";")
    for num in range(len(map)):
        map[num] = map[num].split(",")
    return map

def mapStr(arrMap):
    map = ''
    for row in arrMap:
        map += ','.join(row) + ";"
    return map[:-1]
