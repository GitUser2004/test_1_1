import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from tutorial_interfaces.msg import FilteredSensor

class SensorAggregatorNode(Node):
    def __init__(self):
        super().__init__('node_compiler') 
        self.subscription_a = self.create_subscription(Float64, '/sensor_1', self.callback_a, 10)
        self.subscription_b = self.create_subscription(Float64, '/sensor_2', self.callback_b, 10)
        self.subscription_c = self.create_subscription(Float64, '/sensor_3', self.callback_c, 10)
        self.publisher_ = self.create_publisher(FilteredSensor, '/filtered_sensor', 10)

        self.a = None
        self.b = None
        self.c = None

    def callback_a(self, msg):
        self.a = msg.data
        self.procesar_datos()

    def callback_b(self, msg):
        self.b = msg.data
        self.procesar_datos()

    def callback_c(self, msg):
        self.c = msg.data
        self.procesar_datos()

    def procesar_datos(self):
        if self.a is not None and self.b is not None and self.c is not None:
            promedio = (self.a + self.b + self.c) / 3.0
            msg = FilteredSensor()
            msg.valor_1 = self.a
            msg.valor_2 = self.b
            msg.valor_3 = self.c
            msg.promedio_total = promedio
            self.publisher_.publish(msg)
            self.get_logger().info(
                f'Promedio: {promedio:.2f} (1={self.a:.2f}, 2={self.b:.2f}, 3={self.c:.2f})'
            )

def main(args=None):
    rclpy.init(args=args)
    node = SensorAggregatorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()