#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import Image, Imu, LaserScan
from cv_bridge import CvBridge
import numpy as np

class SensorCollector:
    def __init__(self):
        rospy.init_node('sensor_collector', anonymous=True)
        self.bridge = CvBridge()

        # Публикаторы (для имитации, если датчики не подключены)
        self.image_pub = rospy.Publisher('/camera/image_raw', Image, queue_size=10)
        self.imu_pub = rospy.Publisher('/imu/data', Imu, queue_size=10)
        # Подписчики (для логирования)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        rospy.Subscriber('/imu/data', Imu, self.imu_callback)

        # Захват видео (если камера есть)
        self.cap = None
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Камера не найдена")
        except:
            rospy.logwarn("Камера не доступна, публикуем заглушку")
            self.cap = None

        self.rate = rospy.Rate(30)

    def scan_callback(self, msg):
        rospy.loginfo_once("Получены данные со сканера")

    def imu_callback(self, msg):
        pass  # можно логировать

    def run(self):
        while not rospy.is_shutdown():
            if self.cap is not None:
                ret, frame = self.cap.read()
                if ret:
                    img_msg = self.bridge.cv2_to_imgmsg(frame, "bgr8")
                    self.image_pub.publish(img_msg)
            else:
                # Публикация пустого изображения (заглушка)
                dummy = np.zeros((480, 640, 3), dtype=np.uint8)
                img_msg = self.bridge.cv2_to_imgmsg(dummy, "bgr8")
                self.image_pub.publish(img_msg)

            self.rate.sleep()

if __name__ == '__main__':
    try:
        collector = SensorCollector()
        collector.run()
    except rospy.ROSInterruptException:
        pass
