# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(994, 638)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 40, 291, 291))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 111, 16))
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setGeometry(QtCore.QRect(0, 20, 281, 249))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.btn_search_dates = QtWidgets.QPushButton(self.widget)
        self.btn_search_dates.setObjectName("btn_search_dates")
        self.gridLayout_3.addWidget(self.btn_search_dates, 0, 1, 1, 1)
        self.btn_search_weekend = QtWidgets.QPushButton(self.widget)
        self.btn_search_weekend.setObjectName("btn_search_weekend")
        self.gridLayout_3.addWidget(self.btn_search_weekend, 0, 0, 1, 1)
        self.dateEdit_2 = QtWidgets.QDateEdit(self.widget)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.gridLayout_3.addWidget(self.dateEdit_2, 1, 1, 1, 1)
        self.dateEdit = QtWidgets.QDateEdit(self.widget)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout_3.addWidget(self.dateEdit, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 2, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 9, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_2.addWidget(self.checkBox, 0, 0, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.widget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_2.addWidget(self.checkBox_2, 1, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(330, 40, 571, 291))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.widget1 = QtWidgets.QWidget(self.frame_2)
        self.widget1.setGeometry(QtCore.QRect(20, 10, 531, 271))
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_search_flights = QtWidgets.QPushButton(self.widget1)
        self.btn_search_flights.setObjectName("btn_search_flights")
        self.horizontalLayout.addWidget(self.btn_search_flights)
        self.btn_get_info = QtWidgets.QPushButton(self.widget1)
        self.btn_get_info.setObjectName("btn_get_info")
        self.horizontalLayout.addWidget(self.btn_get_info)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(self.widget1)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.tabWidget = QtWidgets.QTabWidget(self.widget1)
        self.tabWidget.setObjectName("tabWidget")
        self.Operas = QtWidgets.QWidget()
        self.Operas.setObjectName("Operas")
        self.table_operas = QtWidgets.QTableWidget(self.Operas)
        self.table_operas.setGeometry(QtCore.QRect(10, 10, 411, 161))
        self.table_operas.setObjectName("table_operas")
        self.table_operas.setColumnCount(0)
        self.table_operas.setRowCount(0)
        self.tabWidget.addTab(self.Operas, "")
        self.Flights = QtWidgets.QWidget()
        self.Flights.setObjectName("Flights")
        self.table_flights = QtWidgets.QTableWidget(self.Flights)
        self.table_flights.setGeometry(QtCore.QRect(10, 20, 491, 151))
        self.table_flights.setObjectName("table_flights")
        self.table_flights.setColumnCount(0)
        self.table_flights.setRowCount(0)
        self.tabWidget.addTab(self.Flights, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 994, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Opera Search"))
        self.btn_search_dates.setText(_translate("MainWindow", "Search Specific Dates"))
        self.btn_search_weekend.setText(_translate("MainWindow", "Search Weekends"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_2.setText(_translate("MainWindow", "CheckBox"))
        self.btn_search_flights.setText(_translate("MainWindow", "Search Flights"))
        self.btn_get_info.setText(_translate("MainWindow", "Get Opera Info"))
        self.label_2.setText(_translate("MainWindow", "Results"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Operas), _translate("MainWindow", "Operas"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Flights), _translate("MainWindow", "Flights"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

