import math
import pandas
import random
import sqlalchemy

neighbors = [[1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0], [0, 1, -1]];

class Cell:

    def __init__(self, x, y, z, is_street):
        self._x = x
        self._y = y
        self._z = z
        self._is_street = is_street
        self._street = {}
        self._cars = []
        self.__cars = []
        self._light = 0


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

def dist(cell1, cell2):
    return max(
        abs(cell1._x-cell2._x),
        abs(cell1._y-cell2._y),
        abs(cell1._z-cell2._z)
    )

def noise(data):
    cells = data.values();
    cars = []
    for cell in cells:
        if len(cell._cars) > 0:
            cars.append(cell)

    for cell in cells:
        sum = 0;
        for car in cars:
            d = dist(cell, car);
            if d == 0:
                l = 90
            else:
                l = 90 - 16.61 * math.log10(6*d/1);
            sum = sum + math.pow(10, 0.1 * l);

        if sum > 0:
            cell._noise = (10 * math.log10(sum))/100;
        else:
            cell._noise = 0

def light(data, t):
    cells = data.values();
    if 60 <= t and 200 > t:
        for cell in cells:
            cell._light = 0
        return

    streets = []
    for cell in cells:
        if cell._is_street:
            streets.append(cell)
            cell._light = 1

    for cell in streets:
        for neigh in neighbors:
            if key_raw(relative2absolute(cell, neigh)) in data and data[key_raw(relative2absolute(cell, neigh))]._is_street:
                data[key_raw(relative2absolute(cell, neigh))]._light = max(0.5, data[key_raw(relative2absolute(cell, neigh))]._light)

def loop(data, t):
    for cell in data.values():
        neighborsWithStreets = []
        for n in neighbors:
            if key_raw(relative2absolute(cell, n)) in data and data[key_raw(relative2absolute(cell, n))]._is_street:
                neighborsWithStreets.append(n)
        if len(neighborsWithStreets) == 1:
            r = random.random();
            if t <= 60:
                if r <= t/60:
                    car(cell);
            elif t >= 200:
                if r <= (240-t)/40:
                    car(cell);
            else:
                car(cell)


    maxi = 0
    for cell in data.values():
        maxi = max(maxi, len(cell._cars))

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

                if cell._x == 9 and cell._y == 6 and clee._z == -15:
                    direction = 0
                
                key = key_raw(relative2absolute(cell, neighbors[direction]))
                if not key in data:
                    continue

                newcell = data[key]
                newcell.__cars.append(direction)

    for cell in data.values():
        cell._cars = []
        for c in cell.__cars:
            cell._cars.append(c)

    noise(data)
    light(data, t)

df = []
for t in range(240):
    loop(data, t)
    for cell in data.values():
        df.append({'cellid': 0, 'stop': 1, 'x': cell._x, 'y': cell._y, 'z': cell._z, 'timestep': t, 'light': cell._light, 'noise': cell._noise, 'number_of_cars': len(cell._cars)})

engine = sqlalchemy.create_engine('mysql+mysqldb://frank:frank@ladikas.de/c4g')
pandas.DataFrame(df).to_sql('celldata', engine, if_exists='append', index=False)
