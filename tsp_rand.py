# coding: utf-8

import random
import copy
import sys
import tkinter
import math

"""
TSPを乱数で解いてみる
"""

# Parameter
SCREEN_WIDTH = 360
SCREEN_HEIGHT = 360

POINTS_SIZE = 11
LOOP = 10000

def generate_points(point_size):
    points = []
    for i in range(point_size):
        x = random.random()
        y = random.random()
        points.append([x, y])

    return points

# 経路の距離を計算する
def calc_distance(points, route):
    total_distance = 0

    for i in range(len(route)):
        if i == len(route)-1:
            p1 = points[route[i]]
            p2 = points[0]
        else:
            p1 = points[route[i]]
            p2 = points[route[i+1]]

        # 総距離を計算していく
        total_distance += distance(p1, p2)

    return total_distance

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))


# main
if __name__ == "__main__":
    points = generate_points(POINTS_SIZE)
    route = list(range(POINTS_SIZE))
    min_distance = 100000

    # ウインドウ初期化
    root = tkinter.Tk()
    root.title(u"TSPを乱数で解いてみる")

    # ウインドウサイズ
    root.geometry(str(SCREEN_WIDTH) + "x" + str(SCREEN_HEIGHT))

    # キャンバスを作成
    canvas = tkinter.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    canvas.place(x=0, y=0)  # キャンバスの位置を指定

    for _ in range(LOOP):
        random.shuffle(route)

        total_distance = calc_distance(points, route)

        if min_distance > total_distance:
            min_distance = copy.copy(total_distance)
            print(min_distance)

            canvas.delete("all")

            for i in range(POINTS_SIZE):
                (x0, y0) = points[route[i]]

                if i == POINTS_SIZE - 1:
                    # 最後は始点
                    (x1, y1) = points[route[0]]
                else:
                    (x1, y1) = points[route[i+1]]

                # 経路の線を描画
                canvas.create_line(x0*SCREEN_WIDTH, y0*SCREEN_HEIGHT, x1*SCREEN_WIDTH, y1*SCREEN_HEIGHT, fill="black", width=1)

                # 都市を描画
                canvas.create_oval(x0 * SCREEN_WIDTH - 3,
                                   y0 * SCREEN_HEIGHT - 3,
                                   x0 * SCREEN_WIDTH + 3,
                                   y0 * SCREEN_HEIGHT + 3, fill="blue")

            # 距離を描画
            canvas.create_text(5, 5,
                               text="{:.2f}".format(min_distance),
                               anchor="nw", fill="red")

            canvas.update()

    root.mainloop()
















