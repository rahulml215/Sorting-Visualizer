import pygame as pg
import random

pg.init()

width, height = 800, 700
font_sv = pg.font.SysFont('impact', 25)
font_nm = pg.font.SysFont('gabriola', 60)
font_stn = pg.font.SysFont('bahnschrift', 23)

win = pg.display.set_mode((width, height))
pg.display.set_caption('Sorting Visualizer')

black = (0, 0, 0)
blue = (39, 40, 64)
light_blue = (60, 220, 206)
green = (8, 253, 7)
red = (255, 0, 0)
orange = (250, 104, 2)
l_blue = (20, 22, 250)
white = (255, 255, 255)

bar_num = 170
border = 25
sorted = False
space = (width - 25 - border) / bar_num
bar_width, bar_height = space - 1.2, 2.87

count = 0
fps = 85
run = True
down = 25

name = font_nm.render('By Rahul', 1, (88, 66, 248))
project = font_sv.render('SORTING VISUALIZER', 1, (246, 241, 46))
sorting = [font_stn.render('1. Selection Sort', 1, (101, 163, 147)),
           font_stn.render('2. Bubble Sort', 1, (232, 131, 41)),
           font_stn.render('3. Merge Sort', 1, (50, 180, 62)),
           font_stn.render('4. Quick Sort', 1, (181, 47, 229)),
           font_stn.render('5. Heap Sort', 1, (166, 150, 110)),
           font_stn.render('6. Insertion Sort', 1, (211, 15, 57))]
reset = font_stn.render('0. Reset', 1, white)


class Bar:
    def __init__(self, x, y, width, height, value):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = light_blue
        self.value = value

    def reset(self, num):
        self.x = border + num * space
        return self

    def draw(self, win):
        pg.draw.rect(win, self.color,
                     (self.x, self.y, self.width, self.height))

    def check(self):
        self.color = red

    def done(self):
        self.color = green

    def match(self):
        self.color = l_blue

    def back(self):
        self.color = light_blue


sort = [x for x in range(1, bar_num + 2)]
random.shuffle(sort)
bar = [Bar((border + i * space), (height - down - (bar_height * sort[i])),
           bar_width, bar_height * sort[i], sort[i]) for i in range(bar_num)]


def main(win):
    clock = pg.time.Clock()

    global run
    global bar
    global sorted
    while run:

        clock.tick(fps)
        draw(win, bar)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break

        keys = pg.key.get_pressed()

        if keys[pg.K_0]:
            random.shuffle(sort)
            bar = [Bar((border + i * space), (height - down - (bar_height * sort[i])), 
                       bar_width, bar_height * sort[i],sort[i]) for i in range(bar_num)]
            sorted = False
        if keys[pg.K_1]:
            check()
            selection(bar, win)
        if keys[pg.K_2]:
            check()
            bubble(bar, win)
        if keys[pg.K_3]:
            check()
            merge_sort(bar, 0, len(bar) - 1, win)
        if keys[pg.K_4]:
            check()
            quick_sort(bar, 0, len(bar) - 1, win)
        if keys[pg.K_5]:
            check()
            heap_sort(bar, win)
        if keys[pg.K_6]:
            check()
            insertion(bar, win)

    pg.quit()


def check():
    global sorted
    global bar
    if sorted:
        sorted = False
        random.shuffle(sort)
        bar = [Bar((border + i * space), (height - down - (bar_height * sort[i])),
                   bar_width, bar_height * sort[i], sort[i]) for i in range(bar_num)]

# drawing function for the screen

def draw(win, bar):
    # set global variables for all elements before drawing
    global reset
    global name
    global sorting
    global project

    win.fill(blue)

    pg.draw.rect(win, black, (0, 0, 800, 180))

    win.blit(project, (30, 20))

    win.blit(name, (40, 90))

    pg.draw.rect(win, blue, (250, 15, 5, 150))

    for i in range(len(sorting)):
        win.blit(sorting[i], (270, 13 + (25 * i)))
    win.blit(reset, (460, 13))

    for i in bar:
        i.draw(win)

    pg.display.update()


def selection(bar, win):
    # Set global variables to control
    # the quitting function and shuffle function for the list
    # before running
    global sorted
    sorted = True
    global run

    for i in range(len(bar)):
        if not run:
            break
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
        min = i
        for u in range(i + 1, len(bar)):

            bar[min].match()
            bar[u].check()
            draw(win, bar)
            bar[u].back()

            if bar[u].y > bar[min].y:
                bar[min].back()
                min = u

        bar[len(bar) - 1].back()
        temp = bar[min]
        bar[min] = bar[i]
        bar[i] = temp
        bar[min].reset(min)
        bar[i].reset(i).done()


