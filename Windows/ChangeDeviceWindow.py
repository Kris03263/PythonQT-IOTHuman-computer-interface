# Windows/WorkOrderWindow.py
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFrame,QMessageBox,QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QFontDatabase,QPixmap
import requests
from Windows.dialog import show_error_dialog
from Windows.resource import resource_path
from dotenv import load_dotenv
from PyQt5.QtWidgets import QScroller
import os

class ChangeDeviceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.BASE_URL = os.getenv('API_BASE_URL')
        self.work_order_selected_callback = None
        self.cancel_callback = None
        url = f'{self.BASE_URL}GetAllMachine'
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                self.initUI(result)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("機台匯入失敗")
                errorMessage = response.json()["Message"]
                show_error_dialog(errorMessage)

        except requests.exceptions.RequestException as e:
            msg = QMessageBox()
            msg.setWindowTitle("機台匯入失敗")
            show_error_dialog(str(e.response))

    def initUI(self,device_list):
        self.setWindowTitle('機台選擇')
        self.setFixedSize(800, 480)
        self.setStyleSheet("background-color: #000000;")
        font_family = QFontDatabase.applicationFontFamilies(0)[0]
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 標題和取消按鈕佈局
        title_layout = QHBoxLayout()
        title_label = QLabel("請選擇機台")
        title_label.setFont(QFont(font_family,24))
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)

        cancel_btn = QPushButton("取消")
        cancel_btn.setFont(QFont(font_family,16))
        cancel_btn.setFixedSize(120, 45)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        # 創建 logo 標籤
        logo_label = QLabel()
        logo_pixmap = QPixmap(resource_path("./Windows/icon/logo.png"))  # 請替換成你的 logo 路徑
        # 調整 logo 大小（根據需要調整數值）
        scaled_pixmap = logo_pixmap.scaled(100, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        title_layout.addWidget(title_label)
        title_layout.addWidget(cancel_btn)
        title_layout.addStretch()
        title_layout.addWidget(logo_label)
        main_layout.addLayout(title_layout)

        # 創建工單列表的容器
        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        list_layout.setSpacing(10)
        list_layout.setContentsMargins(0, 0, 0, 0)

        for device in device_list:
            item_frame = QFrame()
            item_frame.setFixedHeight(70)  # 設定每個項目的固定高度
            item_frame.setStyleSheet("""
                QFrame {
                    background-color: #333333;
                    border-radius: 5px;
                    padding: 3px;
                }
            """)

            item_layout = QHBoxLayout(item_frame)
            item_layout.setContentsMargins(10, 5, 10, 5)
            info_layout = QVBoxLayout()
            label = QLabel("機台資訊")
            label.setFont(QFont(font_family,12))
            label.setStyleSheet("color: #888888;")
            number = QLabel(f'{device["MachineID"]} | {device["MachineName"]}')
            number.setFont(QFont(font_family,12))
            number.setStyleSheet("color: white;")
            info_layout.addWidget(label)
            info_layout.addWidget(number)

            select_btn = QPushButton("選擇")
            select_btn.setFont(QFont(font_family,16))
            select_btn.setFixedSize(120, 40)
            select_btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #219a52;
                }
            """)

            # 绑定选择按钮事件
            select_btn.clicked.connect(lambda checked, device_id=device["MachineID"]: self.on_device_selected(device_id))

            item_layout.addLayout(info_layout)
            item_layout.addStretch()
            item_layout.addWidget(select_btn)

            list_layout.addWidget(item_frame)
        list_layout.addStretch()

            # 創建滾動區域
        scroll_area = QScrollArea()
        QScroller.grabGesture(scroll_area.viewport(), QScroller.LeftMouseButtonGesture)
        scroll_area.setWidget(list_container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
               QScrollArea {
                   border: none;
                   background-color: transparent;
               }
               QScrollBar:vertical {
                   border: none;
                   background: #444444;
                   width: 10px;
                   margin: 0px;
               }
               QScrollBar::handle:vertical {
                   background: #666666;
                   border-radius: 5px;
                   min-height: 20px;
               }
               QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                   height: 0px;
               }
           """)

        # 將滾動區域添加到主佈局
        main_layout.addWidget(scroll_area)

        # 綁定取消按鈕事件
        cancel_btn.clicked.connect(self.on_cancel)

    def on_device_selected(self, device_id):
        try:
            if self.on_device_selected_callback:
                self.on_device_selected_callback(device_id)
            self.close()
        except Exception as e:
            print(e)

    def on_cancel(self):
        if self.cancel_callback:
            self.cancel_callback()
        self.close()