#!/usr/bin/env python3
import os
import sys
from time import sleep

import monitor_appearance
import background_monitoring
from system_resources import SystemMonitoring
from monitor_appearance import MonitorAppearance
from stress_tests import StressTests
from binary_clock import BinaryClock


__version__ = "0.4.0"


class InterfaceManager:
    """
        Интерфейс UnixMonitor (ZENITHA).
        Управляет визуальной частью программы.
    """
    def __init__(self):
        self.instructions = {
            1: "System Monitor",
            2: "Stress Test",
            3: "Binary Clock",
            4: "Start monitoring",
            5: "Visualize monitoring\n",
            9: "Restart",
            0: "Exit",
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

    def show_logo_in_center(self):
        cols = MonitorAppearance.get_size_of_terminal()
        for row in self.logo_strings_per_row:
            print(row.center(cols))

    @staticmethod
    def restart_program():
        os.execl(sys.executable, sys.executable, *sys.argv)

    def starting_program(self):
        MonitorAppearance.flip()
        self.show_logo_in_center()

        print("\n• CHANGE ACTION\n")

        for key, action in self.instructions.items():
            print("[{}] {}".format(key, action))

        try:
            action = int(input("\nZENITHA/MAIN: ~§ "))
            if action == 1:
                system_monitor = SystemMonitoring()
                try:
                    system_monitor.system_monitoring()
                except KeyboardInterrupt:
                    interface_manager.starting_program()

            elif action == 2:
                load_machine = StressTests()
                load_machine.multiprocess_test()

            elif action == 3:
                try:
                    binary_clock = BinaryClock()
                    binary_clock.starting_binary_clock()
                except KeyboardInterrupt:
                    interface_manager.starting_program()

            elif action == 4:
                monitor_appearance.MonitorAppearance().flip()
                self.show_logo_in_center()
                try:
                    monitor_system_usage = background_monitoring.MonitorSystemUsage()
                    user_params = background_monitoring.UserParameters()
                    interval, duration = user_params.user_select_options()
                    monitor_system_usage.start_background_monitoring(interval=interval, duration=duration)
                except KeyboardInterrupt or ValueError:
                    interface_manager.starting_program()

            elif action == 5:
                monitor_appearance.MonitorAppearance().flip()
                self.show_logo_in_center()
                try:
                    monitor_system_usage = background_monitoring.MonitorSystemUsage()
                    monitor_system_usage.visualize_system_usage()
                except KeyboardInterrupt or ValueError:
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


if __name__ == "__main__":
    interface_manager = InterfaceManager()
    interface_manager.starting_program()
