import sys
import sqlite3
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)

conn = sqlite3.connect('Visechki.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS tab_vis(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    razmer TEXT,
    shape TEXT,
    width INTEGER,
    length INTEGER,
    streams TEXT,
    elements_in_stream TEXT,
    shaft TEXT
)''')
conn.commit()


class visechki(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('База высечек')  # Название окна
        self.setGeometry(600, 250, 300, 100)  # Зададим параметры окна приложения

        self.find_vis = QPushButton('Поиск высечек', self)  # Кнопка для поиска высечки
        self.find_vis.clicked.connect(self.show_find_vis)

        self.add_vis = QPushButton('Добавить высечку', self)  # Кнопка для добавления высечки
        self.add_vis.clicked.connect(self.show_add_vis)

        # Рассположим кнопки по вертикали
        self.hbox = QVBoxLayout()
        self.hbox.addWidget(self.find_vis)
        self.hbox.addWidget(self.add_vis)

        self.setLayout(self.hbox)

    # метод вызова окна поиск высечек при нажатии на кнопку
    def show_find_vis(self):
        self.w2 = find_vis()
        self.w2.show()
        self.hide()

    # метод вызова окна добавить высечку при нажатии на кнопку
    def show_add_vis(self):
        self.w2 = add_vis()
        self.w2.show()
        self.hide()


# Создадим окно, которое покажется при нажатии на поиск высечек
class find_vis(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Поиск высечек')
        self.setGeometry(600, 250, 300, 120)

        self.vvod = QPushButton('Введите параметры высечки', self)
        self.vvod.resize(280, 30)
        self.vvod.move(10, 10)

        self.width = QLineEdit(self)  # Ширина высечки
        self.width.resize(50, 20)
        self.width.move(80, 50)
        self.width_lab = QLabel(self)
        self.width_lab.setText('Ширина (B):')
        self.width_lab.resize(50, 20)
        self.width_lab.move(20, 50)

        self.length = QLineEdit(self)  # Длина высечки
        self.length.resize(50, 20)
        self.length.move(220, 50)
        self.length_lab = QLabel(self)
        self.length_lab.setText('Длина (L):')
        self.length_lab.resize(50, 20)
        self.length_lab.move(170, 50)

        self.shape = QComboBox(self)  # форма высечки
        self.shape.addItems(["Прямоугольник", "Круг", "Овал", "Фигурная", "Пояс"])
        self.shape.resize(280, 30)
        self.shape.move(10, 10)

        self.find_vis = QPushButton("Искать высечку", self)
        self.find_vis.resize(280, 30)
        self.find_vis.move(10, 80)
        self.find_vis.clicked.connect(self.poisk)

    #Метод, который ищет высечки соответсвующие введеным параметрам
    def poisk(self):
        self.width_f = self.width.text() #Ширина
        self.length_f = self.length.text() #Длина
        self.shape_f = self.shape.currentText() #Форма

        # Поиск высечки в базе данных
        if len(self.width_f) == 0 or len(self.length_f) == 0:
            cursor.execute(f'''SELECT shape FROM tab_vis WHERE shape = "{self.shape_f}"''')
            if cursor.fetchone() is None:
                tab_result = []
                conn.commit()
            else:
                cursor.execute(f'''SELECT * FROM tab_vis WHERE shape = "{self.shape_f}"''')
                tab_result = cursor.fetchall()
                conn.commit()
        else:
            cursor.execute(f'''SELECT shape, width, length FROM tab_vis
                    WHERE shape = "{self.shape_f}" AND width = {self.width_f} AND length = {self.length_f}''')
            chek_vvod = cursor.fetchall()
            if len(chek_vvod) == 0:
                cursor.execute(f'''SELECT * FROM tab_vis
                        WHERE shape = "{self.shape_f}" AND width >= {int(self.width_f) - 10} 
                        AND width <= {int(self.width_f) + 10}
                        AND length >= {int(self.length_f) - 10} AND length <={int(self.length_f) + 10}''')
                tab_result = cursor.fetchall()
                conn.commit()
            else:
                cursor.execute(f'''SELECT * FROM tab_vis
                        WHERE shape = "{self.shape_f}" AND width = {self.width_f} AND length = {self.length_f}''')
                tab_result = cursor.fetchall()
                conn.commit()

        self.w3 = result(tab_result)
        self.w3.show()

# Создаем окно с таблицей (вывод результата запроса)
class result(QWidget):
    def __init__(self, tab_res):
        self.tab_result = tab_res
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Результат')
        self.setGeometry(100, 100, 900, 400)
        self.creatingTables()

    #Создаем таблицу
    def creatingTables(self):
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setColumnWidth(10, 100)
        self.tableWidget.setRowCount(len(self.tab_result))
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID",
             "Размер",
             "Форма",
             "Ширина",
             "Длина",
             "Ручьи",
             """Элементы
в ручье""",
             "Вал"]
        )

        # Наполняем таблицу
        for r in range(len(self.tab_result)):
            self.tableWidget.setItem(r, 0, QTableWidgetItem(str(self.tab_result[r][0])))
            self.tableWidget.setItem(r, 1, QTableWidgetItem(self.tab_result[r][1]))
            self.tableWidget.setItem(r, 2, QTableWidgetItem(self.tab_result[r][2]))
            self.tableWidget.setItem(r, 3, QTableWidgetItem(str(self.tab_result[r][3])))
            self.tableWidget.setItem(r, 4, QTableWidgetItem(str(self.tab_result[r][4])))
            self.tableWidget.setItem(r, 5, QTableWidgetItem(self.tab_result[r][5]))
            self.tableWidget.setItem(r, 6, QTableWidgetItem(self.tab_result[r][6]))
            self.tableWidget.setItem(r, 7, QTableWidgetItem(self.tab_result[r][7]))

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.tableWidget)
        self.setLayout(self.vBoxLayout)

# Создадим окно, которое покажется при нажатии на добавить высечку
class add_vis(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добавить высечку')
        self.setGeometry(600, 250, 300, 220)

        self.label = QLabel(self)
        self.label.setText('')
        self.label.resize(200, 30)
        self.label.move(70, 140)

        self.width = QLineEdit(self)  # Ширина высечки
        self.width.resize(50, 20)
        self.width.move(70, 50)
        self.width_lab = QLabel(self)
        self.width_lab.setText('Ширина (B):')
        self.width_lab.resize(50, 20)
        self.width_lab.move(10, 50)

        self.length = QLineEdit(self)  # Длина высечки
        self.length.resize(50, 20)
        self.length.move(220, 50)
        self.length_lab = QLabel(self)
        self.length_lab.setText('Длина (L):')
        self.length_lab.resize(50, 20)
        self.length_lab.move(180, 50)

        self.shape = QComboBox(self)  # форма высечки
        self.shape.addItems(["Прямоугольник", "Круг", "Овал", "Фигурная", "Пояс"])
        self.shape.resize(280, 30)
        self.shape.move(10, 10)

        self.streams = QLineEdit(self)  # Количество ручьев
        self.streams.resize(50, 20)
        self.streams.move(60, 80)
        self.streams_lab = QLabel(self)
        self.streams_lab.setText('Ручьи:')
        self.streams_lab.resize(50, 20)
        self.streams_lab.move(10, 80)

        self.elements_in_stream = QLineEdit(self)  # количество элементов в ручье
        self.elements_in_stream.resize(50, 20)
        self.elements_in_stream.move(220, 80)
        self.elements_in_stream_lab = QLabel(self)
        self.elements_in_stream_lab.setText('Элементы в ручье:')
        self.elements_in_stream_lab.resize(100, 20)
        self.elements_in_stream_lab.move(120, 80)

        self.shaft = QLineEdit(self)  # Вал для высечки
        self.shaft.resize(50, 20)
        self.shaft.move(130, 110)
        self.shaft_lab = QLabel(self)
        self.shaft_lab.setText('Вал:')
        self.shaft_lab.resize(50, 20)
        self.shaft_lab.move(100, 110)

        self.add_vis = QPushButton("Добавить высечку", self)
        self.add_vis.resize(280, 30)
        self.add_vis.move(10, 180)
        self.add_vis.clicked.connect(self.reg_vis)

    # Создадим метод для добавления высечки в базу данных
    def reg_vis(self):
        razmer = str(self.width.text()) + 'x' + str(self.length.text())
        width_add = self.width.text()
        length_add = self.length.text()
        shape_add = self.shape.currentText()
        streams_add = str(self.streams.text())
        elements_in_stream_add = str(self.elements_in_stream.text())
        shaft_add = str(self.shaft.text())

        # Проверим все пустые строки, чтобы они не были пустыми
        if len(width_add) == 0:
            return

        if len(length_add) == 0:
            return

        if len(streams_add) == 0:
            return

        if len(elements_in_stream_add) == 0:
            return

        if len(shaft_add) == 0:
            return

        cursor.execute(f'SELECT shape, razmer FROM tab_vis WHERE shape="{shape_add}" AND razmer="{razmer}"')
        if cursor.fetchone() is None:
            cursor.execute(f'INSERT INTO tab_vis (razmer, shape, width, length, streams, elements_in_stream, shaft)'
                           f'VALUES ("{razmer}", "{shape_add}", "{(width_add)}", "{(length_add)}",'
                           f'"{streams_add}", "{elements_in_stream_add}", "{shaft_add}")')
            self.label.setText(f'Высечка {razmer} добавлена в базу')
            conn.commit()
        else:
            cursor.execute(f'SELECT razmer FROM tab_vis WHERE razmer="{razmer}"')
            if cursor.fetchone() is None:
                cursor.execute(
                    f'INSERT INTO tab_vis (razmer, shape, width, length, streams, elements_in_stream, shaft)'
                    f'VALUES ("{razmer}", "{shape_add}", "{width_add}", "{length_add}",'
                    f'"{streams_add}", "{elements_in_stream_add}", "{shaft_add}")')
                self.label.setText(f'Высечка {razmer} добавлена в базу')
                conn.commit()
            else:
                cursor.execute(f'SELECT streams FROM tab_vis WHERE streams="{streams_add}"')
                if cursor.fetchone() is None:
                    cursor.execute(
                        f'INSERT INTO tab_vis (razmer, shape, width, length, streams, elements_in_stream, shaft)'
                        f'VALUES ("{razmer}", "{shape_add}", "{width_add}", "{length_add}",'
                        f'"{streams_add}", "{elements_in_stream_add}", "{shaft_add}")')
                    self.label.setText(f'Высечка {razmer} добавлена в базу')
                    conn.commit()
                else:
                    cursor.execute(f'SELECT elements_in_stream FROM tab_vis '
                                   f'WHERE elements_in_stream="{elements_in_stream_add}"')
                    if cursor.fetchone() is None:
                        cursor.execute(
                            f'INSERT INTO tab_vis (razmer, shape, width, length, streams, elements_in_stream, shaft)'
                            f'VALUES ("{razmer}", "{shape_add}", "{width_add}", "{length_add}",'
                            f'"{streams_add}", "{elements_in_stream_add}", "{shaft_add}")')
                        self.label.setText(f'Высечка {razmer} добавлена в базу')
                        conn.commit()
                    else:
                        cursor.execute(f'SELECT shaft FROM tab_vis WHERE shaft="{shaft_add}"')
                        if cursor.fetchone() is None:
                            cursor.execute(
                                f'INSERT INTO tab_vis (razmer, shape, width, length, streams, elements_in_stream, shaft)'
                                f'VALUES ("{razmer}", "{shape_add}", "{width_add}", "{length_add}",'
                                f'"{streams_add}", "{elements_in_stream_add}", "{shaft_add}")')
                            self.label.setText(f'Высечка {razmer} добавлена в базу')
                            conn.commit()
                        else:
                            self.label.setText('Такая высечка уже существует')

        self.width.clear()
        self.length.clear()
        self.streams.clear()
        self.elements_in_stream.clear()
        self.shaft.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = visechki()
    ex.show()
    sys.exit(app.exec())
