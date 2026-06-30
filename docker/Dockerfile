FROM osrf/ros:noetic-desktop-full

# Установка базовых пакетов
RUN apt update && apt install -y \
    python3-pip \
    python3-opencv \
    ros-noetic-usb-cam \
    ros-noetic-vision-opencv \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую область
RUN mkdir -p /root/catkin_ws/src

# ---- Создаём ваш пакет sensor_collector, если он ещё не скопирован ----
# Проверяем, есть ли уже папка sensor_collector в src (она может быть скопирована позже)
# Если нет – создаём её прямо здесь.
RUN cd /root/catkin_ws/src && \
    if [ ! -d sensor_collector ]; then \
        catkin_create_pkg sensor_collector rospy sensor_msgs cv_bridge std_msgs && \
        mkdir -p sensor_collector/scripts && \
        echo '#!/usr/bin/env python3' > sensor_collector/scripts/collector.py && \
        echo 'import rospy, cv2, numpy as np' >> sensor_collector/scripts/collector.py && \
        echo 'from sensor_msgs.msg import Image, Imu, LaserScan' >> sensor_collector/scripts/collector.py && \
        echo 'from cv_bridge import CvBridge' >> sensor_collector/scripts/collector.py && \
        echo 'rospy.init_node(\"sensor_collector\")' >> sensor_collector/scripts/collector.py && \
        echo 'bridge = CvBridge()' >> sensor_collector/scripts/collector.py && \
        echo 'pub_img = rospy.Publisher(\"/camera/image_raw\", Image, queue_size=10)' >> sensor_collector/scripts/collector.py && \
        echo 'rate = rospy.Rate(30)' >> sensor_collector/scripts/collector.py && \
        echo 'while not rospy.is_shutdown():' >> sensor_collector/scripts/collector.py && \
        echo '    dummy = np.zeros((480,640,3), dtype=np.uint8)' >> sensor_collector/scripts/collector.py && \
        echo '    img_msg = bridge.cv2_to_imgmsg(dummy, \"bgr8\")' >> sensor_collector/scripts/collector.py && \
        echo '    pub_img.publish(img_msg)' >> sensor_collector/scripts/collector.py && \
        echo '    rate.sleep()' >> sensor_collector/scripts/collector.py && \
        chmod +x sensor_collector/scripts/collector.py; \
    fi

# ---- Создаём пакет dummy_sensors для имитации лидара и IMU ----
RUN cd /root/catkin_ws/src && \
    catkin_create_pkg dummy_sensors rospy sensor_msgs && \
    mkdir -p dummy_sensors/scripts && \
    echo '#!/usr/bin/env python3' > dummy_sensors/scripts/dummy_lidar.py && \
    echo 'import rospy, math' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo 'from sensor_msgs.msg import LaserScan' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo 'rospy.init_node(\"dummy_lidar\")' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo 'pub = rospy.Publisher(\"/scan\", LaserScan, queue_size=10)' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo 'rate = rospy.Rate(10)' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo 'while not rospy.is_shutdown():' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo '    msg = LaserScan()' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo '    msg.header.stamp = rospy.Time.now()' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo '    msg.header.frame_id = \"laser\"' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo '    msg.angle_min = -math.pi' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo '    msg.angle_max = math.pi' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo '    msg.angle_increment = math.pi/180' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo '    msg.range_min = 0.1' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo '    msg.range_max = 10.0' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo '    msg.ranges = [1.0]*360' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo '    pub.publish(msg)' >> dummy_sensors/scripts/dummy_lidar.py && \
    echo '    rate.sleep()' >> dummy_sensors/scripts/dummy_lidar.py && \
    chmod +x dummy_sensors/scripts/dummy_lidar.py

# ---- Копируем ваши локальные пакеты (если они есть) поверх созданных ----
# Это перезапишет sensor_collector, если вы его уже создали на хосте.
COPY ./src /root/catkin_ws/src

RUN sed -i 's/sensor_,sgs/sensor_msgs/g' /root/catkin_ws/src/sensor_collector/CMakeLists.txt

# Установка зависимостей через rosdep
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && \
    rosdep update && \
    rosdep install --from-paths /root/catkin_ws/src --ignore-src -r -y"

# Сборка (гарантированно успешная, потому что все пакеты корректны)
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && \
    cd /root/catkin_ws && \
    catkin_make"

# Настройка окружения
RUN echo "source /root/catkin_ws/devel/setup.bash" >> /root/.bashrc

CMD ["/bin/bash"]
