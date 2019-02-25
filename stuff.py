import time
import random
import numpy as np


class Slice:
    def __init__(self, x=None, y=None, figure=None):
        self.x = x
        self.y = y
        self.figure = figure

    def __str__(self):
        return str(self.y) + " " + str(self.x) + " " + str(self.y + self.figure.height - 1) + " " + str(
            self.x + self.figure.width - 1)

    def Overlaps(self, x, y):
        if (y <= self.y + self.figure.height and y >= self.y):
            if (x <= self.x + self.figure.width and x >= self.x):
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
                figures.append(Figure(i, j))
                if (i != j):
                    figures.append(Figure(j, i))

    for figure in figures:
        print(figure)
    return figures


def CheckFigure(figure, x, y, n, map_pizza, map_checked, x_len, y_len):
    if ((figure.height + y > y_len) or (figure.width + x > x_len)):
        # print (y_len, figure.width, y)
        return 0
    slice_c = map_checked[y : y + figure.height, x : x + figure.width]
    if 1 in slice_c:
        return 0
    slice_p = map_pizza[y : y + figure.height, x : x + figure.width]
    mn = len(np.where(slice_p == 0)[0])
    tn = slice_p.size - mn
    # for yy in range(1, figure.height + 1):
    #     for xx in range(1, figure.width + 1):
    #         if (map_checked[y + yy - 1][x + xx - 1] == 1):
    #             return 0
    #         if (map_pizza[y + yy - 1][x + xx - 1] == 0):
    #             mn += 1
    #         else:
    #             tn += 1
    if (mn >= n and tn >= n):
        # print("t: ", tn, "m: ", mn)
        return 1
    else:
        return 0


# def CheckFigureMin(figure, x, y, n, map_pizza, map_checked, x_len, y_len, xn, yn):
#     tn = 0
#     mn = 0
#     if ((figure.height + y > y_len) or (figure.width + x > x_len)):
#         # print (y_len, figure.width, y)
#         return 0
#     for yy in range(1, figure.height + 1):
#         for xx in range(1, figure.width + 1):
#             if (map_checked[yn, xn] != 1):
#                 if (map_checked[y + yy - 1][x + xx - 1] == 0):
#                     return 0
#             if (map_pizza[y + yy - 1][x + xx - 1] == 0):
#                 mn += 1
#             else:
#                 tn += 1
#     # print("t: ", tn, "m: ", mn)
#     if (mn >= n and tn >= n):
#         return 1
#     else:
#         return 0


def CutASlice(map_pizza, map_checked, x, y, n, slices, figures, x_len, y_len):
    for figure in figures:
        if CheckFigure(figure, x, y, n, map_pizza, map_checked, x_len, y_len) == 1:
            figure.CutFromMap(x, y, map_checked)
            slices.append(Slice(x, y, figure))
            return True
    return False


def CutAllPizza(map_pizza, map_checked, n, slices, figures, x_len, y_len):
    zeros = np.where(map_checked == 0)
    for i in range(len(zeros[0])):
        CutASlice(map_pizza, map_checked, zeros[1][i], zeros[0][i], n, slices, figures, x_len, y_len)


def ChooseBestShuffle(map_pizza, map_checked, n, slices, figures, x_len, y_len):
    for i in range(10):
        map_checked = [[0 for y in range(y_len)] for x in range(x_len)]
        slices = []
        start_time = time.time()
        random.shuffle(figures)
        for figure in figures:
            print (figure)

        CutAllPizza(map_pizza, map_checked, 6, slices, figures, x_len, y_len)
        # for slice in slices:
        #     file.write('\n')
        #     file.write(str(slice))
        #     file.close()
        score = 0
        for y in map_checked:
            for x in y:
                score += x
        print("Time: ", time.time() - start_time)
        print ("Slices: ", len(slices))
        print ("Score: ", score)

"""def PatchAHole(map_pizza, map_checked, min_things, max_size, slices, figures, x_len, y_len, x, y):
    for figure in figures:
            for slice in slices:
                if slice.Overlaps(x,y):
                    if (CheckFigureMin(figure, slice.x, slice.y, min_things, map_pizza, map_checked, x_len, y_len, x, y) == 1):

                        #print("Patchey: ", y, " ", x)
                        #print()

"""


def FindSlicesForFile(input_filename):
    start_time = time.time()
    file_object = open(input_filename, "r")
    y_len, x_len, min_things, max_size = list(
        map(int, file_object.readline().split(' ')))  # initialising things from data file
    figures = GenerateFigures(min_things, max_size)  # generating figures
    a = file_object.readlines()
    for i, line in enumerate(a):
        a[i] = list(line.replace("\n", ""))
    a = np.array(a)
    map_pizza = np.zeros((y_len, x_len), dtype=np.bool)
    map_checked = np.zeros((y_len, x_len), dtype=np.bool)#[[0 for x in range(x_len)] for y in range(y_len)]
    slices = []
    mushroom_locations = np.where(a == "M")
    map_pizza[mushroom_locations] = 1
    shrooms = len(mushroom_locations[0])
    tomatoes = np.size(a) - shrooms
    print(input_filename)
    print("Mushrooms: ", shrooms, " Tomatoes: ", tomatoes, " All: ", shrooms + tomatoes)
    figs = 0
    CutAllPizza(map_pizza, map_checked, min_things, slices, figures, x_len, y_len)
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


FindSlicesForFile("big.in")
# FindSlicesForFile("medium.in")
# FindSlicesForFile("example.in")
# FindSlicesForFile("small.in")
