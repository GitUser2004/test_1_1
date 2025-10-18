import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import random

class Sensor1Node(Node):
    def __init__(self):
        super().__init__('sensor_1_node')  # NODOO
        self.publisher_ = self.create_publisher(Float64, '/sensor_1', 10)  # Tópico 
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.valor = 1.0

    def timer_callback(self):
        msg = Float64()
        msg.data = random.uniform(0.0, 10.0)  # Rango 
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sensor 1 publicó: {msg.data}')
        self.valor += 0.5 

def main(args=None):
    rclpy.init(args=args)
    node = Sensor1Node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()