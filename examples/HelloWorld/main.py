# -*- coding: utf-8 -*-
import random
import time
import json

# Количество существ в поколении
bots = 3


# Действия, ответ 0 1 3 4 3 2
actions = [
    "print", 
    "(",
    ")",
    "\"",
    "Hello World!",
]

# Мы должны иметь точный максимум действий, чтобы не ошибиться
actions_max = len(actions) - 1

# Сами гены
# <Номер гена>, <номер действия>
start_gen = [
    [
        1, 0
    ],
    [
        2, 0
    ],
    [
        3, 0
    ],
    [
        4, 0
    ],
    [
      
        5, 0
    ],
    [
        -1, 0
    ]
]


# Исполнение гена
def exec_gen(gen):
    ptr = 0
    inter = 0
    result = []

    while (not start_gen[ptr] == -1) and (inter < 11):
        action = start_gen[ptr][1]

        result.append(actions[action])

        ptr = start_gen[ptr][0]
        inter += 1
    
    return result


# Проверка гена
def check_gen_valid(data):
    result = 0

    if data[0][1] == 0:
        result += 1
    if data[1][1] == 1:
        result += 1
    if data[2][1] == 3:
        result += 1
    if data[3][1] == 4:
        result += 1
    if data[4][1] == 3:
        result += 1
    if data[5][1] == 2:
        result += 1
    
    return result


# Проверка работы гена
def check_work_valid(gen):
    result = check_gen_valid(gen)

    if result > 4:
        try:
            with open('Hi.py', "w+") as f:
                f.write(codegen(gen))

            os.system("python3 Hi.py>result.txt")
            
            with open('result.txt', "r") as f:
                if need == f.read():
                    return 200
        except Exception as E:
            return result

    return result


# Мутации с небольшим шансом
def mutation(gen):
    new_gen = []
    for i in gen:
        if random.randint(0, 3) == 1:
            new_gen.append(
                [
                    i[0], random.randint(0, actions_max)
                ]
            )
        else:
            new_gen.append(i)
    return new_gen


# Кодогенерация
def codegen(gen):
    ptr = 0
    result = ""

    while(gen[ptr][0] != -1):
        action = gen[ptr][1]
        result += actions[action]
        ptr = gen[ptr][0]

    action = gen[ptr][1]
    result += actions[action]

    return result


# Входная точка
if __name__ == '__main__':
    start_time = time.time()
    generation_history = []

    # 5 ботов с нулевыми(эталонными) генами
    unit1 = mutation(start_gen)
    unit2 = mutation(start_gen)
    unit3 = mutation(start_gen)
    unit4 = mutation(start_gen)
    unit5 = mutation(start_gen)

    # Количество пройденных генераций
    generation = 0
    # Максимум за текущую генерацию
    generation_max = 0
    # Лучший бот
    best_unit = 0

    # Требуемый результат
    need = "Hello World!"
    # Работает ли цикл
    work = True

    while(work):
        generation += 1
        generation_max = 0
        best_unit = random.randint(0, 4)

        if check_gen_valid(unit1) > generation_max:
            generation_max = check_gen_valid(unit1)
            best_unit = 0

        if check_gen_valid(unit2) > generation_max:
            generation_max = check_gen_valid(unit2)
            best_unit = 1

        if check_gen_valid(unit3) > generation_max:
            generation_max = check_gen_valid(unit3)
            best_unit = 2

        if check_gen_valid(unit4) > generation_max:
            generation_max = check_gen_valid(unit4)
            best_unit = 3

        if check_gen_valid(unit5) > generation_max:
            generation_max = check_gen_valid(unit5)
            best_unit = 4

        unit_list = [unit1, unit2, unit3, unit4, unit5]
        best_unit_genetic = unit_list[best_unit]
        
        if generation_max == 6:
            print(f"Конец на генерации: {generation}")
            print(f"Время: {time.time() - start_time}")
            print(f"Лучший бот: unit{best_unit + 1}")
            print("Генофонд:")
            for i in range(0, len(unit_list)):
                print(
                    f"""\tunit{i+1}, соответствие {check_gen_valid(unit_list[i])}, гены: 
    {unit_list[i]}
Код: {codegen(unit_list[i])}
*****"""
                    )
            work = False
        else:
            unit1 = mutation(best_unit_genetic)
            unit2 = mutation(best_unit_genetic)
            unit3 = mutation(best_unit_genetic)
            unit4 = mutation(best_unit_genetic)
            unit5 = mutation(best_unit_genetic)
        generation_history.append(
            {
                'generation': generation,
                'generation_max': generation_max,
                'unit1': unit1,
                'unit2': unit2,
                'unit3': unit3,
                'unit4': unit4,
                'unit5': unit5
            }
        )
    with open('generation.json', 'w+') as f:
        f.write(json.dumps(generation_history, indent = 4, sort_keys = True)) 