# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'formCreerNote1_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(672, 673)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lytTop = QtWidgets.QHBoxLayout()
        self.lytTop.setObjectName("lytTop")
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.lytTop.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lytTop.addItem(spacerItem)
        self.lblTimeCode = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTimeCode.sizePolicy().hasHeightForWidth())
        self.lblTimeCode.setSizePolicy(sizePolicy)
        self.lblTimeCode.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.lblTimeCode.setObjectName("lblTimeCode")
        self.lytTop.addWidget(self.lblTimeCode)
        self.verticalLayout.addLayout(self.lytTop)
        self.lytTabWidget = QtWidgets.QVBoxLayout()
        self.lytTabWidget.setObjectName("lytTabWidget")
        self.tabWidgetNote = QtWidgets.QTabWidget(Dialog)
        self.tabWidgetNote.setObjectName("tabWidgetNote")
        self.tabTitre = QtWidgets.QWidget()
        self.tabTitre.setObjectName("tabTitre")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tabTitre)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 641, 551))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.lytTitre = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.lytTitre.setContentsMargins(0, 0, 0, 0)
        self.lytTitre.setObjectName("lytTitre")
        self.tedTitre = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tedTitre.setFont(font)
        self.tedTitre.setObjectName("tedTitre")
        self.lytTitre.addWidget(self.tedTitre)
        self.lytTitreBtn = QtWidgets.QHBoxLayout()
        self.lytTitreBtn.setObjectName("lytTitreBtn")
        self.btnSauverTitre = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSauverTitre.sizePolicy().hasHeightForWidth())
        self.btnSauverTitre.setSizePolicy(sizePolicy)
        self.btnSauverTitre.setMinimumSize(QtCore.QSize(111, 32))
        self.btnSauverTitre.setObjectName("btnSauverTitre")
        self.lytTitreBtn.addWidget(self.btnSauverTitre)
        self.btnEffacerTitre = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnEffacerTitre.sizePolicy().hasHeightForWidth())
        self.btnEffacerTitre.setSizePolicy(sizePolicy)
        self.btnEffacerTitre.setMinimumSize(QtCore.QSize(111, 32))
        self.btnEffacerTitre.setObjectName("btnEffacerTitre")
        self.lytTitreBtn.addWidget(self.btnEffacerTitre)
        self.btnTagTitre = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTagTitre.sizePolicy().hasHeightForWidth())
        self.btnTagTitre.setSizePolicy(sizePolicy)
        self.btnTagTitre.setMinimumSize(QtCore.QSize(111, 32))
        self.btnTagTitre.setStyleSheet("margin-left: 12; background-color: orange; color: black")
        self.btnTagTitre.setObjectName("btnTagTitre")
        self.lytTitreBtn.addWidget(self.btnTagTitre)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lytTitreBtn.addItem(spacerItem1)
        self.btnFermer0 = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnFermer0.sizePolicy().hasHeightForWidth())
        self.btnFermer0.setSizePolicy(sizePolicy)
        self.btnFermer0.setMinimumSize(QtCore.QSize(111, 32))
        self.btnFermer0.setStyleSheet("padding: 3px")
        self.btnFermer0.setObjectName("btnFermer0")
        self.lytTitreBtn.addWidget(self.btnFermer0)
        self.lytTitre.addLayout(self.lytTitreBtn)
        self.tabWidgetNote.addTab(self.tabTitre, "")
        self.tabImage = QtWidgets.QWidget()
        self.tabImage.setObjectName("tabImage")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.tabImage)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 641, 551))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.lytImage = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.lytImage.setContentsMargins(0, 0, 0, 0)
        self.lytImage.setObjectName("lytImage")
        self.lblImage = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblImage.sizePolicy().hasHeightForWidth())
        self.lblImage.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblImage.setFont(font)
        self.lblImage.setText("")
        self.lblImage.setObjectName("lblImage")
        self.lytImage.addWidget(self.lblImage)
        self.lneLegende = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.lneLegende.setObjectName("lneLegende")
        self.lytImage.addWidget(self.lneLegende)
        self.lytImageBtn = QtWidgets.QHBoxLayout()
        self.lytImageBtn.setObjectName("lytImageBtn")
        self.btnSauverImage = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSauverImage.sizePolicy().hasHeightForWidth())
        self.btnSauverImage.setSizePolicy(sizePolicy)
        self.btnSauverImage.setMinimumSize(QtCore.QSize(111, 32))
        self.btnSauverImage.setObjectName("btnSauverImage")
        self.lytImageBtn.addWidget(self.btnSauverImage)
        self.btnEffaceImage = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnEffaceImage.sizePolicy().hasHeightForWidth())
        self.btnEffaceImage.setSizePolicy(sizePolicy)
        self.btnEffaceImage.setMinimumSize(QtCore.QSize(111, 32))
        self.btnEffaceImage.setObjectName("btnEffaceImage")
        self.lytImageBtn.addWidget(self.btnEffaceImage)
        self.chkIcone = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        self.chkIcone.setObjectName("chkIcone")
        self.lytImageBtn.addWidget(self.chkIcone)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lytImageBtn.addItem(spacerItem2)
        self.btnFermer1 = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnFermer1.sizePolicy().hasHeightForWidth())
        self.btnFermer1.setSizePolicy(sizePolicy)
        self.btnFermer1.setMinimumSize(QtCore.QSize(111, 32))
        self.btnFermer1.setStyleSheet("padding: 3px")
        self.btnFermer1.setObjectName("btnFermer1")
        self.lytImageBtn.addWidget(self.btnFermer1)
        self.lytImage.addLayout(self.lytImageBtn)
        self.tabWidgetNote.addTab(self.tabImage, "")
        self.tabTexte = QtWidgets.QWidget()
        self.tabTexte.setObjectName("tabTexte")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.tabTexte)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 641, 551))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.lytTexte = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.lytTexte.setContentsMargins(0, 0, 0, 0)
        self.lytTexte.setObjectName("lytTexte")
        self.tedTexte = QtWidgets.QTextEdit(self.verticalLayoutWidget_4)
        self.tedTexte.setObjectName("tedTexte")
        self.lytTexte.addWidget(self.tedTexte)
        self.lytTexteBtn = QtWidgets.QHBoxLayout()
        self.lytTexteBtn.setObjectName("lytTexteBtn")
        self.btnSauverTexte = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.btnSauverTexte.setMinimumSize(QtCore.QSize(111, 32))
        self.btnSauverTexte.setObjectName("btnSauverTexte")
        self.lytTexteBtn.addWidget(self.btnSauverTexte)
        self.btnEffacerTexte = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.btnEffacerTexte.setMinimumSize(QtCore.QSize(111, 32))
        self.btnEffacerTexte.setObjectName("btnEffacerTexte")
        self.lytTexteBtn.addWidget(self.btnEffacerTexte)
        self.btnTagTexte = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTagTexte.sizePolicy().hasHeightForWidth())
        self.btnTagTexte.setSizePolicy(sizePolicy)
        self.btnTagTexte.setMinimumSize(QtCore.QSize(111, 32))
        self.btnTagTexte.setStyleSheet("margin-left: 12; background-color: orange; color: black")
        self.btnTagTexte.setObjectName("btnTagTexte")
        self.lytTexteBtn.addWidget(self.btnTagTexte)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lytTexteBtn.addItem(spacerItem3)
        self.btnFermer2 = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.btnFermer2.setMinimumSize(QtCore.QSize(111, 32))
        self.btnFermer2.setObjectName("btnFermer2")
        self.lytTexteBtn.addWidget(self.btnFermer2)
        self.lytTexte.addLayout(self.lytTexteBtn)
        self.tabWidgetNote.addTab(self.tabTexte, "")
        self.lytTabWidget.addWidget(self.tabWidgetNote)
        self.verticalLayout.addLayout(self.lytTabWidget)

        self.retranslateUi(Dialog)
        self.tabWidgetNote.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Saisie d\'une nouvelle note :"))
        self.lblTimeCode.setText(_translate("Dialog", "TextLabel"))
        self.btnSauverTitre.setText(_translate("Dialog", "Sauver le Titre"))
        self.btnEffacerTitre.setText(_translate("Dialog", "Effacer le Titre"))
        self.btnTagTitre.setText(_translate("Dialog", "Tag (Ctrl+T)"))
        self.btnFermer0.setText(_translate("Dialog", "Fermer"))
        self.tabWidgetNote.setTabText(self.tabWidgetNote.indexOf(self.tabTitre), _translate("Dialog", "Titre"))
        self.lneLegende.setPlaceholderText(_translate("Dialog", "Saisir la légende de l\'image."))
        self.btnSauverImage.setText(_translate("Dialog", "Sauver image"))
        self.btnEffaceImage.setText(_translate("Dialog", "Effacer image"))
        self.chkIcone.setText(_translate("Dialog", "Choisir comme vignette"))
        self.btnFermer1.setText(_translate("Dialog", "Fermer"))
        self.tabWidgetNote.setTabText(self.tabWidgetNote.indexOf(self.tabImage), _translate("Dialog", "Image"))
        self.btnSauverTexte.setText(_translate("Dialog", "Sauver le texte"))
        self.btnEffacerTexte.setText(_translate("Dialog", "Effacer le Texte"))
        self.btnTagTexte.setText(_translate("Dialog", "Tag (Ctrl+T)"))
        self.btnFermer2.setText(_translate("Dialog", "Fermer"))
        self.tabWidgetNote.setTabText(self.tabWidgetNote.indexOf(self.tabTexte), _translate("Dialog", "Texte"))