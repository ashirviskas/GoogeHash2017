import time
import random
class Slice:
    def __init__(self, x = None, y = None, figure = None):
        self.x = x
        self.y = y
        self.figure = figure
    def __str__(self):
        return str(self.y)+ " " + str(self.x) + " " + str(self.y + self.figure.height-1) + " " + str(self.x + self.figure.width-1)
    
class Figure:
    def __init__(self, width = None, height = None):
        self.width = width
        self.height = height
    def __str__(self):
        return 'x: '+str(self.width)+' y:' + str(self.height)
    def CutFromMap(self, x, y, map_checked):
        for yy in range(self.height):
            for xx in range(self.width):
                map_checked[y+yy][x+xx] = 1

def GenerateFigures(figures, number):
    figures = []
    figures.append(Figure(12,1))
    figures.append(Figure(1,12))
    figures.append(Figure(4,3))
    figures.append(Figure(3,4))
    figures.append(Figure(2,6))
    figures.append(Figure(6,2))
    figures.append(Figure(1,13))
    figures.append(Figure(13,1))
    figures.append(Figure(7,2))
    figures.append(Figure(2,7))
    return figures

def CheckFigure(figure, x, y, n, map_pizza, map_checked, y_len, x_len):
    tn = 0
    mn = 0
    if ((figure.height+y > y_len) or (figure.width+x > x_len)):
        #print (y_len, figure.width, y)
        return 0
    for yy in range(1, figure.height+1):
        for xx in range(1, figure.width+1):
            if(map_checked[y+yy-1][x+xx-1] == 1):
                return 0
            if (map_pizza[y+yy-1][x+xx-1] == 0):
                mn+=1
            else:
                tn+=1
    #print("t: ", tn, "m: ", mn)
    if (mn >=n and tn >= n):
        return 1
    else:
        return 0
    
def CutASlice(map_pizza, map_checked, x, y, n, slices, figures, y_len, x_len):
    for figure in figures:
        if CheckFigure(figure, x, y, n, map_pizza, map_checked, y_len, x_len) == 1:
            figure.CutFromMap(x, y, map_checked)
            slices.append(Slice(x, y, figure))
            return True
    return False
def CutAllPizza(map_pizza, map_checked, n, slices, figures, x_len, y_len):
    for y in range(y_len):
        for x in range(x_len):
            if(map_checked[y][x] == 0):
                CutASlice(map_pizza, map_checked, x, y, n, slices, figures, x_len, y_len)
def ChooseBestShuffle(map_pizza, map_checked, n, slices, figures, x_len, y_len):
    for i in range(10):
        map_checked = [[0 for y in range(y_len)] for x in range(x_len)]
        slices = []
        start_time = time.time()
        random.shuffle(figures)
        for figure in figures:
            print (figure)
                
        CutAllPizza(map_pizza, map_checked, 6, slices, figures, x_len, y_len)
        """for slice in slices:
            file.write('\n')
            file.write(str(slice))
            file.close()"""
        score = 0
        for y in map_checked:
            for x in y:
                score += x
        print("Time: ", time.time() - start_time)
        print ("Slices: ", len(slices))
        print ("Score: ", score)

        
start_time = time.time()        
file_object  = open("big.in", "r")
figures = []
figures = GenerateFigures(figures, 6)
x_len,y_len,min,max = list(map(int, file_object.readline().split(' ')))
a= file_object.readlines()
map_pizza = [[0 for y in range(y_len)] for x in range(x_len)]
map_checked = [[0 for y in range(y_len)] for x in range(x_len)]
slices = []
shrooms = 0
tomatoes = 0
for y in range(y_len):
    for x in range(x_len):
        if(a[y][x] == "M"):
            map_pizza[y][x] = 0
            shrooms+=1
        else:
            map_pizza[y][x] = 1
            tomatoes+=1

print(shrooms," ",tomatoes, shrooms+tomatoes)
figs = 0
#for y in range(1000):
 #   for x in range(1000): 
  #      for figure in figures:
   #         if(CheckFigure(figure,y,x, 6, map_pizza, map_checked, y_len, x_len) == 1):
    #            figs +=1
CutAllPizza(map_pizza, map_checked, 6, slices, figures, x_len, y_len)
file = open("rez.txt", "w")
file.write(str(len(slices)))
for slice in slices:
    file.write('\n')
    file.write(str(slice))
file.close()
score = 0
for y in map_checked:
    for x in y:
        score += x
                
print("Time: ", time.time() - start_time)
print ("Slices: ", len(slices))
print ("Score: ", score)
#ChooseBestShuffle(map_pizza, map_checked, 6, slices, figures, x_len, y_len)