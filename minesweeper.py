import numpy as np
import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivymd.utils import asynckivy



class Board():
    def __init__(self):
        self.row = 5
        self.cul = 10
        self.board = np.zeros((self.row+2, self.cul+2), dtype=int)
        self.board[0, :] = 10
        self.board[self.row+1, :] = 10
        self.board[:, 0] = 10
        self.board[:, self.cul+1] = 10
    def create_bombs(self):
        self.num_bombs = (self.row*self.cul)//10
        self.bombs = []
        for i in range(self.num_bombs):
            random_row = random_number = random.randint(1, self.row)
            random_cul = random_number = random.randint(1, self.cul)
            bomb_tuple = (random_row, random_cul)
            while bomb_tuple in self.bombs:
                random_row = random_number = random.randint(1, self.row)
                random_cul = random_number = random.randint(1, self.cul)
                bomb_tuple = (random_row, random_cul)
            self.bombs.append(bomb_tuple)
            self.board[random_row][random_cul] = 9
    def neighbors(self):
        counter = 0
        for i in range(1, self.row+1):
            for j in range(1,self.cul+1):
                if(self.board[i][j]!=9):
                    for m in range(i-1,i+2):
                        for k in range(j-1, j+2):
                            if(i != m or j != k):
                                if(self.board[m][k] == 9):
                                    counter+=1
                    self.board[i][j] = counter
                    counter = 0
    def change_board(self):
        self.board = np.delete(self.board, 0 , axis=0)
        self.board = np.delete(self.board, self.row , axis=0)
        self.board = np.delete(self.board, 0 , axis=1)
        self.board = np.delete(self.board, self.cul , axis=1)
        return self.board


class Grafic_Board(App):

    def build(self):
        b1 = Board()
        b1.create_bombs()
        b1.neighbors()
        self.board = b1.change_board()
        self.num_row = self.board.shape[0]
        self.num_cul = self.board.shape[1]
        self.buttons = []
        self.revealed_zeros = []
        self.win_board = []
        self.win_board = self.board.copy()
        self.layout = GridLayout(cols=self.num_cul)
        for i in range(self.num_row):
            for j in range(self.num_cul):
                button = Button(background_normal='GUI_images/background.jpg', font_size=1)
                button.bind(on_press=self.change_pic)
                button.pos_hint = {'center_x': (i), 'center_y': (j)}
                self.layout.add_widget(button)
                self.buttons.append(button)
        self.buttons = [self.buttons[i:i + self.num_cul] for i in range(0, len(self.buttons), self.num_cul)]
        return self.layout

    def change_pic(self, instance):
        self.row = instance.pos_hint['center_x']
        self.cul = instance.pos_hint['center_y']
        if self.board[self.row][self.cul] == 9:
            self.show_bombs()
            self.lose_massage()
        elif self.board[self.row][self.cul] > 0:
            self.reveal_pos()
        else:
            self.reveal_all_zeros(self.row, self.cul)
        self.check_win()


    def show_bombs(self):
        for i in range(self.num_row):
            for j in range(self.num_cul):
                if(self.board[i][j] == 9):
                    self.buttons[i][j].background_normal = 'GUI_images/bomb.jpg'


    def reveal_pos(self):
        num = self.board[self.row][self.cul]
        self.buttons[self.row][self.cul].background_normal = f'GUI_images/number_{num}.jpg'
        self.win_board[self.row][self.cul] = -1


    def reveal_all_zeros(self, row, cul):
        self.buttons[row][cul].background_normal = f'GUI_images/number_0.jpg'
        self.win_board[row][cul] = -1
        tuple = (row, cul)
        self.revealed_zeros.append(tuple)
        for i in range(self.num_row):
            for j in range(self.num_cul):
                if i > row-2 and i<row+2 and j>cul-2 and j<cul+2 and (i!=row or j!=cul):
                    if self.board[i][j] ==0 and (i, j) not in self.revealed_zeros:
                        self.reveal_all_zeros(i, j)
                    else:
                        num = self.board[i][j]
                        self.buttons[i][j].background_normal = f'GUI_images/number_{num}.jpg'
                        self.win_board[i][j] = -1


    def check_win(self):
        async def check_win():
            bool = True
            for i in range(self.num_row):
                for j in range(self.num_cul):
                    if(self.win_board[i][j] != 9 and self.win_board[i][j] != -1):
                        bool = False
            if bool == True:
                await asynckivy.sleep(2)
                self.layout.clear_widgets()
                win_label = Label(text = "YOU WON!", font_size=100)
                self.layout.add_widget(win_label)
                await asynckivy.sleep(4)
                Window.close()
        asynckivy.start(check_win())

    def lose_massage(self):
        async def lose_massage():
            await asynckivy.sleep(3)
            self.layout.clear_widgets()
            lost_label = Label(text = "YOU LOST!", font_size=100)
            self.layout.add_widget(lost_label)
            await asynckivy.sleep(4)
            Window.close()
        asynckivy.start(lose_massage())


if __name__ == "__main__":
    Grafic_Board().run()