def bubble(bar, win):
    # Set global variables to control
    # the quitting function and shuffle function for the list
    # before running
    global run
    global sorted
    sorted = True

    for i in range(len(bar)):
        if not run:
            break
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break

        for j in range(len(bar) - 1 - i):

            bar[j].check()
            draw(win, bar)
            bar[j].back()

            if bar[j].value > bar[j + 1].value:
                temp = bar[j]
                bar[j] = bar[j + 1]
                bar[j + 1] = temp
                bar[j].reset(j)
                bar[j + 1].reset(j + 1)

        bar[len(bar) - 1 - i].done()


def merge(bar, left, mid, right, win):
    temp = []
    i = left
    j = mid + 1

    while i <= mid and j <= right:
        bar[i].check()
        bar[j].check()
        draw(win, bar)
        bar[i].back()
        bar[j].back()
        if bar[i].value < bar[j].value:
            temp.append(bar[i])
            i += 1
        else:
            temp.append(bar[j])
            j += 1
    while i <= mid:
        bar[i].check()
        draw(win, bar)
        bar[i].back()
        temp.append(bar[i])
        i += 1
    while j <= right:
        bar[j].check()
        draw(win, bar)
        bar[j].back()
        temp.append(bar[j])
        j += 1
    k = 0
    for i in range(left, right + 1):
        bar[i] = temp[k]
        bar[i].reset(i)
        bar[i].check()
        draw(win, bar)
        if right - left == len(bar) - 1:
            bar[i].done()
        else:
            bar[i].back()
        k += 1


def merge_sort(bar, left, right, win):
    # Set global variables to control
    # the quitting function and shuffle function for the list
    # before running
    global sorted
    sorted = True
    global run

    mid = left + (right - left) // 2
    if left < right:
        merge_sort(bar, left, mid, win)
        merge_sort(bar, mid + 1, right, win)
        if not run:
            return
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
        merge(bar, left, mid, right, win)


def quick_sort(bar, low, high, win):
    # Set global variables to control
    # the quitting function and shuffle function for the list
    # before running
    global run
    global sorted
    sorted = True

    if len(bar) == 1:
        return bar
    if low < high:

        pi = partition(bar, low, high, win)

        draw(win, bar)

        quick_sort(bar, low, pi - 1, win)

        if not run:
            return
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break

        for i in range(pi + 1):
            bar[i].done()

        quick_sort(bar, pi, high, win)


def partition(bar, low, high, win):
    i = low
    pivot = bar[high]
    pivot.color = orange
    for j in range(low, high):

        bar[j].check()
        bar[i].check()
        draw(win, bar)
        bar[j].back()
        bar[i].back()
        if bar[j].value < pivot.value:

            bar[i], bar[j] = bar[j], bar[i]
            bar[i].reset(i)
            bar[j].reset(j)
            i += 1

    bar[i], bar[high] = bar[high], bar[i]
    bar[i].reset(i)
    pivot.back()
    draw(win, bar)
    bar[high].reset(high)
    return i


def insertion(bar, win):
    # Set global variables to control
    # the quitting function and shuffle function for the list
    # before running
    global run
    global sorted
    sorted = True

    for i in range(1, len(bar)):
        bar[i].check()
        draw(win, bar)
        bar[i].back()
        j = i
        while j > 0 and bar[j].value < bar[j - 1].value:
            if not run:
                return
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    break
            bar[i].check()
            draw(win, bar)
            bar[i].back()
            bar[j], bar[j - 1] = bar[j - 1], bar[j]
            bar[j].reset(j)
            bar[j - 1].reset(j - 1)
            j -= 1
    for i in range(len(bar)):
        bar[i].done()
        pg.time.delay(1)
        draw(win, bar)


def heap_sort(bar, win):
    # Set global variables to control
    # the quitting function and shuffle function for the list
    # before running
    global run
    global sorted
    sorted = True
    n = len(bar)
    for i in range(n // 2 - 1, -1, -1):
        heapify(bar, n, i, win)

    for i in range(n - 1, 0, -1):
        bar[i], bar[0] = bar[0], bar[i]
        bar[i].reset(i)
        bar[0].reset(0)
        bar[i].done()
        draw(win, bar)
        heapify(bar, i, 0, win)


def heapify(bar, n, i, win):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and bar[left].value > bar[largest].value:
        largest = left
    if right < n and bar[right].value > bar[largest].value:
        largest = right
    if largest != i:
        bar[i].check()
        bar[largest].check()
        draw(win, bar)

        bar[i], bar[largest] = bar[largest], bar[i]

        bar[i].reset(i)
        bar[largest].reset(largest)

        bar[i].back()
        bar[largest].back()
        draw(win, bar)

        heapify(bar, n, largest, win)


if __name__ == "__main__":
    main(win)