# UnixMonitor | Zenitha
Simple monitor resources in terminal

## Features
- Dynamic real-time monitoring
- Visual notification of system load (emoji status), which reflects the current load on the cores

## How use
### [1] What do you need
- UNIX-like system: (Linux distribution, Mac OS)
Tested on:
    - Mac OS 14.1 (The temperature indicator is not working)
    - Linux Mint 21.1 (The temperature indicator is working)
- Python 3.9+
Tested on Python 3.11.6

### [2] Installation
Clone repository:
```https://github.com/Berliner187/UnixMonitor.git```

Change direcotry:
```cd UnixMonitor.git```

### [3] Install requirments
Install the dependencies from the file with the command: ```pip install -r requirements.txt```

Or manual: ```pip install psutil```

### [4] Start program
Run with command: ```python3 system_monitor.py```

Or make it executable: ```chmod +x system_monitor.py```
Then you can run it with the command: ```./system_monitor.py```


## Changelog [ENG]
#### Version 0.2.0
- Stress test implemented
- The essence of the stress test has been expanded: random calculations occupy all parallel threads
- The interface has been partially rewritten: at the start, there is a choice between starting the monitor and starting the stress test
- The loading status of the machine and the name of the program with the loading status are separated for further scaling
- The InterfaceSystemMonitor entity has been added so that the user can control the program

#### Version 0.1.2
- Accelerated program launch
- Improved the appearance of the indicators
- Optimized the use of functions: the text in the center completely centers the Monitor Interface method
- Added a code name: Zenitha

#### Version 0.1.1
- Refactoring and renaming functions
- Optimize methods

#### Version 0.1.0
- MPV: The main components of monitoring are implemented
- Added CPU cores, RAM, ROM for display
- Added class StressTest, which will include all kinds of loads on the system (not involved)


## Changelog [RUS]
#### Version 0.2.0
- Реализован стресс-тест
- Расширена сущность стресс-теста: случайные вычисления занимают все параллельные потоки
- Частично переписан интерфейс: на старте есть выбор между запуском монитора и запуском стресс-теста
- Статус загрузки машины и наименование программы со статусом загруженности разделены в целях дальнейшего масштабирования
- Добавлена сущность InterfaceSystemMonitor, чтобы пользователь могу управлять программой

#### Version 0.1.2
- Ускорен запуск программы
- Улучшен внешний вид индикаторов
- Оптимизиновано использование функций: текст по центру полностью центрирует метод MonitorInterface
- Добавлено кодовое имя: Zenitha (Зенита)

#### Version 0.1.1
- Рефакторинг и переименование функций
- Оптимизированы методы

#### Version 0.1.0
- MPV: Реализованы основные компоненты мониторинга
- Добавлены ядра процессора, оперативная память, ПЗУ для отображения
- Добавлен класс StressTest, который будет включать всевозможные нагрузки на систему (не задействован)
