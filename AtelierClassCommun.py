from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import cv2


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************    M A I N W I N D O W      C U S T O M      ********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class MainWindowCustom(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # Masquer la barre de titre
        self.setGeometry(100, 100, 700, 500)
        f = open('styles/QTextEdit.txt', 'r')
        style = f.read()
        self.setStyleSheet(style)

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        self.initUI_sys()

    def initUI_sys(self):
        self.boolMoveWindow = False
        self.mousePressed = False
        self.oldPos = None
        self.resizeCorner = None
        #  Barre de titre
        self.gpbTitre = QGroupBox(self)
        self.gpbTitre.setFixedSize(700, 35)
        self.gpbTitre.setStyleSheet('background-color: #3c3f41; border: 0px')
        self.gpbTitre.installEventFilter(self)
        self.lytTitre = QHBoxLayout()
        self.gpbTitre.setLayout(self.lytTitre)
        self.lytTitre.setContentsMargins(0, 0, 0, 0)
        #  Zone de Titre
        self.lblWindowTitle = QLabel(self.gpbTitre)
        self.lblWindowTitle.setStyleSheet('background-color: transparent; color: white')
        self.lblWindowTitle.setFixedWidth(500)
        #  Bouton mini
        self.btnMini = QPushButton(self.gpbTitre)
        self.btnMini.setFixedSize(58, 35)
        self.btnMini.setIcon(QIcon('ressources/titreMini.png'))
        self.btnMini.setIconSize(QSize(58, 35))
        self.btnMini.setStyleSheet('QPushButton:hover {background-color: #4f5254; color: white;}')
        self.btnMini.clicked.connect(self.miniWindow)
        #  Bouton max
        self.btnMax = QPushButton(self)
        self.btnMax.move(200, 200)
        self.btnMax.setFixedSize(58, 35)
        self.btnMax.setIcon(QIcon('ressources/titreNormal.png'))
        self.btnMax.setIconSize(QSize(58, 35))
        self.btnMax.setStyleSheet('QPushButton:hover {background-color: #4f5254; color: white;}')
        self.btnMax.clicked.connect(self.maxWindow)
        #  Bouton close
        self.btnClose = QPushButton(self.gpbTitre)
        self.btnClose.setFixedSize(58, 35)
        self.btnClose.setIcon(QIcon('ressources/titreClose.png'))
        self.btnClose.setIconSize(QSize(58, 35))
        self.btnClose.setStyleSheet('QPushButton:hover {background-color: #e81123; color: white;}')
        self.btnClose.clicked.connect(self.closeWindow)
        #  Menu
        combobox = QComboBox()
        combobox.addItem("Option 1")
        combobox.addItem("Option 2")
        combobox.addItem("Option 3")

        #
        self.lytTitre.addWidget(self.lblWindowTitle)
        self.lytTitre.addStretch()
        self.lytTitre.addWidget(self.btnMini)
        self.lytTitre.addWidget(self.btnMax)
        self.lytTitre.addWidget(self.btnClose)

        # Poignée de redimensionnement
        self.poignee = QLabel(self)
        self.poignee.setStyleSheet('background-color: transparent')
        self.poignee.setPixmap(QPixmap('ressources/poignee.png'))
        self.poignee.setFixedSize(20, 20)
        cursor = QCursor(Qt.SizeFDiagCursor)
        self.poignee.setCursor(cursor)

        #  Bouton fermer (avec sauvegarde des modifications)
        self.btnFermer = QPushButton(self)
        self.btnFermer.setText(self._trad('Fermer', self.lngCourGlobal))
        self.btnFermer.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                     'QPushButton:hover {border: 3px solid #cccccc}')
        self.btnFermer.setFixedSize(100, 35)
        self.btnFermer.move(600, 520)
        self.btnFermer.clicked.connect(self.closeWindow)

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def closeWindow(self):
        self.close()

    def miniWindow(self):
        self.showMinimized()

    def maxWindow(self):
        if self.isMaximized():
            self.showNormal()
            self.btnMax.setIcon(QIcon('ressources/titreNormal.png'))
        else:
            self.showMaximized()
            self.btnMax.setIcon(QIcon('ressources/titreMax.png'))

    def setTitle(self, aux):
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(False)
        self.lblWindowTitle.setFont(font)
        self.lblWindowTitle.setText(f'   {aux}')

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.LeftButton):
            if source == self.gpbTitre:
                self.boolMoveWindow = True
        return QWidget.eventFilter(self, source, event)

    def resizeEvent(self, event):
        self.gpbTitre.setFixedWidth(self.width())
        w = self.width()
        w = max(w, 200)
        h = self.height()
        h = max(h, 200)
        self.setGeometry(self.x(), self.y(), w, h)
        self.poignee.setGeometry(w - 15, h - 15, 15, 15)
        self.btnFermer.setGeometry(w - 130, h - 50, 100, 35)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.boolMoveWindow:
            self.dragPos = event.globalPos()
            event.accept()
        else:
            self.mousePressed = True
            self.oldPos = event.globalPos()
            # Déterminer si la souris est dans un coin de la fenêtre
            if event.x() < 10 and event.y() < 10:
                self.resizeCorner = Qt.TopLeftCorner
            elif event.x() > self.width() - 10 and event.y() < 10:
                self.resizeCorner = Qt.TopRightCorner
            elif event.x() < 10 and event.y() > self.height() - 10:
                self.resizeCorner = Qt.BottomLeftCorner
            elif event.x() > self.width() - 10 and event.y() > self.height() - 10:
                self.resizeCorner = Qt.BottomRightCorner

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePressed = False
            self.oldPos = None
            self.resizeCorner = None
            self.boolMoveWindow = False
            self.unsetCursor()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.boolMoveWindow:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
        else:
            try:
                delta = event.globalPos() - self.oldPos
                if self.resizeCorner == Qt.TopLeftCorner:
                    self.setGeometry(self.x() + delta.x(), self.y() + delta.y(), self.width() - delta.x(),
                                     self.height() - delta.y())
                elif self.resizeCorner == Qt.TopRightCorner:
                    self.setGeometry(self.x(), self.y() + delta.y(), self.width() + delta.x(),
                                     self.height() - delta.y())
                elif self.resizeCorner == Qt.BottomLeftCorner:
                    self.setGeometry(self.x() + delta.x(), self.y(), self.width() - delta.x(),
                                     self.height() + delta.y())
                elif self.resizeCorner == Qt.BottomRightCorner:
                    self.setGeometry(self.x(), self.y(), self.width() + delta.x(), self.height() + delta.y())
                self.oldPos = event.globalPos()
            except:
                pass

    def setBtnMax(self, boolAux):
        self.btnMax.setVisible(boolAux)

    def setBtnMini(self, boolAux):
        self.btnMini.setVisible(boolAux)

    def setBtnClose(self, boolAux):
        self.btnClose.setVisible(boolAux)

    def setPoignee(self, boolAux):
        self.poignee.setVisible(boolAux)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************            L A B E L I N D E X            ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class LabelIndex(QLabel):
    def __init__(self, parent, index, picture, ligne, colonne):
        QLabel.__init__(self, parent)
        self.index = index
        self.picture = picture
        self.ligne = ligne
        self.colonne = colonne
        self.boolOnglet = False
        self.parent = parent
        self.lytObject = QVBoxLayout()
        self.lblImage = QLabel(self)
        try:
            self.lblImage.setPixmap(picture)
        except:
            pass
        self.lytObject.addWidget(self.lblImage)
        self.lblImage.setScaledContents(True)

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        self.installEventFilter(self)

    def eventFilter(self, source, event):
        self.parent.parent.mainWindowDossier.dragCour = self
        if event.type() == event.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.boolOnglet:
                    self.boolOnglet = False
                    self.lblImage.setStyleSheet('border: 0px')
                    # mainWindow.gridWindow.lstGridVideo[indexCour].boolOnglet = False
                else:
                    self.boolOnglet = True
                    self.lblImage.setStyleSheet('border: 2px solid #74d7fe')
            if event.button() == Qt.RightButton:
                menu = QMenu()
                menu.setStyleSheet('background-color: gray; border: 1px solid #aaaaaa')
                menu.addAction(QIcon('ressources/crayon.png'), self._trad('Mode édition', self.lngCourGlobal),
                               lambda: self.editVideo(source.index))
                menu.addAction(QIcon('ressources/voir.png'), self._trad('Mode étude', self.lngCourGlobal),
                               lambda: self.parent.parent.displayTabWindow([source.index]))
                if self.boolOnglet:
                    #  Contruire liste des vignettes onglet
                    lstOnglet = []
                    for obj in self.parent.parent.selectZoneDroit.lstVignette:
                        labelIndex, obj1, obj2 = obj
                        if labelIndex.boolOnglet:
                            lstOnglet.append(labelIndex.index)

                    menu.addAction(QIcon('ressources/onglet.png'), self._trad('Voir mes vidéos', self.lngCourGlobal),
                                   lambda: self.parent.parent.displayTabWindow(lstOnglet))
                if menu.exec_(event.globalPos()):
                    return True
        return super().eventFilter(source, event)

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def editVideo(self, cleVideo):
        self.parent.parent.editVideo(cleVideo)

    def mousePressEventMethod(self):
        if self.boolOnglet:
            self.boolOnglet = False
            self.setStyleSheet('border: 0px')
            # mainWindow.gridWindow.lstGridVideo[indexCour].boolOnglet = False
        else:
            self.boolOnglet = True
            self.setStyleSheet('border: 2px solid #74d7fe')
            # mainWindow.gridWindow.lstGridVideo[indexCour].boolOnglet = True

    def mouseDoubleClickEvent(self, evt):
        if self.index == -1:
            return
        if evt.buttons() == Qt.RightButton:
            return
        lstVideo = [self.index]
        self.parent.parent.displayTabWindow(lstVideo)

    def mouseDoubleClickMethod(self):
        if self.index == -1:
            return
        lstVideo = [self.index]
        # self.parent.parent.displayTabWindow(lstVideo)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.boolOnglet = False
            self.lblImage.setStyleSheet('border: 0px')
            mimeData = QMimeData()
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            dropAction = drag.exec_(Qt.MoveAction)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************              B O U T O N I N D E X               ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class BoutonIndex(QPushButton):
    def __init__(self, parent=None, timeCode=None, videoID=None):
        super(BoutonIndex, self).__init__(parent)
        self.parent = parent
        self.timeCode = timeCode
        self.videoID = videoID


