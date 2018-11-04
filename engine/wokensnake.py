import math
import pandas
import random
import sqlalchemy

neighbors = [[1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0], [0, 1, -1]];

class Cell:
    _x = 0
    _y = 0
    _z = 0
    _is_street = 0
    _street = {}
    _cars = []
    __cars = []

    def __init__(self, x, y, z, is_street):
        self._x = x
        self._y = y
        self._z = z
        self._is_street = is_street


def relative2absolute(cell, neighbor):
    return [cell._x + neighbor[0], cell._y + neighbor[1], cell._z + neighbor[2]];

def key_cell(cell):
    return "[{}, {}, {}]".format(cell._x, cell._y, cell._z)

def key_raw(n):
    return "[{}, {}, {}]".format(n[0], n[1], n[2])

def makestreets():
    engine = sqlalchemy.create_engine('mysql+mysqldb://frank:frank@ladikas.de/c4g')
    cells_from_db = pandas.read_sql_table('cell', engine)
    data = dict()

    # Remove existing street directions.
    for index, cell in cells_from_db.iterrows():
        cell = Cell(cell['x'], cell['y'], cell['z'], cell['is_street'])
        data[key_cell(cell)] = cell

    for cell in data.values():
        neighborsWithStreets = []
        for n in neighbors:
            if key_raw(relative2absolute(cell, n)) in data and data[key_raw(relative2absolute(cell, n))]._is_street:
                neighborsWithStreets.append(n)
        if len(neighborsWithStreets) > 1:
            for i in range(len(neighbors)):
                neigh = neighbors[(i+3)%3]
                rel = relative2absolute(cell, neigh)
                if key_raw(rel) in data  and data[key_raw(rel)]._is_street:
                    cumm = 0
                    cell._street[i] = dict()
                    for j in range(len(neighbors)):
                        neighborTo = neighbors[j] 
                        if abs(i-j) != 3 and key_raw(relative2absolute(cell, neighborTo)) in data and data[key_raw(relative2absolute(cell, neighborTo))]._is_street:
                            cumm = cumm + 1 / max(1, len(neighborsWithStreets) - 1)
                            cell._street[i][j] = cumm
        else:
            for j in range(len(neighbors)):
                neighborTo = neighbors[j] 
                if key_raw(relative2absolute(cell, neighborTo)) in data and data[key_raw(relative2absolute(cell, neighborTo))]._is_street:
                    cell._street[j] = dict()
                    cell._street[j][j] = 1

    return data

data = makestreets()

def car(cell):
    directions = list(cell._street.keys());
    direction = directions[math.floor(random.random() * len(directions))]
    cell._cars.append(direction)

def loop(data):
    for cell in data.values():
        neighborsWithStreets = []
        for n in neighbors:
            if key_raw(relative2absolute(cell, n)) in data and data[key_raw(relative2absolute(cell, n))]._is_street:
                neighborsWithStreets.append(n)
        if len(neighborsWithStreets) == 1:
            r = random.random();
            if r <= 0.2:
                car(cell);

    for cell in data.values():
        cell.__cars=[]

    for cell in data.values():
        if len(cell._cars)> 0:
            for direct in cell._cars:
                # End of street reached.
                if not direct in cell._street:
                    continue

                directions = list(cell._street[direct].keys())
                direction = directions[math.floor(random.random() * len(directions))]
                r = random.random()
                for d in directions:
                    if r <= cell._street[direct][d]:
                        direction = d
                        break
                
                key = key_raw(relative2absolute(cell, neighbors[direction]))
                if not key in data:
                    continue

                newcell = data[key]
                newcell.__cars.append(direction)

    for cell in data.values():
        cell._cars = []
        for d in cell.__cars:
            cell._cars = []

for t in range(100):
    loop(data)
