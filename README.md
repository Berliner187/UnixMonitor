# UnixMonitor | Zenitha
Linux/OSX simple monitor resources in terminal, as well as background tracking of resources in a file with the ability to visualize this data using matplotlib.

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
```cd UnixMonitor```

### [3] Install requirments
Install the dependencies from the file with the command: ```pip install -r requirements.txt```

Or manual: ```pip install psutil```

### [4] Start program
Run with command: ```python3 system_monitor.py```

Or make it executable: ```chmod +x system_monitor.py```
Then you can run it with the command: ```./system_monitor.py```


## Changelog [ENG]
#### Version 0.3.0
- Added an entity that implements a binary clock and display it in terminal

#### Version 0.2.3
- A little refactoring
- More comments in the methods
- Cosmetic changes

#### Version 0.2.2
- The load status of the machine has been moved to a separate method
- Added a system of transitions between program windows
- Added an art logo
- Added additional actions for the user: closing the program and restarting
- Partial refactoring of some functions

#### Version 0.2.1
- Improved the appearance of displaying resource information: the progress bar takes up more space, resource information is displayed in an improved form
- Refactoring of some functions
- Some of the individual operations are carried out in separate methods
- Unnecessary data visualization methods have been removed

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
#### Версия 0.3.1
- Добавлено больше пояснительных комментариев
- Добавлена в большинстве методов статическая типизация возвращаемых значений в методах
- Добавлена быстрая визуализация времени (по приколу)

#### Версия 0.3.0
- Добавлена сущность, которая реализует двоичные часы и отображает их в терминале

#### Версия 0.2.3
- Небольшой рефакторинг
- Больше комментариев к методам
- Косметические изменения

#### Версия 0.2.2
- Статус загруженности машины вынесен в отдельный метод
- Добавлена система переходов между окнами программы
- Добавлен арт-логотип
- Добавлены дополнительные действия для пользователя: закрытие программы и перезагрузка
- Частичный рефакторинг некоторых функций

#### Версия 0.2.1
- Улучшен внешний вид отображения информации о ресурсах: прогресс бар занимает больше места, информация о ресурсах отображается в улучшенном виде
- Рефакторинг некоторых функций
- Часть отдельных операций вынесены в отдельные методы
- Убраны лишние методы визуализации данных

#### Версия 0.2.0
- Реализован стресс-тест
- Расширена сущность стресс-теста: случайные вычисления занимают все параллельные потоки
- Частично переписан интерфейс: на старте есть выбор между запуском монитора и запуском стресс-теста
- Статус загрузки машины и наименование программы со статусом загруженности разделены в целях дальнейшего масштабирования
- Добавлена сущность InterfaceSystemMonitor, чтобы пользователь могу управлять программой

#### Версия 0.1.2
- Ускорен запуск программы
- Улучшен внешний вид индикаторов
- Оптимизиновано использование функций: текст по центру полностью центрирует метод MonitorInterface
- Добавлено кодовое имя: Zenitha (Зенита)

#### Версия 0.1.1
- Рефакторинг и переименование функций
- Оптимизированы методы

#### Версия 0.1.0
- MPV: Реализованы основные компоненты мониторинга
- Добавлены ядра процессора, оперативная память, ПЗУ для отображения
- Добавлен класс StressTest, который будет включать всевозможные нагрузки на систему (не задействован)
