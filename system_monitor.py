#!/usr/bin/env python3
import psutil
import os
import shutil
import datetime
import sys

from time import sleep
from random import randint


__version__ = "0.1.2"


def main():
    monitor_interface = MonitorInterface()
    try:
        while True:
            system_resources = SystemResources()

            # Информация о дисках
            disk_total, disk_used, disk_usage_percent, disk_free, disk_free_percent = system_resources.get_disk_usage()
            # Информация о ядрах
            cpu_percent = system_resources.get_cpu_usage()
            # Информация об ОЗУ
            ram_percent = system_resources.get_memory_usage()

            monitor_interface.flip()
            monitor_interface.namespace(system_resources.check_cpu_load(cpu_percent))

            # Информация о каждом ядре
            print("[CPU]")
            for i, percent in enumerate(cpu_percent):
                print("  Core [{}] {} {}%".format(i+1, system_resources.visualize_cpu_usage(percent), percent))

            print("\n[RAM]")
            print("  Usage: {} {}%".format(system_resources.visualize_ram_usage(ram_percent), ram_percent))
            print("\n[ROM]")
            print("  Usage: {:.2f} GB / {:.2f} GB ({:.1f}%)".format(
                disk_used, disk_total, disk_usage_percent))
            print("  Free: {} GB ({}%)".format(disk_free, disk_free_percent))
            system_resources.get_temperature()
            sleep(1)

    except KeyboardInterrupt:
        monitor_interface.flip()
        text_close = " ❌ MONITOR CLOSE ❌ "
        print(monitor_interface.text_in_center(text_close))
        exit()


class MonitorInterface:
    @staticmethod
    def flip():
        """ Update Display"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_time_now(self):
        time_now = f" [ {datetime.datetime.now().strftime('%H:%M:%S - %d.%m.%y')} ] "
        return self.text_in_center(time_now)

    @staticmethod
    def get_size_of_terminal():
        """ Получение ширины и длины терминала """
        cols, rows = shutil.get_terminal_size()
        return cols

    def namespace(self, condition):
        """ Отображение названия в топпере """
        cols = self.get_size_of_terminal()

        symbol_state = "⛔"
        if condition == "good":
            symbol_state = "✅"
        elif condition == "well":
            symbol_state = "️🟡"
        elif condition == "medium":
            symbol_state = "🔶"
        elif condition == "hard":
            symbol_state = "⚠️"
        elif condition == "bad":
            symbol_state = "🔴"

        text_namespace = f" [ {symbol_state} ZENITHA {symbol_state} ] "

        # Верхний топпер
        print("_" * cols + '\n')
        print(self.text_in_center(text_namespace))
        print(self.get_time_now())

    def text_in_center(self, text):
        cols = self.get_size_of_terminal()

        final_text_namespace = ''
        for i in range((cols // 2 - len(text) // 3) - (len(text) // 3)):
            final_text_namespace += '-'
        final_text_namespace += text + final_text_namespace
        return final_text_namespace


class SystemResources:
    """
        Информация о нагрузке системных компонентов
    """
    @staticmethod
    def get_disk_usage():
        disk_usage = psutil.disk_usage('.')

        disk_total = disk_usage.total / (2**30)
        disk_usage_percent = disk_usage.percent
        disk_used = disk_usage.used / (2**30)
        disk_free = round(disk_usage.free / (2**30), 2)
        disk_free_percent = round(disk_free * 100 / disk_total, 2)

        return disk_total, disk_used, disk_usage_percent, disk_free, disk_free_percent

    @staticmethod
    def get_cpu_usage():
        return psutil.cpu_percent(interval=None, percpu=True)

    @staticmethod
    def check_cpu_load(kernels):
        delta_cpu_usage = sum(kernels) / len(kernels)
        status = "unknow"

        if delta_cpu_usage < 20:
            status = "good"
        elif 20 <= delta_cpu_usage < 40:
            status = "well"
        elif 40 <= delta_cpu_usage < 70:
            status = "medium"
        elif 70 <= delta_cpu_usage < 90:
            status = "hard"
        elif delta_cpu_usage >= 90:
            status = "bad"

        return status

    @staticmethod
    def __visualize_usage(percent):
        lines = '_' * 20

        range_list = []
        for i in range(0, 100 + 1, 5):
            range_list.append(i)

        for i in range(len(range_list)):
            if range_list[i - 1] < percent <= range_list[i]:
                lines = '=' * i + '_' * (20 - i)

        return lines

    def visualize_cpu_usage(self, kernel_load):
        return self.__visualize_usage(kernel_load)

    def visualize_ram_usage(self, ram_load):
        return self.__visualize_usage(ram_load)

    @staticmethod
    def get_memory_usage():
        return psutil.virtual_memory().percent

    @staticmethod
    def get_temperature():
        # Для x86 процессора
        try:
            temp = psutil.sensors_temperatures()
            print("Disk temp: {}°C".format(temp['nvme'][0][1]))
            print("GPU temp: {}°C".format(temp['amdgpu'][0][1]))
        except Exception:
            pass


class StressTest:
    @staticmethod
    def calculations():
        res = 8.4
        for i in range(-2 ** 30, 2 ** 30):
            res *= i + randint(-2**4, 2**10)
            try:
                res /= i
            except ZeroDivisionError:
                res += i


if __name__ == "__main__":
    main()
