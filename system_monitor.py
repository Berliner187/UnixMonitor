#!/usr/bin/env python3
import os
import shutil
import datetime
from multiprocessing import Process
import time
import sys
from time import sleep
from random import randint

import psutil


__version__ = "0.3.1"


DEFAULT_DATETIME_FORMAT = "%H:%M:%S - %d.%m.%y"


def main():
    monitor_interface = MonitorAppearance()
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
            monitor_interface.display_topper(system_resources.check_cpu_load(cpu_percent))

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
        interface_manager.starting_program()


class MonitorAppearance:
    """
        Внешний вид UNIX монитора.
    """
    @staticmethod
    def flip() -> None:
        """ Updating the content on the screen """
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def get_time_now(datetime_format=DEFAULT_DATETIME_FORMAT):
        return datetime.datetime.now().strftime(datetime_format)

    def get_time_for_topper(self):
        time_now = f" [ {datetime.datetime.now().strftime(DEFAULT_DATETIME_FORMAT)} ] "
        return self.text_in_center(time_now)

    @staticmethod
    def close_program() -> None:
        """
            Close the program.
        """
        MonitorAppearance().flip()
        text_close = " 🔒️ MONITOR CLOSE 🔒️ "
        print(MonitorAppearance().text_in_center(text_close))
        exit()

    @staticmethod
    def get_size_of_terminal() -> int:
        """
            Getting the size (width) of the terminal screen
            :return int, e.g.: 120
        """
        cols, rows = shutil.get_terminal_size()
        return cols

    @staticmethod
    def namespace(symbol_state='') -> str:
        """
            Display the PC name in topper.
            :param symbol_state: load parameter
            :return: str
        """
        return f" [ {symbol_state} {os.uname()[1]} {symbol_state} ] "

    @staticmethod
    def get_load_status(load_status):
        if load_status == "good":
            return "🟢"
        elif load_status == "well":
            return "️🟡"
        elif load_status == "medium":
            return "🔶"
        elif load_status == "hard":
            return "⚠️"
        elif load_status == "bad":
            return "🔴"
        else:
            return "⛔"

    def display_topper(self, condition_load_status) -> None:
        """ Topper: the top part of the program """
        cols = self.get_size_of_terminal()

        symbol_state = self.get_load_status(condition_load_status)
        text_namespace = MonitorAppearance().namespace(symbol_state)

        # Отображения верхнего топпера
        print(f"{'_' * cols}\n")
        print(self.text_in_center(text_namespace))
        print(self.get_time_for_topper())

    def text_in_center(self, text) -> str:
        """
            Отображение текста по центру
            :param text: string text
            :return: str
        """
        cols = self.get_size_of_terminal()

        final_text_namespace = ''
        for i in range((cols // 2 - len(text) // 3) - (len(text) // 3)):
            final_text_namespace += '-'
        final_text_namespace += f" {text}{final_text_namespace}"

        return final_text_namespace


class BinaryClock:
    def __init__(self):
        self.clock_scheme = {
            1: [0, 0, 0, 0],
            2: [0, 0, 0, 0],
            3: [0, 0, 0, 0],
            4: [0, 0, 0, 0],
            5: [0, 0, 0, 0],
            6: [0, 0, 0, 0]
        }

    @staticmethod
    def __convert_time_value(time_value: int) -> str:
        """
            Converting time values to human format.
            Adding zero to the time value.
            e.g.
            if 12 -> 12 - PASS
            if 8 -> 08 - CONVERT
            :return: str
        """

        if len(str(time_value)) == 1:
            time_value = f"0{time_value}"

        return time_value

    def __format_time_numbers(self, hours: int, minutes: int, seconds: int) -> tuple:
        """
            Format ALL time values: hours, minutes, seconds
            :param hours: int
            :param minutes: int
            :param seconds: int
            :return: hours, minutes, seconds
        """

        hours = self.__convert_time_value(hours)
        minutes = self.__convert_time_value(minutes)
        seconds = self.__convert_time_value(seconds)

        return hours, minutes, seconds

    @staticmethod
    def __get_current_time() -> tuple:
        """
            Get current local time
            :return: int hour, int minute, int second
        """
        current_time = time.localtime()

        hour = current_time.tm_hour
        minute = current_time.tm_min
        second = current_time.tm_sec

        return hour, minute, second

    @staticmethod
    def __convert_dec_to_binary_format(time_dec_string: str) -> str:
        """
            Convert decimal time value to binary.
            e.g. 0001 1001 0000 0010 0100 0110
            :param time_dec_string: str
            :return: bin_numbers
        """

        bin_numbers = ''
        for num in time_dec_string:
            bin_numbers += '{0:04b} '.format(int(num))

        return bin_numbers

    @staticmethod
    def __get_dec_numbers_under_binary_values(time_dec_string: str) -> str:
        """
            Get The arrangement of numbers under binary
            e.g. 1    9    0    2    5    8
            :param time_dec_string: str
            :return: dec_format
        """

        dec_format = ''
        for i in time_dec_string:
            dec_format += f"{'  ' + i + '  '}"

        return dec_format

    @staticmethod
    def __generate_values_for_time():
        for hour in range(24):
            for minute in range(60):
                for second in range(60):
                    yield hour, minute, second

    def fast_iterations(self):
        for hour, minute, second in self.__generate_values_for_time():
            sleep(.05)
            hours, minutes, seconds = self.__format_time_numbers(hour, minute, second)

            time_string = f"{hours}{minutes}{seconds}"

            bin_numbers = self.__convert_dec_to_binary_format(time_string)
            dec_format = self.__get_dec_numbers_under_binary_values(time_string)

            monitor_appearance = MonitorAppearance()
            bin_numbers = monitor_appearance.text_in_center(bin_numbers.replace("1", "#").replace("0", "_"))
            dec_format = monitor_appearance.text_in_center(dec_format)

            MonitorAppearance.flip()

            print(bin_numbers)
            print(dec_format)

    def display_binary_time(self) -> None:
        """
            Display binary time format in terminal
            e.g.:
                0001 1001 0000 1000 0001 1000
                  1    9    0    8    1    8
            :return: None
        """

        hour, minute, second = self.__get_current_time()
        hours, minutes, seconds = self.__format_time_numbers(hour, minute, second)

        time_string = f"{hours}{minutes}{seconds}"

        bin_numbers = self.__convert_dec_to_binary_format(time_string)
        dec_format = self.__get_dec_numbers_under_binary_values(time_string)

        monitor_appearance = MonitorAppearance()
        bin_numbers = monitor_appearance.text_in_center(bin_numbers.replace("1", "#").replace("0", "_"))
        dec_format = monitor_appearance.text_in_center(dec_format)

        print(bin_numbers)
        print(dec_format)

    def fill_clock_scheme(self):
        for number, binary in self.clock_scheme.items():
            self.clock_scheme[number] = []
        return

    def display_clocks(self) -> None:
        while True:
            MonitorAppearance.flip()
            self.display_binary_time()
            sleep(1)

    def display_fast_iterations(self) -> None:
        while True:
            MonitorAppearance.flip()
            self.fast_iterations()


class SystemResources:
    """
        An entity that manages information about the load of system components.
    """
    def __init__(self):
        self.cores_load_dict = {}

    @staticmethod
    def __convert_to_gigabytes(value) -> float:
        """
            Convert bits to gigabytes
            TODO: Add additional units of measurement
        """
        return float("{:.2f}".format(value / (2**30)))

    def get_rom_usage(self):
        """ Получение информации о расходовании ПЗУ """
        disk_usage = psutil.disk_usage('.')
        disk_usage_percent = disk_usage.percent

        disk_total_gb = self.__convert_to_gigabytes(disk_usage.total)
        disk_used_gb = round(disk_total_gb * disk_usage_percent / 100, 2)
        disk_free_gb = round(disk_total_gb - disk_used_gb, 2)
        disk_free_percent = round(disk_free_gb * 100 / disk_total_gb, 2)

        return disk_total_gb, disk_used_gb, disk_usage_percent, disk_free_gb, disk_free_percent

    def get_cpu_usage(self):
        """ Получение информации о загрузки ЦПУ """
        cpu_cores_load = psutil.cpu_percent(interval=None, percpu=True)

        __time_now = MonitorAppearance().get_time_now()
        stuff = {}
        for core, percent in enumerate(cpu_cores_load):
            self.cores_load_dict[__time_now] = stuff[core] = percent

        return cpu_cores_load

    @staticmethod
    def check_cpu_load(kernels: list) -> str:
        """
            Assigning the status of cores depending on the load
            TODO: need refactoring, union with get_load_status
            :param kernels: list float, e.g. [10.5, 6.2]
            :return: core load status
        """
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
    def visualize_usage(percent) -> str:
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

    def get_ram_usage(self) -> tuple:
        """ Получение информации о расходовании ОЗУ """
        ram_total = self.__convert_to_gigabytes(psutil.virtual_memory().total)
        ram_percent = psutil.virtual_memory().percent
        ram_used = round(ram_total * ram_percent / 100, 2)
        ram_free = round(ram_total - ram_used, 2)
        ram_free_percent = 100 - ram_percent
        return ram_total, ram_used, ram_free, ram_percent, ram_free_percent

    @staticmethod
    def get_temperature():
        """ Получение температуры ЦПУ и ГПУ """
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
        print("FLOW RUN")
        start_time = time.monotonic()

        res = randint(2, 2**10)
        for i in range(-2 ** 30, 2 ** 30):
            res *= i + randint(-2**4, 2**10)
            try:
                res /= i
            except ZeroDivisionError:
                res += i

        end_time = time.monotonic()
        timing = abs(round(start_time - end_time, 3))

        format_datetime = datetime.datetime.now().strftime('%H:%M:%S - %d.%m')
        print(f"[{format_datetime}] --- {timing} sec")

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
            MonitorAppearance().close_program()


class InterfaceManager:
    def __init__(self):
        self.instructions = {
            1: "System Monitor",
            2: "Stress Test",
            3: "Binary Clock"
        }
        self.logo_strings_per_row = [
            "",
            "░▒▓████████▓▒░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ",
            "       ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░",
            "     ░▒▓██▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░",
            "   ░▒▓██▓▒░  ░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓████████▓▒░",
            " ░▒▓██▓▒░    ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░",
            "░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░",
            "░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░",
            "",
        ]

    def starting_program(self):
        MonitorAppearance.flip()
        self.show_logo_in_center()

        print("\n• CHANGE ACTION")

        for key, action in self.instructions.items():
            print("[{}] {}".format(key, action))

        try:
            action = int(input("\nZENITHA/MAIN: ~§ "))
            if action == 1:
                main()
            elif action == 2:
                load_machine = StressTest()
                load_machine.loading_all_streams()
            elif action == 3:
                try:
                    binary_clock = BinaryClock()
                    binary_clock.display_fast_iterations()
                except KeyboardInterrupt:
                    interface_manager.starting_program()
            elif action == 9:
                self.restart_program()
            elif action == 0:
                MonitorAppearance().close_program()
            else:
                pass
        except KeyboardInterrupt:
            MonitorAppearance().close_program()
        except ValueError:
            MonitorAppearance().close_program()

    def show_logo_in_center(self):
        cols = MonitorAppearance.get_size_of_terminal()
        for row in self.logo_strings_per_row:
            print(row.center(cols))

    @staticmethod
    def restart_program():
        os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == "__main__":
    interface_manager = InterfaceManager()
    interface_manager.starting_program()
