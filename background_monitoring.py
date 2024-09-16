"""
    Модуль сбора, записи и отображения информации о потреблении ресурсов на сервере
"""
import datetime
import time
import csv
import os

import psutil
import pandas as pd
import matplotlib.pyplot as plt

from constants import *


class MonitorSystemUsage:
    def __init__(self):
        self.monitoring_file = f"{DIR_VISUALIZATION_REPORTS}monitoring_{datetime.datetime.now().strftime(DATE_FORMAT_TRACKING)}.{EXTENSION}"

    @staticmethod
    def __timer(time_range=1):
        for i in range(time_range, 0, -1):
            print(i, "sec")
            time.sleep(1)
        os.system("clear")

    @staticmethod
    def __check_dir_for_exist():
        if os.path.exists(DIR_VISUALIZATION_REPORTS) is False:
            os.mkdir(DIR_VISUALIZATION_REPORTS)

    def start_background_monitoring(self, interval: int, duration: int) -> None:
        """
            Starting background monitoring.
            :param interval: int value
            :param duration: int value
            :return: None
        """
        print("Starting...")
        self.__check_dir_for_exist()
        self.__timer()
        print("Monitoring: [ WORK ]")
        print("You: [ WORK ]")

        print(interval, duration)

        file_monitoring = self.monitoring_file
        with open(file_monitoring, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'cpu_percent', 'memory_percent', 'disk_usage_percent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            start_time = time.time()

            try:
                while (time.time() - start_time) < duration:
                    timestamp = int(time.time())
                    cpu_percent = psutil.cpu_percent(interval=interval)
                    memory_percent = psutil.virtual_memory().percent
                    disk_usage_percent = psutil.disk_usage('/').percent

                    writer.writerow(
                        {
                            'timestamp': timestamp,
                            'cpu_percent': cpu_percent,
                            'memory_percent': memory_percent,
                            'disk_usage_percent': disk_usage_percent
                        }
                    )

                    time.sleep(interval)
                print("MONITORING: COMPLETE [ OK ]")
            except KeyboardInterrupt:
                os.system("clear")
                print("[ MONITORING will be STOPPED ]")

    @staticmethod
    def __create_graph(_data, type_indicators, label_name, color_line, name_y_label, name_title):
        plt.figure(figsize=(10, 6))
        plt.plot(_data['timestamp'], _data[type_indicators], label=label_name, color=color_line)
        plt.xlabel('Time')
        plt.ylabel(name_y_label)
        plt.title(name_title)
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def __select_file_for_visualisation():
        print("[ Please, change file for visualisation of usage ]\n")

        files = []
        cnt = 0
        for file in os.listdir(DIR_VISUALIZATION_REPORTS):
            cnt += 1
            print(f"[{cnt}] – {file}")
            files.append(file)

        select = int(input("\n[ CHANGE FILE by number ]: "))

        selected_file = files[select-1]
        path_to_selected_file = DIR_VISUALIZATION_REPORTS + selected_file

        return path_to_selected_file

    def visualize_system_usage(self) -> None:
        """
            Визуализация использования системных ресурсов (на графиках)
        :return: None
        """
        data = pd.read_csv(self.__select_file_for_visualisation())

        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')

        self.__create_graph(
            data, "cpu_percent", "CPU Load", "#9b30ff",
            "CPU Load (%)", "CPU Load Over Time")

        self.__create_graph(
            data, "memory_percent", "RAM Usage", "green",
            "RAM Usage (%)", "Memory Usage Over Time")

        self.__create_graph(
            data, "disk_usage_percent", "ROM Usage", "orange",
            "RAM Usage (%)", "ROM Usage Over Time")


class UserParameters:
    def __init__(self):
        self.default_values = {
            'interval': 5,
            'duration': 86_400
        }

    def user_select_options(self) -> tuple:
        """
            Prompts the user to select interval and duration for monitoring, with error handling and default values.
            :return: tuple (interval, duration)
        """
        print("Start monitoring: Options")

        interval = input(f"\nEnter interval in seconds (default {self.default_values['interval']} sec): ")
        if not interval.isdigit():
            interval = self.default_values['interval']
            print(f"Using default interval: {interval} sec\n")
        else:
            interval = int(interval)

        duration_in_seconds = self.default_values['duration']
        duration_in_hours = round(duration_in_seconds / 3600)
        duration = input(
            f"\nEnter duration in seconds (default {duration_in_seconds} sec, {duration_in_hours:.2f} hours): ")

        if not duration.isdigit():
            duration = duration_in_seconds
            print(f"Using default duration: {duration_in_seconds} sec ({duration_in_hours:.2f} hours)\n")
        else:
            duration = int(duration)

        return interval, duration
