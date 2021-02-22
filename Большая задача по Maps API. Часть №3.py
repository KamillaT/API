import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]


def set_map_params(toponym_longitude, toponym_lattitude, spn=None, z=None):
    if z is not None:
        map_params = {
            "ll": ','.join([str(toponym_longitude), str(toponym_lattitude)]),
            "l": "map",
            "z": str(z)}
    else:
        map_params = {
            "ll": ','.join([str(toponym_longitude), str(toponym_lattitude)]),
            "l": "map",
            "spn": ','.join([str(spn), str(spn)])}
    return map_params


class Map(QWidget):
    def __init__(self):
        super().__init__()
        self.z = 16
        self.spn = 0.002
        self.toponym_longitude = 37.530887
        self.toponym_lattitude = 55.70311
        self.getImage(self.z)
        self.initUI()

    def getImage(self, z):
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        map_params = set_map_params(self.toponym_longitude, self.toponym_lattitude, spn=self.spn)
        response = requests.get(map_api_server, params=map_params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http status:", response.status_code, '(', response.reason, ')')
            sys.exit(1)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle("Отображение карты")
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.z += 1
            self.spn /= 2
            if self.z == 18:
                self.z = 17
            if self.spn < 0.005:
                self.spn = 0.0005
        elif event.key() == Qt.Key_PageDown:
            self.z = (abs(self.z - 1)) % 18
            self.spn *= 2
            if self.z == 0:
                self.z = 1
            if self.spn > 90:
                self.spn = 90
        elif event.key() == Qt.Key_Up:
            self.toponym_lattitude += self.spn
            if self.toponym_lattitude >= 85:
                self.toponym_lattitude = 85
        elif event.key() == Qt.Key_Down:
            self.toponym_lattitude -= self.spn
            if self.toponym_lattitude <= -85:
                self.toponym_lattitude = -85
        elif event.key() == Qt.Key_Left:
            self.toponym_longitude -= self.spn
            if self.toponym_longitude <= -180:
                self.toponym_longitude = -179
        elif event.key() == Qt.Key_Right:
            self.toponym_longitude += self.spn
            if self.toponym_longitude >= 180:
                self.toponym_longitude = 179
        print(self.toponym_lattitude)
        self.getImage(self.z)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.image.update()

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())
