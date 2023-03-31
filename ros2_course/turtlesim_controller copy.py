import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose



class TurtlesimController(Node):

    def __init__(self):
        super().__init__('turtlesim_controller')
        self.pose = None
        self.subscription = self.create_subscription(
            Pose,
            #'/turtle1/pose',
            '/turtlesim1/turtle1/pose',
            self.cb_pose,
            10,
            )
        self.twist_pub = self.create_publisher(Twist, '/turtlesim1/turtle1/cmd_vel', 10)
        
    def go_straight(self, speed, distance):
        vel_msg = Twist()
        if distance > 0:
            vel_msg.linear.x = speed
        else:
            vel_msg.linear.x = -speed
        vel_msg.linear.y = 0.0
        vel_msg.linear.z = 0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0
        vel_msg.angular.z = 0.0

        # Set loop rate
        loop_rate = self.create_rate(100, self.get_clock()) # Hz

        # Calculate time
        T = speed/distance

        # Publish first msg and note time when to stop
        self.twist_pub.publish(vel_msg)
        # self.get_logger().info('Turtle started.')
        when = self.get_clock().now() + rclpy.time.Duration(seconds=T)

        # Publish msg while the calculated time is up
        while (self.get_clock().now() < when) and rclpy.ok():
            self.twist_pub.publish(vel_msg)
            # self.get_logger().info('On its way...')
            rclpy.spin_once(self)   # loop rate

        # turtle arrived, set velocity to 0
        vel_msg.linear.x = 0.0
        self.twist_pub.publish(vel_msg)
        # self.get_logger().info('Arrived to destination.')

    def turn(self, omega, angle):
        # Implement rotation here

        T = angle / omega

        omega = omega*2*math.pi/360
        angle = angle*2*math.pi/360

        vel_msg = Twist()
        vel_msg.linear.x = 0.0
        vel_msg.linear.y = 0.0
        vel_msg.linear.z = 0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0
        vel_msg.angular.z = omega

        # Set loop rate
        loop_rate = self.create_rate(100, self.get_clock()) # Hz

        # Publish first msg and note time when to stop
        self.twist_pub.publish(vel_msg)
        # self.get_logger().info('Turtle started.')
        when = self.get_clock().now() + rclpy.time.Duration(seconds=T)

        # Publish msg while the calculated time is up
        while (self.get_clock().now() < when) and rclpy.ok():
            self.twist_pub.publish(vel_msg)
            # self.get_logger().info('On its way...')
            rclpy.spin_once(self)   # loop rate

        # turtle arrived, set velocity to 0
        vel_msg.angular.z = 0.0
        self.twist_pub.publish(vel_msg)
        # self.get_logger().info('Arrived to destination.')
    
    def draw_square(self, speed, omega, a):
        for i in range(4):
            self.turn(omega,90.0)
            self.go_straight(speed,a)

    def draw_poly(self, speed, omega, N, a):
        angle = 360 / N
        
        for i in range(N):
            self.turn(omega,angle)
            self.go_straight(speed,a)
        self.turn(omega,angle)

    def cb_pose(self, msg):
        self.pose = msg  
    
    def go_to(self, speed, omega, x, y):
        # Wait for position to be received
        loop_rate = self.create_rate(100, self.get_clock()) # Hz
        while self.pose is None and rclpy.ok():
            self.get_logger().info('Waiting for pose...')
            rclpy.spin_once(self)


def main(args=None):
    rclpy.init(args=args)
    tc = TurtlesimController()
    
    #tc.go_to(1.0, 20.0, 2, 8)
    #tc.go_to(1.0, 20.0, 2, 2)
    #tc.go_to(1.0, 20.0, 3, 4)
    #tc.go_to(1.0, 20.0, 6, 2)
    
    tc.draw_poly(1.0,30.0,5,1.0)
    # tc.draw_square(1.0,30.0,2)
    
    #tc.turn(30.0,90.0)
    #tc.go_straight(2.0,1.0)
    #tc.turn(30.0,90.0)
    #tc.go_straight(2.0,1.0)
    #tc.turn(30.0,90.0)
    #tc.go_straight(2.0,1.0)
    #tc.turn(30.0,90.0)
    #tc.go_straight(2.0,1.0)
    #tc.turn(30.0,90.0)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    tc.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
