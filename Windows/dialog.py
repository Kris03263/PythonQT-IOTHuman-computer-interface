from PyQt5.QtWidgets import QMessageBox,QLabel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

def show_error_dialog(error_message):
        msg = QMessageBox()
        msg.setWindowTitle("操作失敗")
        msg.setText(error_message)
        msg.setIcon(QMessageBox.Warning)

        msg.setWindowFlags(Qt.WindowModal |Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        msg.setModal(True)
        msg.closeEvent = lambda event: handle_close(msg, event)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #333333;
                min-width: 300px;
                min-height: 50px;
                font-size: 13px;
                padding: 15px;
                line-height: 1.5;
            }
            QMessageBox QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                min-width: 80px;
                font-size: 13px;
            }
            QMessageBox QPushButton:hover {
                background-color: #c0392b;
            }
            QMessageBox QPushButton:pressed {
                background-color: #a93226;
            }
            QMessageBox {
                border: 1px solid #cccccc;
                border-radius: 6px;
            }
        """)


        msg.setStandardButtons(QMessageBox.Ok)
        msg.button(QMessageBox.Ok).setText("確定")

        icon = msg.findChild(QLabel, "qt_msgboxex_icon_label")
        if icon:
            icon.setStyleSheet("""
                min-width: 40px;
                min-height: 40px;
            """)

        return msg.exec_()
def show_success_dialog(success_message):
        msg = QMessageBox()
        msg.setWindowTitle("操作成功")
        msg.setText(success_message)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowFlags(Qt.WindowModal |Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        msg.setModal(True)
        msg.closeEvent = lambda event: handle_close(msg, event)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #333333;
                min-width: 300px;
                min-height: 50px;
                font-size: 13px;
                padding: 15px;
                line-height: 1.5;
            }
            QMessageBox QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                min-width: 80px;
                font-size: 13px;
            }
            QMessageBox QPushButton:hover {
                background-color: #c0392b;
            }
            QMessageBox QPushButton:pressed {
                background-color: #a93226;
            }
            QMessageBox {
                border: 1px solid #cccccc;
                border-radius: 6px;
            }
        """)

        msg.setStandardButtons(QMessageBox.Ok)
        msg.button(QMessageBox.Ok).setText("確定")

        icon = msg.findChild(QLabel, "qt_msgboxex_icon_label")
        if icon:
            icon.setStyleSheet("""
                min-width: 40px;
                min-height: 40px;
            """)

        return msg.exec_()
def handle_close(msg, event):
    # 將關閉按鈕點擊視為確定按鈕點擊
    msg.done(QMessageBox.Ok)