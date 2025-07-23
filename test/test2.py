import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox,
    QWidget, QLineEdit, QLabel
)
from PyQt5.QtGui import QPainter, QPen, QImage, QColor
from PyQt5.QtCore import Qt, QPoint

# === 基本參數設定 ===
GRID_SIZE = 64
PIXEL_SIZE = 10
CANVAS_SIZE = GRID_SIZE * PIXEL_SIZE

# 資料夾路徑（根據你給的）
BASE_DIR = "/Users/chenpinrong/Desktop/AI_study_project/database"
PATH_DIR = "/Users/chenpinrong/Desktop/AI_study_project/path"
WORD_BASE_PATH = os.path.join(BASE_DIR, "word_number", "path.json")
IMAGES_DIR = os.path.join(BASE_DIR, "word_picture", "images")
DATASET_INDEX_PATH = os.path.join(BASE_DIR, "word_picture", "dataset_index.json")

# === 工具函式 ===

def convert_vector_to_path(vec):
    """將純數字 vector 轉成 [(x, y), (x, y), ...]"""
    return [(vec[i], vec[i+1]) for i in range(0, len(vec) - 1, 2)]

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# === 主畫布 ===

class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(CANVAS_SIZE, CANVAS_SIZE)
        self.paths = []
        self.background = None

    def paintEvent(self, event):
        painter = QPainter(self)

        # === 填滿白色背景 ===
        painter.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE, QColor(255, 255, 255))

        # 背景圖
        if self.background:
            painter.drawImage(0, 0, self.background)

        # 畫線段
        pen = QPen(Qt.blue, 2)
        painter.setPen(pen)
        for path in self.paths:
            for i in range(1, len(path)):
                p1 = QPoint(*self.to_pixel(path[i - 1])) + QPoint(5, 5)
                p2 = QPoint(*self.to_pixel(path[i])) + QPoint(5, 5)
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

    def to_pixel(self, coord):
        return coord[0] * PIXEL_SIZE, coord[1] * PIXEL_SIZE

    def load_background(self, filepath):
        if filepath and os.path.exists(filepath):
            img = QImage(filepath).scaled(CANVAS_SIZE, CANVAS_SIZE)
            self.background = img
        else:
            self.background = None
        self.update()

    def load_paths(self, paths):
        self.paths = paths
        self.update()

# === 主視窗 ===

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("輸入文字 → 載入圖片 + 線條還原")
        self.setFixedSize(CANVAS_SIZE + 400, CANVAS_SIZE + 60)

        self.wordbase = load_json(WORD_BASE_PATH)
        self.dataset_index = load_json(DATASET_INDEX_PATH)

        # 畫布元件
        self.canvas = CanvasWidget()
        self.setCentralWidget(self.canvas)

        # 輸入框
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("請輸入一句文字（Enter執行）")
        self.input_line.setGeometry(10, CANVAS_SIZE + 10, 380, 30)
        self.input_line.returnPressed.connect(self.on_text_entered)

        # 狀態顯示
        self.info_label = QLabel(self)
        self.info_label.setGeometry(400, CANVAS_SIZE + 10, 350, 30)

    def on_text_entered(self):
        text = self.input_line.text().strip().lower()
        if not text:
            self.info_label.setText("⚠️ 請輸入文字")
            return

        entry = next((e for e in self.dataset_index if e["text"].lower() == text), None)

        if not entry:
            self.info_label.setText("❌ 找不到對應文字")
            self.canvas.load_background(None)
            self.canvas.load_paths([])
            return

        # 處理圖片路徑
        image_path = entry.get("image_path", "")
        if not os.path.isabs(image_path):
            image_path = os.path.join(IMAGES_DIR, os.path.basename(image_path))

        # 處理 path.json（如果存在）
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        path_json_path = os.path.join(PATH_DIR, "path.json")

        if os.path.exists(path_json_path):
            with open(path_json_path, "r", encoding="utf-8") as f:
                paths = json.load(f)
        else:
            # 如果沒有就轉換 vector 為單一路徑
            vector = entry.get("vector", [])
            paths = [convert_vector_to_path(vector)] if len(vector) >= 2 else []

        # 載入畫布
        self.canvas.load_background(image_path)
        self.canvas.load_paths(paths)
        self.info_label.setText(f"✅ 載入成功：{text}")

# === 執行主程式 ===

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
