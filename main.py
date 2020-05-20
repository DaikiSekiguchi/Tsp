# coding: utf-8

from . import tsp_ga
import tkinter

CITY_SIZE = 50
POPULATION_SIZE = 25
SELECT_RATE = 0.5
MUTATION_RATE = 0.3
GENERATION = 2000

# インスタンスを生成
ga_tsp = tsp_ga.TspGA(CITY_SIZE, POPULATION_SIZE, SELECT_RATE, MUTATION_RATE)

# ウインドウ初期化
root = tkinter.Tk()

# 描画用のキャンバスを生成する
tsp_ga.generate_canvas(root, POPULATION_SIZE)

# 1. 初期集団を生成する
ga_tsp.generate_init_population()

for i in range(GENERATION):
    print("{0}世代".format(i))

    # 2. 選択
    ga_tsp.selection()

    # 3. 交叉
    ga_tsp.crossover()

    # 4. 突然変異
    ga_tsp.mutation()

    # 集合に属する個体の情報を描画する
    ga_tsp.draw_population_info()

root.mainloop()
