import time
import datetime
from random import randint
from multiprocessing import Process

import psutil


class StressTests:
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
    def multiprocess_test():
        cpu_count = psutil.cpu_percent(interval=None, percpu=True)
        processes = []
        for i in range(len(cpu_count)):
            p = Process(target=StressTests.random_operations)
            processes.append(p)
            p.start()

        for p in processes:
            p.join()