#!/usr/bin/env python3
import psutil
import os
import shutil
import datetime

from time import sleep
from random import randint

import subprocess


def main():
    while True:
        monitor_interface = MonitorInterface()
        try:
            system_resources = SystemResources()

            # Информация о дисках
            disk_total, disk_used, disk_usage_percent, disk_free, disk_free_percent = system_resources.get_disk_usage()
            # Информация о ядрах
            cpu_percent = system_resources.get_cpu_usage()
            # Информация об ОЗУ
            memory_percent = system_resources.get_memory_usage()

            monitor_interface.flip()
            monitor_interface.namespace(system_resources.check_cpu_usage(cpu_percent))

            # Информация о каждом ядре
            print("CPU USAGE")
            for i, percent in enumerate(cpu_percent):
                print("  Core {}: {} {}%".format(i+1, system_resources.visualize_cpu_usage(percent), percent))

            print('\n')
            print("RAM: {}%".format(memory_percent))
            print("ROM: {:.2f} / {:.2f} GB ({:.1f}%) | {} GB free ({}%)".format(
                disk_used, disk_total, disk_usage_percent, disk_free, disk_free_percent))
            try:
                system_resources.get_temperature()
            except Exception:
                pass
        except KeyboardInterrupt:
            monitor_interface.flip()
            cols = monitor_interface.get_size_of_terminal()
            text_close = " ❌ MONITOR CLOSE ❌ "
            start_ris = ''
            for i in range((cols // 2 - len(text_close)//2) - (len(text_close) // 2)):
                start_ris += '-'
            start_ris += text_close + start_ris
            print(start_ris)
            exit()


class MonitorInterface:
    @staticmethod
    def flip():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def get_time_now():
        return f"[{datetime.datetime.now().strftime('%H:%M:%S - %d.%m')}]\n"

    @staticmethod
    def get_size_of_terminal():
        """ Получение ширины и длины терминала """
        cols, rows = shutil.get_terminal_size()
        return cols

    def namespace(self, condition):
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

        text_namespace = f"[ {symbol_state} SYSTEM MONITOR {symbol_state} ]"

        final_text_namespace = ''
        for i in range((cols // 2 - len(text_namespace) // 3) - (len(text_namespace) // 3)):
            final_text_namespace += '-'
        final_text_namespace += text_namespace + final_text_namespace
        print("_" * cols + '\n')
        print(final_text_namespace)
        print(self.get_time_now())


class SystemResources:
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
        return psutil.cpu_percent(interval=1, percpu=True)

    @staticmethod
    def check_cpu_usage(kernels):
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
    def visualize_cpu_usage(kernel):
        lines = '_' * 10

        range_list = []
        for i in range(0, 100+1, 10):
            range_list.append(i)

        for i in range(len(range_list)):
            if range_list[i-1] < kernel <= range_list[i]:
                lines = '=' * i + '_' * (10 - i)

        # if 5 < kernel <= 10:
        #     lines = '=' + '_'*9
        # elif 10 < kernel <= 20:
        #     lines = '='*2 + '_'*8
        # elif 20 < kernel <= 30:
        #     lines = '='*3 + '_'*7
        # elif 30 < kernel <= 40:
        #     lines = '='*4 + '_'*6
        # elif 40 < kernel <= 50:
        #     lines = '='*5 + '_'*5
        # elif 50 < kernel <= 60:
        #     lines = '='*6 + '_'*4
        # elif 60 < kernel <= 70:
        #     lines = '='*7 + '_'*3
        # elif 70 < kernel <= 80:
        #     lines = '='*8 + '_'*2
        # elif 80 < kernel <= 90:
        #     lines = '='*9 + '_'
        # elif 90 < kernel <= 100:
        #     lines = '='*10
        return lines

    @staticmethod
    def get_memory_usage():
        return psutil.virtual_memory().percent

    @staticmethod
    def get_temperature():
        # Для x86 процессора
        temp = psutil.sensors_temperatures()
        print(temp['nvme'][0][1])
        print(temp['amdgpu'][0][1])


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
