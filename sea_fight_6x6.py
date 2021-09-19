#Создание массива игрового поля и функция его печати ??? нужно или нет ХЗ))
# ■

#функция печати игрового поля
def print_board(list_):
    print('\n  | 1 | 2 | 3 | 4 | 5 | 6 | ')
    for i in range(len(list_)):
        print(str(i + 1) + " | " + " | ".join(
            list_[i]) + " | ")  # формирование горизонтальных строк через склеивание аргументов



# Внутренняя логика

# Классы исключений
class Error(Exception):
    '''Базовый класс для возможных исключений'''
    pass
class BoardOutException(Error):
    '''Вызывается если клетка за пределами поля'''
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

            if self.route == "g":
                curr_x += i
            elif self.route == "v":
                curr_y += i

            ship_dots.append(Dot(curr_x, curr_y))

        return ship_dots

    def shooten(self, shot): # метод проверяет было ли попадание по кораблю
        return shot in self.dots

#ship_2 = Ship(2, (3,1), "v")

#for i in range(3):
#    board_[ship_1.dots[i][0]][ship_1.dots[i][1]] = "■"
#for i in range(2):
 #   board_[ship_2.dots[i][0]][ship_2.dots[i][1]] = "■"

#print_board()
#print(ship_1.dots())
#Класс игровой доски
class Board:
    '''Игровая доска'''
    def __init__(self, hid = False, size = 6):
        self.hid = hid  # тип bool, инф. нужно ли скрывать корабли на доске(вывод доски врага) или нет
        self.size = size
        self.count_ships = []      # счётчик уничтоженых кораблей
        self.board_ = [["O"] * size for i in range(size)] #создаем массив доски 6х6
        self.dot_cond = []  # список точек в которые стреляли
        self.ships_list = []  # список кораблей доски

    #МЕТОДЫ ДОСКИ
    # add_ship - Постановка корабля на доску, если поставить не получается выбрасывает исключение
    def add_ship(self, ship):
        for d in ship.dots:
            self.board_[d.x][d.y] = "■"

    # countor - Обводка коробля по контуру, помечает соседние точки где корабля по правилам быть не может
    def countor(self):
        pass

    # hid - Вывод доски в консоль в зависимости от параметра hid
    def hid(self):
        pass

    # out - для точки (объект класса Dot) возвращает True, если точка выходит за пределы поля и False, если не выходит
    def out(self):
        pass

    # shot - делает выстрел по доске
    # (если попытка выстрелить за пределы поля и в использованную точку, выбрасывать исключение)
    def shot(self):
        pass

b = Board()
ship_1 = Ship(3, Dot(0, 0), "g")
b.add_ship(ship_1)
print_board(b.board_)

# Внешняя логика
# Класс игрока
class Player:
    pass

# Наследуем классы AI и User от Player
class AI(Player):
    pass

class User(Player):
    pass

# Главный класс Game
class Game:
    pass

