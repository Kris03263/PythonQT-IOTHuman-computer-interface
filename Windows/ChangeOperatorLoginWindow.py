import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLineEdit, QPushButton, QLabel, QHBoxLayout,QMessageBox)
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QFont,QFontDatabase
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap
from Windows.dialog import show_error_dialog,show_success_dialog
from Windows.resource import resource_path
import requests
import json
from dotenv import load_dotenv
import os

class ChangeOperatorLoginWindow(QMainWindow):
    def __init__(self,workOrderID,oldWorker):
        super().__init__()
        load_dotenv()
        self.BASE_URL = os.getenv('API_BASE_URL')
        # 設定視窗標題
        self.setWindowTitle('換班登入頁面')
        self.workOrderID = workOrderID
        self.oldWorker = oldWorker
        # 獲取使用者目錄
        user_home = os.path.expanduser('~')
        # 創建應用程式的數據目錄
        app_data_dir = os.path.join(user_home, '.yin_yu_QT')

        # 確保目錄存在
        if not os.path.exists(app_data_dir):
            os.makedirs(app_data_dir)

        # 設定 JSON 文件路徑
        self.file_path = os.path.join(app_data_dir, 'temp.json')

        # 如果文件不存在，創建一個默認的 JSON 文件
        if not os.path.exists(self.file_path):
            default_data = {
                "last_login": {
                    "account": "a",
                    "password": "abc"
                },
                "deviceID": "BN0003"
            }
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=4)
        # 設定視窗大小為 800x480（7吋大小）
        self.setFixedSize(800, 480)
        # 建立中央視窗元件和佈局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        font_id = QFontDatabase.addApplicationFont(resource_path("./Windows/font/NotoSansTC-Bold.ttf"))
        print(font_id)
        font_family = ""
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        # 創建 logo 標籤
        logo_label = QLabel()
        logo_pixmap = QPixmap(resource_path("./Windows/icon/logo.png"))
        # 調整 logo 大小（根據需要調整數值）
        scaled_pixmap = logo_pixmap.scaled(100, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # 創建一個水平佈局來放置 logo
        top_layout = QHBoxLayout()
        top_layout.addStretch()  # 將 logo 推到右側
        top_layout.addWidget(logo_label)
        top_layout.setContentsMargins(0, 10, 10, 0)  # 設定邊距 (左, 上, 右, 下)

        # 將 top_layout 加入主佈局
        layout.insertLayout(0, top_layout)  # 在索引 0 的位置插入（最上方）
        # 上方間距
        layout.addSpacing(35)

        # 標題文字
        title_label = QLabel('請輸入帳號密碼')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont(font_family, 24, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        layout.addWidget(title_label)

        # 標題下方間距
        layout.addSpacing(40)

        # 建立表單佈局
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

        # 帳號輸入欄位
        self.username = QLineEdit()
        self.username.setPlaceholderText('請輸入帳號')
        self.username.setInputMethodHints(Qt.ImhPreferUppercase | Qt.ImhPreferLowercase)
        self.username.setFixedSize(400, 50)
        self.username.setFont(QFont(font_family, 10))
        self.username.setStyleSheet("""
            QLineEdit {
                background-color: #3A3A3A;
                border-radius: 5px;
                padding: 10px;
                color: white;
            }
        """)

        # 密碼輸入欄位
        self.password = QLineEdit()
        self.password.setPlaceholderText('請輸入密碼')
        self.password.setEchoMode(QLineEdit.Password)  # 設定密碼遮罩
        self.password.setInputMethodHints(Qt.ImhPreferUppercase | Qt.ImhPreferLowercase)
        self.password.setFixedSize(400, 50)
        self.password.setFont(QFont(font_family, 10))
        self.password.setStyleSheet("""
            QLineEdit {
                background-color: #3A3A3A;
                border-radius: 5px;
                padding: 10px;
                color: white;
            }
        """)

        # 將輸入欄位置中
        username_layout = QHBoxLayout()
        username_layout.addStretch()
        username_layout.addWidget(self.username)
        username_layout.addStretch()

        password_layout = QHBoxLayout()
        password_layout.addStretch()
        password_layout.addWidget(self.password)
        password_layout.addStretch()

        form_layout.addLayout(username_layout)
        form_layout.addLayout(password_layout)

        # 將表單加入主佈局
        layout.addLayout(form_layout)

        # 按鈕佈局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        # 登入按鈕
        login_btn = QPushButton('登入')
        login_btn.setFixedSize(190, 50)
        login_btn.setFont(QFont(font_family, 12))
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)

        # 取消按鈕
        cancel_btn = QPushButton('取消')
        cancel_btn.setFixedSize(190, 50)
        cancel_btn.setFont(QFont(font_family, 12))
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E53935;
            }
        """)

        # 將按鈕置中
        button_layout.addStretch()
        button_layout.addWidget(login_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addStretch()

        # 加入按鈕佈局
        layout.addSpacing(40)
        layout.addLayout(button_layout)
        layout.addStretch()

        # 連接按鈕事件
        login_btn.clicked.connect(self.confirm_change)
        cancel_btn.clicked.connect(self.cancel_change)

        # 設定視窗背景顏色
        self.setStyleSheet("background-color: black;")

    def confirm_change(self):
        account = self.username.text()
        password = self.password.text()
        url = f'{self.BASE_URL}LoginFromDevice'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'account': account,
            'password': password
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            status = bool(response.json()['Result'])
            newWorker = response.json()["Name"]
            if status:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                data["last_login"]["account"] = self.username.text()
                data["last_login"]["password"] = self.password.text()
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                next_url = f'{self.BASE_URL}AddChangeOperator'
                next_headers = {
                    'Content-Type': 'application/json'
                }
                next_data = {
                    'wid': self.workOrderID,
                    'worker': newWorker
                }
                next_response = requests.post(next_url, headers=next_headers, json=next_data)
                if next_response.status_code == 200:
                    result = show_success_dialog("換班成功!")
                    if result in [QMessageBox.Ok, QMessageBox.Close]:  # 接受確定按鈕或關閉按鈕的點擊
                        # 使用 QTimer 確保對話框完全關閉後再執行回調
                        QTimer.singleShot(100, lambda: self._handle_operator_change(newWorker))
            else:
                # 登入失敗，顯示錯誤訊息
                msg = QMessageBox()
                msg.setWindowTitle("登入失敗")
                errorMessage = response.json()["ErrorMessage"]
                show_error_dialog(errorMessage)

        except requests.exceptions.RequestException as e:
            # 處理連線錯誤
            error_msg = QMessageBox()
            error_msg.setWindowTitle("連線錯誤")
            error_msg.setText(f"連線發生錯誤：{str(e)}")
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setStyleSheet("QLabel{min-width: 300px; color: black;}")
            error_msg.exec_()
    def cancel_change(self):
        if hasattr(self,'cancel_callback'):
            self.cancel_callback(self.oldWorker)

    def _handle_operator_change(self, newWorker):
        if hasattr(self, 'change_operator_callback'):
            self.change_operator_callback(newWorker)


