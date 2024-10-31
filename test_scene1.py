import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem, \
    QGraphicsTextItem, QGraphicsEllipseItem, QColorDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QBrush, QPainter
from test_sceneUI import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPen


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.setupUi(self)

        self.scene = QGraphicsScene()
        self.remplirScene()
        self.show()
        for vue in (self.vuePrincipale, self.vueGlobale):
            vue.setScene(self.scene)
            vue.setRenderHints(QPainter.Antialiasing)
            vue.fitInView(self.rectGris, Qt.KeepAspectRatio)
        self.vueGlobale.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vuePrincipale.setDragMode(QGraphicsView.RubberBandDrag)

        self.lineEditTexte.setText('Tous en scène !!!')

        self.angleVue = 0.0

        self.zoomPctVue = 1.0
        self.horizontalSliderZoom.setValue(100)

        self.scene.selectionChanged.connect(self.onSceneSelectionChanged)
        self.onSceneSelectionChanged()

    @pyqtSlot()
    def on_pushButtonCreerDisque_clicked(self):
        disque = self.scene.addEllipse(0, 0, 20, 20, brush=QBrush(Qt.white), pen=QPen(Qt.NoPen))
        disque.setFlag(QGraphicsItem.ItemIsMovable)
        disque.setFlag(QGraphicsItem.ItemIsSelectable)

    @pyqtSlot(str)
    def on_lineEditTexte_textChanged(self, msg):
        self.texte.setPlainText(msg)

    @pyqtSlot()
    def on_pushButtonChangerCouleur_clicked(self):
        itemSelectionnes = self.scene.selectedItems()
        # if len(itemSelectionnes) == 0:
        #     return
        couleurInit = itemSelectionnes[0].brush().color()
        couleur = QColorDialog.getColor(couleurInit, self, 'Changer de couleur')
        if couleur.isValid():
            brosse = QBrush(couleur)
            for item in itemSelectionnes:
                item.setBrush(brosse)

    @pyqtSlot(int)
    def on_dialRotation_valueChanged(self, nouvelAngleVue):
        self.vuePrincipale.rotate(nouvelAngleVue - self.angleVue)
        self.angleVue = nouvelAngleVue

    @pyqtSlot(int)
    def on_horizontalSliderZoom_valueChanged(self, nouvZoomPctVue):
        f = (nouvZoomPctVue / 100.0) / self.zoomPctVue
        self.vuePrincipale.scale(f, f)
        self.zoomPctVue = nouvZoomPctVue / 100.0

    def onSceneSelectionChanged(self):
        nbElementSelectionnes = len(self.scene.selectedItems())
        self.pushButtonChangerCouleur.setEnabled(nbElementSelectionnes > 0)
        msg = '%d éléments sélectionnés' %nbElementSelectionnes
        self.statusBar().showMessage(msg)

    def remplirScene(self):
        scene = self.scene
        rectGris = scene.addRect(0, 0, 200, 150, brush=QBrush(Qt.lightGray))
        self.rectGris = rectGris
        self.texte = scene.addText('')
        dy = rectGris.rect().height() - self.texte.sceneBoundingRect().height()
        self.texte.setPos(rectGris.x(), rectGris.y() + dy)
        self.texte.setDefaultTextColor(Qt.blue)
        self.texte.setZValue(1)
        scene.addItem(self.texte)
        d = 48.  # diamètre smiley
        ox = 4.  # largeur oeil
        oy = 6.  # hauteur  oeil
        smiley = scene.addEllipse(-d/2, -d/2, d, d, brush=QBrush(Qt.yellow))
        yeux = [QGraphicsEllipseItem(-ox/2, -oy/2, ox, oy, parent=smiley) for i in range(2)]
        yeux[0].setPos(-d/6, -d/8)
        yeux[1].setPos(+d/6, -d/8)
        brush = QBrush(Qt.black)
        for oeil in yeux:
            oeil.setBrush(brush)
        smiley.setPos(rectGris.mapToScene(rectGris.rect().center()))
        smiley.setRotation(20)
        smiley.setScale(1.5)
        for item in scene.items():
            item.setFlag(QGraphicsItem.ItemIsMovable)
            item.setFlag(QGraphicsItem.ItemIsSelectable)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
