#Функция для печати матрицы
def print_m(m):
    for i in range(4):
        print('\n')
        for j in m[i]:
            print(j, end="     ")
    print('\n')

# Игровое поле
game_area = [
    [" ", '1', '2', '3'],
    ['1', "-", "-", "-"],
    ['2', "-", "-", "-"],
    ['3', "-", "-", "-"]
]
# Печать матрицы
#for i in range(4):
#    print('\n')
#    for j in game_area[i]:
#        print(j, end="     ")
#print('\n')

# Правила игры
print('=' * 20, '||  ПРАВИЛА ИГРЫ  ||', end='\n'+'='* 20 + '\n', sep = '\n')
print('1. Право первого хода выбирается случайно',
      '2. "Х" ходят первыми',
      '3. Для совершения хода введите координаты ячейки игрового поля в формате:',
      'номер строки (пробел) номер столбца.',
      '4. Для завершения игры вместо координат введите: stop',
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
]
print_m(exmpl_m)

# Исходы игры
tie = "Ничья. Ты отлично сражался!"
loss = 'Проигрыш. Не расстраивайся и попробуй снова.'
win = 'Победа! Ты молодец!'

start = input('Чтобы начать игру нажмите клавишу Enter: ')
# Начало игры

stop_ = 0 # для остановки for eсли break по while

if start == '':
    print('Начинаем')
    for i in range(1, 10):
        symbol_ = 'O' if i % 2 == 0 else 'X' # если не четный - ход Х, четный - О
        enter_ = input(f'{symbol_} - Ваш ход, введите координаты:')

        if enter_ == "stop":
            print("Вы остановили игру")
            break
        else:
            move_ = list(map(int, enter_.split()))
            line_x, col_x = move_[0], move_[1]

            while game_area[line_x][col_x] != '-':
                print('Такой ход уже был, сделайте другой')
                enter_ = input(f'{symbol_} - Ваш ход, введите координаты:')

                if enter_ == "stop":
                    print("Вы остановили игру")
                    stop_ += 1
                    break

                move_ = list(map(int, enter_.split()))
                line_x, col_x = move_[0], move_[1]
            if stop_ == 0:
                game_area[line_x][col_x] = str(symbol_)
                # Печать матрицы
                print_m(game_area)
            else:
                break






