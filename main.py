import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem

EDIT_MODE = 1
ADD_MODE = 0


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle('Капучино')
        self.setGeometry(300, 100, 800, 800)


    def load_data(self):
        con = sqlite3.connect('coffee.splite.db')
        cur = con.cursor()
        self.data = cur.execute("""SELECT * FROM espresso""").fetchall()

    def init_ui(self):
        uic.loadUi('main.ui', self)
        self.addBut.clicked.connect(self.addcoffe)
        self.editBut.clicked.connect(self.editcoffe)
        self.load_data()
        self.table()

    def get_current_films_id(self):
        row = int(self.tableWidget.currentRow())
        if row == -1:
            return -1
        else:
            return self.tableWidget.item(row, 0).text()

    def table(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels([
            'ID', 'title', 'roast_degree', 'type', 'taste', 'price', 'V'
        ])
        self.tableWidget.setRowCount(0)
        for row in range(len(self.data)):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for col in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(self.data[row][col])))
                
    def addcoffe(self):
        self.show_window_addEdit(ADD_MODE, 3)
        
    def editcoffe(self):
        s = self.get_current_films_id()
        if s != -1:
            self.show_window_addEdit(EDIT_MODE, s)

    def show_window_addEdit(self, mode, index_id):
        try:
            self.w2 = MyWidget2(mode, index_id)
        except BaseException as error:
            print(error)
        self.w2.show()


class MyWidget2(QMainWindow):
    def __init__(self, mode, index_id):
        self.index_id, self.mode = int(index_id), int(mode)
        self.button_text = ('Добавить', 'Изменить', 'Удалить')
        self.header_text = ('Добавление кофе', 'Изменение кофе', 'Удаление кофе')
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle(self.header_text[self.mode])
        self.pushButton.setText(self.button_text[self.mode])
        self.pushButton.clicked.connect(self.run)
        if mode == EDIT_MODE:
            self.LoadCurrentCoffe(index_id)

    def LoadCurrentCoffe(self, index):
        # print(index)
        self.con = sqlite3.connect("coffee.splite.db")
        cur = self.con.cursor()
        index = int(index)
        result = cur.execute(f"""SELECT DISTINCT * FROM espresso WHERE id = '{index}'""").fetchall()
        self.con.close()
        # print(result)
        self.title.setText(str(result[0][1]))
        self.roast_degree.setText(str(result[0][2]))
        self.type.setText(str(result[0][3]))
        self.taste.setText(str(result[0][4]))
        self.price.setText(str(result[0][5]))
        self.V.setText(str(result[0][6]))
        
    def run(self):
        title = str(self.title.text())
        roast_degree = str(self.roast_degree.text())
        type_ = str(self.type.text())
        taste = str(self.taste.text())
        price = str(self.price.text())
        v = str(self.V.text())
        
        self.con = sqlite3.connect("coffee.splite.db")
        cur = self.con.cursor()
        if self.mode == ADD_MODE:
            result = cur.execute("""SELECT DISTINCT id FROM espresso ORDER BY id DESC""").fetchone()
            new_id = int(result[0]) + 1
            p = f"""INSERT INTO espresso (ID, title, roast_degree, type, taste, price, V) VALUES ({new_id},
            '{title}', '{roast_degree}', '{type_}', '{taste}', '{price}', '{v}')"""

        elif self.mode == EDIT_MODE:
            p = f"""UPDATE espresso SET title='{title}', roast_degree='{roast_degree}',
        type='{type_}', taste='{taste}', price='{price}', V='{v}' WHERE id = {self.index_id}"""

        elif self.mode == DELETE_MODE:
            p = f"""DELETE FROM films WHERE id = {self.index_id}"""

        try:
            cur.execute(p)
        except sqlite3.Error as error:
            print(error)
        self.con.commit()
        self.con.close()
        ex.load_data()
        ex.table()
        self.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())


