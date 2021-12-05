import sqlite3
import sys
from datetime import datetime

from PyQt5 import QtGui
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QHeaderView, QPushButton
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QDateEdit, QComboBox, QDialog

from bee import Ui_MainWindow
from call import Ui_Dialog_Call
from date_calendar import Ui_Dialog_date
from desin_ylei import Ui_Dialog
from karta import Ui_Dialog_Karta
from open_ulei import Ui_Dialog_OpenUlei
from osmort import Ui_Dialog_Osmotr
from plem import Ui_Dialog_Plem
from vivod import Ui_Dialog_Vivod
from work import Ui_Dialog_work

paseka = []
title = ['№ улья', 'Дата', 'Масса пчел (кг)', 'Кол-во меда (кг)', 'Порода', 'Происхождение матки']
con = sqlite3.connect(r'data\bee.db')
cur = con.cursor()


class Paseka(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Paseka, self).__init__()
        self.setupUi(self)

        self.zapolnenie_tabl()
        self.label_3.setText(str(datetime.now().date()))
        self.add_ulei_btn.clicked.connect(self.add_ulei)
        self.del_ulei_btn.clicked.connect(self.del_ulei)
        self.tableWidget.cellClicked.connect(self.ulei)
        self.bnt_osmotr.clicked.connect(self.osmotr)
        self.btn_vivod_matok.clicked.connect(self.vivod)
        self.btn_open_uley.clicked.connect(self.open_ulei)
        self.btn_jurnal_work.clicked.connect(self.jurnal_work)

        self.btn_cal_pch.clicked.connect(self.call_sirop)
        self.btn_karta.clicked.connect(self.karta)
        self.btn_plem_work.clicked.connect(self.plem)

    def plem(self):
        plem = PlemWork()
        plem.exec()

    def karta(self):
        karta = Karta()
        karta.exec()

    def call_sirop(self):
        call = CallSirop()
        call.exec()

    def jurnal_work(self):
        jur = JurnalWork()
        jur.exec()

    def open_ulei(self):
        res = [i[0] for i in cur.execute("""SELECT UleiId From ulei""").fetchall()]
        paseka_open = OpenUlei(res)
        paseka_open.exec()
        self.zapolnenie_tabl()

    def vivod(self):

        vivod = VivodMatok()
        vivod.exec()

    def osmotr(self):
        osmotr = Osmotr()
        osmotr.exec()

    def ulei(self, row):
        name = int(self.tableWidget.item(row, 0).text())
        ulei = Ulei(name)
        ulei.exec()
        self.zapolnenie_tabl()

    def color_label(self):
        pal = self.label_2.palette()
        pal.setColor(QPalette.WindowText, QColor(0, 255, 100))
        self.label_2.setPalette(pal)

        pal = self.label_3.palette()
        pal.setColor(QPalette.WindowText, QColor(0, 255, 0))
        self.label_3.setPalette(pal)

        self.label_3.setText(str(datetime.now())[:16])

    def zapolnenie_tabl(self):
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        list_ulei = cur.execute("""SELECT Ulei.UleiId as nomer, osmotr.date as date, osmotr.sila_PchS as sila,
                                    osmotr.med as med, Ulei.poroda as poroda, Ulei.pr_matki as pr_matki
                                    FROM Ulei
                                    JOIN osmotr ON Ulei.UleiId=osmotr.UleiId
                                    ORDER BY nomer,date""").fetchall()
        # print(list_ulei)
        if not list_ulei:
            return
        list_ulei.sort(key=lambda x: (x[1], x[0]), reverse=True)
        # print(datetime(int(list_ulei[0][1][-4:]), int(list_ulei[0][1][3:5]), int(list_ulei[0][1][:2])))
        list_ulei_n = []
        list_ulei_sort_1 = []
        for row in list_ulei:

            if row[0] not in list_ulei_n:
                list_ulei_n.append(row[0])
                list_ulei_sort_1.append(row)
        list_ulei_sort_1.sort(key=lambda x: (x[1], x[0]))
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(list_ulei_sort_1):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            if (datetime.now() - datetime(int(row[1][:4]), int(row[1][5:7]), int(row[1][9:]))).days > 12:
                for j, el in enumerate(row):
                    elem = QTableWidgetItem(str(el))
                    self.tableWidget.setItem(i, j, elem)
                    self.tableWidget.item(i, j).setBackground(QColor(255, 0, 0))
            elif (datetime.now() - datetime(int(row[1][:4]), int(row[1][5:7]), int(row[1][9:]))).days > 6:
                for j, el in enumerate(row):
                    elem = QTableWidgetItem(str(el))
                    self.tableWidget.setItem(i, j, elem)
                    self.tableWidget.item(i, j).setBackground(QColor(255, 255, 0))
            else:
                for j, el in enumerate(row):
                    elem = QTableWidgetItem(str(el))
                    self.tableWidget.setItem(i, j, elem)
                    self.tableWidget.item(i, j).setBackground(QColor(0, 255, 0))

    def add_ulei(self):
        name_ulei = [i[0] for i in cur.execute("""SELECT UleiId FROM Ulei""").fetchall()]
        if name_ulei:
            QMessageBox.warning(
                self,
                "ВНИМАНИЕ",
                f"<b style='color: red;'>Следующие номера ульев ЗАНЯТЫ!!!\n{name_ulei}</b>"
            )
        name, flag = QInputDialog.getInt(self, 'Добавление улья', 'Введите № улья')
        if not flag:
            return
        while str(name) in name_ulei:
            QMessageBox.warning(
                self,
                "ВНИМАНИЕ",
                f"<b style='color: red;'>Следующие номера ульев ЗАНЯТЫ!!!\n{name_ulei}</b>"
            )
            name, flag = QInputDialog.getInt(self, 'Добавление улья', 'Введите № улья')
            if not flag:
                return

        year_matka, flag = QInputDialog.getInt(self, 'Добавление улья', 'Введите год рождения матки')
        if not flag:
            return

        massa_bee, flag = QInputDialog.getInt(self, 'Добавление улья', 'Введите массу пчелы')
        if not flag:
            return
        rasplod, flag = QInputDialog.getInt(self, 'Добавление улья', 'Введите количество расплода(полных рамок)')
        if not flag:
            return
        let_bee, flag = QInputDialog.getItem(self, 'Добавление улья', 'Оцените лет пчелы', ('1', '2', '3', '4', '5'), 0,
                                             False)
        if not flag:
            return
        kolichestvo_meda, flag = QInputDialog.getInt(self, 'Добавление улья', 'Введите массу меда')
        if not flag:
            return
        poroda, flag = QInputDialog.getItem(self, 'Добавление улья', 'Какакя порода?',
                                            ('Карника', 'БакФаст', 'Среднерусская', 'Кавказянка'), 2)
        if not flag:
            return
        ocenka_matki, flag = QInputDialog.getItem(self, 'Добавление улья', 'Оцените матку', ('1', '2', '3', '4', '5'),
                                                  0, False)
        if not flag:
            return
        pr_matki, flag = QInputDialog.getItem(self, 'Добавление улья', 'Происхождение матки',
                                              ('Свищевая', 'Роевая', 'Тихая смена', 'Своя Матка', 'Покупная'),
                                              0, False)
        if not flag:
            return
        date_1 = DateTime()
        date_1.exec()
        date = date_1.date()
        try:
            cur.execute("""INSERT INTO ulei(UleiId,god_rog_matki,pr_matki,poroda,PasekaId) 
                                                       Values (?,?,?,?,?)""", (name, year_matka, pr_matki, poroda, 1))
            cur.execute("""INSERT INTO osmotr(UleiId,date,sila_PchS,med,rasplod,let,ocenka_matki,
                                                vzyato_ramok) Values (?,?,?,?,?,?,?,?)""",
                        (name, date[:16], massa_bee, kolichestvo_meda, rasplod, let_bee,
                         ocenka_matki, ''))
            con.commit()
        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self,
                "ВНИМАНИЕ",
                "<b style='color: red;'>Этот № улья уже занят!</b>"
            )

        self.zapolnenie_tabl()

    def del_ulei(self):
        res = [i[0] for i in cur.execute("""SELECT uleiID FROM ulei""").fetchall()]
        # print(res)
        name, flag = QInputDialog.getItem(self, 'Удаление улья', 'Выберете улей который желаете удалить!', res, 0)
        if flag:
            cur.execute("""DELETE FROM ulei
                                    WHERE UleiID=?""",
                        (name,))
            cur.execute("""DELETE FROM osmotr
                                            WHERE UleiID=?""",
                        (name,))
            cur.execute("""DELETE FROM work
                                                    WHERE UleiID=?""",
                        (name,))
            cur.execute("""DELETE FROM VivodMatok
                        WHERE mater_sem=? or 
                        otzov_sem=? or
                        vosp_sem=?""",
                        (name, name, name))
            cur.execute("""DELETE FROM work
                                WHERE UleiId=? """,
                        (name,))
            con.commit()
        self.zapolnenie_tabl()


