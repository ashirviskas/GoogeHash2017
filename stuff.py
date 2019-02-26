import time
import random
import numpy as np
from random import shuffle


class Slice:
    def __init__(self, x=None, y=None, figure=None):
        self.x = x
        self.y = y
        self.figure = figure

    def __str__(self):
        return str(self.y) + " " + str(self.x) + " " + str(self.y + self.figure[0] - 1) + " " + str(
            self.x + self.figure[1] - 1)

    def Overlaps(self, x, y):
        if (y <= self.y + self.figure[0] and y >= self.y):
            if (x <= self.x + self.figure[1] and x >= self.x):
                return True
        return False

    def CanBePatchedOver(self, x, y):
        if True:
            print()


class Figure:
    def __init__(self, width=None, height=None):
        self.width = width
        self.height = height

    def __str__(self):
        return 'x: ' + str(self.width) + ' y:' + str(self.height)

    def CutFromMap(self, x, y, map_checked):
        map_checked[y : y + self.height, x : x + self.width] = 1
        # print(map_checked[y : y + self.height, x : x + self.width])
        # for yy in range(self.height):
        #     for xx in range(self.width):
        #         map_checked[y + yy][x + xx] = 1


def GenerateFigures(min_things, max_size):  # used for auto generating figures
    figures = []
    for i in range(1, (max_size // 2) + 1):
        for j in range(max_size + 1, i, -1):
            if (i * j <= max_size and i * j >= min_things * 2):
                figures.append([i, j])
                if (i != j):
                    figures.append([j, i])

    for figure in figures:
        print(figure)
    figures = np.array(figures[::-1], dtype=np.uint8)
    return figures


def CheckFigure(figure, x, y, n, map_pizza, map_checked, x_len, y_len, check_checked = True):
    if ((figure[0] + y > y_len) or (figure[1] + x > x_len)):
        return False
    if check_checked:
        if 1 in map_checked[y : y + figure[0], x: x + figure[1]]:
            return False
    # slice_p = map_pizza[y : y + figure[0], x: x + figure[1]]
    # mn = len(np.where(slice_p == 0)[0])
    mn = np.count_nonzero(map_pizza[y : y + figure[0], x: x + figure[1]] == 1)
    tn = figure[0] * figure[1] - mn
    if (mn >= n and tn >= n):
        # print("t: ", tn, "m: ", mn)
        return True
    else:
        return False


def generate_figure_possibilitymap(map_pizza, figures, n):
    figure_possibilitymap = np.zeros((map_pizza.shape[0], map_pizza.shape[1], len(figures)), dtype=np.uint8)
    figure_areas = np.array([x*y for x, y in figures])
    y_len, x_len = map_pizza.shape
    for i, row in enumerate(map_pizza):
        for j, cell in enumerate(map_pizza):
            possible = np.array([CheckFigure(figure, j, i, n, map_pizza, None, x_len, y_len, False) for figure in figures])
            possible = np.where(possible == True)
            figure_possibilitymap[i, j, possible] = figure_areas[possible]
            # print(possible)
    print(figure_areas.nbytes)
    return figure_possibilitymap


def calculate_slice_impact(x, y, figure_possibilitymap, figure):
    return np.sum(figure_possibilitymap[y:y+figure[0] - 1, x:x+figure[1] - 1])


def CutASlice(map_pizza, map_checked, y, x, n, slices, figures, x_len, y_len, figure_possibilitymap):
    figure_impacts = [calculate_slice_impact(x, y, figure_possibilitymap, figure) for figure in figures]
    new_figures = [xx for yy, xx in sorted(zip(figure_impacts, figures.tolist()), reverse=True)]
    for figure in new_figures:
        fy, fx = figure
        if CheckFigure(figure, x, y, n, map_pizza, map_checked, x_len, y_len):
            map_checked[y : y + fy, x : x + fx] = 1
            slices.append(Slice(x, y, figure))
            return fx - 1
    return 0


def CutAllPizza(map_pizza, map_checked, n, slices, figures, x_len, y_len, figure_possibilitymap):
    for j in range(len(map_checked)):
        row = map_checked[j, :]
        zeros = np.where(row == False)
        skip = 0
        for i in range(len(zeros[0])):
            if skip > 0:
                skip += -1
                continue
            skip = CutASlice(map_pizza, map_checked, j, zeros[0][i], n, slices, figures, x_len, y_len, figure_possibilitymap)


def read_file(filename):
    file_object = open(filename, "r")
    y_len, x_len, min_things, max_size = list(
        map(int, file_object.readline().split(' ')))  # initialising things from data file

    a = file_object.readlines()
    for i, line in enumerate(a):
        a[i] = list(line.replace("\n", ""))
    a = np.array(a)
    mushroom_locations = np.where(a == "M")
    map_pizza = np.zeros((y_len, x_len), dtype=np.bool)
    map_pizza[mushroom_locations] = 1
    return y_len, x_len, min_things, max_size, map_pizza


def find_slices_for_file(input_filename):
    start_time = time.time()
    y_len, x_len, min_things, max_size, map_pizza = read_file(input_filename)
    figures = GenerateFigures(min_things, max_size)  # generating figures

    map_checked = np.zeros((y_len, x_len), dtype=np.bool)#[[0 for x in range(x_len)] for y in range(y_len)]
    slices = []
    print(input_filename)
    figure_possibilitymap = generate_figure_possibilitymap(map_pizza, figures, min_things)
    CutAllPizza(map_pizza, map_checked, min_things, slices, figures, x_len, y_len, figure_possibilitymap)
    input_filename += '_results'
    file = open(input_filename, "w")
    file.write(str(len(slices)))
    for slice in slices:
        file.write('\n')
        file.write(str(slice))
    file.close()
    score = 0
    for y in map_checked:
        for x in y:
            score += x
    print(input_filename)
    print("Time: ", time.time() - start_time, " sec.")
    print("Found Sllices: ", len(slices))
    print("Total score: ", score, " out of ", y_len * x_len)
    # ChooseBestShuffle(map_pizza, map_checked, 6, slices, figures, x_len, y_len)
    print()
    """for y in range(y_len):
        for x in range(x_len):
            if (map_checked[y][x] == 0):
                PatchAHole(map_pizza, map_checked, min_things, max_size, slices, figures, x_len, y_len, x, y)"""


if __name__ == '__main__':
    find_slices_for_file("big.in")
    find_slices_for_file("medium.in")
    find_slices_for_file("example.in")
    find_slices_for_file("small.in")
