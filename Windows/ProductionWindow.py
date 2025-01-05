from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QGridLayout,QMessageBox)
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap
import requests
from PyQt5.QtCore import Qt,QTimer
from Windows.dialog import show_error_dialog,show_success_dialog
from Windows.resource import resource_path
from dotenv import load_dotenv
import os

class ProductionWindow(QMainWindow):
    def __init__(self,worker,deviceID):
        super().__init__()
        load_dotenv()
        self.BASE_URL = os.getenv('API_BASE_URL')
        self.setWindowTitle('生產設備管理系統')
        self.setFixedSize(800, 480)
        self.setStyleSheet("background-color: black;")
        self.work_id = ""
        self.deviceID = deviceID
        self.worker = worker
        url = f'{self.BASE_URL}GetDeviceData?id={deviceID}'
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                self.createPage(worker,result)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("資料匯入失敗")
                errorMessage = response.json()["Message"]
                show_error_dialog(errorMessage)

        except requests.exceptions.RequestException as e:
            msg = QMessageBox()
            msg.setWindowTitle("資料匯入失敗")
            show_error_dialog(str(e.response))

    def createPage(self,worker,data):
        # 建立中央視窗元件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        status = data['Status']
        font_id = QFontDatabase.addApplicationFont(resource_path("./Windows/font/NotoSansTC-Bold.ttf"))
        font_family = ""
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        # 頂部區域
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft)
        # 設備標題
        title_label = QLabel(data["Name"])
        title_label.setFont(QFont(font_family, 25, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setContentsMargins(10, 10, 10, 10)
        subtitle_label = QLabel(f"操作員: {worker}")
        subtitle_label.setFont(QFont(font_family, 10, QFont.Bold))
        subtitle_label.setStyleSheet("color: white;")
        subtitle_label.setContentsMargins(10, 10, 10, 10)

        # 狀態標籤
        status_label = QLabel(data["StatusText"])
        if status == "stopped":
            status_label.setStyleSheet("""
                        QLabel {
                            background-color: #F44336;
                            color: white;
                            border-radius: 8px;
                            padding: 5px;
                            text-align: center;
                            font-size: 25px;
                        }
                    """)
        elif status == "waiting":
            status_label.setStyleSheet("""
                        QLabel {
                            background-color: #E18300;
                            color: white;
                            border-radius: 8px;
                            padding: 5px;
                            text-align: center;
                            font-size: 25px;
                        }
                    """)
        elif status == "running":
            status_label.setStyleSheet("""
                        QLabel {
                            background-color: #11C800;
                            color: white;
                            border-radius: 8px;
                            padding: 5px;
                            text-align: center;
                            font-size: 25px;
                        }
                    """)
        status_label.setContentsMargins(10, 10, 10, 10)
        status_label.setFont(QFont(font_family))
        top_layout.addWidget(title_label)
        top_layout.addWidget(status_label)
        top_layout.addWidget(subtitle_label)
        top_layout.addStretch()
        # 創建 logo 標籤
        logo_label = QLabel()
        logo_pixmap = QPixmap(resource_path("./Windows/icon/logo.png"))  # 請替換成你的 logo 路徑
        # 調整 logo 大小（根據需要調整數值）
        scaled_pixmap = logo_pixmap.scaled(100, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        top_layout.addWidget(logo_label)
        # 添加分隔線
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #333333;")

        # 內容區域
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)

        # 左側資訊網格
        info_grid = QGridLayout()
        info_grid.setSpacing(15)  # 增加間距

        # 資訊欄位樣式
        info_style = """
                    QWidget {
                        background-color: #333333;
                        border-radius: 8px;
                    }
                    QLabel {
                        padding: 2px;
                        min-height: 15px;
                    }
                """

        title_style = """
                    QLabel {
                        color: #888888;
                        font-size: 14px;
                        padding: 3px;
                    }
                """

        value_style = """
                    QLabel {
                        color: white;
                        font-size: 16px;
                        padding: 3px;
                    }
                """
        # 資訊欄位數據
        info_data = [
            [(0, 0, '工單號碼', data["WorkOrder"]),
             (0, 1, '產品型號', data["ProductModel"])],
            [(1, 0, '運轉時數', data["OperationHours"]),
             (1, 1, '操作人員', data["Operator"])],
            [(2, 0, '預計完工', data["ExpectedCompletion"]),
             (2, 1, '工作效率', str(data["WorkEfficiency"]))],
            [(3, 0, '稼動率', str(data["Efficiency"])),
             (3, 1, '生產進度', f'{str(data["Production"]["Current"])}/{str(data["Production"]["Total"])}')]
        ]
        self.work_id = data["WorkOrder"]
        for row_data in info_data:
            for row, col, title, value in row_data:
                try:
                    container = QWidget()
                    container.setStyleSheet(info_style)
                    container_layout = QVBoxLayout(container)
                    container_layout.setContentsMargins(12, 12, 12, 12)
                    container_layout.setSpacing(5)
                    title_label = QLabel(title)
                    title_label.setStyleSheet(title_style)
                    title_label.setFont(QFont(font_family, 14))
                    value_label = QLabel(value)
                    value_label.setStyleSheet(value_style)
                    value_label.setFont(QFont(font_family, 16))
                    container_layout.addWidget(title_label)
                    container_layout.addWidget(value_label)
                    info_grid.addWidget(container, row, col)
                except Exception as e:
                    print(e)
        # 右側按鈕
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)
        button_data = []
        if status == 'stopped':
            button_data = [
                ('登出', '#2E89F0'),
                ('開始生產', '#4CAF50'),
                ('暫停生產', '#999999'),
                ('結束生產', '#999999'),
                ('換班', '#999999')
            ]
        elif status == 'waiting':
            button_data = [
                ('登出', '#999999'),
                ('恢復生產', '#4CAF50'),
                ('暫停生產', '#999999'),
                ('結束生產', '#F02E2E'),
                ('換班', '#2E89F0')
            ]
        elif status == 'running':
            button_data = [
                ('登出', '#999999'),
                ('開始生產', '#999999'),
                ('暫停生產', '#E18300'),
                ('結束生產', '#F02E2E'),
                ('換班', '#2E89F0')
            ]
        for text, color in button_data:
            btn = QPushButton(text)
            btn.setFixedHeight(55)
            btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {color};
                            color: white;
                            border-radius: 8px;
                            padding: 10px;
                            font-size: 25px;
                            min-width: 120px;
                        }}
                    """)
            btn.setFont(QFont(font_family))
            btn.setContentsMargins(0, 5, 0, 5)
            buttons_layout.addWidget(btn)
            if text == '登出' and color != '#999999':
                btn.clicked.connect(self.log_out)
            if text == '開始生產' and color != '#999999':
                btn.clicked.connect(self.start_work)
            if text == '暫停生產' and color != '#999999':
                btn.clicked.connect(self.start_down_time)
            if text == '恢復生產' and color != '#999999':
                btn.clicked.connect(self.end_down_time)
            if text == '結束生產' and color != '#999999':
                btn.clicked.connect(self.end_work)
            if text == '換班' and color != '#999999':
                btn.clicked.connect(self.add_change_operator)
        # 設置資訊區域和按鈕區域的比例
        info_widget = QWidget()
        info_widget.setLayout(info_grid)
        info_widget.setMinimumWidth(580)  # 設置較寬的最小寬度

        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)
        buttons_widget.setFixedWidth(160)  # 設置固定寬度

        # 組合布局
        content_layout.addWidget(info_widget)
        content_layout.addWidget(buttons_widget)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(separator)
        main_layout.addLayout(content_layout)

    def log_out(self):
        self.close()
        if hasattr(self, 'logout_callback'):
            self.logout_callback()

    def start_work(self):
        self.close()
        if hasattr(self, 'show_work_order_callback'):
            self.show_work_order_callback()

    def end_work(self):
        url = f'{self.BASE_URL}EndWork'
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            data = {
                "wid": self.work_id,
                "did": self.deviceID,
            }
        except Exception as e:
            print(e)
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                device_url = f'{self.BASE_URL}GetDeviceData?id={self.deviceID}'
                device_response = requests.get(device_url, headers=headers)
                if device_response.status_code == 200:
                    if self.centralWidget() is not None:
                        current_widget = self.centralWidget()
                        self.setCentralWidget(None)
                        current_widget.deleteLater()
                    result = show_success_dialog("停止工單成功")
                    if result in [QMessageBox.Ok, QMessageBox.Close]:
                        # 使用 QTimer 確保對話框完全關閉後再刷新
                        QTimer.singleShot(100, lambda: self.createPage(self.worker, device_response.json()))
            else:
                msg = QMessageBox()
                msg.setWindowTitle("停止操作失敗")
                errorMessage = response.json()["Message"]
                show_error_dialog(errorMessage)

        except requests.exceptions.RequestException as e:
            # 處理連線錯誤
            msg = QMessageBox()
            msg.setWindowTitle("停止操作失敗")
            show_error_dialog(str(e.response))
    def start_down_time(self):
        self.close()
        if hasattr(self, 'show_start_down_time'):
            self.show_start_down_time(self.work_id)
    def end_down_time(self):
        url = f'{self.BASE_URL}EndDownTime'
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            data = {
                "wid": self.work_id,
                "worker": self.worker,
            }
        except Exception as e:
            print(e)
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                device_url = f'{self.BASE_URL}GetDeviceData?id={self.deviceID}'
                device_response = requests.get(device_url, headers=headers)
                if device_response.status_code == 200:
                    if self.centralWidget() is not None:
                        current_widget = self.centralWidget()
                        self.setCentralWidget(None)
                        current_widget.deleteLater()
                    result = show_success_dialog("恢復操作成功")
                    if result in [QMessageBox.Ok,QMessageBox.Close]:
                        QTimer.singleShot(100,lambda: self.createPage(self.worker, device_response.json()))
            else:
                msg = QMessageBox()
                msg.setWindowTitle("恢復操作失敗")
                errorMessage = response.json()["Message"]
                show_error_dialog(errorMessage)

        except requests.exceptions.RequestException as e:
            # 處理連線錯誤
            msg = QMessageBox()
            msg.setWindowTitle("恢復操作失敗")
            show_error_dialog(str(e.response))
    def add_change_operator(self):
        self.close()
        if hasattr(self, 'show_change_operator_login'):
            self.show_change_operator_login(self.work_id,self.worker)
