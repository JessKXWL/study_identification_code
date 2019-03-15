# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TrainForm.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TrainForm(object):
    def setupUi(self, TrainForm):
        TrainForm.setObjectName("TrainForm")
        TrainForm.resize(526, 296)
        self.gridLayout = QtWidgets.QGridLayout(TrainForm)
        self.gridLayout.setObjectName("gridLayout")
        self.StartpushButton = QtWidgets.QPushButton(TrainForm)
        self.StartpushButton.setObjectName("StartpushButton")
        self.gridLayout.addWidget(self.StartpushButton, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(TrainForm)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)
        self.lineEdit = QtWidgets.QLineEdit(TrainForm)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(TrainForm)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 2, 0, 1, 4)
        self.ServerpushButton = QtWidgets.QPushButton(TrainForm)
        self.ServerpushButton.setObjectName("ServerpushButton")
        self.gridLayout.addWidget(self.ServerpushButton, 1, 3, 1, 1)
        self.ChooseFilepushButton = QtWidgets.QPushButton(TrainForm)
        self.ChooseFilepushButton.setObjectName("ChooseFilepushButton")
        self.gridLayout.addWidget(self.ChooseFilepushButton, 1, 1, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(TrainForm)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 4)

        self.retranslateUi(TrainForm)
        QtCore.QMetaObject.connectSlotsByName(TrainForm)

    def retranslateUi(self, TrainForm):
        _translate = QtCore.QCoreApplication.translate
        TrainForm.setWindowTitle(_translate("TrainForm", "Form"))
        self.StartpushButton.setText(_translate("TrainForm", "开始"))
        self.label.setText(_translate("TrainForm", "选择需要训练的图集,训练过程比较长,请耐心等候,训练结束后可通过启动服务按钮，在web端上传需要识别的验证码\n提示: 图片的文件名必须是图片所对应的验证码.jpg"))
        self.ServerpushButton.setText(_translate("TrainForm", "启动服务"))
        self.ChooseFilepushButton.setText(_translate("TrainForm", "浏览"))