#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************    D I A L O G C U S T O M    **************************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************
class DialogCustom(QDialog):
    def __init__(self, parent=None, contenant=None, x=100, y=100):
        super(DialogCustom, self).__init__(parent)
        self.x = x
        self.y = y
        self.contenant = contenant

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        self.setUpUISystem()

        self.button_ok = QPushButton(self)
        self.button_ok.setFixedSize(100, 35)
        self.button_ok.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                     'QPushButton:hover {border: 3px solid #cccccc}')
        self.button_ok.setText(self._trad('Accepter', self.lngCourGlobal))
        self.button_ok.move(50, 200)

        self.button_annul = QPushButton(self)
        self.button_annul.setFixedSize(100, 35)
        self.button_annul.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                        'QPushButton:hover {border: 3px solid #cccccc}')
        self.button_annul.setText(self._trad('Refuser', self.lngCourGlobal))
        self.button_annul.move(300, 200)

        #  Zone de message
        grpMessage = QGroupBox(self)
        grpMessage.setFixedSize(350, 155)
        grpMessage.setStyleSheet('background-color: #223333; border: 0px;')
        grpMessage.move(50, 35)

        # Label message
        self.lblMessage = QLabel(grpMessage)
        self.lblMessage.setStyleSheet('color: #ffffff; background-color: #223333')
        self.lblMessage.setFixedSize(300, 155)
        self.lblMessage.setWordWrap(True)
        self.lblMessage.setAlignment(Qt.AlignTop)
        self.lblMessage.setWordWrap(True)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(False)
        self.lblMessage.setFont(font)
        self.lblMessage.move(20, 15)
        #  Zone saisie
        self.grpSaisie = QGroupBox(self)
        self.grpSaisie.setFixedSize(350, 75)
        self.grpSaisie.setStyleSheet('background-color: #223333; border: 0px')
        self.grpSaisie.move(50, 115)
        # lineEdit saisie
        self.lneSaisie = QLineEdit(self.grpSaisie)
        self.lneSaisie.setStyleSheet('color: #ffffff; background-color: #666666; border-radius: 6px')
        self.lneSaisie.setFixedSize(350, 35)
        self.lneSaisie.setAlignment(Qt.AlignLeft)
        # self.lblMessage.setWordWrap(True)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(9)
        font.setBold(False)
        self.lneSaisie.setFont(font)
        self.lneSaisie.setVisible(True)
        self.lneSaisie.move(0, 15)

        # Connexion des signaux et des slots
        self.button_ok.clicked.connect(self.accept)
        self.button_annul.clicked.connect(self.reject)

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def setUpUISystem(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Masquer la barre de titre
        self.setGeometry(self.x, self.y, 450, 250)
        self.move(0, 0)
        self.setStyleSheet('background-color: #223333; border: 1px solid gray')

        self.boolMoveWindow = False
        self.mousePressed = False
        self.oldPos = None
        self.resizeCorner = None

        #  Barre de titre
        self.gpbTitre = QGroupBox(self)
        self.gpbTitre.setFixedSize(450, 35)
        self.gpbTitre.setStyleSheet('background-color: #3c3f41; border-left: 1px solid gray; '
                                    'border-top: 1px solid gray; border-right: 1px solid gray; border-bottom: 0px')
        self.gpbTitre.installEventFilter(self)
        self.lytTitre = QHBoxLayout()
        self.gpbTitre.setLayout(self.lytTitre)
        self.lblWindowTitle = QLabel(self.gpbTitre)
        self.lblWindowTitle.setFixedSize(300, 35)
        self.lblWindowTitle.setStyleSheet('background-color: transparent; color: white; border: 0px')
        self.lytTitre.addWidget(self.lblWindowTitle)
        self.lytTitre.setContentsMargins(0, 0, 0, 0)

        #  Bouton close
        self.btnClose = QPushButton(self.gpbTitre)
        self.btnClose.setFixedSize(58, 35)
        self.btnClose.setIcon(QIcon('ressources/titreClose.png'))
        self.btnClose.setIconSize(QSize(58, 35))
        self.btnClose.setStyleSheet('QPushButton{border: 0px} '
                                    'QPushButton:hover {background-color: #e81123; color: white;}')
        self.btnClose.clicked.connect(self.closeWindow)

        self.lytTitre.addStretch()
        self.lytTitre.addWidget(self.btnClose)

    def setMessage(self, aux):
        self.lblMessage.setText(aux)

    def setBouton1(self, aux, boolVisible):
        self.button_ok.setVisible(boolVisible)
        if boolVisible:
            self.button_ok.setText(aux)

    def setBouton2(self, aux, boolVisible):
        self.button_annul.setVisible(boolVisible)
        if boolVisible:
            self.button_annul.setText(aux)

    def setSaisie(self, aux, boolVisible):
        self.grpSaisie.setVisible(boolVisible)
        if boolVisible:
            self.lneSaisie.setPlaceholderText(aux)

    def setPosition(self, x, y):
        self.move(x, y)

    def closeWindow(self):
        self.close()

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.LeftButton):
            if source == self.gpbTitre:
                self.boolMoveWindow = True
        return QWidget.eventFilter(self, source, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.boolMoveWindow:
            self.dragPos = event.globalPos()
            event.accept()
        else:
            self.mousePressed = True
            self.oldPos = event.globalPos()
            # Déterminer si la souris est dans un coin de la fenêtre
            if event.x() < 10 and event.y() < 10:
                self.resizeCorner = Qt.TopLeftCorner
            elif event.x() > self.width() - 10 and event.y() < 10:
                self.resizeCorner = Qt.TopRightCorner
            elif event.x() < 10 and event.y() > self.height() - 10:
                self.resizeCorner = Qt.BottomLeftCorner
            elif event.x() > self.width() - 10 and event.y() > self.height() - 10:
                self.resizeCorner = Qt.BottomRightCorner

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePressed = False
            self.oldPos = None
            self.resizeCorner = None
            self.boolMoveWindow = False
            self.unsetCursor()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.boolMoveWindow:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
        else:
            delta = event.globalPos() - self.oldPos
            if self.resizeCorner == Qt.TopLeftCorner:
                self.setGeometry(self.x() + delta.x(), self.y() + delta.y(), self.width() - delta.x(),
                                 self.height() - delta.y())
            elif self.resizeCorner == Qt.TopRightCorner:
                self.setGeometry(self.x(), self.y() + delta.y(), self.width() + delta.x(),
                                 self.height() - delta.y())
            elif self.resizeCorner == Qt.BottomLeftCorner:
                self.setGeometry(self.x() + delta.x(), self.y(), self.width() - delta.x(),
                                 self.height() + delta.y())
            elif self.resizeCorner == Qt.BottomRightCorner:
                self.setGeometry(self.x(), self.y(), self.width() + delta.x(), self.height() + delta.y())
            self.oldPos = event.globalPos()

    def setBtnClose(self, boolAux):
        self.btnClose.setVisible(boolAux)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************               L A B E L T A G             ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class LabelTag(QLabel):
    def __init__(self, parent, contenant, texte, color):
        # QLabel.__init__(self, parent)
        super(LabelTag, self).__init__(parent)
        self.texte = texte
        self.styleDeselect = f'color: white; background-color: {color}; border: 1px solid {color}; border-radius: 10px'
        self.styleSelect = f'color: white; background-color: #f05a24; border: 1px solid {color}; border-radius: 10px'
        self.setStyleSheet(self.styleDeselect)
        self.setFixedSize(50, 50)
        width = self.fontMetrics().boundingRect(texte).width()
        self.parent = parent
        self.contenant = contenant
        self.width = width
        self.setFixedWidth(width + 20)
        self.setFixedHeight(20)
        self.setAlignment(Qt.AlignCenter)
        self.largeur = self.width
        self.setText(texte)
        self.boolSelect = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.majEtatSelect()

    def setPosition(self, x, y):
        self.move(x, y)

    def majEtatSelect(self):
        if self.boolSelect:
            self.boolSelect = False
            self.setStyleSheet(self.styleDeselect)
            self.contenant.listTagSelect.remove(self)

        else:
            self.boolSelect = True
            self.setStyleSheet(self.styleSelect)
            self.contenant.listTagSelect.append(self)
            self.contenant.motCour = self.texte


#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************   P A S T I L L E   S I M P L E  ***********************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************
class PastilleSimple(QLabel):
    def __init__(self, parent=None, radius=5, color=None):
        super(PastilleSimple, self).__init__(parent)
        self.radius = radius
        self.color = color
        self.setStyleSheet('background-color: transparent')
        self.setFixedSize(2 * self.radius + 3, 2 * self.radius + 3)

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen(QColor(self.color))
        painter.setPen(pen)
        brush = QBrush(QColor(self.color))
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(brush)
        painter.drawEllipse(1, 1, 2 * self.radius, 2 * self.radius)

    def setPosition(self, x, y):
        self.move(x, y)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           V I D E O R E C O R D           ***********************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class VideoFileRecord:
    def __init__(self, cle=0):
        self.cle = cle
        query = QSqlQuery()
        query.exec(f'SELECT * FROM videoFileTab WHERE cle={self.cle}')
        self.timeCodeIcone = 0
        self.titreVideo = ''
        self.boolOnglet = False

        #  Initialisation de la langue
        query1 = QSqlQuery()
        query1.exec(f'SELECT langue FROM parametersTab')
        if query1.next():
            aux = query1.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        if query.next():
            self.cleClasseur = query.value('cleClasseur')
            self.ordreClasseur = query.value('ordreClasseur')
            self.videoName = query.value('videoName')
            self.videoPath = query.value('videoFullPath')
            self.marquePage = query.value('marquePage')
            self.dateLastView = query.value('dateLastView')
            self.dateCreation = query.value('dateCreation')
            self.statut = query.value('statut')
            self.nomClasseur = ''
            if self.cleClasseur > -1:
                query1 = QSqlQuery()
                query1.exec(f'SELECT nom FROM classeurTab WHERE cle={self.cleClasseur}')
                if query1.next():
                    self.nomClasseur = query1.value('nom')
            else:
                self.nomClasseur = self._trad('Aucun classeur', self.lngCourGlobal)
            self.nomStatut = ''
            if self.statut > -1:
                query1 = QSqlQuery()
                query1.exec(f'SELECT nom, color FROM statutTab WHERE cle={self.statut}')
                if query1.next():
                    self.nomStatut = query1.value('nom')
                    self.colorStatut = query1.value('color')
                else:
                    self.nomStatut = self._trad('Aucun label', self.lngCourGlobal)
                    self.colorStatut = ''
            # self.boolTag = boolTag
            self.Favori = query.value('Favori')
            self.internalPath = query.value('internalPath')
            self.cleBiblio = query.value('cleBiblio')
            self.note = query.value('note')
            self.deleted = query.value('deleted')
        self.ongletVideo = False

        # recherche présence de la video dans paragraph
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM paragraph WHERE cleVideo={self.cle} AND timeNote=0 AND Titre={True}')
        if query.next():
            self.boolTag = True
            self.titreVideo = query.value('texte')
            #  Recherche de la picture icone
            query1 = QSqlQuery()
            query1.exec(f'SELECT timeNote FROM paragraph WHERE cleVideo={self.cle} AND icone={True}')
            if query1.next():
                self.timeCodeIcone = query1.value('timeNote')
            else:
                self.timeCodeIcone = 10
        else:
            self.boolTag = False

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def __str__(self):
        aux = f'cle->{self.cle} - cleClasseur->{self.cleClasseur} - ordreClasseur->{self.ordreClasseur} - ' \
              f'viodeoName->{self.videoName} - videoPath->{self.videoPath} - marquePage->{self.marquePage} - ' \
              f'dateLastView->{self.dateLastView} - statut->{self.statut} - nomClasseur->{self.nomClasseur}' \
              f' - boolTag->{self.boolTag} - Favori->{self.Favori} - InternalPath->{self.internalPath}' \
              f' - cleBiblio->{self.cleBiblio} - ongletVideo->{self.ongletVideo} - timeCodeIcone->{self.timeCodeIcone}' \
              f' - titreVideo->{self.titreVideo} - note->{self.note} - deleted->{self.deleted}' \
              f' - dateCreation->{self.dateCreation}'
        return aux


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************        F O R M T A G I N T E R N E      *************************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class FormTagInterne(QGroupBox):
    def __init__(self, parent, contenant, videoID, lytMain, marqueCour):
        super().__init__()
        self.setStyleSheet('background-color: #333333; margin: 0px')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(100)

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        self.parent = parent
        self.contenant = contenant
        self.videoID = videoID
        self.motCour = ''
        self.boolModif = False
        self.indexCour = -1
        self.titreComment = ''
        self.listTag = []
        self.listTagSelect = []
        self.marqueCour = marqueCour

        grpTop = QGroupBox()
        grpTop.setStyleSheet('background: transparent')
        grpTop.setFixedSize(600, 50)
        lytMain.addWidget(grpTop)

        #  Saisie du tag
        self.lneTag = QLineEdit(grpTop)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.lneTag.setFont(font)
        self.lneTag.returnPressed.connect(self.sauverTag)
        self.lneTag.setPlaceholderText(self._trad('Saisir un tag ou cliquer sur la liste...', self.lngCourGlobal))
        self.lneTag.setStyleSheet('margin: 0px; color: white; background: #666666; border-radius: 6px')
        self.lneTag.setFixedSize(400, 35)
        self.lneTag.move(0, 1)
        # Bouton Plus
        self.btnAdmiPlus = QPushButton(grpTop)
        self.btnAdmiPlus.setIcon(QIcon('ressources/admiPlus.png'))
        self.btnAdmiPlus.setFixedSize(39, 39)
        self.btnAdmiPlus.setIconSize(QSize(33, 33))
        self.btnAdmiPlus.move(410, 0)
        self.btnAdmiPlus.setCursor(Qt.PointingHandCursor)
        self.btnAdmiPlus.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiPlus.clicked.connect(self.sauverTag)
        #  Bouton Modif
        self.btnAdmiModif = QPushButton(grpTop)
        self.btnAdmiModif.setIcon(QIcon('ressources/admiModif.png'))
        self.btnAdmiModif.setFixedSize(39, 39)
        self.btnAdmiModif.setIconSize(QSize(33, 33))
        self.btnAdmiModif.move(450, 0)
        self.btnAdmiModif.setCursor(Qt.PointingHandCursor)
        self.btnAdmiModif.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiModif.clicked.connect(self.modifTag)
        #  Bouton Suppr
        self.btnAdmiSuppr = QPushButton(grpTop)
        self.btnAdmiSuppr.setIcon(QIcon('ressources/admiSuppr.png'))
        self.btnAdmiSuppr.setFixedSize(39, 39)
        self.btnAdmiSuppr.setIconSize(QSize(33, 33))
        self.btnAdmiSuppr.move(490, 0)
        self.btnAdmiSuppr.setCursor(Qt.PointingHandCursor)
        self.btnAdmiSuppr.setStyleSheet('QPushButton:hover {background-color: #dddddd; color: white;}')
        self.btnAdmiSuppr.clicked.connect(self.effaceTag)

        self.grpBoxAffichTag = QGroupBox(self)
        self.grpBoxAffichTag.setStyleSheet('border: 0px; background: #333333')
        self.lytAffichTag = QVBoxLayout()
        self.grpBoxAffichTag.setLayout(self.lytAffichTag)
        self.grpBoxAffichTag.setFixedSize(590, 120)  # 590

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(self.grpBoxAffichTag)
        scroll.setWidgetResizable(True)
        scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        f = open('styles/listItem.txt', 'r')
        style = f.read()
        styleQScrollBar = style
        scroll.setStyleSheet(styleQScrollBar)
        layout = QHBoxLayout(self)
        layout.addWidget(scroll)

        self.populateGrpBoxAffichTag()

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def effaceTag(self):
        if len(self.listTagSelect) == 0:
            self.dialog = DialogCustom()
            aux = self._trad('Pas de tag sélectionné.', self.lngCourGlobal)
            self.dialog.setMessage(aux)
            self.dialog.setPosition(100, 100)
            self.dialog.setBouton1(self._trad('Fermer', self.lngCourGlobal), False)
            self.dialog.setBouton2(self._trad('Fermer', self.lngCourGlobal), True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return
        #  la cle correspodant au tag concerné
        query = QSqlQuery()
        lenListe = len(self.listTagSelect)
        self.dialog = DialogCustom()
        aux = 'Vous êtes en train de supprimer les tags sélectionnés. \nEtes-vous certain de votre choix ?'
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)
        if self.dialog.exec_() == DialogCustom.Accepted:

            for i in range(0, lenListe):
                query.exec(
                    f'SELECT * FROM tagTab WHERE cleVideo={self.videoID} AND mot="{self.listTagSelect[i].texte}"')
                cle = 0
                if query.next():
                    cle = query.value('cle')
                query = QSqlQuery()
                bOk = query.exec(f'DELETE FROM tagTab WHERE cle = {cle}')
        self.listTagSelect = []
        self.populateGrpBoxAffichTag()

    def modifTag(self):
        if len(self.listTagSelect) == 0:
            self.dialog = DialogCustom(self, 0, 0)
            aux = self._trad('Pas de tag sélectionné.', self.lngCourGlobal)
            self.dialog.setMessage(aux)
            self.dialog.setPosition(0, 0)
            self.dialog.setBouton1(self._trad('Fermer', self.lngCourGlobal), False)
            self.dialog.setBouton2(self._trad('Fermer', self.lngCourGlobal), True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return

        if len(self.listTagSelect) > 1:
            self.dialog = DialogCustom()
            aux = self._trad("L'opération de modification ne s'applique\nqu'à un tag à la fois.", self.lngCourGlobal)
            self.dialog.setMessage(aux)
            self.dialog.setPosition(0, 0)
            self.dialog.setBouton1(self._trad('Fermer', self.lngCourGlobal), False)
            self.dialog.setBouton2(self._trad('Fermer', self.lngCourGlobal), True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return

        self.motCour = self.listTagSelect[0].texte
        self.lneTag.setText(self.motCour)
        self.listTagSelect = []
        self.indexCour = self.listTag.index(self.motCour)
        self.boolModif = True

    def sauverTag(self):
        #  Vérifier l'existence du tag en doublon
        self.listTag = []
        query = QSqlQuery()
        query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID}')
        while query.next():
            self.listTag.append(query.value('mot'))
        mot = self.lneTag.text()

        if mot in self.listTag:
            QMessageBox.information(self, self._trad('Enregistrement annulé', self.lngCourGlobal),
                                    self._trad('Le tag existe déja pour cette vidéo.', self.lng))
        else:
            if self.boolModif:
                #  la cle correspodant au tag concerné
                query = QSqlQuery()
                query.exec(f'SELECT * FROM tagTab WHERE cleVideo={self.videoID} AND mot="{self.motCour}"')
                if query.next():
                    cle = query.value('cle')
                query = QSqlQuery()
                tplChamps = ('cle', 'timeCode', 'mot', 'cleVideo')
                tplData = (cle, self.marqueCour, self.lneTag.text(), self.videoID)
                bOk = query.exec(f'UPDATE tagTab SET {tplChamps} = {tplData} WHERE cle = {cle}')
                self.populateGrpBoxAffichTag()
            else:
                #  Recherche de l'index suivant
                cleMax = 1
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) AS cleMax FROM tagTab')
                try:
                    if query.next():
                        cleMax = query.value('cleMax') + 1
                except:
                    pass
                tplData = (cleMax, self.marqueCour, mot, self.videoID)
                tplChamps = ('cle', 'timeCode', 'mot', 'cleVideo')
                query1 = QSqlQuery()
                query1.exec(f'INSERT INTO tagTab {tplChamps} VALUES {tplData}')
                self.listTag.append(mot)
        self.lneTag.setText('')
        self.boolModif = False
        self.listTagSelect = []
        self.populateGrpBoxAffichTag()

    def populateGrpBoxAffichTag(self):
        # Remplacer les notes (Null) par 0
        query = QSqlQuery()
        query.exec('UPDATE videoFileTab SET note = 0 WHERE note IS NULL')
        query = QSqlQuery()
        # Effacer le contenu de lytAffichTag
        while 1:
            child = self.lytAffichTag.takeAt(0)
            if not child:
                break
            try:
                child.widget().deleteLater()
            except:
                pass

        self.listTag = []
        query = QSqlQuery()
        ok = query.exec(f'SELECT * FROM tagTab where timeCode={self.marqueCour} AND cleVideo={self.videoID}')
        while query.next():
            self.listTag.append(query.value('mot'))

        if len(self.listTag) == 0:
            return
        ligne = 0
        # *********************************************************************************************
        # *********************************************************************************************
        i = 0
        continuerLigne = True
        largLigneTag = 0
        largeur = 550
        offSet = 28
        lenList = len(self.listTag)
        grpBox = QGroupBox()
        grpBox.setFixedHeight(1000)
        grpBox.setStyleSheet('border: 0px; background: #333333')
        self.lytAffichTag.addWidget(grpBox)
        self.lytAffichTag.setSpacing(0)
        nbLigne = 0
        while continuerLigne:
            continuerColonne = True
            while continuerColonne:
                lblTag = LabelTag(grpBox, self, self.listTag[i], '#666666')
                # lblTag.installEventFilter(self)
                lblTag.setPosition(largLigneTag, nbLigne * 30)
                largLigneTag += lblTag.width + offSet
                if i + 1 == lenList:
                    self.lytAffichTag.addWidget(grpBox)
                    continuerLigne = False
                    continuerColonne = False
                    lblTag.setPosition(largLigneTag - lblTag.width - offSet, nbLigne * 30)
                else:
                    if largLigneTag > largeur - lblTag.width - offSet - 20:
                        largLigneTag = 0
                        lblTag.close()
                        nbLigne += 1
                        i -= 1
                        continuerColonne = False
                i += 1
        self.lneTag.setText('')


#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************        S T A R R A T I N G       ***********************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************
class StarRating(QGroupBox):
    def __init__(self, rating):
        super().__init__()
        self.setFixedSize(150, 35)
        self.setStyleSheet('background-color: #333333; border: 0px')
        self.lyt = QHBoxLayout()
        self.setLayout(self.lyt)
        self.rating = rating
        # self.parent = parent
        self.lstBtn = []
        self.initStarRating()

    def initStarRating(self):
        for i in range(1, 6):
            btn = QPushButton()
            if self.rating + 1 > i:
                btn.setIcon(QIcon('ressources/orangeStar.png'))
            else:
                btn.setIcon(QIcon('ressources/blackStar.png'))
            btn.setStyleSheet('QPushButton {background-color: transparent; border: 0px} '
                              'QPushButton:hover{background-color: #888888} QToolTip{color: white}')

            btn.setFixedSize(25, 25)
            btn.setToolTip(str(i))
            self.lyt.addWidget(btn)
            btn.clicked.connect(self.evt_btn_clicked)
            self.lstBtn.append(btn)

    def majRatingStar(self):
        i = 0
        for itm in self.lstBtn:
            if int(itm.toolTip()) == 0:
                pass
            else:
                if self.rating + 1 > int(itm.toolTip()):
                    pass
                    itm.setIcon(QIcon('ressources/orangeStar.png'))
                else:
                    pass
                    itm.setIcon(QIcon('ressources/blackStar.png'))

    def evt_btn_clicked(self):
        sender = self.sender()
        nbStar = int(sender.toolTip())
        if nbStar == 1 and self.rating == 1:
            self.rating = 0
        else:
            self.rating = nbStar
        self.majRatingStar()

    def setBackgound(self, coulor):
        self.setStyleSheet(f'background-color: {coulor}')


#  ************************************************************************************************************
#  ************************************************************************************************************
#  ***************        W I D G E T F A V O R I       *******************************************************
#  ************************************************************************************************************
#  ************************************************************************************************************
class WidgetFavori(QLabel):
    def __init__(self, boolFavori):
        super().__init__()
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.boolFavori = boolFavori
        self.setFixedSize(25, 25)
        self.setStyleSheet('background-color: transparent')
        if self.boolFavori:
            self.setPixmap(QPixmap('ressources/favoriRouge'))
        else:
            self.setPixmap(QPixmap('ressources/favoriGris'))

    def mousePressEvent(self, event):
        self.boolFavori = not self.boolFavori
        if self.boolFavori:
            self.setPixmap(QPixmap('ressources/favoriRouge'))
        else:
            self.setPixmap(QPixmap('ressources/favoriGris'))

    def setPosition(self, x, y):
        self.move(x, y)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************              B O U T O N O F F O N               ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class BoutonOffOn(QGroupBox):
    def __init__(self, parent=None):
        super(BoutonOffOn, self).__init__(parent)
        self.setStyleSheet('background-color: #222222; padding: 0, 0, 0, 0;border: 1px solid gray')
        self.setFixedSize(105, 32)
        self.button = QPushButton(self)
        self.button.setFixedSize(46, 26)
        self.button.move(2, 0)
        self.boolON = True
        self.button.setIconSize(QSize(46, 26))
        self.button.setStyleSheet('border: 1px; border-radius: 4px')
        self.button.clicked.connect(self.move_button)
        self.button.setCursor(Qt.PointingHandCursor)
        self.move_button()

    def initBool(self, boolValue):
        self.boolON = not boolValue
        self.move_button()

    def move_button(self):
        if self.boolON:
            self.boolON = False
            self.button.setIcon(QIcon('ressources/btnOFF.png'))
            self.button.move(55, 3)
        else:
            self.boolON = True
            self.button.setIcon(QIcon('ressources/btnON1.png'))
            self.button.move(4, 3)

    def setPos(self, x, y):
        self.move(x, y)

    def setBackGround(self, color):
        self.setStyleSheet(f'background-color: {color}; padding: 0, 0, 0, 0; ')


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           P A R A G R A P H R E C O R D           ***************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class ParagrapheRecord():
    def __init__(self, cle):
        self.cle = cle

        query = QSqlQuery()
        query.exec(f'SELECT * FROM paragraph WHERE cle={cle}')
        if query.next():
            self.timeNote = query.value('timeNote')
            self.indentation = query.value('indentation')
            self.titre = query.value('titre')
            self.picture = query.value('picture')
            self.texte = query.value('texte')
            self.icone = query.value('icone')
            self.cleLien = query.value('cleLien')
            self.cleVideo = query.value('cleVideo')
            self.note = query.value('note')
            self.hauteur = query.value('hauteur')
            self.largeur = query.value('largeur')
            self.icone = query.value('icone')
            self.boolModif = False
            self.lienWeb = query.value('lienWeb')

        # query = QSqlQuery()
        # query.exec(f'SELECT icone FROM paragraph WHERE cle=116')

    def __str__(self):
        aux = f'cle->{self.cle} - timeNote->{self.timeNote} - indentation->{self.indentation} - ' \
              f'titre->{self.titre} - picture->{self.picture} - texte->{self.texte} - ' \
              f'icone->{self.icone} - cleLien->{self.cleLien} - cleVideo->{self.cleVideo} - note->{self.note}'
        return aux


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************           B U T T O N  L E F T  R I G H T           *************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class ButtonLeftRight(QPushButton):
    def __init__(self, parent, callBackLeft, callBackRight):
        super().__init__(parent)
        self.parent = parent
        self.callBackLeft = callBackLeft
        self.callBackRight = callBackRight

    def mousePressEvent(self, event):
        self.pos = (event.globalPos())
        if event.button() == Qt.LeftButton:
            self.callBackLeft()
        elif event.button() == Qt.RightButton:
            self.callBackRight()


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************              B O U T O N I N D E X               ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class BoutonIndex(QPushButton):
    def __init__(self, parent=None, timeCode=None, videoID=None):
        super(BoutonIndex, self).__init__(parent)
        self.parent = parent
        self.timeCode = timeCode
        self.videoID = videoID
        # print(videoID, timeCode)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************        T E X TT E D I T  F O N T      ***************************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class TextEditFont(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print(event.pos())
            cursor = self.cursorForPosition(event.pos())
            format = cursor.charFormat()
            font = format.font()


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************        F O R M B L O C K N O T E      ***************************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************

class FormBlockNote(MainWindowCustom):
    def __init__(self, parent, videoPath, videoID, marqueCour, boolCreer):
        super().__init__()
        # print(parent.mainWin.nbColonnes)
        self.setGeometry(100, 100, 1210, 768)

        self.setStyleSheet('background-color: #262626')
        # ***** ARGUMENTS  ***************
        self.parent = parent
        self.videoPath = videoPath
        self.videoID = videoID
        self.marqueCour = marqueCour
        self.boolCreer = boolCreer
        # ********************************
        self.cleNoteCour = -1
        self.cleSnapShotCour = -1
        self.cleTitreCour = -1
        self.listTpl = []

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        self.setTitle(self._trad('Ceci est un exemple de titre', self.lngCourGlobal))

        self.setUpUI()

        if not self.boolCreer:
            self.populateNoteModif()

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def setUpUI(self):
        # **************************************************************
        # lne saisie titre ou paragraphe
        # **************************************************************
        self.lneTitreParagraph = QLineEdit(self)
        self.lneTitreParagraph.setFixedSize(513, 35)
        self.lneTitreParagraph.setPlaceholderText(self._trad('Saisir le titre de la vidéo ou du paragraphe',
                                                             self.lngCourGlobal))
        self.lneTitreParagraph.setStyleSheet('background-color: #666666; color: white; border: 0px;'
                                             'border-radius: 6px')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.lneTitreParagraph.setFont(font)
        self.lneTitreParagraph.move(20, 60)
        self.lneTitreParagraph.textChanged.connect(self.evt_lneTitreParagraph_textChanged)
        # **************************************************************
        #  Bouton ValideTitre
        # **************************************************************
        self.btnValideTitre = BoutonOffOn(self)
        aux = self.lneTitreParagraph.text()
        if aux == '':
            self.btnValideTitre.initBool(False)
        else:
            self.btnValideTitre.initBool(True)
        self.btnValideTitre.move(563, 60)
        # **************************************************************
        #  Liste des fonts disponibles
        # **************************************************************
        font_db = QFontDatabase()
        font_families = font_db.families()
        self.cmbFontWidget = QComboBox(self)
        # self.cmbFontWidget.setStyleSheet('QComboBox {background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #eeeeee, stop:1 #aaaaaa);'
        #                                  ' color: black; border: 0px;}')
        f = open('styles/QComboBoxDegrade.txt', 'r')
        style = f.read()
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(True)
        self.cmbFontWidget.setStyleSheet(style)
        self.cmbFontWidget.setFont(font)
        self.cmbFontWidget.setFixedSize(180, 30)
        self.cmbFontWidget.setWindowTitle(self._trad('Polices disponibles', self.lngCourGlobal))
        # Ajouter chaque police à QListWidget
        i = 0
        for font_family in font_families:
            # list_item = QListWidgetItem(font_family)
            self.cmbFontWidget.addItem(font_family, i)
            i += 1
        self.cmbFontWidget.setCurrentIndex(3)
        self.cmbFontWidget.move(20, 140)
        self.cmbFontWidget.currentIndexChanged.connect(self.changeFontNote)
        # **************************************************************
        #  Liste des tailles de font
        # **************************************************************
        self.spnTaillePolice = QSpinBox(self)
        self.spnTaillePolice.setRange(8, 72)
        self.spnTaillePolice.setFixedSize(60, 30)
        self.spnTaillePolice.setFont(font)
        self.spnTaillePolice.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                           'stop:0 #aaaaaa, stop:1 #eeeeee); color: black; border: 0px;'
                                           'border-radius: 4px; border: 1px solid #262626')
        self.spnTaillePolice.move(207, 140)
        self.spnTaillePolice.valueChanged.connect(self.evt_spnTaillePolice_changed)
        # **************************************************************
        #  Bouton Gras
        # **************************************************************
        self.btnGras = QPushButton(self)
        self.btnGras.setFixedSize(30, 30)
        self.btnGras.setStyleSheet('QPushButton {background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                   'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
                                   'border-radius: 4px; border: 1px solid #262626} '
                                   'QPushButton:hover {border: 3px solid #ffffff}')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(True)
        self.btnGras.setFont(font)
        self.btnGras.setFont(font)
        self.btnGras.setText('B')
        self.btnGras.move(280, 140)
        self.btnGras.clicked.connect(self.evt_btnGras_clicked)

        # **************************************************************
        #  Bouton Italic
        # **************************************************************
        self.btnItalic = QPushButton(self)
        self.btnItalic.setFixedSize(30, 30)
        self.btnItalic.setStyleSheet('QPushButton {background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                     'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
                                     'border-radius: 4px; border: 1px solid #262626} '
                                     'QPushButton:hover {border: 3px solid #ffffff}')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setItalic(True)
        font.setBold(True)
        self.btnItalic.setFont(font)
        self.btnItalic.setText('I')
        self.btnItalic.move(317, 140)
        self.btnItalic.clicked.connect(self.evt_btnItalic_clicked)

        # **************************************************************
        #  Bouton Underline
        # **************************************************************
        self.btnUnderline = QPushButton(self)
        self.btnUnderline.setFixedSize(30, 30)
        self.btnUnderline.setStyleSheet('QPushButton {background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                     'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
                                     'border-radius: 4px; border: 1px solid #262626} '
                                     'QPushButton:hover {border: 3px solid #ffffff}')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setUnderline(True)
        font.setBold(True)
        self.btnUnderline.setFont(font)
        self.btnUnderline.setText('I')
        self.btnUnderline.move(354, 140)
        self.btnUnderline.clicked.connect(self.evt_btnUnderline_clicked)


        # **************************************************************
        #  Bouton undo
        # **************************************************************
        self.btnUndo = QPushButton(self)
        self.btnUndo.setFixedSize(30, 30)
        self.btnUndo.setStyleSheet('QPushButton {background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                   'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
                                   'border-radius: 4px; border: 1px solid #262626} '
                                   'QPushButton:hover {border: 3px solid #ffffff}')
        self.btnUndo.setIcon(QIcon('ressources/undo.png'))
        self.btnUndo.move(405, 140)
        self.btnUndo.clicked.connect(self.textEditNote_undo)
        # **************************************************************
        #  Bouton redo
        # **************************************************************
        self.btnRedo = QPushButton(self)
        self.btnRedo.setFixedSize(30, 30)
        self.btnRedo.setStyleSheet('QPushButton {background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                   'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
                                   'border-radius: 4px; border: 1px solid #262626} '
                                   'QPushButton:hover {border: 3px solid #ffffff}')
        self.btnRedo.setIcon(QIcon('ressources/redo.png'))
        self.btnRedo.move(440, 140)
        self.btnRedo.clicked.connect(self.textEditNote_redo)
        # **************************************************************
        #  Bouton link
        # **************************************************************
        self.btnLink = QPushButton(self)
        self.btnLink.setFixedSize(30, 30)
        self.btnLink.setStyleSheet('QPushButton {background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                   'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
                                   'border-radius: 4px; border: 1px solid #262626} '
                                   'QPushButton:hover {border: 3px solid #ffffff}')
        self.btnLink.setIcon(QIcon('ressources/link.png'))
        self.btnLink.move(490, 140)
        self.btnLink.clicked.connect(self.creerLink)
        # **************************************************************
        #  Bouton suppr link
        # **************************************************************
        self.btnLinkSuppr = QPushButton(self)
        self.btnLinkSuppr.setFixedSize(30, 30)
        self.btnLinkSuppr.setStyleSheet('QPushButton {background: qlineargradient(x1:0, y1:0, x2:0, y2:1, '
                                        'stop:0 #eeeeee, stop:1 #aaaaaa); color: black; border: 0px;'
                                        'border-radius: 4px; border: 1px solid #262626} '
                                        'QPushButton:hover {border: 3px solid #ffffff}')
        self.btnLinkSuppr.setIcon(QIcon('ressources/linkSuppr.png'))
        self.btnLinkSuppr.move(525, 140)
        self.btnLinkSuppr.clicked.connect(self.supprLink)
        # **************************************************************
        #  textEditNote
        # **************************************************************
        self.grpNote = QGroupBox(self)
        self.grpNote.setFixedSize(650, 300)
        self.grpNote.setStyleSheet('background-color: #222222; border-radius: 6px; color: white')
        self.grpNote.move(20, 178)
        lytGrpNote = QVBoxLayout()
        self.grpNote.setLayout(lytGrpNote)

        self.textEditNote = QTextEdit(self.grpNote)
        # self.textEditNote = TextEditLink(self.grpNote)
        self.textEditNote.setFixedSize(630, 280)
        f = open('styles/QTextEdit.txt', 'r')
        style = f.read()
        lytGrpNote.addWidget(self.textEditNote)
        self.textEditNote.viewport().installEventFilter(self)

        # self.textEditNote.setStyleSheet('background-color: #333333; border-radius: 6px; color: white')
        self.textEditNote.setPlaceholderText(self._trad('Saisir une note...', self.lngCourGlobal))
        self.textEditNote.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.textEditNote.setStyleSheet(style)
        self.textEditNote.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        self.textEditNote.setFont(font)
        self.textEditNote.textChanged.connect(self.evt_textEditNote_textChanged)
        self.btnUndo.clicked.connect(self.textEditNote.undo)
        self.btnRedo.clicked.connect(self.textEditNote.redo)

        #  grpSupprLink
        self.grpSupprLink = QGroupBox(self.textEditNote)
        self.grpSupprLink.setFixedSize(200, 250)
        self.grpSupprLink.setStyleSheet('background-color: #333333; border: 1px solid white')
        self.grpSupprLink.setVisible(False)
        self.grpSupprLink.move(300, 0)
        lblSupptLink = QLabel(self.grpSupprLink)
        lblSupptLink.setText(self._trad('Supprimer un lien', self.lngCourGlobal))
        lblSupptLink.setStyleSheet('border: 0px')
        lblSupptLink.move(40, 5)
        #
        self.listSupprLink = QListWidget(self.grpSupprLink)
        self.listSupprLink.setFixedSize(180, 170)
        self.listSupprLink.move(10, 30)
        #
        boutonEffaceLink = QPushButton(self.grpSupprLink)
        boutonEffaceLink.setText(self._trad('Supprimer', self.lngCourGlobal))
        boutonEffaceLink.move(20, 220)
        boutonEffaceLink.clicked.connect(self.evt_boutonEffaceLink_clicked)
        boutonFermeLink = QPushButton(self.grpSupprLink)
        boutonFermeLink.setText(self._trad('Fermer', self.lngCourGlobal))
        boutonFermeLink.move(140, 220)
        boutonFermeLink.clicked.connect(self.evt_boutonFermeLink_clicked)

        # **************************************************************
        #  Bouton ValideNote
        # **************************************************************
        self.btnValideNote = BoutonOffOn(self)
        aux = self.textEditNote.toPlainText()
        if aux == '':
            self.btnValideNote.initBool(False)
        else:
            self.btnValideNote.initBool(True)
        self.btnValideNote.move(563, 140)
        # **************************************************************
        # Gestion des tags internes
        # **************************************************************
        self.cadreWidgetTag = QGroupBox(self)
        self.cadreWidgetTag.setFixedSize(650, 220)
        self.cadreWidgetTag.setStyleSheet('background-color: #222222; border-radius: 6px;')
        self.cadreWidgetTag.move(20, 520)
        #  Installation de GrpBoxMetaData
        lytTag = QVBoxLayout()
        self.cadreWidgetTag.setLayout(lytTag)
        grpBoxTag = FormTagInterne(self, self, self.videoID, lytTag, self.marqueCour)
        lytTag.addWidget(grpBoxTag)
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        lytTag.addItem(spacer)
        # **************************************************************
        # SnapShot + legende
        # **************************************************************
        self.cadreSnapShot = QGroupBox(self)
        self.cadreSnapShot.setFixedSize(500, 270)
        self.cadreSnapShot.setStyleSheet('background-color: #222222; border-radius: 6px;')
        self.cadreSnapShot.move(690, 60)
        #  lblSnapShot
        self.lblSnapShot = QLabel(self.cadreSnapShot)
        self.lblSnapShot.setStyleSheet('background-color: #222222;')
        self.lblSnapShot.setFixedSize(340, 180)
        self.lblSnapShot.move(15, 10)
        self.populateSnapShot()
        #  lblLegende
        self.lneLegende = QLineEdit(self.cadreSnapShot)
        self.lneLegende.setStyleSheet('background-color: #333333; color: white')
        self.lneLegende.setPlaceholderText("Saisir la légende de l'image...")
        self.lneLegende.setFixedSize(450, 60)
        self.lneLegende.move(15, 200)
        #  checkBoxIcone
        self.chkIcone = QCheckBox(self.cadreSnapShot)
        self.chkIcone.setStyleSheet('color: white')
        self.chkIcone.setText('Vignette')
        self.chkIcone.move(360, 70)
        #  Bouton valide
        self.btnValideSnapShot = BoutonOffOn(self.cadreSnapShot)
        if aux == '':
            self.btnValideSnapShot.initBool(False)
        else:
            self.btnValideSnapShot.initBool(True)
        self.btnValideSnapShot.move(360, 10)
        # **************************************************************
        #  cadre Info Générale
        # **************************************************************
        videoCour = VideoFileRecord(self.videoID)
        self.cadreInfoGene = QGroupBox(self)
        self.cadreInfoGene.setFixedSize(500, 350)
        self.cadreInfoGene.setStyleSheet('background-color: #222222; border-radius: 6px;')
        self.cadreInfoGene.move(690, 350)
        #  Titre info générales
        self.lblInfoGene = QLabel(self.cadreInfoGene)
        self.lblInfoGene.setStyleSheet('background-color: transparent; color: #cccccc')
        self.lblInfoGene.setText(self._trad('Informations générales', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        font.setBold(True)
        self.lblInfoGene.setFont(font)
        self.lblInfoGene.move(20, 10)
        #  Titre vidéo
        lblLibelTitre = QLabel(self.cadreInfoGene)
        lblLibelTitre.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelTitre.setText(self._trad('Titre :', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelTitre.setFont(font)
        lblLibelTitre.move(30, 45)
        #
        lblTitre = QLabel(self.cadreInfoGene)
        lblTitre.setStyleSheet('background-color: transparent; color: #bbbbbb')
        lblTitre.setText(videoCour.titreVideo)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblTitre.setFont(font)
        lblTitre.move(130, 45)
        #  Titre favori
        lblLibelFavori = QLabel(self.cadreInfoGene)
        lblLibelFavori.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelFavori.setText(self._trad('Favori :', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelFavori.setFont(font)
        lblLibelFavori.move(30, 80)
        #
        cadreFavori = QGroupBox(self.cadreInfoGene)
        cadreFavori.setFixedSize(40, 40)
        lytFavori = QVBoxLayout()
        cadreFavori.setLayout(lytFavori)
        cadreFavori.move(125, 65)
        self.lblFavoriVideo = WidgetFavori(boolFavori=videoCour.Favori)
        lytFavori.addWidget(self.lblFavoriVideo)
        #  Titre durée
        lblLibelDuree = QLabel(self.cadreInfoGene)
        lblLibelDuree.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelDuree.setText(self._trad('Durée :', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelDuree.setFont(font)
        lblLibelDuree.move(30, 115)
        #
        self.lblDureeVideo = QLabel(self.cadreInfoGene)
        query = QSqlQuery()
        ok = query.exec(f'SELECT path FROM biblioTab WHERE cle={videoCour.cleBiblio}')
        if query.next():
            racineCour = query.value('path')
        #  extraction de la vignette
        video = videoCour.videoPath
        self.lblDureeVideo.setText(str(self.videoDuration(video)))
        font2 = QFont()
        font2.setFamily('Arial')
        font2.setPointSize(10)
        font2.setItalic(True)
        self.lblDureeVideo.setFont(font2)
        self.lblDureeVideo.setStyleSheet('color: #bbbbbb')
        self.lblDureeVideo.move(130, 115)
        #  Titre Note
        lblLibelNote = QLabel(self.cadreInfoGene)
        lblLibelNote.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelNote.setText(self._trad('Note :', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelNote.setFont(font)
        lblLibelNote.move(30, 150)
        #
        self.grpRating = QGroupBox(self.cadreInfoGene)
        self.lblNoteVideo = StarRating(videoCour.note)
        self.lblNoteVideo.setBackgound('transparent')
        self.grpRating.setFixedSize(250, 43)
        self.grpRating.setStyleSheet('background-color: transparent; margin-top: 0px')
        self.grpRating.move(105, 125)
        lytRating = QVBoxLayout()
        lytRating.setSpacing(0)
        lytRating.addWidget(self.lblNoteVideo)
        self.grpRating.setLayout(lytRating)
        #  Titre Bibliothèque
        lblLibelBiblio = QLabel(self.cadreInfoGene)
        lblLibelBiblio.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelBiblio.setText(self._trad('Bibliothèque :', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelBiblio.setFont(font)
        lblLibelBiblio.move(30, 190)
        #
        lblBiblio = QLabel(self.cadreInfoGene)
        lblBiblio.setStyleSheet('background-color: transparent; color: #bbbbbb')
        query = QSqlQuery()
        query.exec(f'SELECT nom FROM biblioTab WHERE cle={videoCour.cleBiblio}')
        aux = ''
        if query.next():
            aux = query.value('nom')
        lblBiblio.setText(aux)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblBiblio.setFont(font)
        lblBiblio.move(135, 190)
        #  Titre Timecodee
        lblLibelTimeCode = QLabel(self.cadreInfoGene)
        lblLibelTimeCode.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelTimeCode.setText(self._trad('Timecode :', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelTimeCode.setFont(font)
        lblLibelTimeCode.move(30, 230)
        #
        lblTimeCode = QLabel(self.cadreInfoGene)
        lblTimeCode.setStyleSheet('background-color: transparent; color: #bbbbbb')
        lblTimeCode.setText(self.strTime(self.marqueCour))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblTimeCode.setFont(font)
        lblTimeCode.move(135, 230)
        #  Titre Classeur
        lblLibelClasseur = QLabel(self.cadreInfoGene)
        lblLibelClasseur.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelClasseur.setText(self._trad('Classeur :', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelClasseur.setFont(font)
        lblLibelClasseur.move(30, 270)
        #
        lblClasseur = QLabel(self.cadreInfoGene)
        lblClasseur.setStyleSheet('background-color: transparent; color: #bbbbbb')
        lblClasseur.setText(videoCour.nomClasseur)
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblClasseur.setFont(font)
        lblClasseur.move(135, 270)
        #  Titre Label
        self.lblLabelVideo = QLabel(self.cadreInfoGene)
        lblLibelLabel = QLabel(self.cadreInfoGene)
        lblLibelLabel.setStyleSheet('background-color: transparent; color: #999999')
        lblLibelLabel.setText(self._trad('Label :', self.lngCourGlobal))
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        font.setBold(False)
        lblLibelLabel.setFont(font)
        lblLibelLabel.move(30, 310)
        #
        self.lblLabelVideo = QLabel(self.cadreInfoGene)
        self.lblLabelVideo.setStyleSheet('color: #888888')
        try:
            color = videoCour.colorStatut
            nomLabel = videoCour.nomStatut
        except:
            color = '#ffffff'
            nomLabel = self._trad('Aucun label', self.lngCourGlobal)
        self.lblLabelVideo.setText('         ' + nomLabel)
        font2 = QFont()
        font2.setFamily('Arial')
        font2.setPointSize(10)
        font2.setItalic(True)
        self.lblLabelVideo.setFont(font2)
        self.lblPastilleInfo = QLabel(self.lblLabelVideo)
        self.lblPastilleInfo.setFixedSize(19, 19)
        self.lblPastilleInfo.setStyleSheet('background: transparent')
        self.lblPastilleInfo.move(3, 4)
        if videoCour.statut == -1:
            self.lblPastilleInfo.setPixmap(self.drawPastille(8, ''))
        else:
            self.lblPastilleInfo.setPixmap(self.drawPastille(8, color))
        self.lblLabelVideo.move(135, 310)

        # Bouton sauver
        self.btnSauver = QPushButton(self)
        self.btnSauver.setFixedSize(100, 35)
        self.btnSauver.setStyleSheet('QPushButton {background-color: #f05a24; border-radius: 5px; color: white}'
                                     'QPushButton::hover {border: 3px solid #ffffff}')
        self.btnSauver.setText(self._trad('Sauver', self.lngCourGlobal))
        self.btnSauver.move(960, 718)
        self.btnSauver.clicked.connect(self.sauverBlockNote)

    def evt_btnUnderline_clicked(self):
        cursor = self.textEditNote.textCursor()
        textSelected = cursor.selectedText()
        if textSelected == '':
            return
        font = self.textEditNote.currentFont()
        if font.underline():
            font.setUnderline(False)
        else:
            font.setUnderline(True)
        self.textEditNote.setCurrentFont(font)

    def evt_btnItalic_clicked(self):
        cursor = self.textEditNote.textCursor()
        textSelected = cursor.selectedText()
        if textSelected == '':
            return
        font = self.textEditNote.currentFont()
        if font.italic():
            font.setItalic(False)
        else:
            font.setItalic(True)
        self.textEditNote.setCurrentFont(font)

    def evt_btnGras_clicked(self):
        cursor = self.textEditNote.textCursor()
        textSelected = cursor.selectedText()
        if textSelected == '':
            return
        font = self.textEditNote.currentFont()
        if font.bold():
            font.setBold(False)
        else:
            font.setBold(True)
        self.textEditNote.setCurrentFont(font)

    def evt_lneTitreParagraph_textChanged(self):
        if self.lneTitreParagraph.text() == '':
            self.btnValideTitre.initBool(False)
        else:
            self.btnValideTitre.initBool(True)

    def evt_textEditNote_textChanged(self):
        if self.textEditNote.toPlainText() == '':
            self.btnValideNote.initBool(False)
        else:
            self.btnValideNote.initBool(True)

    def changeFontNote(self):
        cursor = self.textEditNote.textCursor()
        text_selected = cursor.selectedText()
        if text_selected == '':
            return
        aux = self.cmbFontWidget.currentText()
        self.textEditNote.setCurrentFont(QFont(aux))

    def evt_spnTaillePolice_changed(self):
        cursor = self.textEditNote.textCursor()
        text_selected = cursor.selectedText()
        if text_selected == '':
            return
        font = self.textEditNote.currentFont()
        font.setPointSize(self.spnTaillePolice.value())
        self.textEditNote.setCurrentFont(font)

    def supprLink(self):
        self.grpSupprLink.setVisible(True)
        self.listSupprLink.clear()
        for tpl in self.listTpl:
            lien, URL = tpl
            self.listSupprLink.addItem(lien)

    def evt_boutonFermeLink_clicked(self):
        self.grpSupprLink.setVisible(False)

    def eventFilter(self, source, event):
        try:
            if source is self.textEditNote.viewport() and event.type() == event.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    cursor = self.textEditNote.cursorForPosition(event.pos())
                    cursor.select(QTextCursor.WordUnderCursor)
                    selected_text = cursor.selectedText()
                    format = cursor.charFormat()
                    font = format.font()
                    if format.fontWeight() == QFont.Bold and format.fontUnderline():
                        for tpl in self.listTpl:
                            lien, URL = tpl
                            if selected_text in lien:
                                QDesktopServices.openUrl(QUrl(URL))
                    else:
                        pass
        except:
            pass
        return super().eventFilter(source, event)

    def evt_boutonEffaceLink_clicked(self):
        itm = self.listSupprLink.currentItem()
        lienAux = itm.text()
        self.listSupprLink.takeItem(self.listSupprLink.row(itm))
        i = 0
        lien = ''
        URL = ''
        for tpl in self.listTpl:
            lien, URL = tpl
            if lien == lienAux:
                del self.listTpl[i]
            i += 1
        # MaJ de textEditNote
        cursor = self.textEditNote.textCursor()
        format = QTextCharFormat()
        format.setFontWeight(QFont.Normal)
        format.setForeground(QBrush(QColor("#ffffff")))
        format.setFontUnderline(False)
        cursor.mergeCharFormat(format)
        while True:
            cursor = self.textEditNote.document().find(lienAux, cursor)
            format1 = cursor.charFormat()
            if format1.fontWeight() == QFont.Bold and format1.fontUnderline() and not cursor.isNull():
                cursor.mergeCharFormat(format)
            else:
                break
        #  MaJ de la base de données
        query = QSqlQuery()
        query.exec(f'DELETE FROM linkTab WHERE timeCode={self.marqueCour} AND cleVideo={self.videoID} AND mot={lien}')

    def populateNoteModif(self):
        self.btnValideTitre.initBool(False)
        self.btnValideNote.initBool(False)
        self.btnValideSnapShot.initBool(False)
        query = QSqlQuery()
        query.exec(f'SELECT * FROM Paragraph WHERE cleVideo={self.videoID}  AND timeNote={self.marqueCour}')
        while query.next():
            if query.value('titre'):
                self.lneTitreParagraph.setText(query.value('texte'))
                self.btnValideTitre.initBool(True)
                self.cleTitreCour = query.value('cle')
            if query.value('picture'):
                self.lneLegende.setText(query.value('texte'))
                self.btnValideSnapShot.initBool(True)
                if query.value('icone'):
                    self.chkIcone.setChecked(True)
                self.cleSnapShotCour = query.value('cle')
            if query.value('Note'):
                aux = query.value('texte')
                cleAux = query.value('cle')
                #  Récupération des éventuels liens URL
                query1 = QSqlQuery()
                ok = query1.exec(
                    f'SELECT mot, URL FROM linkTab WHERE timecode={self.marqueCour} AND cleVideo={self.videoID}')
                self.listTpl = []
                while query1.next():
                    self.listTpl.append((query1.value('mot'), query1.value('URL')))

                #  Récupération du texte brut
                aux = aux.replace("²", "'")
                aux = aux.replace('<br>', '')
                aux = aux.replace("&#09", "\t")
                self.textEditNote.setText(aux)
                self.btnValideNote.initBool(True)
                self.cleNoteCour = cleAux

    def sauverBlockNote(self):
        msg = ''
        if not self.btnValideSnapShot.boolON:
            if msg == '':
                msg += self._trad("l'image et sa légende", self.lngCourGlobal)
            else:
                msg += self._trad(", l'image et sa légende", self.lngCourGlobal)
        if not self.btnValideTitre.boolON:
            if msg == '':
                msg += self._trad("le titre", self.lngCourGlobal)
            else:
                msg += self._trad(", le titre", self.lngCourGlobal)
        if not self.btnValideNote.boolON:
            if msg == '':
                msg += self._trad("la note", self.lngCourGlobal)
            else:
                msg += self._trad(", la note", self.lngCourGlobal)
        msg1 = ''
        if msg != '':
            msg1 = self._trad("Les éléments suivants ne seront pas sauvegardés: " + msg + " . \n"
                    "S'ils ont déja été créés, ils seront effacés.", self.lngCourGlobal)
        else:
            msg1 = "Confirmez-vous l'enregeristrement de la note ?"

        self.dialog = DialogCustom(self, 0, 0)
        self.dialog.lblWindowTitle.setText(self._trad("Sauvegarde de la note", self.lngCourGlobal))
        self.dialog.setMessage(msg1)
        self.dialog.setPosition(0, 0)
        self.dialog.setBouton1(self._trad('Accepter', self.lngCourGlobal), True)
        self.dialog.setBouton2(self._trad('Annuler', self.lngCourGlobal), True)
        self.dialog.setSaisie('', False)
        if self.dialog.exec_() != DialogCustom.Accepted:
            return
        # Sauvegarde du titre
        if self.cleTitreCour == -1:
            if self.btnValideTitre.boolON:
                # recherche de la clé suivante
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) FROM paragraph')
                try:
                    if query.next():
                        maxCle = query.value(0) + 1
                except:
                    maxCle = 1
                query = QSqlQuery()
                tplChamps = ('cle', 'timeNote', 'titre', 'texte', 'cleVideo')
                tplData = (maxCle, self.marqueCour, True, self.lneTitreParagraph.text(), self.videoID)
                query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
        else:
            if self.btnValideTitre.boolON:
                query = QSqlQuery()
                tplChamps = ('timeNote', 'titre', 'texte', 'cleVideo')
                tplData = (self.marqueCour, True, self.lneTitreParagraph.text(), self.videoID)
                query.exec(f'UPDATE paragraph SET {tplChamps} = {tplData} WHERE cle={self.cleTitreCour}')
            else:
                query = QSqlQuery()
                query.exec(f'DELETE FROM paragraph WHERE cle={self.cleTitreCour}')
        # Sauvegarde de la note
        if self.cleNoteCour == -1:
            if self.btnValideNote.boolON:
                # recherche de la clé suivante
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) FROM paragraph')
                try:
                    if query.next():
                        maxCle = query.value(0) + 1
                except:
                    maxCle = 1
                aux = self.textEditNote.toHtml()
                aux = aux.replace("'", "²")
                aux = aux.replace("\n", "<br>")
                aux = aux.replace("\t", "&#09")

                query = QSqlQuery()
                tplChamps = ('cle', 'timeNote', 'note', 'texte', 'cleVideo')
                tplData = (maxCle, self.marqueCour, True, aux, self.videoID)
                query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
                #  sauvegarde des liens/URL
                for tpl in self.listTpl:
                    lien, URL = tpl
                    # recherche de la clé suivante
                    query = QSqlQuery()
                    query.exec(f'SELECT MAX(cle) FROM linkTab')
                    maxCle1 = 0
                    try:
                        if query.next():
                            maxCle1 = query.value(0) + 1
                    except:
                        maxCle1 = 1
                    query = QSqlQuery()
                    tplChamps = ('cle', 'timeCode', 'mot', 'URL', 'cleVideo')
                    tplData = (maxCle1, self.marqueCour, lien, URL, self.videoID)
                    query.exec(f'INSERT INTO linkTab {tplChamps} VALUES {tplData}')
        else:
            if self.btnValideNote.boolON:
                #  Suppression des entrées dans linkTab correspondant àla note courante
                query = QSqlQuery()
                query.exec(f'DELETE FROM linkTab WHERE cleVideo={self.videoID} AND timeCode={self.marqueCour}')
                #  enregistrement du texte de la note
                query = QSqlQuery()
                aux = self.textEditNote.toHtml()
                aux = aux.replace("'", "²")
                aux = aux.replace("\n", "<br>")
                aux = aux.replace("\t", "&#09")
                tplChamps = ('timeNote', 'Note', 'texte', 'cleVideo', 'titre')
                tplData = (self.marqueCour, True, aux, self.videoID, False)
                query.exec(f'UPDATE paragraph SET {tplChamps} = {tplData} WHERE cle={self.cleNoteCour}')
                # sauvegarde des liens/URL
                for tpl in self.listTpl:
                    lien, URL = tpl
                    #  recherche de la clé suivante
                    query = QSqlQuery()
                    query.exec(f'SELECT max(cle) FROM linkTab')
                    maxCle1 = 0
                    try:
                        if query.next():
                            maxCle1 = query.value(0) + 1
                    except:
                        maxCle1 = 1
                    query = QSqlQuery()
                    tplChamps = ('cle', 'timeCode', 'mot', 'URL', 'cleVideo')
                    tplData = (maxCle1, self.marqueCour, lien, URL, self.videoID)
                    query.exec(f'INSERT INTO linkTab {tplChamps} VALUES {tplData}')
            else:
                query = QSqlQuery()
                query.exec(f'DELETE FROM paragraph WHERE cle={self.cleNoteCour}')
                #  Suppression des entrées dans linkTab correspondant àla note courante
                query = QSqlQuery()
                query.exec(f'DELETE FROM linkTab WHERE cleVideo={self.videoID} AND timeCode={self.marqueCour}')
        # Sauvegarde de l'image
        if self.chkIcone.isChecked():
            #  Supprimer l'ancienne image icone
            query = QSqlQuery()
            query.exec(f'SELECT * FROM paragraph where cleVideo={self.videoID} AND icone={True}')
            if query.next():
                cleAux = query.value('cle')
                query = QSqlQuery()
                tplChamps = ('icone')
                tplData = (False)
                query.exec(f'UPDATE paragraph SET {tplChamps} = {tplData} WHERE cle={cleAux}')
        if self.cleSnapShotCour == -1:
            if self.btnValideSnapShot.boolON:
                # recherche de la clé suivante
                query = QSqlQuery()
                query.exec(f'SELECT MAX(cle) FROM paragraph')
                try:
                    if query.next():
                        maxCle = query.value(0) + 1
                except:
                    maxCle = 1
                query = QSqlQuery()
                tplChamps = ('cle', 'timeNote', 'picture', 'texte', 'cleVideo', 'icone')
                tplData = (maxCle, self.marqueCour, True, self.lneLegende.text(), self.videoID,
                           self.chkIcone.isChecked())
                query.exec(f'INSERT INTO paragraph {tplChamps} VALUES {tplData}')
        else:
            if self.btnValideSnapShot.boolON:
                query = QSqlQuery()
                tplChamps = ('timeNote', 'picture', 'texte', 'cleVideo', 'icone')
                tplData = (self.marqueCour, True, self.lneLegende.text(), self.videoID, self.chkIcone.isChecked())
                query.exec(f'UPDATE paragraph SET {tplChamps} = {tplData} WHERE cle={self.cleSnapShotCour}')
            else:
                query = QSqlQuery()
                query.exec(f'DELETE FROM paragraph WHERE cle={self.cleSnapShotCour}')

        # en cas de suppression totale supprimer les tags internes
        # query = QSqlQuery()
        # query.exec(f'DELETE FROM tagTab WHERE cleVideo={self.videoID} AND timeCode={self.marqueCour}')
        #
        try:  # cas de l'éditon de la note à partir du bouton Editer de FormScreen1
            mainXX = self.parent.mainWin.tabObjetScreen.docParagraph.widget()
            mainXX.objNote.populateParagraph(self.videoID)
        except:  # cas de l'édition de la note à partir du bouton modif de Paragraph
            self.parent.populateParagraph(self.videoID)
        self.close()

    def creerLink(self):
        cursor = self.textEditNote.textCursor()
        lien = cursor.selectedText()

        if len(lien) == 0:
            self.dialog = DialogCustom(self, 0, 0)
            self.dialog.lblWindowTitle.setText(self._trad("Création d'un lien Web", self.lngCourGlobal))
            aux = self._trad("Pas d'expression sélectionnée.", self.lngCourGlobal)
            self.dialog.setMessage(aux)
            self.dialog.setPosition(0, 0)
            self.dialog.setBouton1(self._trad('Accepter', self.lngCourGlobal), False)
            self.dialog.setBouton2(self._trad('Annuler', self.lngCourGlobal), True)
            self.dialog.setSaisie('', False)
            if self.dialog.exec_() == DialogCustom.Accepted:
                return
            return

        #  Formatage en gras souligné
        format = QTextCharFormat()
        format.setFontWeight(QFont.Bold)
        format.setForeground(QBrush(QColor("#ef6634")))
        format.setFontUnderline(True)
        cursor.mergeCharFormat(format)
        self.textEditNote.mergeCurrentCharFormat(format)

        #  Saisie de l'URL
        self.dialog = DialogCustom(self, 0, 0)
        self.dialog.lblWindowTitle.setText(self._trad("Création d'un lien Web", self.lngCourGlobal))
        aux = self._trad("Saisir une URL...", self.lngCourGlobal)
        self.dialog.setMessage(aux)
        self.dialog.setPosition(0, 0)
        self.dialog.setBouton1(self._trad('Accepter', self.lngCourGlobal), True)
        self.dialog.setBouton2(self._trad('Annuler', self.lngCourGlobal), True)
        self.dialog.setSaisie(self._trad('Saisir une URL...', self.lngCourGlobal), True)
        address = ''
        if self.dialog.exec_() == DialogCustom.Accepted:
            address = self.dialog.lneSaisie.text()
            self.dialog.close()
            self.listTpl.append((lien, address))
        else:
            format = QTextCharFormat()
            format.setFontWeight(QFont.Normal)
            format.setForeground(QBrush(QColor("#ffffff")))
            format.setFontUnderline(False)
            cursor.mergeCharFormat(format)
            self.textEditNote.mergeCurrentCharFormat(format)
            cursor.clearSelection()
            self.textEditNote.setTextCursor(cursor)
            self.dialog.close()
            return

    def drawPastille(self, radius, color):
        if color == '':
            dim = radius * 2 + 4
            pixmap = QPixmap(dim, dim)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            pen = QPen(QColor('#ffffff'))
            painter.setPen(pen)
            brush = QBrush(QColor('#ffffff'))
            painter.setBrush(brush)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.drawEllipse(1, 1, 2 * radius, 2 * radius)
            pen = QPen(QColor('#ff0000'), 2, Qt.SolidLine)
            painter.setPen(pen)
            brush = QBrush(QColor('#ff0000'))
            painter.setBrush(brush)
            painter.drawLine(1, radius + 2, radius * 2 + 4, radius + 2)
            del painter
        else:
            dim = radius * 2 + 4
            pixmap = QPixmap(dim, dim)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            pen = QPen(QColor(color))
            painter.setPen(pen)
            brush = QBrush(QColor(color))
            painter.setBrush(brush)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.drawEllipse(1, 1, 2 * radius, 2 * radius)
            del painter
        return pixmap

    def strTime(self, seconde):
        heure = seconde / 3600
        seconde %= 3600
        minute = seconde / 60
        seconde %= 60
        strHeure, strMinute, strSeconde = '', '', ''
        if heure >= 10:
            strHeure = str(int(heure))
        else:
            strHeure = '0' + str(int(heure))[0]
        if minute >= 10:
            strMinute = str(int(minute))
        else:
            strMinute = '0' + str(int(minute))[0]
        if seconde >= 10:
            strSeconde = str(int(seconde))
        else:
            strSeconde = '0' + str(int(seconde))[0]
        return (f'{strHeure}:{strMinute}:{strSeconde}')

    def videoDuration(self, video):
        v = cv2.VideoCapture(video)
        fps = v.get(cv2.CAP_PROP_FPS)
        frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        v.release()
        heureTxt = '00'
        if duration > 3600:
            heure = int(duration / 3600)
            duration = duration - (3600 * heure)
            if heure < 10:
                heureTxt = f'0{heure}'

        minute = int(duration / 60)
        if minute < 10:
            minuteTxt = f'0{minute}'
        else:
            minuteTxt = f'{minute}'
        seconde = int((duration - minute * 60) * .6)
        if seconde < 10:
            secondeTxt = f'0{seconde}'
        else:
            secondeTxt = f'{seconde}'

        duration = f'{heureTxt}:{minuteTxt}:{secondeTxt}'
        return duration

    def populateSnapShot(self):
        videoCour = VideoFileRecord(self.videoID)
        query = QSqlQuery()
        ok = query.exec(f'SELECT path FROM biblioTab WHERE cle={videoCour.cleBiblio}')
        if query.next():
            racineCour = query.value('path')
        #  extraction de la vignette
        video = videoCour.videoPath
        vidcap = cv2.VideoCapture(video)
        vidcap.set(cv2.CAP_PROP_POS_MSEC, self.marqueCour * 1000)
        success, image = vidcap.read()
        if success:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap01 = QPixmap.fromImage(image)
        self.lblSnapShot.setPixmap(pixmap01.scaled(330, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def textEditNote_undo(self):
        self.textEditNote.undo()

    def textEditNote_redo(self):
        self.textEditNote.redo()
