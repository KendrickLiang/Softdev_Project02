import random, time

from util import db as silo

def createFarm(owner, name, location, area, visible):
    time_created = int(time.time())
    map = createMap(area, time)
    silo.addFarm(owner, name, location, area, time_created, map, visible)

def createMap(area, time):
    random.seed(time);
    size = int(area**(1/2))
    print (size)
    map = ''
    for x in range(size):
        row = ",".join(random.choices(['Dirt', 'Rock', 'Tree'], [1, 10, 10], k=size))
        map += row + ";"

    return map[:-1]
