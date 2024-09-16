from time import sleep, localtime

from monitor_appearance import MonitorAppearance


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
        current_time = localtime()

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
            e.g. 1   9    0    2    5    8
            :param time_dec_string: str
            :return: dec_format
        """

        dec_format = ''
        for i in time_dec_string:
            dec_format += f"{'  ' + i + '  '}"

        return dec_format

    @staticmethod
    def __replace_binary_values(string: str, t_symbol='#', f_symbol='_'):
        return string.replace("1", t_symbol).replace("0", f_symbol)

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

            _monitor_appearance = MonitorAppearance()

            format_bin_numbers = self.__replace_binary_values(bin_numbers, '|', '_')
            format_bin_numbers = _monitor_appearance.text_in_center(format_bin_numbers)
            dec_format = _monitor_appearance.text_in_center(dec_format)

            MonitorAppearance.flip()

            print(format_bin_numbers)
            print(dec_format)

    def __display_binary_time(self) -> None:
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

        _monitor_appearance = MonitorAppearance()
        bin_numbers = _monitor_appearance.text_in_center(
            bin_numbers.replace("1", "#").replace("0", "_"))
        dec_format = _monitor_appearance.text_in_center(dec_format)

        print(bin_numbers)
        print(dec_format)

    def fill_clock_scheme(self):
        for number, binary in self.clock_scheme.items():
            self.clock_scheme[number] = []
        return

    def starting_binary_clock(self) -> None:
        while True:
            MonitorAppearance.flip()
            self.__display_binary_time()
            sleep(1)

    def starting_fast_iterations(self) -> None:
        while True:
            MonitorAppearance.flip()
            self.fast_iterations()
