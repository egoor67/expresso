import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidget, QTableWidgetItem, \
    QVBoxLayout
from PyQt5 import uic


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def data(self):
        con = sqlite3.connect('coffee.splite.db')
        cur = con.cursor()
        self.data = cur.execute("""
        SELECT * FROM espresso
        """).fetchall()

    def init_ui(self):
        uic.loadUi('main.ui', self)
        self.v_layout = QVBoxLayout(self)
        self.tableWidget = QTableWidget(self)
        self.v_layout.addWidget(self.tableWidget)
        self.data()
        self.table()

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

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Эсспрессо')
        self.setGeometry(300, 100, 800, 800)
        widget = MyWidget()
        self.setCentralWidget(widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
