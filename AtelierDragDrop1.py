import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
# from PyQt5.QtWebEngineWidgets import *
import sys
from PyQt5.QtSql import QSqlDatabase
import sqlite3
from PyQt5.QtSql import *
from AtelierClassCommun import DialogCustom, VideoFileRecord
import datetime
import os


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************        D I A L O G D O S S I E R                 ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class DialogDossier(QDialog):
    def __init__(self, parent=None, modif=None, cleCreate=None, contenant=None):
        super().__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.parent = parent
        self.modif = modif
        self.contenant = contenant

        button_global_pos = self.parent.mapToGlobal(QPoint(0, 0))

        x = button_global_pos.x() + self.parent.width() + 10
        y = button_global_pos.y()

        self.setGeometry(x, y, 300, 150)
        self.setStyleSheet('background-color: #333333')
        self.cleDossierCour = cleCreate
        self.returnCmb = True
        #
        self.setUpUI()

    def setUpUI(self):
        lblNom = QLabel(self)
        lblNom.setText('Nom :')
        lblNom.setStyleSheet('color: white')
        lblNom.move(25, 23)
        #
        self.lneNom = QLineEdit(self)
        self.lneNom.setFixedSize(220, 25)
        self.lneNom.setPlaceholderText('Saisir le nom du dossier')
        self.lneNom.setStyleSheet('color: #cccccc')
        self.lneNom.move(70, 20)
        if self.modif:
            query = QSqlQuery()
            query.exec(f'SELECT * FROM biblioTreeTab WHERE cle={self.cleDossierCour}')
            if query.next():
                self.lneNom.setText(query.value('data'))
        #
        lblParent = QLabel(self)
        lblParent.setText('Parent :')
        lblParent.setStyleSheet('color: white')
        lblParent.move(15, 63)
        #
        self.cmbParent = QComboBox(self)
        self.cmbParent.setFixedSize(220, 25)
        self.cmbParent.setStyleSheet('color: #cccccc')
        self.cmbParent.move(70, 63)
        self.cmbParent.currentIndexChanged.connect(self.handleIndexChanged)
        self.populateParent()
        #
        btnSauver = QPushButton(self)
        btnSauver.setFixedSize(110, 35)
        btnSauver.setText('Sauver')
        btnSauver.setStyleSheet('color: white; background-color: #3a67ae')
        btnSauver.move(25, 110)
        btnSauver.clicked.connect(self.evt_btnSauver_clicked)
        #
        btnFermer = QPushButton(self)
        btnFermer.setFixedSize(110, 35)
        btnFermer.setText('Fermer')
        btnFermer.setStyleSheet('color: white; background-color: #3a67ae')
        btnFermer.move(175, 110)
        btnFermer.clicked.connect(self.evt_btnFermer_clicked)

    def populateParent(self):
        self.returnCmb = True
        self.cmbParent.clear()
        query = QSqlQuery()
        query.exec('SELECT * FROM biblioTreeTab')
        dataAux = ''
        while query.next():
            self.cmbParent.addItem(query.value('data'), userData=query.value('cle'))
            if query.value('cle') == self.cleDossierCour:
                dataAux = query.value('data')
        # self.cleDossierCour -= 1
        self.cmbParent.setCurrentIndex(self.cleDossierCour - 1)
        self.returnCmb = False

    def handleIndexChanged(self, index):
        if self.returnCmb:
            return
        self.cleDossierCour = self.cmbParent.itemData(index)

    def evt_btnSauver_clicked(self):
        if self.lneNom.text() == '':
            return
        if self.modif:
            query = QSqlQuery()
            query.exec(f'SELECT * FROM biblioTreeTab WHERE cle={self.cleDossierCour}')
            parent_idAux = ''
            if query.next():
                parent_idAux = query.value('parent_id')
            query = QSqlQuery()
            tplChamps = ('parent_id', 'data')
            tplData = (parent_idAux, self.lneNom.text())
            query.exec(f'UPDATE biblioTreeTab SET {tplChamps} = {tplData} WHERE cle={self.cleDossierCour}')
        else:
            #  Recherche de l'index suivant
            cleMax = 1
            query = QSqlQuery()
            query.exec(f'SELECT MAX(cle) AS cleMax FROM biblioTreeTab')
            try:
                if query.next():
                    cleMax = query.value('cleMax') + 1
            except:
                pass

            tplData = (cleMax, self.cleDossierCour, self.lneNom.text())
            tplChamps = ('cle', 'parent_id', 'data')
            query1 = QSqlQuery()
            query1.exec(f'INSERT INTO biblioTreeTab {tplChamps} VALUES {tplData}')
        self.contenant.refreshTree()
        self.close()

    def evt_btnFermer_clicked(self):
        self.close()


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************                 T R E E N O D E                  ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class TreeNode:
    def __init__(self, node_id, parent_id, data, boolDev):
        self.cle = node_id
        self.lstChildren = []
        self.data = data
        self.parent_id = parent_id
        self.boolDev = boolDev

    def __str__(self):
        aux = f'cle: {self.cle} - data: {self.data} - parent: {self.parent_id} - boolDev: {self.boolDev}'
        return aux


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************       M A I N W I N D O W D O S S I E R          ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class MainWindowDossier(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.dragCour = None
        self.listWidget = []

        self.initUI()

    def initUI(self):
        self.setStyleSheet('background-color: #222')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.grpTree = QGroupBox()
        self.grpTree.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grpTree.setStyleSheet('background-color: #222')
        self.grpTree.setFixedSize(500, 600)
        self.grpTree.move(0, 0)

        #  Menu contextuel
        self.grpTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.grpTree.customContextMenuRequested.connect(self.showMenuContextuel0)

        self.loadListTree()

        #  Installation d'un ScrollArea
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.grpTree)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        centralLayout = self.setCentralWidget(self.scrollArea)
        f = open('styles/QScrollBar.txt', 'r')
        style = f.read()
        self.scrollArea.setStyleSheet(style)
        self.setStyleSheet('background-color: #222222; border: 0px')

    def showMenuContextuel0(self):
        pass

    def refreshTree(self):
        self.grpTree.close()
        # self.scrollArea

        self.grpTree = QGroupBox(self)
        self.grpTree.setStyleSheet('background-color: #222')
        self.grpTree.setGeometry(0, 0, 300, 600)

        self.loadListTree()
        self.grpTree.show()

        #  Installation d'un ScrollArea
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.grpTree)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        centralLayout = self.setCentralWidget(self.scrollArea)
        f = open('styles/QScrollBar.txt', 'r')
        style = f.read()
        self.scrollArea.setStyleSheet(style)
        self.setStyleSheet('background-color: #222222; border: 0px')

    def loadListTree(self):
        self.listTree = []
        self.listWidget = []
        query = QSqlQuery()
        bOk = query.exec(f'SELECT * FROM biblioTreeTab ORDER BY cle')
        while query.next():
            cle = query.value('cle')
            parent_id = query.value('parent_id')
            data = query.value('data')
            node = TreeNode(cle, parent_id, data, query.value('boolDev'))
            self.listTree.append(node)


        for node in self.listTree:
            lstChildren = [itm.cle for itm in self.listTree if itm.parent_id == node.cle]
            node.lstChildren = lstChildren

        #  tri de la liste par ordre de cle
        self.listTree = sorted(self.listTree, key=lambda x: x.cle)

        listEtage = []
        for node in self.listTree:
            if len(node.lstChildren) > 0:
                if node not in listEtage:
                    listEtage.append(node)
                indice = listEtage.index(node)
                for itm in node.lstChildren:
                    indice += 1
                    nodeChild = [node for node in self.listTree if node.cle == itm][0]
                    listEtage.insert(indice, nodeChild)

        self.listTree = listEtage

        if len(listEtage) == 0:
            query = QSqlQuery()
            query.exec(f'SELECT data FROM biblioTreeTab')
            if query.next():
                nodeAux = TreeNode(1, -1, query.value('data'), True)
                listEtage.append(nodeAux)

        try:
            self.indice = 0
            self.listWidget = []
            self.displayTree(listEtage[0])
        except:
            pass

    def unSelectBtnSelect(self):
        for obj in self.listWidget:
            obj.selectVert = False
            obj.setStyleSheet('QLabel {background-color: transparent; border: 0px; color: gray} '
                              'QLabel::hover {background-color: #444}')
        self.parent.dossierSelectCour = -1

    def displayTree(self, root, indent=''):
        if True:  # os.path.isdir(root) -> cas répertoires + fichiers
            lblNode = DraggableWidget(self.grpTree, self, root)
            self.listWidget.append(lblNode)

            lblNode.contenant = self
            lblNode.move(len(indent) * 12 + 10, self.indice * 40 + 20)

            lblNode.setFixedWidth(lblNode.width() - lblNode.x())
            lblNode.posInit = (len(indent) * 12 + 10, self.indice * 30)

            items = root.lstChildren
            if len(items) == 0:
                lblNode.btDeveloppe.setVisible(False)
            else:
                for item in items:
                    nodeChild = [node for node in self.listTree if node.cle == item][0]
                    if True:  # os.path.isdir(item_path)  -> cas répertoires + fichiers
                        if root.boolDev:
                            self.indice += 1
                            self.displayTree(nodeChild, indent + "  ")
                else:
                    pass
                    return
                    print(indent * 3 + f"  📄 {item}")
        self.grpTree.setFixedHeight((self.indice + 1) * 180)


