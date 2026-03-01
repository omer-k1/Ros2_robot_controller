#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import math


class RobotControllerNode(Node):

    def __init__(self):
        super().__init__("robot_controller")

        self.target_x = 2.4
        self.target_y = 1.7
        self.distance_tolerance = 0.1
        
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0
        
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.subscriber = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        
        self.timer = self.create_timer(0.1, self.move_to_goal)

        self.scan_subscriber = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.obstacle_ahead = False
    
    def scan_callback(self, msg):
        #60 derecelik gorus acisi
        front_ranges = msg.ranges[0:30] + msg.ranges[330:360]
    
        if min(front_ranges) < 0.5:
            self.obstacle_ahead = True
        else:
            self.obstacle_ahead = False


    def euler_from_quaternion(self, x, y, z, w):
        #düzlem açısına çevirme
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        return math.atan2(t3, t4)
    
    def odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        
        ori = msg.pose.pose.orientation
        self.current_yaw = self.euler_from_quaternion(ori.x, ori.y, ori.z, ori.w)

    def move_to_goal(self):
        distance = math.sqrt((self.target_x - self.current_x)**2 + (self.target_y - self.current_y)**2)
        
        vel_msg = Twist()
        if self.obstacle_ahead:
            vel_msg.linear.x = 0.0
            vel_msg.angular.z = 0.5
            self.publisher.publish(vel_msg)
            self.get_logger().warning('Engel')
            return
        if distance >= self.distance_tolerance:
            
            angle_to_goal = math.atan2(self.target_y - self.current_y, self.target_x - self.current_x)
            
            angle_error = angle_to_goal - self.current_yaw
            
            vel_msg.angular.z = 1.0 * angle_error
            
            vel_msg.linear.x = min(0.5 * distance, 0.2)
            
            self.publisher.publish(vel_msg)
            self.get_logger().info(f'Kalan mesafe: {distance:.2f} m')
            
        else:
            vel_msg.linear.x = 0.0
            vel_msg.angular.z = 0.0
            self.publisher.publish(vel_msg)
            
            self.get_logger().info('Hedefe ulasildi')
            self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)

    node=RobotControllerNode()

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__=='__main__':
    main()



