# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vivod.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_Vivod(object):
    def setupUi(self, Dialog_Vivod):
        Dialog_Vivod.setObjectName("Dialog_Vivod")
        Dialog_Vivod.resize(768, 595)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog_Vivod)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lab_zaklad = QtWidgets.QLabel(Dialog_Vivod)
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.lab_zaklad.setFont(font)
        self.lab_zaklad.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_zaklad.setObjectName("lab_zaklad")
        self.verticalLayout.addWidget(self.lab_zaklad)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Dialog_Vivod)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBox_materinskay_semya = QtWidgets.QComboBox(Dialog_Vivod)
        self.comboBox_materinskay_semya.setObjectName("comboBox_materinskay_semya")
        self.horizontalLayout_2.addWidget(self.comboBox_materinskay_semya)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Dialog_Vivod)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.comboBox_ozovskay_semya = QtWidgets.QComboBox(Dialog_Vivod)
        self.comboBox_ozovskay_semya.setObjectName("comboBox_ozovskay_semya")
        self.horizontalLayout_3.addWidget(self.comboBox_ozovskay_semya)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(Dialog_Vivod)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.comboBox_vospitalka = QtWidgets.QComboBox(Dialog_Vivod)
        self.comboBox_vospitalka.setObjectName("comboBox_vospitalka")
        self.horizontalLayout_4.addWidget(self.comboBox_vospitalka)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.label_4 = QtWidgets.QLabel(Dialog_Vivod)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.calendarWidget = QtWidgets.QCalendarWidget(Dialog_Vivod)
        self.calendarWidget.setObjectName("calendarWidget")
        self.verticalLayout.addWidget(self.calendarWidget)
        self.rbn_data_kladki = QtWidgets.QRadioButton(Dialog_Vivod)
        self.rbn_data_kladki.setObjectName("rbn_data_kladki")
        self.verticalLayout.addWidget(self.rbn_data_kladki)
        self.rbn_data_odnovnev_lich = QtWidgets.QRadioButton(Dialog_Vivod)
        self.rbn_data_odnovnev_lich.setObjectName("rbn_data_odnovnev_lich")
        self.verticalLayout.addWidget(self.rbn_data_odnovnev_lich)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog_Vivod)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.tableWidget = QtWidgets.QTableWidget(Dialog_Vivod)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.btn_del_raschet = QtWidgets.QPushButton(Dialog_Vivod)
        self.btn_del_raschet.setObjectName("btn_del_raschet")
        self.horizontalLayout_6.addWidget(self.btn_del_raschet)
        self.pushButton = QtWidgets.QPushButton(Dialog_Vivod)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_6.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog_Vivod)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Vivod)

    def retranslateUi(self, Dialog_Vivod):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Vivod.setWindowTitle(_translate("Dialog_Vivod", "Вывод маток"))
        self.lab_zaklad.setText(_translate("Dialog_Vivod", "закладка"))
        self.label.setText(_translate("Dialog_Vivod", "Материнская семья № улья"))
        self.label_2.setText(_translate("Dialog_Vivod", "Отцовская семья № улья"))
        self.label_3.setText(_translate("Dialog_Vivod", "Семья воспитательница № улья"))
        self.label_4.setText(_translate("Dialog_Vivod", "Данные для расчета:"))
        self.rbn_data_kladki.setText(_translate("Dialog_Vivod", "Дата начала - дата кладки яйца"))
        self.rbn_data_odnovnev_lich.setText(_translate("Dialog_Vivod", "Дата начало - дата однодневной личинки"))
        self.pushButton_2.setText(_translate("Dialog_Vivod", "Расчитать"))
        self.btn_del_raschet.setText(_translate("Dialog_Vivod", "Удалить расчет"))
        self.pushButton.setText(_translate("Dialog_Vivod", "Сохранить"))