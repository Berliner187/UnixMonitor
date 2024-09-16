import os
import datetime
import shutil


from constants import *


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

    def __get_time_for_topper(self):
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
            Display the name of PC in topper.
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
        print(self.__get_time_for_topper())

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
