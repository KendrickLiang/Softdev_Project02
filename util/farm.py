import random, time

from util import db as silo

def createFarm(owner, name, location, area, visible):
    time_created = time.time()
    map = createMap(area, time)
    silo.addFarm(owner, name, location, area, time, map, visible)

def createMap(area, time):
    random.seed(time);
    size = int(area**(1/2))
    print (size)
    map = []
    for x in range(size):
        row = random.choices(['Dirt', 'Rock', 'Tree'], [1, 15, 15], k=size)
        map.append(row)

    return map