class Ulei(Ui_Dialog, QDialog):
    def __init__(self, name, *args, **kwargs):
        super(Ulei, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.name = name
        self.flag_save_osmotr = True
        self.Ui__()
        self.table_zapolnenie()

    def Ui__(self):
        matkovodsto_mater = \
            sorted(cur.execute("""SELECT mater_sem, data_ FROM VivodMatok """).fetchall(), key=lambda x: x[1],
                   reverse=True)[0][0]
        matkovodsto_otzov = sorted(cur.execute("""SELECT otzov_sem,data_ FROM VivodMatok """).fetchall(),
                                   key=lambda x: x[1], reverse=True)[0][0]
        matkovodsto_vosp = sorted(cur.execute("""SELECT vosp_sem,data_ FROM VivodMatok """).fetchall(),
                                  key=lambda x: x[1], reverse=True)[0][0]

        if self.name == matkovodsto_mater:
            self.label_2.setText(self.label_2.text() + str(self.name) + " Материнская семья ")

        elif self.name == matkovodsto_otzov:
            self.label_2.setText(self.label_2.text() + str(self.name) + " Отцовская семья ")

        elif self.name == matkovodsto_vosp:
            self.label_2.setText(self.label_2.text() + str(self.name) + " Семья воспитательница")

        else:
            self.label_2.setText(self.label_2.text() + str(self.name))
        god_rog = cur.execute("""SELECT god_rog_matki FROM Ulei
                                    WHERE UleiId=?""", (self.name,)).fetchall()[0][0]
        self.god_rogdeniy.setText(str(god_rog))
        prois = cur.execute("""SELECT pr_matki FROM Ulei WHERE UleiID=?""", (self.name,)).fetchall()[0][0]
        self.prois_matki.setText(prois)

        pixmap = QPixmap('img\\schab.jpg')
        self.foto_label.setPixmap(pixmap)

        self.pushButton.clicked.connect(self.add_osmotr)
        self.pushButton_2.clicked.connect(self.del_osmotr)

        self.tableWidget.cellClicked.connect(self.cell_t)

        self.pushButton_3.clicked.connect(self.save_osmotr)
        self.pushButton_3.hide()

        self.pushButton_4.clicked.connect(self.otmena)
        self.pushButton_4.hide()

    def table_zapolnenie(self):

        osmotr = cur.execute("""SELECT osmotr.date as date,
                                            osmotr.sila_PchS as sila,
                                            osmotr.rasplod as rasplod,
                                            osmotr.let as let,
                                            osmotr.ocenka_matki as ocenka_matki,
                                            osmotr.vzyato_ramok as vzyato_ramok
                                            FROM osmotr
                                            WHERE osmotr.UleiID=?""", (self.name,)).fetchall()
        # print(osmotr)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(osmotr):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, el in enumerate(row):
                elem = QTableWidgetItem(str(el))
                elem.setFlags(Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, elem)

    def add_osmotr(self):
        self.flag_save_osmotr = True
        self.pushButton_3.show()
        self.pushButton_4.show()

        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        row = self.tableWidget.rowCount()
        self.tableWidget.update()

        self.dateEdit = QDateEdit(self)
        self.dateEdit.setDate(QDate.currentDate())
        font = QtGui.QFont()
        font.setPointSize(8)
        self.dateEdit.setFont(font)
        self.dateEdit.setCalendarPopup(True)  # +++
        self.tableWidget.setCellWidget(row - 1, 0, self.dateEdit)

        self.dateEdit.date().toString('yyyy.MM.dd')

        comboBox = QComboBox(self)
        comboBox.addItems(('1', '2', '3', '4', '5'))
        self.tableWidget.setCellWidget(row - 1, 3, comboBox)

        comboBox1 = QComboBox(self)
        comboBox1.addItems(('1', '2', '3', '4', '5'))
        self.tableWidget.setCellWidget(row - 1, 4, comboBox1)

        self.tableWidget.update()

    def save_osmotr(self):
        self.tableWidget.update()
        row_list = []

        row = self.tableWidget.rowCount() - 1
        col = self.tableWidget.columnCount()
        # print(row)
        for i in range(col):
            if i == 1 or i == 2 or i == 5:
                row_list.append('' if self.tableWidget.item(row, i) == None else self.tableWidget.item(row, i).text())
            elif i == 0:
                row_list.append(self.tableWidget.cellWidget(row, i).date().toString('yyyy.MM.dd'))
            else:
                row_list.append(self.tableWidget.cellWidget(row, i).currentText())

        row_list.append(self.name)
        try:
            med = cur.execute("""SELECT osmotr.med as med,
                                        osmotr.date as date
                                FROM osmotr
                                JOIN Ulei ON osmotr.UleiId=Ulei.UleiId
                                WHERE Ulei.UleiId =?
                                ORDER BY date ASC""", (self.name,)).fetchall()[0][0]
            row_list.append(med)
        except IndexError:
            pass

        # print(row_list)
        if self.flag_save_osmotr:
            if len(row_list) < 8:
                row_list.append('')
            cur.execute("""INSERT INTO osmotr(date,sila_PchS,rasplod,
                                let,ocenka_matki,vzyato_ramok,UleiId,med) Values (?,?,?,?,?,?,?,?)
                            """, tuple(row_list))
            con.commit()
            self.flag_save_osmotr = False
        self.table_zapolnenie()

    def otmena(self):
        pass

    def cell_t(self, row, col):
        self.del_row = row

    def del_osmotr(self):
        row = []

        try:
            for i in range(self.tableWidget.columnCount()):
                row.append(self.tableWidget.item(self.del_row, i).text())
            self.tableWidget.removeRow(self.del_row)
            # print(row)
            cur.execute("""DELETE FROM osmotr 
                        WHERE UleiID=? and date=?""",
                        (str(self.name), row[0]))
            con.commit()
        except AttributeError:
            QMessageBox.warning(
                self,
                "ВНИМАНИЕ",
                "<b style='color: red;'>Выберите осмотр который желаете удалить!</b>"
            )


class DateTime(QDialog, Ui_Dialog_date):
    def __init__(self):
        super(DateTime, self).__init__()
        self.setupUi(self)

    def date(self):
        return (self.calendarWidget.selectedDate().toString('yyyy.MM.dd'))


class Osmotr(QDialog, Ui_Dialog_Osmotr):
    def __init__(self):
        super(Osmotr, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.vivod)
        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit_2.setDate(QDate.currentDate())

        title = ['Улей', 'дата осмотра', 'сила ПчС', 'расплод', 'мед']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(title)

    def vivod(self):

        self.zapolnenie_tabl()

    def zapolnenie_tabl(self):
        date_1 = self.dateEdit.date().toString('yyyy.MM.dd')
        date_2 = self.dateEdit_2.date().toString('yyyy.MM.dd')
        res = cur.execute("""SELECT UleiId, date,sila_PchS,rasplod,med FROM osmotr
                        WHERE date>=? and date<=?
                         """, (date_1, date_2)).fetchall()
        # print(res)
        res.sort(key=lambda x: (x[1], x[0], x[2]))
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, el in enumerate(row):
                elem = QTableWidgetItem(str(el))
                self.tableWidget.setItem(i, j, elem)


class VivodMatok(QDialog, Ui_Dialog_Vivod):
    def __init__(self):
        super(VivodMatok, self).__init__()
        self.setupUi(self)
        self.index = 0

        self.lab_zaklad.setText('Матководство')

        self.pushButton_2.clicked.connect(self.raschet)
        self.pushButton.clicked.connect(self.save)
        self.btn_del_raschet.clicked.connect(self.del_raschet)
        self.tableWidget.cellClicked.connect(self.cell)

        self.res = [i[0] for i in cur.execute("""SELECT UleiId from ulei WHERE UleiId""").fetchall()]

        self.comboBox_materinskay_semya.addItems(self.res)
        self.comboBox_ozovskay_semya.addItems(self.res)
        self.comboBox_vospitalka.addItems(self.res)
        self.zapolnenie_tab()

    def zapolnenie_tab(self):

        title = ['№', 'Материнская \nсемья', 'Отцовская \nсемья', 'Семья \nвоспитательница', 'Дата \nпрививки',
                 'Дата отбора\n маточников', 'Дата выхода\nматок']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(title)
        res = cur.execute("""SELECT * FROM VivodMatok""").fetchall()[::-1]
        if not res:
            return
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, el in enumerate(row):
                elem = QTableWidgetItem(str(el))
                self.tableWidget.setItem(i, j, elem)

        self.index = res[0][0]
        # print(res)

    def raschet(self):
        date = self.calendarWidget.selectedDate()
        ulei = [self.index + 1, self.comboBox_materinskay_semya.currentText(),
                self.comboBox_ozovskay_semya.currentText(),
                self.comboBox_vospitalka.currentText()]

        if self.rbn_data_kladki.isChecked():
            date_otbora_matochnika = date.addDays(14)
            date_vixod_matki = date.addDays(16)
            ulei += [date.toString('yyyy.MM.dd'), date_otbora_matochnika.toString('yyyy.MM.dd'),
                     date_vixod_matki.toString('yyyy.MM.dd')]
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            row = self.tableWidget.rowCount() - 1
            for i, el in enumerate(ulei):
                elem = QTableWidgetItem(str(el))
                self.tableWidget.setItem(row, i, elem)
            cur.execute("""INSERT INTO VivodMatok values(null,?,?,?,?,?,?,?)""",
                        (ulei[1], ulei[2], ulei[3], ulei[4], ulei[4], ulei[5], ulei[6]))
        if self.rbn_data_odnovnev_lich.isChecked():
            date_otbora_matochnika = date.addDays(11)
            date_vixod_matki = date.addDays(13)
            ulei += [date.toString('yyyy.MM.dd'), date_otbora_matochnika.toString('yyyy.MM.dd'),
                     date_vixod_matki.toString('yyyy.MM.dd')]
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            row = self.tableWidget.rowCount() - 1
            for i, el in enumerate(ulei):
                elem = QTableWidgetItem(str(el))
                self.tableWidget.setItem(row, i, elem)

            cur.execute("""INSERT INTO VivodMatok values(null,?,?,?,?,?,?,?)""",
                        (ulei[1], ulei[2], ulei[3], ulei[4], ulei[4], ulei[5], ulei[6]))

    def cell(self, row, col):
        self.del_row = row

    def del_raschet(self):
        row = []

        try:
            for i in range(self.tableWidget.columnCount()):
                row.append(self.tableWidget.item(self.del_row, i).text())
            self.tableWidget.removeRow(self.del_row)
            # print(row)
            cur.execute("""DELETE FROM VivodMAtok 
                                WHERE number=? and mater_sem=?""",
                        (row[0], row[1]))
            con.commit()
        except AttributeError:
            QMessageBox.warning(
                self,
                "ВНИМАНИЕ",
                "<b style='color: red;'>Выберите расчет который желаете удалить!</b>"
            )

    def paintCell(self, painter, rect, date):
        self.calendarWidget.paintCell(painter, rect, date)
        painter.setBrush(QtGui.QColor(0, 200, 200, 50))
        painter.drawRect(rect)

    def save(self):
        con.commit()


class OpenUlei(QDialog, Ui_Dialog_OpenUlei):
    def __init__(self, *args):
        super(OpenUlei, self).__init__()
        self.setupUi(self)
        self.uleis = args[0]
        # print(self.uleis)

        self.tableWidget.setRowCount(0)
        k = 0
        self.tableWidget.setColumnCount(int(len(self.uleis) ** 0.5) + 1)
        for i in range(int(len(self.uleis) ** 0.5) + 1):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j in range(int(len(self.uleis) ** 0.5 + 1)):
                if len(self.uleis) > k:
                    btn = QPushButton()
                    btn.setObjectName(f'{self.uleis[k]}')
                    btn.setText(f'Открыть улей №{self.uleis[k]}')
                    btn.resize(25, 25)
                    btn.clicked.connect(lambda cheked, arg=btn.text(): self.open_ulei(arg))
                    self.tableWidget.setCellWidget(i, j, btn)
                    k += 1
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def open_ulei(self, name):
        ulei_n = int(name[14:])
        # print(ulei_n)
        ulei = Ulei(ulei_n)
        ulei.exec()


class JurnalWork(QDialog, Ui_Dialog_work):
    def __init__(self):
        super(JurnalWork, self).__init__()
        self.setupUi(self)
        self.zapolnenie_tabl()
        self.dateEdit.setDate(QDate.currentDate())
        self.pushButton.clicked.connect(self.dobavit)

        ulei = [ulei[0] for ulei in cur.execute("""SELECT uleiId From ulei""").fetchall()]
        ulei.insert(0, 'Пасека')
        self.comboBox.addItems(ulei)

        self.vid_rabot_paseka = ['Составить график и план вывода маток', 'Скосить траву', 'Перетопка воска',
                                 ' Развешивание привоя']
        self.vid_rabot_ulei = ['Постановка вощины', 'Расширить гнездовой корпус', 'Оценка плодовитости маток',
                               'Создать отводки', 'Подкрасить улей']
        self.comboBox.currentTextChanged.connect(self.comboBox_)

    def comboBox_(self):
        if self.comboBox.currentText() == 'Пасека':
            self.comboBox_2.clear()
            self.comboBox_2.addItems(self.vid_rabot_paseka)
        else:
            self.comboBox_2.clear()
            self.comboBox_2.addItems(self.vid_rabot_ulei)

    def dobavit(self):
        date_1 = self.dateEdit.date().toString('yyyy.MM.dd')
        mesto_raboti = self.comboBox.currentText()
        vid_raboti = self.comboBox_2.currentText()
        cur.execute("""INSERT INTO work values(NULL,?,?,?)""", (date_1, mesto_raboti, vid_raboti))
        con.commit()
        self.zapolnenie_tabl()

    def zapolnenie_tabl(self):
        res = cur.execute("""SELECT date,UleiId,work FROM work""").fetchall()
        title = ['Дата работы', 'Место работы', 'Работа']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if res:
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(res):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, el in enumerate(row):
                    if j == 1:
                        elem = QTableWidgetItem(f'Улей №{el}')
                        self.tableWidget.setItem(i, j, elem)
                    else:
                        elem = QTableWidgetItem(el)
                        self.tableWidget.setItem(i, j, elem)


class CallSirop(QDialog, Ui_Dialog_Call):
    def __init__(self):
        super(CallSirop, self).__init__()
        self.setupUi(self)
        self.UI()

    def UI(self):
        self.title = ['№ улья', 'Нал. меда\n в улье(кг)', 'Объем нужного\n сиропа(л)', 'Масса нужного\n сахара(кг)',
                      'Объем нужной\nводы(л)']

        res = sorted(cur.execute("""SELECT UleiId, date,sila_PchS,med FROM osmotr""").fetchall(),
                     key=lambda x: (-int(x[0]), x[1]), reverse=True)
        # print(res)
        res_temp = [res[0]]
        for i in range(1, len(res)):
            if res[i - 1][0] != res[i][0]:
                res_temp.append(res[i])

        self.res = res_temp[:]
        # print(self.res)
        self.tableWidget.setColumnCount(len(self.title))
        self.tableWidget.setHorizontalHeaderLabels(self.title)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.pushButton.clicked.connect(self.raschet)

    def raschet(self):
        if self.rbn_1.isChecked():
            res_tab = []
            for i, row in enumerate(self.res):
                res_tab.append([])
                for j in range(len(self.title)):
                    if j == 0:
                        res_tab[i].append(row[j])
                    elif j == 1:
                        res_tab[i].append(str(row[3]))
                    elif j == 2:
                        res_tab[i].append(str((20 - int(row[3])) * 1.6))
                    elif j == 3:
                        res_tab[i].append(str(20 - int(row[3])))
                    elif j == 4:
                        res_tab[i].append(str(20 - int(row[3])))
            # print(res_tab)

            self.tableWidget.setRowCount(0)
            for i, row in enumerate(res_tab):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, el in enumerate(row):
                    elem = QTableWidgetItem(el[:4])
                    self.tableWidget.setItem(i, j, elem)

        if self.rbn_2.isChecked():
            res_tab = []
            for i, row in enumerate(self.res):
                res_tab.append([])
                for j in range(len(self.title)):
                    if j == 0:
                        res_tab[i].append(row[j])
                    elif j == 1:
                        res_tab[i].append(str(row[3]))
                    elif j == 2:
                        res_tab[i].append(str(round((20 - int(row[3])) * 1.33)))
                    elif j == 3:
                        res_tab[i].append(str(20 - int(row[3])))
                    elif j == 4:
                        res_tab[i].append(str(int(row[3] // 2)))
            # print(res_tab)

            self.tableWidget.setRowCount(0)
            for i, row in enumerate(res_tab):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, el in enumerate(row):
                    elem = QTableWidgetItem(el[:4])
                    self.tableWidget.setItem(i, j, elem)

        if self.rbn_3.isChecked():
            res_tab = []
            for i, row in enumerate(self.res):
                res_tab.append([])
                for j in range(len(self.title)):
                    if j == 0:
                        res_tab[i].append(row[j])
                    elif j == 1:
                        res_tab[i].append(str(row[3]))
                    elif j == 2:
                        res_tab[i].append(str(round((20 - int(row[3])) * 1.2)))
                    elif j == 3:
                        res_tab[i].append(str(20 - int(row[3])))
                    elif j == 4:
                        res_tab[i].append(str(int(row[3] // 2)))
            # print(res_tab)

            self.tableWidget.setRowCount(0)
            for i, row in enumerate(res_tab):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, el in enumerate(row):
                    elem = QTableWidgetItem(el[:4])
                    self.tableWidget.setItem(i, j, elem)


class Karta(QDialog, Ui_Dialog_Karta):
    def __init__(self):
        super(Karta, self).__init__()
        self.setupUi(self)
        label = QPixmap(r'img/paseka_img.jpg')
        self.label.setPixmap(label)


class PlemWork(QDialog, Ui_Dialog_Plem):
    def __init__(self):
        super(PlemWork, self).__init__()
        self.setupUi(self)
        res = sorted(cur.execute("""SELECT mater_sem,otzov_sem, vosp_sem, data_ FROM VivodMatok""").fetchall(),
                     key=lambda x: x[3], reverse=True)
        print(res)
        title = ['Материнская семья', 'Отцовская семья', 'Семья воспитательница', 'Дата работы с ними']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, el in enumerate(row):
                if j in (0, 1, 2):
                    btn = QPushButton(f'Открыть улей №{el} ')
                    btn.resize(25, 25)
                    btn.clicked.connect(lambda cheked, arg=btn.text(): self.open_ulei(arg))
                    self.tableWidget.setCellWidget(i, j, btn)

                else:
                    elem = QTableWidgetItem(str(el))
                    self.tableWidget.setItem(i, j, elem)

    def open_ulei(self, name):
        ulei_n = int(name[14:])
        # print(ulei_n)
        ulei = Ulei(ulei_n)
        ulei.exec()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication([])
    wnd = Paseka()
    wnd.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
