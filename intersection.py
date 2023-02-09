from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

from get_road_element_dict import get_intersection_dict


class IntersectionWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        font = QFont('Roboto', 10)
        self.setFont(font)

        self.setWindowTitle('Kreuzung einfügen')
        self.resize(260, 200)

        self.length = QLineEdit(self)
        self.length.setToolTip('Länge der beiden Kreuzungsarme')
        self.length.setPlaceholderText('Länge')
        self.length.setValidator(QtGui.QDoubleValidator())
        self.length.resize(260, 30)

        self.onewayLabel = QLabel('Einbahnstrasse?', self)
        self.onewayLabel.move(10, 40)

        self.oneway = QComboBox(self)
        self.oneway.addItems(('Nein', 'Ja'))
        self.oneway.resize(130, 30)
        self.oneway.move(130, 40)

        self.stopped_lanes = QLineEdit(self)
        self.stopped_lanes.setToolTip('Wie viele Spuren sollen eine Haltelinie haben?')
        self.stopped_lanes.setPlaceholderText('Gestoppte Fahrspuren')
        self.stopped_lanes.setValidator(QtGui.QDoubleValidator())
        self.stopped_lanes.resize(260, 30)
        self.stopped_lanes.move(0, 80)

        self.direction = QComboBox(self)
        self.direction.addItems(('Gerade', 'Rechtskurve', 'Linkskurve'))
        self.direction.resize(260, 30)
        self.direction.move(0, 110)

        self.directionLabel = QLabel('Bei Track_Generator nur Gerade verwenden!', self)
        self.directionLabel.resize(260, 30)
        self.directionLabel.move(0, 140)

        self.finish_button = QPushButton('Fertig', self)
        self.finish_button.clicked.connect(self.finish_button_clicked)
        self.finish_button.move(0, 170)
        self.finish_button.setFixedWidth(260)

        self.parent_window = parent_window

        self.road = parent_window.road
        self.factor = parent_window.factor

    def finish_button_clicked(self):
        if self.length.text():
            if float(self.length.text()) > 0:
                self.hide()
                self.parent_window.append_road_element(
                    get_intersection_dict(self.road[-1]['end'], self.road[-1]['endDirection'],
                                          self.direction.currentText(), float(self.length.text()),
                                          self.parent_window.open_intersections, self.oneway.currentText(),
                                          self.stopped_lanes.text(), self.factor))
                self.parent_window.update()
                del self
