import os
import shutil
from PyQt5.QtWidgets import QWidget, QMessageBox, QShortcut, QGraphicsScene, QGraphicsView, QMainWindow
from PyQt5.QtGui import QFont, QTransform, QKeySequence
from PyQt5.QtSvg import QSvgWidget
from PyQt5 import QtCore

from track_generator.generator import generate_track


from xml_writer_reader import xml_writer
from get_road_element_dict import get_int


def xml_preview(parent_window, lanes):
    """
    Generate xml file.
    Generate svg file with track generator.
    Open window with svg file.
    Delete the generated files.
    """
    os.makedirs(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp'))
    xml_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp', 'temp.xml')
    svg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp')
    try:
        xml_writer(parent_window.road, xml_path, parent_window.factor, lanes)
        generate_track([xml_path], svg_path, False, False)
        parent_window.preview_window = PreviewWindow(os.path.join(svg_path, 'temp', 'temp.svg'))
        parent_window.preview_window.show()
    except Exception as e:
        QMessageBox.about(parent_window, 'Error', f'Die Vorschau konnte nicht erstellt werden.\nFehlermeldung:\n{e}')
    shutil.rmtree(svg_path)


class SvgWidget(QWidget):
    def __init__(self, svg_path, parent_window):
        super().__init__()

        self.container_widget = QWidget()

        self.parent_window = parent_window
        self.mouse_pos = QtCore.QPoint(0, 0)
        self.cursor_start = QtCore.QPoint(0, 0)
        font = QFont('Roboto', 10)
        self.setFont(font)

        self.setWindowTitle('Vorschau')

        svg_widget = QSvgWidget(svg_path, self)
        height = get_int(svg_widget.sizeHint().height() / 40)
        width = get_int(svg_widget.sizeHint().width() / 40)

        svg_widget.resize(width, height)

    def wheelEvent(self, event):
        """
        Is calles if left mouse button is clicked and mouse moves
        """
        delta = event.angleDelta().y()
        if delta > 0:
            self.parent_window.zoom_in()

        elif delta < 0:
            self.parent_window.zoom_out()

    def mousePressEvent(self, event):
        """
        Is calles if left mouse button is clicked
        """
        self.cursor_start = self.container_widget.cursor().pos()
        print(self.cursor_start)
        if event.button() == QtCore.Qt.LeftButton:
            self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        """
        Is calles if left mouse button is clicked and mouse moves
        """
        delta = self.cursor_start - self.container_widget.cursor().pos()

        # panning area
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.parent_window.move_window.x() - delta.x(), self.parent_window.move_window.y() - delta.y())

        self.mouse_pos = event.localPos()

    def mouseReleaseEvent(self, event):
        """
        Is calles if left mouse button is released
        """
        self.unsetCursor()
        self.mouse_pos = event.localPos()
        self.parent_window.move_window.setX(
            self.parent_window.move_window.x() - (self.cursor_start - self.container_widget.cursor().pos()).x())
        self.parent_window.move_window.setY(
            self.parent_window.move_window.y() - (self.cursor_start - self.container_widget.cursor().pos()).y())


class PreviewWindow(QMainWindow):
    factor = 1.5

    def __init__(self, svg_path):
        super().__init__()

        self.move_window = QtCore.QPoint(0, 0)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)

        self.svg_widget = SvgWidget(svg_path, self)
        self.svg_widget.setFixedSize(2000, 2000)
        self.scene.addWidget(self.svg_widget)

        self.setCentralWidget(self.view)

        QShortcut(QKeySequence(QtCore.Qt.Key_Minus), self.view, context=QtCore.Qt.WidgetShortcut,
                  activated=self.zoom_out)

        QShortcut(QKeySequence(QtCore.Qt.Key_Plus), self.view, context=QtCore.Qt.WidgetShortcut, activated=self.zoom_in)

    @QtCore.pyqtSlot()
    def zoom_in(self):
        """
        Is called from mouse wheel or plus button
        """
        scale_tr = QTransform()
        scale_tr.scale(self.factor, self.factor)
        tr = self.view.transform() * scale_tr
        self.view.setTransform(tr)

    @QtCore.pyqtSlot()
    def zoom_out(self):
        """
        Is called from mouse wheel os minus button
        """
        scale_tr = QTransform()
        scale_tr.scale(self.factor, self.factor)
        scale_inverted, invertible = scale_tr.inverted()
        if invertible:
            tr = self.view.transform() * scale_inverted
            self.view.setTransform(tr)
