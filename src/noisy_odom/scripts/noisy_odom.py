#! /usr/bin/env python

import random
import rospy
from nav_msgs.msg import Odometry


class NoisyOdom():
    def __init__(self):
        self.odom_subscriber = rospy.Subscriber(
            '/odom', Odometry, self.odom_callback)
        self.odom_publisher = rospy.Publisher(
            '/noisy_odom', Odometry, queue_size=1)
        self.odom_msg = Odometry()
        self.ctrl_c = False
        rospy.on_shutdown(self.shutdownhook)
        self.rate = rospy.Rate(5)

    def shutdownhook(self):
        self.ctrl_c = True

    def odom_callback(self, msg):
        self.odom_msg = msg
        self.add_noise()

    def add_noise(self):
        # add random noise to the y position of the odometry messsage
        rand_float = random.uniform(-0.5, 0.5)
        self.odom_msg.pose.pose.position.y = self.odom_msg.pose.pose.position.y + rand_float

    def publish_noisy_odom(self):
        while not rospy.is_shutdown():
            self.odom_publisher.publish(self.odom_msg)
            self.rate.sleep()


if __name__ == '__main__':
    rospy.init_node('noisy_odom_node', anonymous=True)
    noisyodom_object = NoisyOdom()

    try:
        noisyodom_object.publish_noisy_odom()
    except rospy.ROSInterruptException:
        pass
