from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLabel, QComboBox,QMessageBox)
from PyQt5.QtGui import QFont, QFontDatabase,QPixmap
from PyQt5.QtCore import Qt
from Windows.dialog import show_error_dialog
from Windows.resource import resource_path
import requests
import os
from dotenv import load_dotenv

class StartDownTimeWindow(QMainWindow):
    def __init__(self,worker,deviceID,workOrderID):
        super().__init__()
        load_dotenv()
        self.BASE_URL = os.getenv('API_BASE_URL')
        self.worker = worker
        self.deviceID = deviceID
        self.workOrderID = workOrderID
        self.combo = None
        url = f'{self.BASE_URL}GetAllStopReason'
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                self.initUI(worker,result)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("停機原因匯入失敗")
                errorMessage = response.json()["Message"]
                show_error_dialog(errorMessage)

        except requests.exceptions.RequestException as e:
            msg = QMessageBox()
            msg.setWindowTitle("停機原因匯入失敗")
            show_error_dialog(str(e.response))

    def initUI(self, worker, result):
        # 设置窗口基本属性
        self.setWindowTitle('暫停原因')
        self.setFixedSize(800, 480)
        self.setStyleSheet("background-color: black;")

        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        font_family = QFontDatabase.applicationFontFamilies(0)[0]
        # 創建 logo 標籤
        logo_label = QLabel()
        logo_pixmap = QPixmap(resource_path("./Windows/icon/logo.png"))  # 請替換成你的 logo 路徑
        # 調整 logo 大小（根據需要調整數值）
        scaled_pixmap = logo_pixmap.scaled(100, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        main_layout.addWidget(logo_label)

        # 标题
        title_label = QLabel("請選擇暫停原因")
        title_label.setFont(QFont(font_family, 24))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setContentsMargins(0,45,0,0)
        main_layout.addWidget(title_label)

        # 下拉选单
        self.combo = QComboBox()
        self.combo.setFont(QFont(font_family, 18))
        self.combo.setStyleSheet(f"""
           QComboBox {{
               background-color: #333333;
               color: white;
               border-radius: 5px;
               padding: 10px;
               min-height: 50px;
               min-width: 480px; 
               max-width: 480px;  
               margin: 20px 0px;
           }}
           QComboBox::drop-down {{
               border: none;
               padding-right: 20px;
           }}
           QComboBox::down-arrow {{
               image: url('{resource_path("./Windows/icon/drop_down_arrow_2.png").replace(os.sep, "/")}');
               width: 20px;
               height: 20px;
           }}
           QComboBox QAbstractItemView {{
               background-color: #333333;
               color: white;
               selection-background-color: #444444;
               selection-color: white;
               padding: 8px;
           }}
       """)

        # 创建水平布局来居中放置下拉框
        combo_layout = QHBoxLayout()
        combo_layout.addStretch(1)
        combo_layout.addWidget(self.combo)
        combo_layout.addStretch(1)

        for item in result:
            _id = item["ID"]
            _text = item["Name"]
            self.combo.addItem(_text, _id)

        main_layout.addLayout(combo_layout)

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)

        # 确定按钮
        confirm_btn = QPushButton("確定")
        confirm_btn.setFont(QFont(font_family, 18))
        confirm_btn.setStyleSheet("""
           QPushButton {
               background-color: #2196F3;
               color: white;
               border-radius: 5px;
               padding: 10px 20px;
               min-width: 100px;
               max-width: 100px;
               min-height: 50px;
           }
           QPushButton:hover {
               background-color: #1976D2;
           }
       """)
        confirm_btn.clicked.connect(self.confirm_selection)

        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.setFont(QFont(font_family, 18))
        cancel_btn.setStyleSheet("""
           QPushButton {
               background-color: #F44336;
               color: white;
               border-radius: 5px;
               padding: 10px 20px;
               min-width: 100px;
               max-width: 100px;
               min-height: 50px;
           }
           QPushButton:hover {
               background-color: #D32F2F;
           }
       """)
        cancel_btn.clicked.connect(self.on_cancel)

        button_layout.addStretch()
        button_layout.addWidget(confirm_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        # 添加弹性空间将内容推到中间
        main_layout.addStretch(1)

    def confirm_selection(self):
        selected_text = self.combo.currentText()
        selected_id = self.combo.currentData()
        url = f'{self.BASE_URL}StartDownTime'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "wid": self.workOrderID,
            "reasonID": selected_id,
            "worker": self.worker
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                if hasattr(self, 'reason_selected_callback'):
                    self.reason_selected_callback(self.worker)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("原因選擇失敗")
                errorMessage = response.json()["Message"]
                show_error_dialog(errorMessage)

        except requests.exceptions.RequestException as e:
            # 處理連線錯誤
            msg = QMessageBox()
            msg.setWindowTitle("原因選擇失敗")
            show_error_dialog(str(e.response))
        self.close()
    def on_cancel(self):
        if self.cancel_callback:
            self.cancel_callback(self.worker)
        self.close()