# *********************************************************************************************************************
# *********************************************************************************************************************
# ***************         D R A G G A B L E W I D G E T            ****************************************************
# *********************************************************************************************************************
# *********************************************************************************************************************
class DraggableWidget(QLabel):
    def __init__(self, parent, contenant, node):
        super().__init__(parent)
        self.setFixedSize(500, 30)
        self.setStyleSheet('QLabel {background-color: #222; border: 0px; color: gray} '
                           'QLabel::hover {background-color: #444}')
        self.installEventFilter(self)
        self.parent = parent
        self.contenant = contenant
        self.node = node
        self.selectVert = False
        self.listSupprDossier = []

        #  Initialisation de la langue
        query = QSqlQuery()
        query.exec(f'SELECT langue FROM parametersTab')
        if query.next():
            aux = query.value('langue')
            if aux == 'Français':
                self.lngCourGlobal = 'fr'
            if aux == 'Anglais':
                self.lngCourGlobal = 'en'

        #  Icone du dossier
        pixmap = QPixmap('ressources/dossier25.png')
        pixmapLabel = QLabel(self)
        pixmapLabel.setPixmap(pixmap)
        pixmapLabel.move(30, 5)
        #  Fléche de développement
        self.btDeveloppe = QPushButton(self)
        self.btDeveloppe.setFixedSize(20, 20)
        self.btDeveloppe.setStyleSheet('background-color: transparent')
        if self.node.boolDev:
            self.btDeveloppe.setIcon(QIcon('ressources/devPlus.png'))
        else:
            self.btDeveloppe.setIcon(QIcon('ressources/devMoins.png'))
        self.btDeveloppe.move(0, 10)
        self.btDeveloppe.clicked.connect(self.evt_btDeveloppe_clicked)
        #  Data du treeNode
        titreLabel = QLabel(self)
        titreLabel.setStyleSheet('background-color: transparent; color: white')
        titreLabel.setText(node.data)
        titreLabel.move(65, 7)

        #  Rendre le widget glissable
        self.setAcceptDrops(True)
        self.contenant.dragCour = self

    def evt_btDeveloppe_clicked(self):
        #  Swap développé / non développé
        sender = self.sender()
        cle = sender.parent().node.cle
        if sender.parent().node.boolDev:
            sender.parent().node.boolDev = False
            sender.parent().btDeveloppe.setIcon(QIcon('ressources/devMoins.png'))
        else:
            sender.parent().node.boolDev = True
            sender.parent().btDeveloppe.setIcon(QIcon('ressources/devPlus.png'))
        #  Enregistrement dans la table du statut du noeud (développé / non développé)
        query = QSqlQuery()
        tplChamps = ('boolDev')
        tplData = (sender.parent().node.boolDev)
        query.exec(f'UPDATE biblioTreeTab SET {tplChamps} = {tplData} WHERE cle = {cle}')
        #
        self.contenant.refreshTree()

    def eventFilter(self, object, event):
        if (event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.RightButton):
            menu = QMenu()
            menu.setStyleSheet('background-color: #aaa; border: 1px solid #aaaaaa')
            menu.addAction(self._trad('Créer nouveau dossier', self.lngCourGlobal),
                           lambda:  self.createSousDossier(self.cleCreate))
            if object.node.parent_id != -1:
                # menu.addAction('Supprimer  dossier', lambda: self.supprSousDossier(self.cleCreate))
                menu.addAction(self._trad('Supprimer dossier', self.lngCourGlobal),
                              lambda: self.supprSousDossier(self.cleCreate))
                menu.addAction(self._trad('Renommer dossier', self.lngCourGlobal), lambda: self.renommerDossier(self.cleCreate))
                menu.addAction(self._trad('Importer un dossier', self.lngCourGlobal),  lambda:  self.importerDossier(self.cleCreate))
                menu.addAction(self._trad('Importer une vidéo', self.lngCourGlobal), lambda: self.importerVideo(self.cleCreate))
            if menu.exec_(event.globalPos()):
                return True
        if (event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.LeftButton):
            self.evt_btnSelect_clicked()
        if event.type() == QEvent.Enter:
            self.cleCreate = object.node.cle
        if event.type() == QEvent.Leave:
            pass
        if event.type() == QEvent.Drop:
            # if object.node.parent_id != -1:
            #     return
            cleTarget = object.node.cle
            auxVideo = VideoFileRecord(cleTarget)
            aux = str(type(self.contenant.dragCour))
            if 'DraggableWidget' in aux and not event.mimeData().hasUrls():
                cleDrag = self.contenant.dragCour.node.cle
                auxVideo = VideoFileRecord(cleTarget)
                #  Mise à jour de la base de données puis l'affichage de l'arbre modifié
                query = QSqlQuery()
                tplChamps = ('parent_id')
                tplData = (cleTarget)
                if cleDrag != cleTarget:  # cas du dossier déplacé sur lui-même
                    query.exec(f'UPDATE biblioTreeTab SET {tplChamps} = {tplData} WHERE cle = {cleDrag}')
                    self.contenant.refreshTree()
            if 'LabelIndex' in aux:
                cleVideo = self.contenant.dragCour.index
                auxVideo = VideoFileRecord(cleVideo)
                if auxVideo.deleted:  # déplacement d'une vidéo dans la corbeille dans un dossier
                    query =QSqlQuery()
                    tplChamps = ('cleClasseur', 'deleted')
                    tplData = (cleTarget, False)
                    query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tplData} WHERE cle={cleVideo}')
                    self.contenant.parent.selectZoneDroit.populateLstVideoSelect()
                else:  # autres cas de déplacement de vidéos d'un dossier à un autre
                    self.dropVideoGridDossier(cleTarget)

            if event.mimeData().hasUrls():  # Cas d'un drag and drop d'un fichier ou d'un dossier
                aux = event.mimeData().urls()[0].toLocalFile()
                videoFullPath = aux
                if os.path.isdir(aux): # Cas importation de dossier
                    self.importArbre(aux, cleTarget)
                    return super().eventFilter(object, event)
                videoName = os.path.splitext(os.path.basename(aux))[0] + os.path.splitext(os.path.basename(aux))[1]
                cleClasseur = cleTarget
                date_du_jour = datetime.date.today()
                dateLastView = date_du_jour.strftime("%d-%m-%Y")
                query = QSqlQuery()
                query.exec(f'SELECT * FROM statutTab WHERE defaut')
                statut = 0
                if query.next():
                    statut = query.value('cle')
                    aux = f"- {query.value('nom')}"
                favori = False
                #  Vérifier que la vidéo ne figure pas déja dans la base
                query = QSqlQuery()
                bOk = query.exec(f'SELECT * From videoFileTab')
                lst = []
                while query.next():
                    lst.append(query.value('videoFullPath'))
                if aux in lst:
                    self.dialog = DialogCustom(None, 500, 500)
                    aux = 'La vidéo figure déja dans la base de données.'
                    self.dialog.setSaisie('', False)
                    self.dialog.setMessage(aux)
                    self.dialog.setBouton1('', False)
                    self.dialog.setBouton2('Fermer', True)
                    if self.dialog.exec_() == DialogCustom.Accepted:
                        pass
                else:
                    #  recherche de l'indice suivant
                    query = QSqlQuery()
                    bOk = query.exec(f'SELECT MAX(cle) FROM videoFileTab')
                    maxCle = 1
                    try:
                        if bOk:
                            if query.next():
                                maxCle = query.value(0) + 1
                    except:
                        pass
                    #  Last view
                    dateCreation = QDate.currentDate()
                    dateCreationString = dateCreation.toString('yyyy-MM-dd')
                    dateLastView = dateCreationString
                    #  Duration
                    v = cv2.VideoCapture(videoFullPath)
                    fps = v.get(cv2.CAP_PROP_FPS)
                    frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
                    duration = int(frame_count/fps)
                    tplChamps = ('videoName', 'videoFullPath', 'cleClasseur', 'dateLastView', 'statut', 'favori',
                                 'deleted', 'cle', 'dateCreation', 'duration', 'marquePage')
                    tplData = (videoName, videoFullPath, cleClasseur, dateLastView, statut, favori, False, maxCle,
                               dateCreationString, duration, 0)
                    query = QSqlQuery()

                    query.exec(f'INSERT INTO videoFileTab {tplChamps} VALUES {tplData}')
                    self.dialog = DialogCustom(None, 500, 500)
                    aux = self._trad("La vidéo a été enregistrée.", self.lngCourGlobal)
                    self.dialog.setSaisie('', False)
                    self.dialog.setMessage(aux)
                    self.dialog.setBouton1('', False)
                    self.dialog.setBouton2(self._trad("Fermer", self.lngCourGlobal), True)
                    if self.dialog.exec_() == DialogCustom.Accepted:
                        pass

            self.contenant.parent.selectZoneDroit.populateLstVideoSelect()
        return super().eventFilter(object, event)

    def _trad(self, mot, langue):
        query = QSqlQuery()
        query.exec(f'SELECT * FROM langueTab WHERE fr="{mot}"')
        if query.next():
            return query.value(langue)

    def mousePressEvent(self, event):
        self.contenant.dragCour = self
        #  Commencer le processus de glissement
        mimeData = QMimeData()
        mimeData.setText(self.text())

        drag = QDrag(self)
        drag.setMimeData(mimeData)

        drag.exec_(Qt.CopyAction)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def importerVideo(self, cleCreate):
        #  recherche de l'indice suivant videoFileTab
        query = QSqlQuery()
        btOk = query.exec(f'SELECT MAX(cle) FROM videoFileTab')
        maxCleVideo = 1
        try:
            if btOk:
                if query.next():
                    maxCleVideo = query.value(0) + 1
        except:
            pass
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file, b = QFileDialog.getOpenFileName(self, 'Enregistrer une nouvelle vidéo', script_dir, '*.mp4')
        if file == '':
            return
        videoName = os.path.basename(file)
        videoPath = os.path.dirname(file)
        #  Enregistrement de la vidéo dans la base de données
        dateCreation = QDate.currentDate()
        dateCreationString = dateCreation.toString('yyyy-MM-dd')
        dateLastView = dateCreationString
        favori = False
        #  Duration
        v = cv2.VideoCapture(file)
        fps = v.get(cv2.CAP_PROP_FPS)
        frameCount = int(v.get((cv2.CAP_PROP_FRAME_COUNT)))
        duration = int(frameCount / fps)
        statut = 0
        tplChamps = ('videoName', 'videoFullPath', 'cleClasseur', 'dateLastView', 'statut', 'favori', 'deleted', 'cle',
                     'dateCreation', 'duration', 'marquePage')
        tplData = (videoName, file, cleCreate, dateLastView, statut, favori, False, maxCleVideo, dateCreationString,
                   duration, 0)
        query = QSqlQuery()
        query.exec(f'INSERT INTO videoFileTab {tplChamps} VALUES {tplData}')

        self.evt_btnSelect_clicked()

    def importerDossier(self, cleDossier):
        directory = QFileDialog.getExistingDirectory(self, self._trad("Choisir un répertoire", self.lngCourGlobal))
        if directory:
            self.importArbre(directory, cleDossier)

    def importArbre(self, directory, cleDossier):
        query = QSqlQuery()
        btOk = query.exec(f'SELECT * FROM videoFileTab ')
        #  lstVideo -> éviter les doublons
        lstVideo = []
        while query.next():
            lstVideo.append(query.value('videoFullPath'))
        #
        #  recherche de l'indice suivant videoFileTab
        query = QSqlQuery()
        btOk = query.exec(f'SELECT MAX(cle) FROM videoFileTab')
        maxCleVideo = 1
        try:
            if btOk:
                if query.next():
                    maxCleVideo = query.value(0) + 1
        except:
            pass
        #
        #  recherche de l'indice suivant BiblioTreeTab
        query = QSqlQuery()
        btOk = query.exec(f'SELECT MAX(cle) FROM BiblioTreeTab')
        maxCleNode = 1
        try:
            if btOk:
                if query.next():
                    maxCleNode = query.value(0) + 1
        except:
            pass

        dirRacine = directory
        dirRacine = dirRacine.replace(chr(92), '$')
        dirRacine = dirRacine.replace(chr(47), '$')
        dernier_index = dirRacine.rfind('$')
        dirNameRacine = dirRacine[dernier_index + 1:]
        lenDir = -len(dirNameRacine)
        dirPathRacine = dirRacine[:lenDir]
        dirFullRacine = dirPathRacine + dirNameRacine
        #
        listTupleNamePath = [(dirNameRacine, dirPathRacine, dirFullRacine)]
        #
        listDir = []  # Liste des répertoires de l'arborescence à importer avec les index des parents
        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                pathDir = root
                pathDir = pathDir.replace(chr(92), '$')
                pathDir = pathDir.replace(chr(47), '$')
                fullDir = pathDir + '$' + dir
                listTupleNamePath.append((dir, pathDir, fullDir))
        listAuxFull = [fullDir for dir, pathDir, fullDir in listTupleNamePath]
        #  Récupérer les vidéos dans les répertoires importés
        listFile = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                # print(root, file)
                pathDir = root
                pathDir = pathDir.replace(chr(47), '$')
                pathDir = pathDir.replace(chr(92), '$')
                indexDir = listAuxFull.index(pathDir) + maxCleNode
                pathDir = pathDir.replace('$', chr(47))
                listFile.append((indexDir, file, pathDir))
                # print(indexDir, file, pathDir)
        #  Enregistrer les videos importées dans vidoFileTab
        i = 0
        for itm in listFile:
            indexDir, file, pathDir = itm
            videoFullPath = pathDir + '/' + file
            statut = 0
            query = QSqlQuery()
            query.exec(f'SELECT * FROM statutTab WHERE defaut')
            if query.next():
                statut = query.value('cle')
                aux = f'-  {query.value("nom")}'

            dateCreation = QDate.currentDate()
            dateCreationString = dateCreation.toString('yyyy-MM-dd')
            dateLastView = dateCreationString
            favori = False
            #  Duration
            v = cv2.VideoCapture(videoFullPath)
            fps = v.get(cv2.CAP_PROP_FPS)
            frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = int(frame_count / fps)
            tplChamps = ('videoName', 'videoFullPath', 'cleClasseur', 'dateLastView', 'statut', 'favori',
                         'deleted', 'cle', 'dateCreation', 'duration', 'marquePage')
            tplData = (file, videoFullPath, indexDir, dateLastView, statut, favori, False,
                       maxCleVideo + i, dateCreationString, duration, 0)
            query = QSqlQuery()
            bOk = query.exec(f'INSERT INTO videoFileTab {tplChamps} VALUES {tplData}')
            i += 1
        # Construction de listDir -> liste des dossiers avec leur arborecence
        racineImport = True
        increment = 0
        # for itm in listAuxFull:
        #     print(itm, listAuxFull.index(itm))
        for itm in listTupleNamePath:
            dirName, dirPath, dirFull = itm
            if racineImport:
                nodeAux = TreeNode(node_id=maxCleNode, parent_id=cleDossier, data=dirName, boolDev=True)
                racineImport = False
                listDir.append(nodeAux)
            else:
                # print(dirPath)
                indexParent = listAuxFull.index(dirPath)
                # print(indexParent)
                nodeAux = TreeNode(node_id=maxCleNode + increment, parent_id=maxCleNode + indexParent,
                                   data=dirName, boolDev=True)
                listDir.append(nodeAux)
            increment += 1
        #  Enregistrer l'arbre importé dans la table biblioTreeTab
        for node in listDir:
            tplData = (node.cle, node.parent_id, node.data, node.boolDev)
            tplChamps = ('cle', 'parent_id', 'data', 'boolDev')
            query1 = QSqlQuery()
            query1.exec(f'INSERT INTO biblioTreeTab {tplChamps} VALUES {tplData}')

        self.contenant.refreshTree()


    def dropVideoGridDossier(self, cleDossier):
        cursor = QCursor()
        x_pos = cursor.pos().x()
        y_pos = cursor.pos().y()
        #  boite de dialogue menu
        self.dialMenuDrop = QDialog()
        self.dialMenuDrop.setStyleSheet('background-color: #333; border: 1px solid #555')
        self.dialMenuDrop.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.dialMenuDrop.setGeometry(x_pos, y_pos, 200, 100)
        self.dialMenuDrop.setFixedSize(200, 100)
        self.dialMenuDrop.show()
        lytMenu = QVBoxLayout()
        lytMenu.setSpacing(0)
        self.dialMenuDrop.setLayout(lytMenu)
        # QListWidget
        self.listMenuDrop = QListWidget()
        self.listMenuDrop.setStyleSheet('background-color: #333; color: #999; border: 0px;')
        self.listMenuDrop.addItem(self._trad(("Déplacer la vidéo"), self.lngCourGlobal))
        self.listMenuDrop.addItem(self._trad(("Copier la vidéo"), self.lngCourGlobal))
        self.listMenuDrop.addItem(self._trad(("Annuler..."), self.lngCourGlobal))
        lytMenu.addWidget(self.listMenuDrop)
        self.listMenuDrop.currentItemChanged.connect(lambda: self.evt_listMenuDrop_currentItemChanged(cleDossier))

    def evt_listMenuDrop_currentItemChanged(self, cleDossier):
        indice = self.listMenuDrop.currentRow()
        if indice == 0:  # déplacer la vidéo
            query = QSqlQuery()
            tplChamps = ('cleClasseur')
            tplData = (cleDossier)
            query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tplData} WHERE cle={self.contenant.dragCour.index}')
            self.contenant.parent.selectZoneDroit.populateLstVideoSelect()
        if indice == 1:  # copier la vidéo
            vAux = VideoFileRecord(self.contenant.dragCour.index)
            #  Recherche de l'index suivant
            cleMax = 1
            query = QSqlQuery()
            query.exec(f'SELECT MAX(cle) AS cleMax FROM videoFileTab')
            try:
                if query.next():
                    cleMax = query.value('cleMax') + 1
            except:
                pass

            tplData = (vAux.videoName, vAux.videoPath, cleDossier, vAux.ordreClasseur, vAux.marquePage, cleMax,
                       vAux.dateLastView, vAux.statut, vAux.Favori, vAux.internalPath, vAux.cleBiblio, vAux.note,
                       vAux.deleted, 0)
            tplChamps = ('videoName', 'videoFullPath', 'cleClasseur', 'ordreClasseur', 'marquePage', 'cle',
                         'DateLastView', 'statut', 'Favori', 'internalPath', 'cleBiblio', 'note', 'deleted',
                         'marquePage')
            query1 = QSqlQuery()
            query1.exec(f'INSERT INTO videoFileTab {tplChamps} VALUES {tplData}')

        if indice == 2:
            self.dialMenuDrop.close()
        self.dialMenuDrop.close()

    def evt_btnMenu_clicked(self):
        sender = self.sender().parent()
        button_global_pos = sender.mapToGlobal(QPoint(0, 0))
        x = button_global_pos.x() + sender.width() + 10
        y = button_global_pos.y()
        #  Affichage d'un menu dans un QListWidget dans un QDialog
        self.dialMenu = QDialog()
        self.dialMenu.setStyleSheet('background-color: #333; border: 1px solid #555')
        self.dialMenu.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.dialMenu.setGeometry(x, y, 200, 150)
        self.dialMenu.show()
        lytMenu = QVBoxLayout()
        self.dialMenu.setLayout(lytMenu)
        #  QListWidget
        self.listMenu = QListWidget()
        self.listMenu.setStyleSheet('background-color: #333; color: #999; border: 0px')
        self.listMenu.addItem(self._trad('Créer nouveau dossier', self.lngCourGlobal))
        self.listMenu.addItem(self._trad('Supprimer dossier', self.lngCourGlobal))
        self.listMenu.addItem(self._trad('Renommer dossier', self.lngCourGlobal))
        self.listMenu.addItem(self._trad('Annuler...', self.lngCourGlobal))
        lytMenu.addWidget(self.listMenu)
        self.listMenu.currentItemChanged.connect(self.evt_listMenu_currentItemChanged)
        self.contenant.parent.selectZoneDroit.populateLstVideoSelect()

    def evt_btnSelect_clicked(self):
        #  Déselectionner les bouton TopLeft + savedSearch
        self.contenant.parent.selectZoneGauche.unSelectTopLeft()
        self.contenant.parent.boolExecuterSearch = False
        self.contenant.parent.selectZoneGauche.lblSavedSearch.setSelected(False)
        #
        sender = self.sender()
        for obj in self.contenant.listWidget:
            obj.selectVert = False
            obj.setStyleSheet('QLabel {background-color: transparent; border: 0px; color: gray} '
                               'QLabel::hover {background-color: #444}')
        if self.selectVert:
            self.selectVert = False
            self.setStyleSheet('QLabel {background-color: transparent; border: 0px; color: gray} '
                               'QLabel::hover {background-color: #444}')
            self.contenant.parent.dossierSelectCour = 0
            self.contenant.parent.selectZoneDroit.populateLstVideoSelect()
        else:
            self.contenant.parent.dossierSelectCour = self.node.cle
            self.selectVert = True
            self.setStyleSheet('QLabel {background-color: #395da4; border: 0px; color: gray} '
                               'QLabel::hover {background-color: #444}')
            self.contenant.parent.selectZoneDroit.populateLstVideoSelect()

    def evt_listMenu_currentItemChanged(self, current):
        indice = self.listMenu.currentRow()
        if indice == 0:
            # self.parent.parent().parent().createSousDossier(self.cleCreate)
            self.createSousDossier(self.cleCreate)
        if indice == 1:
            self.supprSousDossier(self.cleCreate)
        if indice == 2:
            self.renommerDossier(self.cleCreate)
        if indice == 3:
            self.dialMenu.close()
        self.dialMenu.close()
        # self.parent.parent().setFocus(True)
        self.contenant.setFocus(True)

    def createSousDossier(self, cleCreate):
        dialogDossier = DialogDossier(self, modif=False, cleCreate=cleCreate, contenant=self.contenant)
        dialogDossier.show()

    def supprSousDossier(self, cleCreate):
        if len(self.listSupprDossier) == 0: # initialise la racine
            self.listSupprDossier.append(cleCreate)
        listAux = []
        query = QSqlQuery()
        query.exec(f'SELECT * FROM biblioTreeTab WHERE parent_id = {cleCreate}')
        while query.next():
            listAux.append(query.value('cle'))
        if len(listAux) == 0:
            #  Plus d'enfants dans le morceau d'arbre
            for cle in self.listSupprDossier:
                #  suppression du dossier et des sous dossiers
                query = QSqlQuery()
                query.exec(f'DELETE FROM biblioTreeTab WHERE cle={cle}')
                #  Transfert des vidéos contenues dans les dossiers supprimés dans la corbeille
                query = QSqlQuery()
                tplChamps = ('cleClasseur', 'deleted')
                tplData = (-1, True)
                query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tplData} WHERE cleClasseur={cle}')
            self.contenant.refreshTree()
        else:
            self.listSupprDossier += listAux
            self.listSupprDossier = list(set(self.listSupprDossier))
            for cle in listAux:
                self.supprSousDossier(cle)
        return
        # ***************************************************************
        self.dialog = DialogCustom(None, 500, 500)
        aux = self._trad('Vous êtes en train de supprimer un nouveau dossier. \nEtes-vous certain de votre choix ?', self.lngCourGlobal)
        self.dialog.setSaisie('', False)
        self.dialog.setMessage(aux)
        if self.dialog.exec_() == DialogCustom.Accepted:
            #  Mise à jour des vidéos concernées par le dossier à supprimer
            query = QSqlQuery()
            tplChamps = ('cleClasseur', 'deleted')
            tplData = (-1, True)
            query.exec(f'UPDATE videoFileTab SET {tplChamps} = {tplData} WHERE cleClasseur={cleCreate}')
            #  Suppression du dossier
            query = QSqlQuery()
            query.exec(f'DELETE FROM biblioTreeTab WHERE cle={cleCreate}')
            self.contenant.refreshTree()

    def renommerDossier(self, cleCreate):
        sender = self.sender().parent()
        button_global_pos = sender.mapToGlobal(QPoint(0, 0))

        x = button_global_pos.x() + sender.width() + 10
        y = button_global_pos.y()
        dialogDossier = DialogDossier(self, modif=True, cleCreate=cleCreate, contenant=self.contenant)
        dialogDossier.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindowDossier()
    mainWindow.show()
    sys.exit(app.exec_())
