# -*- coding: utf-8 -*-
import random
import time
import json

# Количество существ в поколении
bots = 3


# Действия
actions = [
    "print", 
    "(",
    ")",
    "\"",
    "Hello World!",
]

# Ответ
need = [0, 1, 3, 4, 3, 2]

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
    ptr = 0
    rec = 0
    work = True
    valid = []

    while work:
        if data[ptr][1] == need[ptr]:
            valid.append(data[ptr][1])
        
        work = data[ptr][0] != -1
        ptr = data[ptr][0]
        rec += 1

        if rec > len(need) - 1:
            break
    
    for i in range(0, len(valid)):
        if valid[i] == need[i]:
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
        if random.randint(0, 2) == 1:
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
    rec = 0

    while(gen[ptr][0] != -1):
        action = gen[ptr][1]
        result += actions[action]
        ptr = gen[ptr][0]
        
        rec += 1
        if rec > len(need) - 1:
            break

    action = gen[ptr][1]
    result += actions[action]

    return result


# Вывод информации о генах
def dump_gen(gen, num):
    print(f"Unit {num + 1}")
    print(f"Соответствие {check_gen_valid(gen)}")
    print(f"Генетический код: {gen}")
    print(f"Кодогенерация: {codegen(gen)}")


if __name__ == '__main__':
    start_time = time.time()
    generation_history = []
    unit_list = []

    # 5 ботов с случайными генами
    for i in range(5):
        unit_list.append(mutation(start_gen))

    # Количество пройденных генераций
    generation = 0

    # Максимум за текущую генерацию
    generation_max = 0

    # Лучший бот
    best_unit = 0
    best_unit_genetic = start_gen

    # Работает ли цикл
    work = True

    while(work):
        generation += 1
        generation_max = 0
        best_unit = random.randint(0, 4)

        

        # Выбираем лучшего из всех
        for i in range(len(unit_list)):
            if check_gen_valid(unit_list[i]) > generation_max:
                generation_max = check_gen_valid(unit_list[i])
                best_unit = i
                best_unit_genetic = unit_list[best_unit]
        
        # Если цель достигнута, выводим информацию о генофонде
        if generation_max == 6:
            print(f"Конец на генерации: {generation}")
            print(f"Время: {time.time() - start_time}")
            print(f"Лучший бот: unit{best_unit + 1}")
            print("Генофонд:")
            for i in range(0, len(unit_list)):
                dump_gen(unit_list[i], i)

            work = False
        else:
            for i in range(len(unit_list)):
                unit_list[i] = mutation(best_unit_genetic)

        # Сохраняем текущую генерацию
        generation_history.append(
            {
                'generation': generation,
                'generation_max': generation_max,
                'unit_list': unit_list
            }
        )

    # Сохраняем последнюю генерацию и историю генераций
    with open('generation.json', 'w+') as f:
        f.write(json.dumps(unit_list, indent = 4, sort_keys = True))
        
    with open('generation_history.json', 'w+') as f:
        f.write(json.dumps(generation_history, indent = 4, sort_keys = True))
