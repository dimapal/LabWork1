"""Лабораторна робота №1  Б18_д/122Б  Паляниця Дмитро """
import random
import sys

card_rows = 7
height = 5
width = 8
space =' '
deque = ['2'] + ['2'] + ['2'] + ['2'] + ['3'] + ['3'] + ['3'] + ['3'] + ['4'] + ['4'] + ['4'] + ['4'] + ['5'] + ['5'] + ['5'] + ['5'] + ['10'] + ['10'] +\
        ['10'] + ['10']+['6'] + ['6'] + ['6'] + ['6'] + ['7'] + ['7'] + ['7'] + ['7'] + ['8'] + ['8'] + ['8'] + ['8'] + ['9'] + ['9'] + ['9'] + ['9'] +\
        ['V'] + ['V'] + ['V'] + ['V'] + ['D'] + ['D'] + ['D'] + ['D'] + ['K'] + ['K'] + ['K'] + ['K'] + ['T'] + ['T'] + ['T'] + ['T']
values = {'T':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'V' : 11, 'D':12, 'K':13}

class Card:
    def __init__(self, value, num = '0.0',unavailable_card = True, width = 8):
        self.value = value
        self.num = num
        self.unavaible = unavailable_card
        self.width = width 
        self.passed = False

    @property
    def cart(self):
        return
    @cart.getter
    def cart(self):
        value = self.value
        num = self.num
        width = self.width

        if self.passed:#вигляд карт(1 - для карт, що були викинуті з гри(пусте місце),2 - для карт, що недоступні для вибору, 3 - для карт, що доступні для вибору)
            return [f'{space * width}', f'{space * width}', f'{space * width}', f'{space * width}', f'{space * width}']
        elif self.unavaible:
            return[f'********', f'*{value:<6}*', f'*      *', f'*      *', f'{num:*^{width}}']
        else:
            return [f'########', f'#{value:<6}#', f'#      #', f'#      #', f'{num:#^{width}}']
#CardCurrent - клас для формування карт підбору
class CardCurrent:
    def __init__(self):
        self.line = []
        self.current = None
        
    def createline(self):#Тут формується черга карт задопомогою shuffle
        values = deque
        random.shuffle(values)
        for c_value in values:
            self.line.append(Card(c_value))
        self.scrolling()
        return self
    
    def scrolling(self):
        if self.current is not None and not self.current.passed:
            self.current.unavaible = True
            self.line = [self.current] + self.line
        self.current = self.line.pop()
        self.current.unavaible = False
        
    @property
    def cart(self):
        return
    @cart.getter
    def cart(self):
        current_card = self.current.cart
        c = len(self.line)
        return[f'######## ' + current_card[0], f'######## ' + current_card[1], f'{c:#^{width}} ' + current_card[2],\
               f'######## ' + current_card[3], f'######## ' + current_card[4]]

class Table:#Тут відбувається розкладання карт та їхня індексація
    def __init__(self):
        self.cards = []

    def createcard(self, deline):
        self.cards = []
        for i in range(card_rows):
            self.cards.append([])
            for j in range(i + 1):
                card = deline.pop()
                card.num = f'{i+1}.{j+1}'
                self.cards[i].append(card)
        return self
    
    def pssd(self):
        v = len(self.cards)
        for i in range(v):
            for j in range(len(self.cards[i])):
                if (len(self.cards) < i + 2 or(self.cards[i + 1][j].passed and self.cards[i + 1][j + 1].passed)):
                    self.cards[i][j].unavaible = False

class Sltr:#Тут відбувається основна гра
    def __init__(self):
        self.deline = CardCurrent().createline()
        self.table = Table().createcard(self.deline.line)
        
    def restart(self):#функція для рестарту гри за бажанням користувача
        self.deline = CardCurrent().createline()
        self.table = Table().createcard(self.deline.line)
        
    def console(self):#прорисовка карт на столі, піраміда
        deline_cart = self.deline.cart
        rows = card_rows
        for j in range(rows):
            cards = self.table.cards[j]
            for i in range(height):
                puff = space * 2
                if j == 0:
                    deline_row = deline_cart[i]
                else:
                    deline_row = ''
                cards_row = puff.join([card.cart[i] for card in cards])
                print(f'{deline_row:{space}<20}{cards_row:{space}^{(width + len(puff)) * rows}}')

    def final(self):#перевірка на перемогу(чи залишились карти на столі)
        if not self.table.cards[0][0].passed:
            return False
        return True

    @staticmethod
    def win():#функція, яка спрацьовує у разі перемоги
        print('YOU WIN!!!')
    @staticmethod
    def summa(card1,card2):#функція для перевірки рівності суми двох карт 13-ти, та перевірка самих карт на їхню наявність на столі та доступність
        if (not card1.unavaible and not card2.unavaible and not card1.passed and not card2.passed and\
            (values[card1.value] + values[card2.value] == 13 or (values[card1.value] == 13 and values[card2.value] == 13))):
            card1.passed = True
            card2.passed = True
            
    def run(self):#управління грою, користувацький ввід та перевірка на коректність введених даних
        while not self.final():
            self.table.pssd()
            self.console()
            while True:
                command = input('Scroll - 1, restart - 2, fast win - 3, continue - enter: ')
                if command == '1':
                    self.deline.scrolling()
                    break
                elif command == '2':
                    self.restart()
                    break
                
                elif command == '':
                    while True:
                        try:
                            row1 = int(input('Enter the row number of first card: '))
                            break
                        except ValueError:
                            print('Incorrect value. Please try again.')

                    while True:
                        try:
                            column1 = int(input('Enter the column number of first card: '))
                            break
                        except ValueError:
                            print('Incorrect value. Please try again.')
                            
                    while True:
                        try:
                            row2 = int(input('Enter the row number of second card: '))
                            break
                        except ValueError:
                            print('Incorrect value. Please try again.')
                            
                    while True:
                        try:
                            column2 = int(input('Enter the column number of second card:'))
                            break
                        except ValueError:
                            print('Incorrect value. Please try again.')
                            
                    if (row1 == 0) and (column1 == 0):
                        card1 = self.deline.current
                    else:
                        card1 = self.table.cards[row1 - 1][column1 - 1]
                        
                    if (row2 == 0) and (column2 == 0):
                        card2 = self.deline.current
                    else:
                        card2 = self.table.cards[row2 - 1][column2 - 1]
                        
                    if card1 is not None and card2 is not None:
                            self.summa(card1, card2)
                            break
                        
                elif command == '3':
                    
                    self.win()
                    sys.exit()
                    break
                    

        self.win()
        self.run()
    def start(self):
        self.run()
if __name__ == '__main__':
    game = Sltr()
    game.start()
                
                
                
        












        
        
        
