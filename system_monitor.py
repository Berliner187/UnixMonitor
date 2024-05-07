#!/usr/bin/env python3
import psutil
import os
import shutil
import datetime
from multiprocessing import Process
import time

from time import sleep
from random import randint


__version__ = "0.2.1"


DEFAULT_DATETIME_FORMAT = "%H:%M:%S - %d.%m.%y"


def main():
    monitor_interface = MonitorInterface()
    system_resources = SystemResources()
    try:
        while True:
            # Информация о дисках
            disk_total, disk_used, rom_usage_percent, disk_free, disk_free_percent = system_resources.get_rom_usage()
            # Информация о ядрах
            cpu_percent = system_resources.get_cpu_usage()
            # Информация об ОЗУ
            ram_total, ram_used, ram_free, ram_percent, ram_free_percent = system_resources.get_ram_usage()

            monitor_interface.flip()
            monitor_interface.load_status(system_resources.check_cpu_load(cpu_percent))

            # Информация о каждом ядре
            print("\n[CPU]")
            for i, percent in enumerate(cpu_percent):
                print("  • CORE [{}] {} {}%".format(i+1, system_resources.visualize_usage(percent), percent))

            print("\n[RAM]")
            print("  • {} {}%".format(system_resources.visualize_usage(ram_percent), ram_percent))
            print("  • USAGE {} GB / {:.0f} GB    |    FREE {} GB / {:.0f} GB  ({:.1f}%)".format(
                ram_used, ram_total, ram_free, ram_total, ram_free_percent))

            print("\n[ROM]")
            print("  • {} {:.1f}%".format(
                system_resources.visualize_usage(rom_usage_percent), rom_usage_percent))
            print("  • USAGE {} GB / {} GB    |    FREE {} GB / {} GB  ({:.1f}%)".format(
                disk_used, disk_total, disk_free, disk_total, disk_free_percent))

            system_resources.get_temperature()
            sleep(1)

    except KeyboardInterrupt:
        MonitorInterface().close_program()


class MonitorInterface:
    """
        Внешний вид монитора ресурсов
    """
    @staticmethod
    def flip():
        """ Update Display"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def get_time_now(datetime_format=DEFAULT_DATETIME_FORMAT):
        return datetime.datetime.now().strftime(datetime_format)

    def get_time_for_topper(self):
        time_now = f" [ {datetime.datetime.now().strftime(DEFAULT_DATETIME_FORMAT)} ] "
        return self.text_in_center(time_now)

    @staticmethod
    def close_program():
        MonitorInterface().flip()
        text_close = " 🔒️ MONITOR CLOSE 🔒️ "
        print(MonitorInterface().text_in_center(text_close))
        exit()

    @staticmethod
    def get_size_of_terminal():
        """ Получение ширины и длины терминала """
        cols, rows = shutil.get_terminal_size()
        return cols

    @staticmethod
    def namespace(symbol_state=''):
        return f" [ {symbol_state} {os.uname()[1]} {symbol_state} ] "

    def load_status(self, condition):
        """ Отображение статуса нагрузки в топпере """
        cols = self.get_size_of_terminal()

        symbol_state = "⛔"
        if condition == "good":
            symbol_state = "🟢"
        elif condition == "well":
            symbol_state = "️🟡"
        elif condition == "medium":
            symbol_state = "🔶"
        elif condition == "hard":
            symbol_state = "⚠️"
        elif condition == "bad":
            symbol_state = "🔴"

        text_namespace = MonitorInterface().namespace(symbol_state)

        # Отображения верхнего топпера
        print(f"{'_' * cols}\n")
        print(self.text_in_center(text_namespace))
        print(self.get_time_for_topper())

    def text_in_center(self, text) -> str:
        """
            Отображение текста в топпере по центру
            :param text: str
            :return: str
        """
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
    def __init__(self):
        self.cores_load_dict = {}

    @staticmethod
    def __convert_to_gigabytes(value) -> float:
        return round(value / (2**30), 2)

    def get_rom_usage(self):
        disk_usage = psutil.disk_usage('.')
        disk_usage_percent = disk_usage.percent

        disk_total = self.__convert_to_gigabytes(disk_usage.total)
        disk_used = round(disk_total * disk_usage_percent / 100, 2)
        disk_free = round(disk_total - disk_used, 2)
        disk_free_percent = round(disk_free * 100 / disk_total, 2)

        return disk_total, disk_used, disk_usage_percent, disk_free, disk_free_percent

    def get_cpu_usage(self):
        cpu_cores_load = psutil.cpu_percent(interval=None, percpu=True)

        __time_now = MonitorInterface().get_time_now()
        stuff = {}
        for core, percent in enumerate(cpu_cores_load):
            self.cores_load_dict[__time_now] = stuff[core] = percent

        return cpu_cores_load

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
    def visualize_usage(percent):
        """ Визуализация использования системных ресурсов """
        number_divisions = 50
        one_division = round(100 / number_divisions)
        lines = '_' * number_divisions

        range_list = []
        for i in range(0, 100 + 1, one_division):
            range_list.append(i)

        for i in range(len(range_list)):
            if range_list[i - 1] < percent <= range_list[i]:
                lines = '#' * i + '_' * (number_divisions - i)

        return lines

    def get_ram_usage(self):
        ram_total = self.__convert_to_gigabytes(psutil.virtual_memory().total)
        ram_percent = psutil.virtual_memory().percent
        ram_used = round(ram_total * ram_percent / 100, 2)
        ram_free = round(ram_total - ram_used, 2)
        ram_free_percent = 100 - ram_percent
        return ram_total, ram_used, ram_free, ram_percent, ram_free_percent

    @staticmethod
    def get_temperature():
        try:
            # Для x86 процессора
            temp = psutil.sensors_temperatures()
            print("Disk temp: {}°C".format(temp['nvme'][0][1]))
            print("GPU temp: {}°C".format(temp['amdgpu'][0][1]))
        except AttributeError:
            pass


class StressTest:
    @staticmethod
    def random_operations():
        print("RUN")
        start_time = time.monotonic()
        cnt_operations = 0

        res = randint(2, 2**10)
        for i in range(-2 ** 30, 2 ** 30):
            cnt_operations += 1
            res *= i + randint(-2**4, 2**10)
            try:
                res /= i
            except ZeroDivisionError:
                res += i

        end_time = time.monotonic()
        timing = abs(round(start_time - end_time, 3))
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S - %d.%m')}] --- {timing} sec, operations - {cnt_operations}")

    @staticmethod
    def __multiprocess_test():
        cpu_count = psutil.cpu_percent(interval=None, percpu=True)
        processes = []
        for i in range(len(cpu_count)):
            p = Process(target=StressTest.random_operations)
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

    def loading_all_streams(self):
        try:
            self.__multiprocess_test()
        except KeyboardInterrupt:
            MonitorInterface().close_program()


class InterfaceManager:
    @staticmethod
    def starting_program():
        MonitorInterface.flip()
        text = MonitorInterface.namespace()
        print(text)
        print("\nCHANGE ACTION")
        print("[1] System Monitor")
        print("[2] Stress test")
        action = int(input("~§: "))
        if action == 1:
            main()
        elif action == 2:
            load_machine = StressTest()
            load_machine.loading_all_streams()


if __name__ == "__main__":
    InterfaceManager.starting_program()
