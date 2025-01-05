import sys
from PyQt5.QtWidgets import QApplication
from Windows.LoginWindow import LoginWindow
from Windows.ProductionWindow import ProductionWindow
from Windows.WorkOrderWindow import WorkOrderWindow
from Windows.StartDownTimeWindow import StartDownTimeWindow
from Windows.ChangeOperatorLoginWindow import ChangeOperatorLoginWindow
from Windows.ChangeDeviceWindow import ChangeDeviceWindow
import json,os
from Windows.resource import resource_path
from json import load

class MainApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = None
        self.production_window = None
        self.work_order_window = None
        self.start_down_time_window = None
        self.change_operator_login_window = None
        self.change_device_window = None
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
        with open(self.file_path, 'r',encoding='utf-8') as file:
            data = json.load(file)
            if data["deviceID"] != "":
                self.deviceID = data["deviceID"]
            else:
                self.deviceID = "BN0001"
        self.worker = ""
        self.show_login()

    def show_login(self):
        self.login_window = LoginWindow(self.deviceID)
        self.login_window.login_success_callback = self.show_production
        self.login_window.change_device_callback = self.show_change_device
        self.login_window.showFullScreen()

    def show_change_device(self):
        self.change_device_window = ChangeDeviceWindow()
        self.change_device_window.cancel_callback = self.show_login
        self.change_device_window.on_device_selected_callback = self.set_device
        self.change_device_window.showFullScreen()
        if self.login_window:
            self.login_window.close()

    def show_production(self,worker):
        self.worker = worker
        self.production_window = ProductionWindow(self.worker,self.deviceID)
        self.production_window.logout_callback = self.show_login
        self.production_window.show_work_order_callback = self.show_work_order_selection
        self.production_window.show_start_down_time = self.show_start_down_time
        self.production_window.show_change_operator_login = self.show_change_operator_login
        self.production_window.showFullScreen()
        if self.login_window:
            self.login_window.close()
        if self.work_order_window:
            self.work_order_window.close()
        if self.change_operator_login_window:
            self.change_operator_login_window.close()

    def show_work_order_selection(self):
        self.work_order_window = WorkOrderWindow(self.worker, self.deviceID)
        self.work_order_window.work_order_selected_callback = self.show_production
        self.work_order_window.cancel_callback = self.show_production
        self.work_order_window.showFullScreen()
        if self.production_window:
            self.production_window.close()

    def show_start_down_time(self,workOrderID):
        try:
            self.start_down_time_window = StartDownTimeWindow(self.worker, self.deviceID,workOrderID)
            self.start_down_time_window.reason_selected_callback = self.show_production
            self.start_down_time_window.cancel_callback = self.show_production
            self.start_down_time_window.showFullScreen()
            if self.production_window:
                self.production_window.close()
        except Exception as e:
            print(e)
    def show_change_operator_login(self,workOrderID,oldWorker):
        try:
            self.change_operator_login_window = ChangeOperatorLoginWindow(workOrderID,oldWorker)
            self.change_operator_login_window.change_operator_callback = self.show_production
            self.change_operator_login_window.cancel_callback = self.show_production
            self.change_operator_login_window.showFullScreen()
            if self.production_window:
                self.production_window.close()
        except Exception as e:
            print(e)
    def set_device(self,deviceID):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        data["deviceID"] = deviceID
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        self.deviceID = deviceID
        self.show_login()

    def run(self):
        return self.app.exec_()


if __name__ == '__main__':
    app = MainApplication()
    sys.exit(app.run())