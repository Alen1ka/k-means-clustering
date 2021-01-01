import sys


def read(num):
    try:
        file = open("clustering2.csv", "r")
    except FileNotFoundError:
        sys.exit('Файл не существует!')
    objects = []  # список для хранения объектов
    standards = []  # список для хранения эталонных точек
    array = []  # список для хранения признаков
    line_array = 0  # количество списков для хранения признаков
    number = -1

    for line in file:  # для каждой строки из файла
        if number == -1:
            for element in line.strip().split(';'):  # убираем из строки лишние
                # точки с запятыми, что между ними попадает элементы списка
                objects.append(element)  # записываем элемент в список

        if number == 0:
            for element in line.strip().split(';'):
                standards.append(element)

        if number > 0:
            for element in line.strip().split(';'):
                try:
                    array.append(float(element))
                # проверяем на ошибки
                except:
                    sys.exit("Количество признаков X не равно количеству "
                             "признаков или количество эталонных точек "
                             "больше количества объектов")
            line_array += 1

        number += 1

    file.close()

    # делим один список из признаков на несколько
    len_a = len(array)
    array = [array[i:i + len_a // line_array] for i in
             range(0, len_a, len_a // line_array)]

    # находим количество эталонных точек
    count_e = 0
    for x in range(len(standards)):
        if f"e{x}" in standards:
            count_e += 1
    o_emptiness = objects.count('')

    # проверяем на ошибки
    if count_e + 1 == len(objects):
        sys.exit("Количество эталонных точек равно количеству объектов")
    for i in range(line_array):
        if len(array[i]) != len(objects) - o_emptiness:
            sys.exit("Количество признаков не равно количеству объектов")

    # вывод списков и переменных
    if num == -3:
        return count_e
    if num == -1:
        return objects
    if num == 0:
        return standards
    if num > 0:
        return array

    return line_array


def calculations():
    # берем прочитанные списки и переменные из функции read
    num = -3
    count_e = read(num)
    num = -2
    line_array = read(num)
    num = -1
    objects = read(num)
    num = 0
    standards = read(num)
    num = 1
    array = read(num)

    # находим количество эталонных точек в начале
    count_e_begin = 0
    x = 1
    while f"e{x}" in standards[x - 1]:
        count_e_begin += 1
        x += 1
    x -= 1

    num_e = 1
    e = []
    while num_e < count_e + 1:
        index_e = 0
        while index_e < line_array:
            e.append(float(array[index_e][standards.index(f"e{num_e}")]))
            index_e += 1
        num_e += 1

    # для расстояний от точек объектов до эталонных точек
    # создаем массивы и заполняем их нулями
    d_e = []
    for i in range(count_e):
        d_e.insert(i, 0)

    # для эталонов e1...en создаем массивы и заполняем их нулями
    e_object = []
    e_object = [e_object[i:i + len(standards) // count_e] for i in
                range(0, len(standards), len(standards) // count_e)]
    e_object_copy = []
    for i in range(count_e):
        e_object_copy.insert(i, 0)

    # итерацаии
    index2 = x
    number_objects = x
    number_iteration = 0
    while e_object != e_object_copy:
        print(f"\nИтерация №{number_iteration}")
        e_object_copy = e_object
        e_object = []
        e_object = [e_object[i:i + len(standards) // count_e] for i in
                    range(0, len(standards), len(standards) // count_e)]
        q = 0
        for _objects in range(len(array[0]) - x):
            # сравниваем расстояния
            num_e = 0
            while num_e < count_e:
                """print(standards.index(f"e{num_e + 1}"))"""

                print(f"\nСравниваем расстояние от точки "
                      f"{objects[number_objects]} до эталонных точек:")
                summa = 0
                index1 = 0
                for x in range(len(array)):
                    summa = summa + pow((float(array[index1][index2]) - e[q]),
                                        2)
                    index1 += 1
                    q += 1

                d_e[num_e] = pow(summa, 0.5)

                print(
                    f"d({objects[number_objects]}e{num_e + 1}) = {d_e[num_e]}")
                num_e += 1

            # находим минимальное расстояние
            d_e_copy = d_e.copy()
            d_e_copy.sort()
            minimum = d_e_copy[0]
            index_min = d_e.index(minimum)
            print(
                f"\nМинимальным является расстояние "
                f"d({objects[number_objects]}e{index_min + 1}).\n"
                f"Пересчитываем значения для эталонной точки."
                f"Получаем значения e{index_min + 1}:")

            # пересчитываем значения для эталонных точек
            index1 = 0
            q = index_min * 2
            num_e = index_min * 2
            number_e = 0
            while number_e < line_array:
                e[num_e] = (array[index1][index2] + e[q]) / 2
                print(e[num_e])
                index1 += 1
                q += 1
                num_e += 1
                number_e += 1
            number_objects += 1
            index2 += 1
            q = 0

        # классификация объектов
        print("\n\nПроизведем классификацию объектов:")
        number_objects = 0
        index2 = 0
        z = 0
        for _objects in range(len(array[0])):
            q = 0
            num_e = 0
            while num_e < count_e:

                summa = 0
                index1 = 0
                for x in range(len(array)):
                    summa = summa + pow((float(array[index1][index2]) - e[q]),
                                        2)
                    index1 += 1
                    q += 1

                d_e[num_e] = pow(summa, 0.5)

                print(
                    f"d({objects[number_objects]}e{num_e + 1}) = {d_e[num_e]}")
                num_e += 1

            d_e_copy = d_e.copy()
            d_e_copy.sort()
            minimum = d_e_copy[0]
            index_min = d_e.index(minimum)
            print(
                f"Объект {objects[number_objects]} "
                f"ближе всех к e{index_min + 1}\n")
            e_object[index_min].append(objects[number_objects])
            z += 1
            index2 += 1
            number_objects += 1
        print(e_object)
        x = 0
        number_objects = 0
        index2 = 0
        number_iteration += 1
    input("Нажмите любую кнопку для выхода")


calculations()
