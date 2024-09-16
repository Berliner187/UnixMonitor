from time import sleep

from monitor_appearance import MonitorAppearance

import psutil


class SystemResources:
    """
        An entity that manages information about the load of system components.
        Available: CPU, RAM, ROM, temperature (optional)
    """
    def __init__(self):
        self.cores_load_dict = {}

    def reset_cores_load_dict(self):
        self.cores_load_dict.clear()

    @staticmethod
    def __convert_to_gigabytes(value) -> float:
        """
            Convert bits to gigabytes
            TODO: Add additional units of measurement
        """
        return float("{:.2f}".format(value / (2**30)))

    def get_rom_usage(self) -> tuple:
        """ Получение информации о расходовании ПЗУ """
        disk_usage = psutil.disk_usage('.')
        disk_usage_percent = disk_usage.percent

        disk_total_gb = self.__convert_to_gigabytes(disk_usage.total)
        disk_used_gb = round(disk_total_gb * disk_usage_percent / 100, 2)
        disk_free_gb = round(disk_total_gb - disk_used_gb, 2)
        disk_free_percent = round(disk_free_gb * 100 / disk_total_gb, 2)

        return disk_total_gb, disk_used_gb, disk_usage_percent, disk_free_gb, disk_free_percent

    def get_cpu_usage(self) -> list:
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
            # For x86 arch
            temp = psutil.sensors_temperatures()
            print("Disk temp: {}°C".format(temp['nvme'][0][1]))
            print("GPU temp: {}°C".format(temp['amdgpu'][0][1]))
        except AttributeError:
            pass

    def display_cpu_consumption(self) -> None:
        # Информация о каждом ядре
        cpu_percent = self.get_cpu_usage()
        print("\n[CPU]")
        for i, percent in enumerate(cpu_percent):
            print("  • CORE [{}] {} {}%".format(i + 1, self.visualize_usage(percent), percent))


class SystemMonitoring(SystemResources):
    def system_monitoring(self):
        monitor_interface = MonitorAppearance()
        while True:
            # Информация о ядрах
            cpu_percent = self.get_cpu_usage()

            monitor_interface.flip()
            monitor_interface.display_topper(self.check_cpu_load(cpu_percent))

            # Информация об ОЗУ
            ram_total, ram_used, ram_free, ram_percent, ram_free_percent = self.get_ram_usage()
            # Информация о дисках
            disk_total, disk_used, rom_usage_percent, disk_free, disk_free_percent = self.get_rom_usage()

            # Информация о каждом ядре
            print("\n[CPU]")
            for i, percent in enumerate(cpu_percent):
                print("  • CORE [{}] {} {}%".format(i + 1, self.visualize_usage(percent), percent))

            print("\n[RAM]")
            print("  • {} {}%".format(self.visualize_usage(ram_percent), ram_percent))
            print("  • USAGE {} GB / {:.0f} GB    |    FREE {} GB / {:.0f} GB  ({:.1f}%)".format(
                ram_used, ram_total, ram_free, ram_total, ram_free_percent))

            print("\n[ROM]")
            print("  • {} {:.1f}%".format(
                self.visualize_usage(rom_usage_percent), rom_usage_percent))
            print("  • USAGE {} GB / {} GB    |    FREE {} GB / {} GB  ({:.1f}%)".format(
                disk_used, disk_total, disk_free, disk_total, disk_free_percent))

            self.get_temperature()
            sleep(1)
