from random import randint

# Внутренняя логика

# Классы исключений
class BoardException(Exception):
    '''Базовый класс для возможных исключений'''
    pass

class BoardOutException(BoardException):
    '''Вызывается если клетка за пределами поля '''
    def __str__(self):
        return "Вы пытаетесь выстрелить за пределы доски!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass

#Класс точек на поле
class Dot:
    '''Класс для координат точек на поле'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        f"({self.x}, {self.y}"

class Ship:
    '''Класс корабля на игровом поле'''
    def __init__(self, leight, start_dot, route):
        self.leight = leight            # длинна корабля
        self.start_dot = start_dot      # начальная точка
        self.route = route              # направление (горизонтальное вертикальное)
        self.health = leight            # количество

    @property
    # делает метод свойством чтобы обращаться к нему без скобок ship_1.dots[i][0], а не ship_1.dots()[i][0]
    def dots(self):                     # метод возвращающий список точек корабля
        ship_dots = []
        for i in range(self.leight):
            curr_x = self.start_dot.x
            curr_y = self.start_dot.y

            if self.route == 0:
                curr_x += i
            elif self.route == 1:
                curr_y += i

            ship_dots.append(Dot(curr_x, curr_y))

        return ship_dots

    def shooten(self, shot): # метод проверяет было ли попадание по кораблю
        return shot in self.dots

#Класс игровой доски
class Board:
    '''Игровая доска'''
    def __init__(self, hid = False, size = 6):
        self.hid = hid  # тип bool, инф. нужно ли скрывать корабли на доске(вывод доски врага) или нет
        self.size = size
        self.count_ships = 0      # счётчик уничтоженых кораблей
        self.board_ = [["O"] * size for i in range(size)] #создаем массив доски 6х6
        self.dot_cond = []  # список точек в которые стреляли
        self.ships_list = []  # список кораблей доски

    #МЕТОДЫ ДОСКИ
    # add_ship - Постановка корабля на доску, если поставить не получается выбрасывает исключение
    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.dot_cond:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.board_[d.x][d.y] = "■"
            self.dot_cond.append(d)

        self.ships_list.append(ship)
        self.countor(ship)

    # countor - Обводка коробля по контуру, помечает соседние точки где корабля по правилам быть не может
    def countor(self, ship, verb = False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1), (1, -1),
            (1, 0), (1, 1), (0, 0)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.dot_cond:
                    if verb:
                        self.board_[cur.x][cur.y] = '.'
                    self.dot_cond.append(cur)

    def __str__(self): #печать игрвого поля
        res = ""
        res += '\n  | 1 | 2 | 3 | 4 | 5 | 6 | '
        for i, row in enumerate(self.board_):
            res += f'\n{i + 1} | ' + " | ".join(row) + " | "  # формирование горизонтальных строк через склеивание аргументов
        if self.hid:
            res = res.replace("■", "O")
        return res

    # out - для точки (объект класса Dot) возвращает True, если точка выходит за пределы поля и False, если не выходит
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    # hid - Вывод доски в консоль в зависимости от параметра hid
    def hid(self):
        pass

    # shot - делает выстрел по доске
    # (если попытка выстрелить за пределы поля и в использованную точку, выбрасывать исключение)
    def shot(self, d):
        if self.out(d):
            raise BoardOutException
        if d in self.dot_cond:
            raise BoardUsedException

        self.dot_cond.append(d)

        for ship in self.ships_list:
            if d in ship.dots:
                ship.health -= 1
                self.board_[d.x][d.y] = "X"
                if ship.health == 0:
                    self.count_ships += 1
                    self.countor(ship, verb = True)
                    print("Корабль уничтожен!")
                    return  False
                else:
                    print('Корабль подбит!')
                    return  True
        self.board_[d.x][d.y] = "."
        print('Промах!')
        return False

    def begin(self):
        self.dot_cond = []

# Внешняя логика
# Класс игрока
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat

            except BoardException as e:
                print(e)


# Наследуем классы AI и User от Player
class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d

class User(Player):
    def ask(self):
        while True:
            move_ = input("Введите координаты:").split()

            if len(move_) != 2:  # если координаты введены без пробела
                print("Координаты состоят из 2х чисел и вводятся через пробел")
                continue
            # если координаты не числовые
            if not (move_[0].isdigit()) or not (move_[1].isdigit()):
                print("Вводить можно только числовые значения")
                continue

            x, y = map(int, move_)  # принимаем коррдинаты

            return Dot(x - 1, y - 1)

# Главный класс Game
class Game:
    def __init__(self, size = 6):
        self.size = size
        player_ = self.random_board()
        comp_ = self.random_board()
        comp_.hid = True

        self.ai = AI(comp_, player_)
        self.user = User(player_, comp_)


    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attemts = 0
        for l in lens:
            while True:
                attemts += 1
                if attemts > 2000:
                    return None
                ship = Ship(l, Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("===================")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("===================")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
        print("координаты вводятся")
        print("   через пробел    \n")


    def loop(self ):
        num = 0

        while True:
            print("=" * 27)
            print("Поле пользователя:")
            print(self.user.board)
            print("=" * 27)
            print("Поле компьютера:")
            print(self.ai.board)

            if num % 2 == 0:
                print("=" * 27)
                print("Ход игрока!:")
                repeat = self.user.move()
            elif num % 2 == 1:
                print("=" * 27)
                print("Ход компьютера!:")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count_ships == 7:
                print('=' * 27)
                print('Игрок - вы победили!!!')
                exit()
            if self.user.board.count_ships == 7:
                print('=' * 27)
                print('Компьтер победил.')
                exit()
            num += 1

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()

#PycharmProjects\pythonProject\practice C1>python sea_fight_6x6.py