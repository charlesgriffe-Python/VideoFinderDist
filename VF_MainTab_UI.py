# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VF_MainTab_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(881, 630)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lytMain = QtWidgets.QVBoxLayout()
        self.lytMain.setObjectName("lytMain")
        self.lytTitre = QtWidgets.QHBoxLayout()
        self.lytTitre.setObjectName("lytTitre")
        self.lblTitre = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTitre.sizePolicy().hasHeightForWidth())
        self.lblTitre.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblTitre.setFont(font)
        self.lblTitre.setStyleSheet("\n"
"")
        self.lblTitre.setObjectName("lblTitre")
        self.lytTitre.addWidget(self.lblTitre)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lytTitre.addItem(spacerItem)
        self.cmbStatut = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbStatut.sizePolicy().hasHeightForWidth())
        self.cmbStatut.setSizePolicy(sizePolicy)
        self.cmbStatut.setObjectName("cmbStatut")
        self.lytTitre.addWidget(self.cmbStatut)
        self.lneRecherche = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lneRecherche.sizePolicy().hasHeightForWidth())
        self.lneRecherche.setSizePolicy(sizePolicy)
        self.lneRecherche.setObjectName("lneRecherche")
        self.lytTitre.addWidget(self.lneRecherche)
        self.btnLoupe = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoupe.setText("")
        self.btnLoupe.setObjectName("btnLoupe")
        self.lytTitre.addWidget(self.btnLoupe)
        self.lytMain.addLayout(self.lytTitre)
        self.lytCentral = QtWidgets.QHBoxLayout()
        self.lytCentral.setObjectName("lytCentral")
        self.lytListe = QtWidgets.QVBoxLayout()
        self.lytListe.setObjectName("lytListe")
        self.lstVue = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lstVue.sizePolicy().hasHeightForWidth())
        self.lstVue.setSizePolicy(sizePolicy)
        self.lstVue.setObjectName("lstVue")
        self.lytListe.addWidget(self.lstVue)
        self.lytCentral.addLayout(self.lytListe)
        self.lytGrille = QtWidgets.QGridLayout()
        self.lytGrille.setObjectName("lytGrille")
        self.lytCentral.addLayout(self.lytGrille)
        self.lytMain.addLayout(self.lytCentral)
        self.verticalLayout_2.addLayout(self.lytMain)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 881, 26))
        self.menubar.setObjectName("menubar")
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        self.menuGestion_database = QtWidgets.QMenu(self.menubar)
        self.menuGestion_database.setObjectName("menuGestion_database")
        self.menuConsultation = QtWidgets.QMenu(self.menubar)
        self.menuConsultation.setObjectName("menuConsultation")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuitter = QtWidgets.QAction(MainWindow)
        self.actionQuitter.setObjectName("actionQuitter")
        self.actionEditerVideo = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Ressources/listVideo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEditerVideo.setIcon(icon)
        self.actionEditerVideo.setText("")
        self.actionEditerVideo.setObjectName("actionEditerVideo")
        self.actionEnregistrerVideo = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Ressources/addVideo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEnregistrerVideo.setIcon(icon1)
        self.actionEnregistrerVideo.setText("")
        self.actionEnregistrerVideo.setObjectName("actionEnregistrerVideo")
        self.actionGestionTags = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Ressources/gestionTags.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGestionTags.setIcon(icon2)
        self.actionGestionTags.setText("")
        self.actionGestionTags.setObjectName("actionGestionTags")
        self.actionGestionClasseurs = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Ressources/classeurs.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGestionClasseurs.setIcon(icon3)
        self.actionGestionClasseurs.setText("")
        self.actionGestionClasseurs.setObjectName("actionGestionClasseurs")
        self.actionTableau_de_bord = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Ressources/dashBoard.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTableau_de_bord.setIcon(icon4)
        self.actionTableau_de_bord.setObjectName("actionTableau_de_bord")
        self.actionTableau_de_bord_2 = QtWidgets.QAction(MainWindow)
        self.actionTableau_de_bord_2.setObjectName("actionTableau_de_bord_2")
        self.actionTableau_de_bord_3 = QtWidgets.QAction(MainWindow)
        self.actionTableau_de_bord_3.setIcon(icon4)
        self.actionTableau_de_bord_3.setObjectName("actionTableau_de_bord_3")
        self.actionTableau_de_bord_4 = QtWidgets.QAction(MainWindow)
        self.actionTableau_de_bord_4.setIcon(icon4)
        self.actionTableau_de_bord_4.setText("")
        self.actionTableau_de_bord_4.setObjectName("actionTableau_de_bord_4")
        self.actionTableau_de_bord_5 = QtWidgets.QAction(MainWindow)
        self.actionTableau_de_bord_5.setIcon(icon4)
        self.actionTableau_de_bord_5.setObjectName("actionTableau_de_bord_5")
        self.actionParagraph = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Ressources/paragraph.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionParagraph.setIcon(icon5)
        self.actionParagraph.setText("")
        self.actionParagraph.setObjectName("actionParagraph")
        self.actionPlayer_vid_o = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Ressources/screenVideo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlayer_vid_o.setIcon(icon6)
        self.actionPlayer_vid_o.setText("")
        self.actionPlayer_vid_o.setObjectName("actionPlayer_vid_o")
        self.menuFichier.addAction(self.actionQuitter)
        self.menuGestion_database.addAction(self.actionEditerVideo)
        self.menuGestion_database.addAction(self.actionEnregistrerVideo)
        self.menuGestion_database.addSeparator()
        self.menuGestion_database.addAction(self.actionGestionTags)
        self.menuGestion_database.addAction(self.actionGestionClasseurs)
        self.menuGestion_database.addSeparator()
        self.menuConsultation.addAction(self.actionTableau_de_bord_5)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuGestion_database.menuAction())
        self.menubar.addAction(self.menuConsultation.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lblTitre.setText(_translate("MainWindow", "DERNIERES VUES"))
        self.lneRecherche.setPlaceholderText(_translate("MainWindow", "Recherche ..."))
        self.menuFichier.setTitle(_translate("MainWindow", "Fichier"))
        self.menuGestion_database.setTitle(_translate("MainWindow", "Saisie Vidéo"))
        self.menuConsultation.setTitle(_translate("MainWindow", "Consultation"))
        self.actionQuitter.setText(_translate("MainWindow", "Quitter"))
        self.actionTableau_de_bord.setText(_translate("MainWindow", "Tableau de bord"))
        self.actionTableau_de_bord_2.setText(_translate("MainWindow", "Tableau de bord"))
        self.actionTableau_de_bord_3.setText(_translate("MainWindow", "Tableau de bord"))
        self.actionTableau_de_bord_5.setText(_translate("MainWindow", "Tableau de bord"))
