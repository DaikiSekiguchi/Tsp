# coding: utf-8

import copy
import random
import math
import tkinter

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 200
canvas_list = []


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))


def generate_canvas(root, population_size):
    # ウインドウ初期化
    root.title("TSP問題をGAで解く")

    width_size = 5  # 横方向の配置数
    height_size = 5  # 縦方向の配置数

    window_width = SCREEN_WIDTH * width_size  # ウインドウの横幅
    window_height = SCREEN_HEIGHT * height_size  # ウインドウの縦幅

    root.geometry(str(window_width) + "x" + str(window_height))  # ウインドウサイズを指定

    # 集団に属する個体の数だけTkinterのキャンバスを作成する
    for i in range(population_size):
        canvas = tkinter.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)  # キャンバスを作成
        cx = (i % width_size) * SCREEN_WIDTH  # キャンバスのX座標
        cy = (i // width_size) * SCREEN_HEIGHT  # キャンバスのY座標
        canvas.place(x=cx, y=cy)  # キャンバスの位置を指定

        # リストに追加
        canvas_list.append(canvas)


class TspGA:
    # 初期化
    def __init__(self, city_size, population_size, select_rate, mutation_rate):
        self.city_size = city_size  # 都市の数(遺伝子の数)
        self.population_size = population_size  # 集団に属する個体の数
        self.select_rate = select_rate  # エリート戦略として残す個体の割合
        self.mutation_rate = mutation_rate  # 突然変異が起こる割合

        self.population = []  # 集団
        self.individuals_fitness = []  # 集合に属する各個体の適応度
        self.selected_individuals = []  # 選択で残った適応度の高い個体群
        self.child_individuals = []  # 交叉、突然変異を経て新たに生成された個体群

        self.cities = []  # 各都市の座標値

    # 都市情報を描画する
    def generate_cities(self):
        for i in range(self.city_size):
            self.cities.append([random.uniform(0.1, 0.9), random.uniform(0.1, 0.9)])

    # 1. 初期集団を生成する
    def generate_init_population(self):
        # 都市を生成する
        self.generate_cities()

        # 各都市を巡回するルート順を遺伝子として持つ個体を生成する
        for i in range(self.population_size):
            route = list(range(self.city_size))
            random.shuffle(route)
            self.population.append(route)

    # 経路の距離を計算する
    def calc_distance(self, route):
        total_distance = 0

        for i in range(len(route)):
            if i == len(route) - 1:
                p1 = self.cities[route[i]]
                p2 = self.cities[route[0]]
            else:
                p1 = self.cities[route[i]]
                p2 = self.cities[route[i + 1]]

            # 総距離を計算していく
            total_distance += distance(p1, p2)

        return total_distance

    # 2. 適応度の高い個体を残し、残りを淘汰する
    def selection(self):
        # 各個体の適応度を計算する
        for route in self.population:
            fitness = self.calc_distance(route)
            self.individuals_fitness.append([route, fitness])

        # 適応度が高い順にソートする→この場合は総距離が小さいほど適応度が高い
        self.individuals_fitness.sort(key=lambda x: x[1])

        # 適応度の高い個体を残す
        n = int(self.population_size * self.select_rate)

        for individual in self.individuals_fitness[0:n]:
            self.selected_individuals.append(copy.deepcopy(individual[0]))

    # 3. 交叉(順序交叉)
    def crossover(self):

        # 新しく子を生成する数
        n = self.population_size - len(self.selected_individuals)

        for _ in range(n):
            parent = random.sample(self.selected_individuals, 2)

            intersection1 = random.randint(0, self.city_size - 2)
            intersection2 = random.randint(intersection1 + 1, self.city_size - 1)

            # 子の個体(-1で遺伝子を初期化しておく)
            child = [-1] * self.city_size

            # 交叉点1から交叉点2間の遺伝子を親2から複製
            for i in range(intersection1, intersection2):
                city = parent[1][i]
                child[i] = city

            order_crossover_list = list(range(intersection2, self.city_size)) + list(range(0, intersection2))
            start_n = 0

            # 交叉点1から交叉点2間以外を親1から複製(順序交叉で子を生成する→子のi番目の都市を決定する)
            for i in range(len(order_crossover_list)):

                # 親1のj番目の都市が子個体(親2から一部受け継いだ)に既にある(訪問済)かないかを判定
                for j in range(start_n, len(order_crossover_list)):
                    city = parent[0][order_crossover_list[j]]

                    # 既に訪問済な場合
                    if city in child:
                        continue

                    # まだ訪問していない場合
                    else:
                        child[order_crossover_list[i]] = city
                        start_n = j + 1
                        break

                # 全ての都市の巡回順を満たした場合
                if -1 not in child:
                    break

            # 新しく生成された子をリストに格納する
            self.child_individuals.append(child)

    # 4. 突然変異
    def mutation(self):
        for individual in self.child_individuals:
            n = random.random()
            if n < self.mutation_rate:
                copy_individual = copy.deepcopy(individual)

                city1, city2 = random.sample(range(0, len(individual)), 2)
                if city1 > city2:
                    city1, city2 = city2, city1

                # city1~city2間の巡回順を逆にする
                individual[city1:city2] = reversed(copy_individual[city1:city2])

        # 新しい集団 = 選択された個体群(親) + 新しく生成された個体群(子)
        self.selected_individuals.extend(self.child_individuals)
        self.population = copy.deepcopy(self.selected_individuals)

        # 変数を初期化
        self.reset()

    # 変数の初期化
    def reset(self):
        self.individuals_fitness = []
        self.selected_individuals = []
        self.child_individuals = []

    # 都市の巡回を描画する
    def draw_population_info(self):
        for individual in range(self.population_size):
            canvas = canvas_list[individual]
            route = self.population[individual]
            total_distance = self.calc_distance(route)

            # キャンバスをクリア
            canvas.delete("all")

            # 枠を描画
            canvas.create_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, outline="black", width=1, fill="gray")

            for i in range(self.city_size):
                (x0, y0) = self.cities[route[i]]

                if i == self.city_size - 1:
                    (x1, y1) = self.cities[route[0]]
                else:
                    (x1, y1) = self.cities[route[i + 1]]

                # 経路の線を描画
                canvas.create_line(x0 * SCREEN_WIDTH, y0 * SCREEN_HEIGHT,
                                   x1 * SCREEN_WIDTH, y1 * SCREEN_HEIGHT,
                                   fill="white", width=1)

                # 都市を描画
                canvas.create_oval(x0 * SCREEN_WIDTH - 2, y0 * SCREEN_HEIGHT - 2,
                                   x0 * SCREEN_WIDTH + 2, y0 * SCREEN_HEIGHT + 2,
                                   fill="blue")

            # 距離を描画
            canvas.create_text(5, 5, text="{0}".format(round(total_distance, 2)), anchor="nw", fill="black")

            canvas.update()
