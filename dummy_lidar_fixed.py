#!/usr/bin/env python3
import rospy
import math
from sensor_msgs.msg import LaserScan

rospy.init_node("dummy_lidar")
pub = rospy.Publisher("/scan", LaserScan, queue_size=10)
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    msg = LaserScan()
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = "laser"
    msg.angle_min = -math.pi
    msg.angle_max = math.pi
    msg.angle_increment = math.pi / 180.0
    msg.range_min = 0.1
    msg.range_max = 10.0
    msg.ranges = [1.0] * 360
    pub.publish(msg)
    rate.sleep()
