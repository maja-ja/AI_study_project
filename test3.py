import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QWidget
)
from PyQt5.QtGui import QPainter, QPen, QImage, QColor, QPixmap
from PyQt5.QtCore import Qt, QPoint

GRID_SIZE = 64
PIXEL_SIZE = 10
CANVAS_SIZE = GRID_SIZE * PIXEL_SIZE

class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(CANVAS_SIZE, CANVAS_SIZE)
        self.paths = [[]]  # 多條路徑，每條是點座標list
        self.redo_stack = []
        self.confirmed = False
        self.space_pressed_once = False
        self.background = None

    def paintEvent(self, event):
        painter = QPainter(self)
        # 背景圖片
        if self.background:
            painter.drawImage(0, 0, self.background)

        # 畫所有路徑點線
        pen = QPen(Qt.blue, 2)
        painter.setPen(pen)
        for path in self.paths:
            for i in range(1, len(path)):
                p1 = QPoint(*self.to_pixel(path[i - 1]))
                p2 = QPoint(*self.to_pixel(path[i]))
                p1 += QPoint(5, 5)
                p2 += QPoint(5, 5)
                painter.drawLine(p1, p2)
            for x, y in path:
                px, py = self.to_pixel((x, y))
                painter.setBrush(Qt.blue)
                painter.setPen(Qt.black)
                painter.drawEllipse(px + 2, py + 2, 6, 6)

        # 畫格線
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        for i in range(0, CANVAS_SIZE, PIXEL_SIZE):
            painter.drawLine(i, 0, i, CANVAS_SIZE)
            painter.drawLine(0, i, CANVAS_SIZE, i)

    def mousePressEvent(self, event):
        if self.confirmed:
            return
        x = event.x() // PIXEL_SIZE
        y = event.y() // PIXEL_SIZE
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            self.paths[-1].append((x, y))
            self.redo_stack.clear()
            self.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_A, Qt.Key_Left):
            if self.paths[-1]:
                self.redo_stack.append(self.paths[-1].pop())
                self.update()
        elif key in (Qt.Key_D, Qt.Key_Right):
            if self.redo_stack:
                self.paths[-1].append(self.redo_stack.pop())
                self.update()
        elif key == Qt.Key_S:
            # 斷點：開始新路徑段
            if self.paths[-1]:  # 只有非空才新增路徑段
                self.paths.append([])
                self.redo_stack.clear()
                self.update()
        elif key == Qt.Key_Space:
            if self.space_pressed_once:
                self.save_all()
                self.confirmed = True
                QMessageBox.information(self, "提交", "已提交並儲存！")
            else:
                self.space_pressed_once = True
                QMessageBox.information(self, "確認", "已確認（再按一次空白提交）")
        else:
            self.space_pressed_once = False

    def to_pixel(self, coord):
        return coord[0] * PIXEL_SIZE, coord[1] * PIXEL_SIZE

    def load_background(self):
        file, _ = QFileDialog.getOpenFileName(self, "選擇背景圖片", "", "Images (*.png *.jpg *.jpeg)")
        if file:
            img = QImage(file).scaled(CANVAS_SIZE, CANVAS_SIZE)
            self.background = img
            self.update()

    def save_all(self):
        # 儲存多段點資料
        with open("path.json", "w") as f:
            json.dump(self.paths, f)

        # 儲存圖像（含背景與線條）
        image = QImage(CANVAS_SIZE, CANVAS_SIZE, QImage.Format_RGB32)
        image.fill(Qt.white)
        painter = QPainter(image)
        if self.background:
            painter.drawImage(0, 0, self.background)

        pen = QPen(Qt.blue, 2)
        painter.setPen(pen)
        for path in self.paths:
            for i in range(1, len(path)):
                p1 = QPoint(*self.to_pixel(path[i - 1])) + QPoint(5, 5)
                p2 = QPoint(*self.to_pixel(path[i])) + QPoint(5, 5)
                painter.drawLine(p1, p2)
        painter.end()
        image.save("output.png")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("三層畫板：背景圖 + 畫布 + 格線")
        self.canvas = CanvasWidget()
        self.setCentralWidget(self.canvas)

        btn = QPushButton("載入背景圖", self)
        btn.move(10, CANVAS_SIZE + 10)
        btn.clicked.connect(self.canvas.load_background)
        self.setFixedSize(CANVAS_SIZE, CANVAS_SIZE + 50)

        self.canvas.setFocus()  # 讓鍵盤事件正常觸發

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
