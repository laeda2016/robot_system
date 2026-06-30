# Система управления роботом на ROS Noetic

## Описание проекта
Данный проект представляет собой систему сбора и обработки данных с нескольких датчиков робота. 
Разработан в рамках курса «Linux для робототехников». Система построена на базе **ROS Noetic** и **Docker**, 
включает симуляцию датчиков (лидар, камера, IMU) и демонстрирует работу ROS-узлов, публикацию топиков, 
визуализацию в RViz и запись данных в bag-файлы.

Проект включает:
- 3+ датчика (камера, лидар, IMU)
- Поддержку драйвера из исходников (`rplidar_ros`)
- Docker-контейнеризацию с поддержкой GUI (RViz)
- Автоматизацию через bash-скрипты
- Готовую инструкцию по установке и запуску

---

## Архитектура системы

### Структура проекта

robot_system/
├── docker/
│ ├── Dockerfile # Основной образ ROS
│ └── docker-compose.yml # Оркестрация контейнеров
├── src/
│ ├── sensor_collector/ # узел-сборщик данных
│ ├── dummy_sensors/ # Симуляторы датчиков
│ ├── rplidar_ros/ # Драйвер лидара
│ └── imu_bno055/ # Драйвер IMU 
├── scripts/
│ ├── setup.sh # Установка зависимостей
│ ├── build.sh # Сборка Docker-образов
│ └── run.sh # Запуск контейнеров
├── config/ # Конфигурационные файлы 
├── screenshots/ # Скриншоты для демонстрации
├── docker-compose.yml # Основной файл композa
└── README.md



### Взаимодействие компонентов
Система состоит из двух Docker-контейнеров, объединённых в сеть `rosnet`:

1. **Контейнер `ros-master`**  
   - Запускает `roscore` – центральный узел ROS.
   - Служит для обнаружения всех узлов и обмена сообщениями.

2. **Контейнер `robot`**  
   - Содержит рабочую область `catkin_ws` со всеми пакетами.
   - После сборки в нём запускаются узлы:
     - **`dummy_lidar.py`** – публикует симулированные данные лидара в топик `/scan`.
     - **`sensor_collector.py`** – публикует заглушку изображения в топик `/camera/image_raw` и подписывается на `/scan` для логирования.
   - Также присутствуют собранные драйверы реальных датчиков: `rplidar_ros` (лидар) и `imu_bno055` (IMU), но в демонстрационной версии используются симуляторы для надёжности.

**Топики ROS:**
- `/scan` – данные лидара (тип `sensor_msgs/LaserScan`).
- `/camera/image_raw` – изображение с камеры (тип `sensor_msgs/Image`).
- `/imu/data` – данные IMU (тип `sensor_msgs/Imu`) – публикуется симулятором IMU (опционально).

Связь между контейнерами осуществляется через переменную `ROS_MASTER_URI=http://ros-master:11311`.

---

## Список датчиков (3–5)

| Датчик | Топик | ROS-пакет | Источник |
|--------|-------|-----------|----------|
| USB-камера | `/camera/image_raw` | `usb_cam` | Установлен через `apt` внутри Docker-образа |
| Лидар RPLIDAR | `/scan` | `rplidar_ros` | **Собран из исходников** (клон с GitHub) |
| IMU BNO055 | `/imu/data` | `imu_bno055` | **Собран из исходников** (клон с GitHub) |
| Симулятор лидара | `/scan` | `dummy_sensors` | Создан внутри Dockerfile (исходный код) |
| (дополнительно) GPS | – | `nmea_navsat_driver` | Установлен через `apt` (не используется в демо) |

**Выполнено требование:** минимум один пакет собран из исходников (`rplidar_ros` и `imu_bno055`).

---

## Инструкция по установке и запуску

### Требования к хосту
- Ubuntu 20.04 (или другая ОС с поддержкой Docker)
- Установленные Docker и Docker Compose
- (Опционально) для работы GUI – настроенный X-сервер и проброс дисплея

### 1. Клонирование репозитория
```bash
git clone https://github.com/laeda2016/robot_system.git
cd robot_system

2. Настройка окружения.

# Установка ROS и Docker (можно пропустить, если уже установлены)
./scripts/setup.sh

Примечание: скрипт выполняет установку ROS Noetic, Docker и необходимых пакетов.

3. Сборка Docker-образа.

./scripts/build.sh 

Или

docker-compose -f docker/docker-compose.yml build

4. Запуск контейнеров.

./scripts/run.sh

Или

docker-compose -f docker/docker-compose.yml up -d

5. Вход в контейнер robot.

docker exec -it robot_container bash

6. Запуск ROS-узлов (внутри контейнера).

source /root/catkin_ws/devel/setup.bash
rosrun dummy_sensors dummy_lidar.py &
rosrun sensor_collector collector.py &

7. Проверка работы.

rostopic list


Ожидаемый вывод: /camera/image_raw, /imu/data, /rosout, /rosout_agg, /scan

Данные лидара:

rostopic echo /scan -n 1

Данные камеры:

rostopic echo /camera/image_raw -n 1

8. Визуализация в RViz

В отдельном терминале:

docker exec -it robot_container bash
source /root/catkin_ws/devel/setup.bash
rviz


9. Запись данных в bag-файл

Внутри контейнера:

rosbag record -O /root/sensor_data.bag /scan /camera/image_raw /imu/data

(Нажмите Ctrl+C через 10–15 секунд)

Скопируйте bag-файл на хост:

docker cp robot_container:/root/sensor_data.bag ~/robot_system/

Скриншоты и демонстрация

Все скриншоты находятся в папке screenshots/ репозитория.
Примеры:

    docker_ps.png – работающие контейнеры

    rostopic_list.png – список топиков

    rostopic_echo_scan.png – данные лидара

    rviz_laser.png – визуализация в RViz
    
    rosbag_record.png – запись bag-файла

Результаты:

    Система успешно собирается в Docker.

    Все узлы запускаются и публикуют данные.

    Топики доступны для подписки.

    RViz работает через проброс X11.

    Данные записаны в bag-файл для дальнейшего анализа.


Используемые технологии:

    ROS Noetic

    Python 3

    Docker / Docker Compose

    OpenCV

    Git


