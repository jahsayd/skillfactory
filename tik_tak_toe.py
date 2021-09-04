#Функция для печати матрицы
def print_m(m):
    for i in range(4):
        print('\n')
        for j in m[i]:
            print(j, end="     ")
    print('\n')
#Функция для проверки победы
def win_check():
    win_comb = [((1, 1), (2, 2), (3, 3)), ((1, 1), (1, 2), (1, 3)), ((1, 1), (2, 1), (3, 1)),
                ((1, 2), (2, 2), (3, 2)), ((1, 3), (2, 3), (3, 3)), ((1, 3), (2, 2), (3, 1)),
                ((2, 1), (2, 2), (2, 3)), ((3, 1), (3, 2), (3, 3))]
    for comb in win_comb:
        symbols = []
        for c in comb:
            symbols.append(game_area[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print("\nХ - Победили!")
            print(f"\nКонец игры.")
            return True
            break
        if symbols == ["O", "O", "O"]:
            print("\nO - Победили!")
            print(f"\nКонец игры.")
            return True
            break
    return False
#Функция для проверки и получения координат хода
def move_coord():
    while True:
        enter_ = input("Введите координаты:")

        if enter_ == "stop": #Если введено слово 'stop' игра останавливается
            print("Вы остановили игру, возвращайтесь снова!")
            exit()
        else:
            move_ = enter_.split()

        if len(move_) != 2: # если координаты введены без пробела
            print("Координаты состоят из 2х чисел и вводятся через пробел")
            continue
        # если координаты не числовые
        if (not move_[0].isdigit()) or (not move_[1].isdigit()):
            print("Вводить можно только числовые значения")
            continue
        line_x, col_x = map(int, move_) #принимаем коррдинаты

        if line_x < 1 or line_x > 3 or col_x < 1 or line_x > 3 :
            print("Введите координаты в пределах игрового поля (числа от 1 до 3)")
            continue
        if game_area[line_x][col_x] != '-':
            print('Такой ход уже был, сделайте другой')
            continue
        break
    return line_x, col_x
def repeat_game():
    while True:
        repeat_ = input("Хотите играть ещё раз? Введите y - да, n - нет:").lower()
        if repeat_ == "stop": print("Вы остановили игру, возвращайтесь снова!"), exit()
        if repeat_ != "y" or repeat_ != "n":
            print("Вводить нужно y или n")
            continue
        break
    return repeat_
# Игровое поле
game_area = [
    [" ", '1', '2', '3'],
    ['1', "-", "-", "-"],
    ['2', "-", "-", "-"],
    ['3', "-", "-", "-"]
]

# Правила игры
print('=' * 20, '||  ПРАВИЛА ИГРЫ  ||', end='\n'+'='* 20 + '\n', sep = '\n')
print('1. "Х" ходят первыми',
      '2. Для совершения хода введите координаты ячейки игрового поля в формате:',
      'номер строки (пробел) номер столбца.',
      '3. Для завершения игры вместо координат введите: stop',
      'ПРИМЕР:',
      '-' * 10, '',
      'X - Ваш ход, введите координаты: 1 2',
    sep='\n', end = ''
      )
exmpl_m =  [
    [" ", '1', '2', '3'],
    ['1', "-", "X", "-"],
    ['2', "-", "-", "-"],
    ['3', "-", "-", "-"]
]  #Матрица для печати примера в правилах
print_m(exmpl_m)

# Начало игры
start = input('Чтобы начать игру нажмите клавишу Enter: ')
while True:
    if start == '':
        print('Начинаем')
        for i in range(1, 10):
            symbol_ = 'O' if i % 2 == 0 else 'X' # если не четный - ход Х, четный - О
            print(f'{symbol_} - Ваш ход! \n')

            line_x, col_x = move_coord() # Получение координат
            game_area[line_x][col_x] = str(symbol_) # Запись хода в массив
            print_m(game_area) # Печать матрицы

            if win_check():#Проверка условий победы
                break

            if i == 9:
                print("Ничья! Это эпичная битва!")
    repeat_ = repeat_game()
    if repeat_ == "n": break