# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pending.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PendingWidget(object):
    def setupUi(self, PendingWidget):
        PendingWidget.setObjectName("PendingWidget")
        PendingWidget.resize(542, 297)
        self.verticalLayout = QtWidgets.QVBoxLayout(PendingWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tab_widget = QtWidgets.QTabWidget(PendingWidget)
        self.tab_widget.setObjectName("tab_widget")
        self.loans_tab = QtWidgets.QWidget()
        self.loans_tab.setObjectName("loans_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.loans_tab)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.loans_table = QtWidgets.QTableWidget(self.loans_tab)
        self.loans_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.loans_table.setObjectName("loans_table")
        self.loans_table.setColumnCount(5)
        self.loans_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.loans_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.loans_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.loans_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.loans_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.loans_table.setHorizontalHeaderItem(4, item)
        self.verticalLayout_2.addWidget(self.loans_table)
        self.tab_widget.addTab(self.loans_tab, "")
        self.debts_tab = QtWidgets.QWidget()
        self.debts_tab.setObjectName("debts_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.debts_tab)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.debts_table = QtWidgets.QTableWidget(self.debts_tab)
        self.debts_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.debts_table.setObjectName("debts_table")
        self.debts_table.setColumnCount(5)
        self.debts_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.debts_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.debts_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.debts_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.debts_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.debts_table.setHorizontalHeaderItem(4, item)
        self.verticalLayout_3.addWidget(self.debts_table)
        self.tab_widget.addTab(self.debts_tab, "")
        self.verticalLayout.addWidget(self.tab_widget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.refresh_button = QtWidgets.QPushButton(PendingWidget)
        self.refresh_button.setObjectName("refresh_button")
        self.horizontalLayout.addWidget(self.refresh_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(PendingWidget)
        self.tab_widget.setCurrentIndex(0)
        self.refresh_button.clicked.connect(PendingWidget.refresh)
        QtCore.QMetaObject.connectSlotsByName(PendingWidget)

    def retranslateUi(self, PendingWidget):
        _translate = QtCore.QCoreApplication.translate
        PendingWidget.setWindowTitle(_translate("PendingWidget", "Form"))
        item = self.loans_table.horizontalHeaderItem(1)
        item.setText(_translate("PendingWidget", "UOMe ID"))
        item = self.loans_table.horizontalHeaderItem(2)
        item.setText(_translate("PendingWidget", "Borrower"))
        item = self.loans_table.horizontalHeaderItem(3)
        item.setText(_translate("PendingWidget", "Amount"))
        item = self.loans_table.horizontalHeaderItem(4)
        item.setText(_translate("PendingWidget", "Description"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.loans_tab), _translate("PendingWidget", "Loans"))
        item = self.debts_table.horizontalHeaderItem(1)
        item.setText(_translate("PendingWidget", "UOMe ID"))
        item = self.debts_table.horizontalHeaderItem(2)
        item.setText(_translate("PendingWidget", "Loaner"))
        item = self.debts_table.horizontalHeaderItem(3)
        item.setText(_translate("PendingWidget", "Amount"))
        item = self.debts_table.horizontalHeaderItem(4)
        item.setText(_translate("PendingWidget", "Description"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.debts_tab), _translate("PendingWidget", "Debts"))
        self.refresh_button.setText(_translate("PendingWidget", "Refresh"))
