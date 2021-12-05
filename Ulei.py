
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import  QTableWidgetItem, QMessageBox, QDateEdit, QComboBox, QDialog


from desin_ylei import Ui_Dialog


class Ulei(Paseka,Ui_Dialog, QDialog):
    def __init__(self, name,*args,**kwargs):
        super(Ulei, self).__init__(*args,**kwargs)
        self.setupUi(self)
        self.name = name

        self.Ui__()
        self.table_zapolnenie()

    def Ui__(self):
        self.label_2.setText(self.label_2.text() + str(self.name))
        god_rog = self.cur.execute("""SELECT god_rog_matki FROM Ulei
                                    WHERE UleiId=?""", (self.name,)).fetchall()[0][0]
        self.god_rogdeniy.setText(str(god_rog))

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
        osmotr = self.cur.execute("""SELECT osmotr.date as date,
                                            osmotr.sila_PchS as sila,
                                            osmotr.rasplod as rasplod,
                                            osmotr.let as let,
                                            osmotr.ocenka_matki as ocenka_matki,
                                            osmotr.vzyato_ramok as vzyato_ramok
                                            FROM osmotr
                                            WHERE osmotr.UleiID=?""", (self.name,)).fetchall()
        print(osmotr)
        for i, row in enumerate(osmotr):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, el in enumerate(row):
                elem = QTableWidgetItem(str(el))
                elem.setFlags(Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, elem)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.update()

    def add_osmotr(self):
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
        row_list=[]

        row=self.tableWidget.rowCount()-1
        col=self.tableWidget.columnCount()
        print(row)
        for i in range(col):
            if i==1 or i==2:
                row_list.append('' if self.tableWidget.item(row,i)==None else  self.tableWidget.item(row,i).text())
            if i==0:
                print(self.tableWidget.cellWidget(row,i).date().toString('dd.MM.yyyy'))
        print(row_list)

        # self.cur.execute("""INSERT INTO osmotr(date,sila_PchS,rasplod,
        #                     let,ocenka_matki,vzyato_ramok) Values (?,?,?,?,?,?)
        #                 """, tuple(row_list))

    def otmena(self):
        pass

    def cell_t(self, row, col):
        self.del_row = row

    def del_osmotr(self):
        try:
            self.tableWidget.removeRow(self.del_row)
        except AttributeError:
            QMessageBox.warning(
                self,
                "ВНИМАНИЕ",
                "<b style='color: red;'>Выберите осмотр который желаете удалить!</b>"
            )

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        pass

    def dannie_ulya(self):
        return [self.name, self.tableWidget.item()]


# def except_hook(cls, exception, traceback):
#     sys.__excepthook__(cls, exception, traceback)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     wnd = Ulei(2)
#     wnd.show()
#     sys.excepthook = except_hook
#     sys.exit(app.exec())
