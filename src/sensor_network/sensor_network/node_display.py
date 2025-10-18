import rclpy
from rclpy.node import Node
from tutorial_interfaces.msg import FilteredSensor

class SensorDisplayNode(Node):
    def __init__(self):
        super().__init__('node_display')  
        self.sub = self.create_subscription(
            FilteredSensor,
            '/filtered_sensor',
            self.callback,
            10
        )

    def callback(self, msg):
        self.get_logger().info(
            f'Resultado recibido → Promedio: {msg.promedio_total:.2f}, '
            f'1={msg.valor_1:.2f}, 2={msg.valor_2:.2f}, 3={msg.valor_3:.2f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = SensorDisplayNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()