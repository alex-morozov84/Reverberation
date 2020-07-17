import sys
from PyQt5.QtWidgets import *
# следующие две библиотеки для отображения графиков
from PyQt5.QtChart import *
from PyQt5.QtGui import QPainter

# для отображения легенды графика внизу
from PyQt5.QtCore import Qt

import sqlite3
import pandas as pd
import math
import Style

con = sqlite3.connect('options.db')
cur = con.cursor()

i = 1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Назначаем центральный виджет, чтоб он отображался в QMainWindow. Далее надо назначить ему основной layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle('Расчет времени реверберации')
        self.setStyleSheet(Style.main())
        self.ui()
        self.showMaximized()

    def ui(self):
        self.excel_parsing()
        self.widgets()
        self.layouts()
        self.data_from_db()

    def widgets(self):
        # self.title = QLabel('Введите параметры помещения')
        self.length = QLineEdit()
        self.length.setPlaceholderText('Введите длину')
        self.length.setFixedWidth(130)
        self.width = QLineEdit()
        self.width.setPlaceholderText('Введите ширину')
        self.width.setFixedWidth(130)
        self.height = QLineEdit()
        self.height.setPlaceholderText('Введите высоту')
        self.height.setFixedWidth(130)
        self.walls = QComboBox()
        self.walls.setFixedWidth(500)
        self.ceiling = QComboBox()
        self.ceiling.setFixedWidth(500)
        self.floor = QComboBox()
        self.floor.setFixedWidth(500)

        # виджеты окон
        self.window_label = QLabel('Выберите тип окон')
        self.window_type = QComboBox()
        self.window_square_label = QLabel('Введите площадь окна, м\u00b2')
        self.window_square = QLineEdit()
        self.window_square.setFixedWidth(50)
        self.window_quant_label = QLabel('Введите количество окон')
        self.window_quant = QLineEdit()
        self.window_quant.setFixedWidth(40)

        # виджеты дверей
        self.door_label = QLabel('Выберите тип дверей')
        self.door_type = QComboBox()
        self.door_square_label = QLabel('Введите площадь двери, м\u00b2')
        self.door_square = QLineEdit()
        self.door_square.setFixedWidth(50)
        self.door_quant_label = QLabel('Введите количество дверей')
        self.door_quant = QLineEdit()
        self.door_quant.setFixedWidth(40)

        # виджеты предметов интерьера
        self.interior_label = QLabel('Выберите предмет интерьера')
        self.interior_choose = QComboBox()
        self.interior_quant_label = QLabel('Введите количество')
        self.interior_quant = QLineEdit()
        self.interior_quant.setFixedWidth(40)

        # Кнопка для добавления (удаления) еще одной строчки с интерьером
        self.add_interior_label = QLabel('Добавить предмет интерьера')
        # self.add_interior_label.setFixedWidth(220)
        self.add_interior_button = QPushButton('Добавить')
        self.add_interior_button.setObjectName("addInteriorBtn")
        self.add_interior_button.setFixedWidth(100)
        self.add_interior_button.clicked.connect(self.add_interior_func)
        self.interior_delete_label = QLabel('Удалить предмет интерьера')
        self.interior_delete_button = QPushButton('Удалить')
        self.interior_delete_button.setObjectName("addInteriorBtn")
        self.interior_delete_button.setFixedWidth(100)
        self.interior_delete_button.clicked.connect(self.interior_delete_func)

        # виджеты людей
        self.people = QLabel('Количество людей в помещении:')
        self.people.setFixedWidth(250)
        self.people_quant = QComboBox()
        self.people_quant.setFixedWidth(40)
        self.people_quant.addItems(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        self.people_blank = QLabel()

        # Кнопка расчет и результаты
        self.result_button = QPushButton('Расчёт')
        self.result_button.clicked.connect(self.result_func)
        self.result_button.setObjectName("resultBtn")
        self.result_button.setFixedWidth(300)
        # self.result_empty = QLabel()
        # self.result_full = QLabel()
        # self.result_empty_people = QLabel()
        # self.result_full_without_people = QLabel()
        
    def layouts(self):
        self.window_layout = QHBoxLayout()

        self.left_layout = QVBoxLayout()
        self.options_layout = QFormLayout()
        self.door_window_layout = QGridLayout()
        self.interior_layout = QGridLayout()
        self.blank_layout = QHBoxLayout()

        self.rigth_layout = QVBoxLayout()
        self.people_layout = QHBoxLayout()
        self.result_btn_layout = QHBoxLayout()
        self.result_layout = QFormLayout()

        self.window_layout.addLayout(self.left_layout, 65)
        self.window_layout.addLayout(self.rigth_layout, 35)

        self.options_group = QGroupBox('Параметры помещения')
        self.options_group.setLayout(self.options_layout)
        self.options_group.setStyleSheet(Style.options_group())
        self.options_group.setFixedHeight(340)

        self.doors_and_windows_group = QGroupBox('Окна и двери')
        self.doors_and_windows_group.setLayout(self.door_window_layout)
        self.doors_and_windows_group.setStyleSheet(Style.doors_and_windows_group())
        self.doors_and_windows_group.setFixedHeight(150)

        self.interior_group = QGroupBox('Интерьер')
        self.interior_group.setLayout(self.interior_layout)
        self.interior_group.setStyleSheet(Style.interior_group())

        self.people_group = QGroupBox('Люди в помещении')
        self.people_group.setLayout(self.people_layout)
        self.people_group.setStyleSheet(Style.people_group())
        self.people_group.setFixedHeight(100)

        # для того, чтобы правая часть сдвинулась вверх
        self.blank_group = QGroupBox()
        self.blank_group.setLayout(self.result_layout)
        self.blank_group.setStyleSheet(Style.blank_group())

        self.left_layout.addWidget(self.options_group)
        self.left_layout.addWidget(self.doors_and_windows_group)
        self.left_layout.addWidget(self.interior_group)
        self.left_layout.addLayout(self.blank_layout, 30)

        self.rigth_layout.addWidget(self.people_group)
        self.rigth_layout.addLayout(self.result_btn_layout)
        self.rigth_layout.addWidget(self.blank_group)

        # Основные параметры помещения
       
        self.options_layout.addRow(QLabel('Длина помещения, м'), self.length)
        self.options_layout.addRow(QLabel('Ширина помещения, м'), self.width)
        self.options_layout.addRow(QLabel('Высота помещения, м'), self.height)
        self.options_layout.addRow(QLabel('Выберите тип покрытия стен'), self.walls)
        self.options_layout.addRow(QLabel('Выберите тип покрытия пола'), self.floor)
        self.options_layout.addRow(QLabel('Выберите тип покрытия потолка'), self.ceiling)

        # Задаем двери и окна (сетка)
        self.door_window_layout.addWidget(self.door_label, 0, 0)
        self.door_window_layout.addWidget(self.door_type, 0, 1)
        self.door_window_layout.addWidget(self.door_square_label, 0, 2)
        self.door_window_layout.addWidget(self.door_square, 0, 3)
        self.door_window_layout.addWidget(self.door_quant_label, 0, 4)
        self.door_window_layout.addWidget(self.door_quant, 0, 5)
        self.door_window_layout.addWidget(self.window_label, 1, 0)
        self.door_window_layout.addWidget(self.window_type, 1, 1)
        self.door_window_layout.addWidget(self.window_square_label, 1, 2)
        self.door_window_layout.addWidget(self.window_square, 1, 3)
        self.door_window_layout.addWidget(self.window_quant_label, 1, 4)
        self.door_window_layout.addWidget(self.window_quant, 1, 5)

        # Задаем предметы интерьера (первая строка, остальные по нажатию)
        self.interior_layout.addWidget(self.interior_label, 0, 0)
        self.interior_layout.addWidget(self.interior_choose, 0, 1)
        self.interior_layout.addWidget(self.interior_quant_label, 0, 2)
        self.interior_layout.addWidget(self.interior_quant, 0, 3)

        # Задаем количество людей в помещении
        self.people_layout.addWidget(self.people)
        self.people_layout.addWidget(self.people_quant)
        self.people_layout.addWidget(self.people_blank)

        # Кнопка для добавления предметов интерьера
        self.interior_layout.addWidget(self.add_interior_label, 10, 0)
        self.interior_layout.addWidget(self.add_interior_button, 10, 1)
        self.interior_layout.addWidget(self.interior_delete_label, 10, 2)
        self.interior_layout.addWidget(self.interior_delete_button, 10, 3)

        # Кнопка подсчета результатов
        self.result_btn_layout.addWidget(self.result_button)  

        # Применяем layout именно к виджету, который назначили в самаом начале ЦЕНТРАЛЬНЫМ
        self.main_widget.setLayout(self.window_layout)

    def excel_parsing(self):
        # Парсим Excel файл с данными, получаем DataFrame на каждую страницу

        # старый файл со средними значениями a
        # xl = pd.ExcelFile('sound_absorption.xlsx')

        # # файл со значениями a по частотам
        xl = pd.ExcelFile('sound_absorption_freaq.xlsx')
        df_walls = xl.parse('Walls')
        df_ceiling = xl.parse('Ceiling')
        df_floor = xl.parse('Floor')
        df_interior = xl.parse('Interior')
        df_window = xl.parse('Window')
        df_door = xl.parse('Door')
        df_other = xl.parse('Other')

        # Помещаем DF в нужную таблицу в БД
        df_walls.to_sql('walls', con, if_exists='replace')
        df_ceiling.to_sql('ceiling', con, if_exists='replace')
        df_floor.to_sql('floor', con, if_exists='replace')
        df_interior.to_sql('interior', con, if_exists='replace')
        df_window.to_sql('window', con, if_exists='replace')
        df_door.to_sql('door', con, if_exists='replace')
        df_other.to_sql('other', con, if_exists='replace')
        con.commit()

    # получаем виды поверхностей и интерьера из БД и вставляем в списки
    def data_from_db(self):

        # Заполняем каждый комбобокс данными из БД
        def combobox_creation(surface, surface_to_combobox):
            query = cur.execute("SELECT material FROM {}".format(surface))
            options = []
            for materail in query:
                options += materail
            surface_to_combobox.addItems(options)

        combobox_creation('walls', self.walls)
        combobox_creation('ceiling', self.ceiling)
        combobox_creation('floor', self.floor)
        combobox_creation('interior', self.interior_choose)
        combobox_creation('window', self.window_type)
        combobox_creation('door', self.door_type)

    # добавляем дополнительные элементы интерьера при нажатии на кнопку
    def add_interior_func(self):

        global i

        if i > 7:
            QMessageBox.information(self, 'Внимание!', 'Можно добавить не более 8 предметов интерьера')
        # В случае, если удалили все строки кнопкой, а потом добавили, то в первой должна создаться надпись
        elif i == 0:
            # Надо в каждом цикле (после очередного нажатия кнопки) заново создавать эти переменные, иначе они не отображаются. Вначале создал в при объявлении всех виджетов, и их же пытался пересоздать. Но так, видимо, нельзя!
            self.add_interior_label = QLabel('Добавить предмет интерьера')
            self.interior_choose = QComboBox()
            self.interior_quant_label = QLabel('Введите количество')
            self.interior_quant = QLineEdit()
            self.interior_quant.setFixedWidth(40)

            self.interior_layout.addWidget(self.add_interior_label, 0, 0)
            self.interior_layout.addWidget(self.interior_choose, 0, 1)
            self.interior_layout.addWidget(self.interior_quant_label, 0, 2)
            self.interior_layout.addWidget(self.interior_quant, 0, 3)
            self.interior_layout.addWidget(self.interior_delete_label, 10, 2)
            self.interior_layout.addWidget(self.interior_delete_button, 10, 3)

            # Добавляем данные в сформированные списки
            query = cur.execute("SELECT material FROM interior")
            options = []
            for materail in query:
                options += materail
            self.interior_choose.addItems(options)

            i += 1

        else:
            # Надо в каждом цикле (после очередного нажатия кнопки) заново создавать эти переменные, иначе они не отображаются. Вначале создал в при объявлении всех виджетов, и их же пытался пересоздать. Но так, видимо, нельзя!
            self.interior_choose = QComboBox()
            self.interior_quant_label = QLabel('Введите количество')
            self.interior_quant = QLineEdit()
            self.interior_quant.setFixedWidth(40)

            self.interior_layout.addWidget(self.interior_choose, i, 1)
            self.interior_layout.addWidget(self.interior_quant_label, i, 2)
            self.interior_layout.addWidget(self.interior_quant, i, 3)

            # Добавляем данные в сформированные списки
            query = cur.execute("SELECT material FROM interior")
            options = []
            for materail in query:
                options += materail
            self.interior_choose.addItems(options)

            i += 1
    
    # Удалене строк интерьера по кнопке (для случая только первой строки надо удалить еще и подпись)
    def interior_delete_func(self):
        global i

        # self.interior_layout.removeWidget(self.interior_choose)
        if i > 1:
            self.interior_layout.itemAtPosition(i - 1, 3).widget().setParent(None)
            self.interior_layout.itemAtPosition(i - 1, 2).widget().setParent(None)
            self.interior_layout.itemAtPosition(i - 1, 1).widget().setParent(None)
            i -= 1

        elif i == 1:
            self.interior_layout.itemAtPosition(i - 1, 0).widget().setParent(None)
            self.interior_layout.itemAtPosition(i - 1, 3).widget().setParent(None)
            self.interior_layout.itemAtPosition(i - 1, 2).widget().setParent(None)
            self.interior_layout.itemAtPosition(i - 1, 1).widget().setParent(None)
            # Удаление кнопки и надписи "Удалить", когда не осталось ни одного предмета
            self.interior_layout.itemAtPosition(10, 2).widget().setParent(None)
            self.interior_layout.itemAtPosition(10, 3).widget().setParent(None)

            i -= 1

    def result_func(self):

        global i

        # Функция проверки на то, что введенное число - целое (используем ниже для проверки количества)
        def isreal(value):
            try:
                int(value)
                return False
            except:
                return True
       
        # Функция проверки на то, что введено число
        def is_digit(string):
            if string.isdigit():
                return True
            else:
                try:
                    float(string)
                    return True
                except:
                    return False

        # Заменяем во всех полях запятую на точку (чтоб не было ошибок с числами)
        parameters = [self.length.text(), self.height.text(), self.width.text(), self.door_square.text(), self.door_quant.text(), self.window_square.text(), self.window_quant.text()]
        parameters_checked = []
        for param in parameters:
            param_checked = param.replace(',', '.')
            parameters_checked.append(param_checked)

        # Проверяем, чтоб все было заполнено (кроме количеств предметов интерьера, оно дальше). Проверяем по всем полям, чтоб не было пустого. Если пусто, цикл прерываем и технической переменной Х присваиваем 5. 
        for param_checked in parameters_checked:
            x = 0
            if param_checked == '' or not is_digit(param_checked):
                x = 5
                break
        # Если Х = 5, значит одно из полей было пустое, выводим сообщение. Если Х != 5, то считаем результат
        # Также проверяем, что количество - целое число
        if x == 5 or isreal(parameters_checked[4]) or isreal(parameters_checked[6]):
            QMessageBox.information(self, 'Внимание!', 'Введите ВСЕ основные параметры помещения. Количество должно быть целым числом!')
        else:
            
            # Проверяем по всем строкам с интерьером, чтоб не было пустого количества. Если пусто, цикл прерываем и технической переменной Х присваиваем 5
            # Также проверяем, что количество - целое число
            for inter in range(0, i):
                if (self.interior_layout.itemAtPosition(inter, 3).widget().text() == '' or isreal(self.interior_layout.itemAtPosition(inter, 3).widget().text())):
                    print('ok3')
                    x = 5
                    break
            # Если Х = 5, значит одно из полей с количеством предметов интерьера было пустое, выводим сообщение. Если Х != 5, то считаем результат
            
            if x == 5:
                QMessageBox.information(self, 'Внимание!', 'Введите количество ВСЕХ предметов интерьера (целое число!)')
            else:

                # считаем объем помещения. Вначале строки превращаем в вещественные числа. Затем перемножаем. Потом округляем до 2х знаков
                v = round((float(parameters_checked[0]) * float(parameters_checked[1])) * float(parameters_checked[2]), 2)
                # площадь пола
                s_floor = round((float(parameters_checked[0]) * float(parameters_checked[2])), 2)
                # площадь стен (учитываем площадь окон и дверей)
                s_walls = round((float(parameters_checked[0]) + float(parameters_checked[2]) ) * 2 * float(parameters_checked[1]) - float(parameters_checked[3]) * int(parameters_checked[4]) - float(parameters_checked[5])*int(parameters_checked[6]), 2)
                # площадь дверей:
                s_door = round((float(parameters_checked[3]) * int(parameters_checked[4])), 2)
                # площадь окон:
                s_window = round((float(parameters_checked[5]) * int(parameters_checked[6])), 2)


                # # Расчет для средних значений a (работает только, если выбрать xl = pd.ExcelFile('sound_absorption.xlsx') в строке 212, а # xl = pd.ExcelFile('sound_absorption_freaq.xlsx') закомментировать)
                # # получаем коэф-ты звукопогл (а) для всего из БД в зависимости от того, что выбрано в списке
                # # для пола:
                # floor_material = self.floor.currentText()
                # query = "SELECT a FROM floor WHERE material = ?"
                # floor_a = (cur.execute(query, (floor_material,)).fetchone())[0]
                # # для потолка:
                # ceiling_material = self.ceiling.currentText()
                # query = "SELECT a FROM ceiling WHERE material = ?"
                # ceiling_a = (cur.execute(query, (ceiling_material,)).fetchone())[0]
                # # для стен:
                # wall_material = self.walls.currentText()
                # query = "SELECT a FROM walls WHERE material = ?"
                # wall_a = (cur.execute(query, (wall_material,)).fetchone())[0]
                # # для окон:
                # window_material = self.window_type.currentText()
                # query = "SELECT a FROM window WHERE material = ?"
                # window_a = (cur.execute(query, (window_material,)).fetchone())[0]
                # # для дверей:
                # door_material = self.door_type.currentText()
                # query = "SELECT a FROM door WHERE material = ?"
                # door_a = (cur.execute(query, (door_material,)).fetchone())[0]

                # # площадь * ln(1-a) для каждой поверхности
                # s_floor_ln = round((s_floor * math.log(1 - floor_a)), 2)
                # s_ceiling_ln = round((s_floor * math.log(1 - ceiling_a)), 2)
                # s_wall_ln = round((s_walls * math.log(1 - wall_a)), 2)
                # s_door_ln = round((s_door * math.log(1 - door_a)), 2)
                # s_window_ln = round((s_window * math.log(1 - window_a)), 2)

                # # расчет * ln(1-a) для всех деталей интерьера сразу. Зависит от i, которая меняется в зависимости от количества строк с деталями интерьера. Затем для каждой детали считается * ln(1-a), умножается на количество таких деталей. Далее все детали суммируются:
                # s_interior_ln = 0
                # for inter in range(0, i):
                #     interior_item = self.interior_layout.itemAtPosition(inter, 1).widget().currentText()
                #     query = "SELECT a FROM interior WHERE material = ?"
                #     interior_a = (cur.execute(query, (interior_item,)).fetchone())[0]
                #     interior_item_quant = int(self.interior_layout.itemAtPosition(inter, 3).widget().text())
                #     s_interior_ln += round((interior_item_quant * math.log(1 - interior_a)), 2)

                # # расчет * ln(1-a) для людей в помещении в зависимости от их количества. Коэфф-т взят стандартный: 0.45
                # s_people = round((int(self.people_quant.currentText()) * math.log(1 - 0.45)), 2)

                # # время реверберации в пустом помещении:
                # t_empty = round((v / 6 / (-(s_floor_ln + s_ceiling_ln + s_wall_ln + s_door_ln + s_window_ln))), 2)
                # # время реверберации в пустом помещении с людьми:
                # t_empty_people = round((v / 6 / (-(s_floor_ln + s_ceiling_ln + s_wall_ln + s_door_ln + s_window_ln + s_people))), 2)
                # # время реверберации в помещении с мебелью и людьми:
                # t_full = round((v / 6 / (-(s_floor_ln + s_ceiling_ln + s_wall_ln + s_door_ln + s_window_ln + s_interior_ln + s_people))), 2)
                # # время реверберации в помещении с мебелью без людей:
                # t_full_without_people = round((v / 6 / (-(s_floor_ln + s_ceiling_ln + s_wall_ln + s_door_ln + s_window_ln + s_interior_ln))), 2)

                # self.result_empty.setText('{} c'.format(str(t_empty)))
                # self.result_full.setText('{} c'.format(str(t_full)))
                # self.result_full_without_people.setText('{} c'.format(str(t_full_without_people)))
                # self.result_empty_people.setText('{} c'.format(str(t_empty_people)))


                # Расчет для значений a на разных частотах (работает только, если выбрать xl = pd.ExcelFile('sound_absorption_freaq.xlsx'), а # xl = pd.ExcelFile('sound_absorption.xlsx') в строке 212 закомментировать)
                # Функция по расчету (s * ln(1-a)) на разных частотах и для среднего a 
                def s_ln_calc(surface, material, s):

                    query = "SELECT * FROM {} WHERE material = ?".format(surface)
                    # получаем все значения a для выбранного материала (в виде списка с кортежем)
                    a = (cur.execute(query, (material,)).fetchall())
                    # преобразуем в обычный список
                    a_list = list(a[0])
                    # удаляем первые два элемента (порядковый номер и название)
                    del a_list[0:2]

                    # получаем список (площаль * ln(1-1)) для каждой частоты (и для среднего a)
                    s_ln_list = []
                    for a_freaquency in a_list:
                        
                        s_ln = round((s * math.log(1 - a_freaquency)), 2)
                        s_ln_list.append(s_ln)
                        
                    return(s_ln_list)

                # Получаем данные о материалах, выбранных пользователем
                floor_material = self.floor.currentText()
                ceiling_material = self.ceiling.currentText()
                wall_material = self.walls.currentText()
                window_material = self.window_type.currentText()
                door_material = self.door_type.currentText()

                # Вычисляем значения (s * ln(1-a)) на всех частотах (и для среднего a) для всего
                s_floor_ln_list = s_ln_calc('floor', floor_material, s_floor)
                s_ceiling_ln_list = s_ln_calc('ceiling', ceiling_material, s_floor)
                s_wall_ln_list = s_ln_calc('walls', wall_material, s_walls)
                s_door_ln_list = s_ln_calc('door', door_material, s_door)
                s_window_ln_list = s_ln_calc('window', window_material, s_window)
                s_people_ln_list = s_ln_calc('other', 'Человек', int(self.people_quant.currentText()))

                # расчет * ln(1-a) для всех деталей интерьера сразу. Зависит от i, которая меняется в зависимости от количества строк с деталями интерьера. Затем для каждой детали считается * ln(1-a), умножается на количество таких деталей. Далее все детали суммируются:
                s_interior_ln_list = [0, 0, 0, 0, 0, 0, 0]
                for inter in range(0, i):
                    interior_item = self.interior_layout.itemAtPosition(inter, 1).widget().currentText()
                    interior_item_quant = int(self.interior_layout.itemAtPosition(inter, 3).widget().text())
                    s_interior_ln = s_ln_calc('interior', interior_item, interior_item_quant)
                    # специальная функция, которая поэлементно складывает списки. В итоге получаем список с (кол-во * ln(1-a)), просуммированный на каждой частоте
                    s_interior_ln_list = list(map(lambda x,y: round(x, 2) + round(y, 2), s_interior_ln_list, s_interior_ln))

                # Вычисление времени реверберации на основе a на разных частотах (на выходе получаем списки Tрев от частоты)
                t_empty_freq = []
                t_empty_people_freq = []
                t_full_freq = []
                t_full_without_people_freq = []
                for j in range(0,6):
                    t_empty = round((v / 6 / (-(s_floor_ln_list[j] + s_ceiling_ln_list[j] + s_wall_ln_list[j] + s_door_ln_list[j] + s_window_ln_list[j]))), 2)
                    t_empty_people = round((v / 6 / (-(s_floor_ln_list[j] + s_ceiling_ln_list[j] + s_wall_ln_list[j] + s_door_ln_list[j] + s_window_ln_list[j] + s_people_ln_list[j]))), 2)
                    t_full = round((v / 6 / (-(s_floor_ln_list[j] + s_ceiling_ln_list[j] + s_wall_ln_list[j] + s_door_ln_list[j] + s_window_ln_list[j] + s_interior_ln_list[j] + s_people_ln_list[j]))), 2)
                    t_full_without_people = round((v / 6 / (-(s_floor_ln_list[j] + s_ceiling_ln_list[j] + s_wall_ln_list[j] + s_door_ln_list[j] + s_window_ln_list[j] + s_interior_ln_list[j]))), 2)
                    # Время реверберации пустого помещения
                    t_empty_freq.append(t_empty)
                    # Время реверберации пустого помещения с людьми
                    t_empty_people_freq.append(t_empty_people)
                    # Время реверберации в помещении с мебелью и людьми:
                    t_full_freq.append(t_full)
                    # Время реверберации в помещении с мебелью без людей:
                    t_full_without_people_freq.append(t_full_without_people)

                # Среднее время реверберации (среднее арифметическое по всем частотам)
                def average(arg):
                    return sum(arg) / len(arg)
            
                t_empty_average = round((average(t_empty_freq)), 2)
                t_empty_people_average = round((average(t_empty_people_freq)), 2)
                t_full_average = round((average(t_full_freq)), 2)
                t_full_without_people_average = round((average(t_full_without_people_freq)), 2)

                # Время реверберации, рассчитанное на основе среднего a (использую для сверки с Людиной методикой)
                t_empty_average_a = round((v / 6 / (-(s_floor_ln_list[6] + s_ceiling_ln_list[6] + s_wall_ln_list[6] + s_door_ln_list[6] + s_window_ln_list[6]))), 2)
                t_empty_people_average_a = round((v / 6 / (-(s_floor_ln_list[6] + s_ceiling_ln_list[6] + s_wall_ln_list[6] + s_door_ln_list[6] + s_window_ln_list[6] + s_people_ln_list[6]))), 2)
                t_full_average_a = round((v / 6 / (-(s_floor_ln_list[6] + s_ceiling_ln_list[6] + s_wall_ln_list[6] + s_door_ln_list[6] + s_window_ln_list[6] + s_interior_ln_list[6] + s_people_ln_list[6]))), 2)
                t_full_without_people_average_a = round((v / 6 / (-(s_floor_ln_list[6] + s_ceiling_ln_list[6] + s_wall_ln_list[6] + s_door_ln_list[6] + s_window_ln_list[6] + s_interior_ln_list[6]))), 2)

                # Расчет оптимального времени реверберации
                t_optimal = round((0.31 * math.log10(v) - 0.05), 2)

                # при нажатии на кнопку Расчет открывается новое окно с результатами. Передаем туда все полученные результаты
                self.results = Results(t_empty_freq, t_empty_people_freq, t_full_freq, t_full_without_people_freq, t_empty_average, t_empty_people_average, t_full_average, t_full_without_people_average, t_optimal)

# окно с результатами                
class Results(QWidget):
    def __init__(self, t_empty_freq, t_empty_people_freq, t_full_freq, t_full_without_people_freq, t_empty_average, t_empty_people_average, t_full_average, t_full_without_people_average, t_optimal):
        super().__init__()
        # присваиваем результаты, полученные ранее, новым переменным (их будем использовать в этом окне)
        self.t_empty_freq = t_empty_freq
        self.t_empty_people_freq = t_empty_people_freq
        self.t_full_freq = t_full_freq
        self.t_full_without_people_freq = t_full_without_people_freq
        self.t_empty_average = t_empty_average
        self.t_empty_people_average = t_empty_people_average
        self.t_full_average = t_full_average
        self.t_full_without_people_average = t_full_without_people_average
        self.t_optimal = t_optimal


        self.setWindowTitle('Результаты')
        self.setStyleSheet(Style.main())
        self.setGeometry(100, 100, 1700, 900)
        self.ui()
        self.show()

    def ui(self):
        self.widgets()
        self.layouts()
        self.show_results()

    def widgets(self):
        # Виджеты для работы с графиками
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)  # сглаживание линии (чтоб не было зубцов)

        # Результаты
        self.result_empty = QLabel()
        self.result_full = QLabel()
        self.result_empty_people = QLabel()
        self.result_full_without_people = QLabel()
        self.result_optimal = QLabel()

    def layouts(self):
        self.main_layout = QVBoxLayout()    
        self.bottom_layout = QHBoxLayout()
        self.result_layout = QFormLayout()

        # графики
        self.chart_layout = QHBoxLayout()
        self.chart_layout.addWidget(self.chart_view)
      

        self.result_group = QGroupBox('Результаты')
        self.result_group.setLayout(self.result_layout)
        self.result_group.setStyleSheet(Style.result_group())

        self.main_layout.addLayout(self.chart_layout)
        self.main_layout.addWidget(self.result_group)

        # результаты
        self.result_layout.addRow(QLabel('Время реверберации в пустом помещении:'), self.result_empty)
        self.result_layout.addRow(QLabel('Время реверберации в пустом помещении с людьми:'), self.result_empty_people)
        self.result_layout.addRow(QLabel('Время реверберации в помещении c мебелью без людей:'), self.result_full_without_people)
        self.result_layout.addRow(QLabel('Время реверберации в помещении c мебелью и людьми:'), self.result_full)
        self.result_layout.addRow(QLabel('Оптимальное время реверберации для данного помещения:'), self.result_optimal)

        self.setLayout(self.main_layout)

    def show_results(self):

        # создаем две линейных оси
        axis_X = QLogValueAxis() 
        axis_Y = QValueAxis()  

        # в оси y массив из массивов данных со всеми рассчитаными ранее временами
        x = [250, 500, 1000, 2000, 4000, 6000]
        y = [self.t_empty_freq, self.t_empty_people_freq, self.t_full_freq, self.t_full_without_people_freq]
        # названия графиков для легенды
        names = ['Пустое помещение', 'Пустое помещение с людьми', 'Помещение с людьми и мебелью', 'Помещение с мебелью без людей']

        # помещаем на график все 4 посчитанных ранее времени реверберации
        for result in range(0, 4):

            # формируем массив даннных. Должен состоять из координат (x, y)
            series = QLineSeries()
            for i in range(0, len(x)):
                series.append(x[i], y[result][i])

            # Задаем имя для отображения в легенде
            series.setName('<div style="font-size: 17px;">{}   </div>'.format(names[result]))

            # добавляем данные и оси
            self.chart.addSeries(series)
            self.chart.setAxisX(axis_X, series)
            self.chart.setAxisY(axis_Y, series)

        # Заголовок графика (можно использовать html и так менять стили)
        self.chart.setTitle('<div style="font-size: 25px;">Частотная характерстика времени реверберации</div>')
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        # параметры оси X
        self.chart.axisX(series).setTitleText('<div style="font-size: 15px;">Частота, Гц</div>')
        self.chart.axisX(series).setMinorTickCount(-1)  # автоматические отсчеты между главными значениями

        # параметры оси Y
        self.chart.axisY(series).setTitleText('<div style="font-size: 15px;">Время, с</div>')
        self.chart.axisY(series).setRange(0, 4)
        self.chart.axisY(series).setTickCount(5)

        # создаем легенду
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        # Вывод значений на экран
        self.result_empty.setText('{} c'.format(str(self.t_empty_average)))
        self.result_full.setText('{} c'.format(str(self.t_full_average)))
        self.result_full_without_people.setText('{} c'.format(str(self.t_full_without_people_average)))
        self.result_empty_people.setText('{} c'.format(str(self.t_empty_people_average)))
        self.result_optimal.setText('{} c'.format(str(self.t_optimal)))

               
def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()

    
