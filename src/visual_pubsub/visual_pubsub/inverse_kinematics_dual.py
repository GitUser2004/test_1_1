#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point
import numpy as np

class InverseKinematicsDual(Node):
    def __init__(self):
        super().__init__('inverse_kinematics_dual')

        # --- Robot A ---
        self.qA = np.array([0.0, 0.0, 0.0], dtype=float)
        self.targetA = np.array([1.2, 0.5, 0.0])
        self.lA = [2.0, 1.5, 0.8]
        self.pubA = self.create_publisher(JointState, 'robotA/joint_states', 10)
        self.subA = self.create_subscription(Point, 'robotA/target_position', self.cb_targetA, 10)

        # --- Robot B ---
        self.qB = np.array([0.0, 0.0, 0.0], dtype=float)
        self.targetB = np.array([-0.5, -2.0, -0.5])
        self.lB = [0.5, 1.3, 0.9]
        self.pubB = self.create_publisher(JointState, 'robotB/joint_states', 10)
        self.subB = self.create_subscription(Point, 'robotB/target_position', self.cb_targetB, 10)

        # --- Parámetros comunes ---
        self.step_size = 0.05
        self.max_iterations = 100
        self.tolerance = 0.01
        self.damping = 0.1

        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info("Inverse Kinematics Dual Node started.")

    # ====================== FUNCIONES COMUNES ======================
    def forward_kinematics_A(self, q):
        """Modelo tipo plano (como el primer código)"""
        l1, l2, l3 = self.lA
        q1, q2, q3 = q
        x = - l1 * np.cos(q1) - l2 * np.cos(q1+q2) - l3 * np.cos(q1+q2+q3)
        y = - l1 * np.sin(q1) - l2 * np.sin(q1+q2) - l3 * np.sin(q1+q2+q3)
        z = 0.0
        return np.array([x, y, z])

    def jacobian_A(self, q):
        """Jacobiano para robot A (plano)"""
        l1, l2, l3 = self.lA
        q1, q2, q3 = q

        j11 = l1*np.sin(q1) + l2*np.sin(q1 + q2) + l3*np.sin(q1 + q2 + q3)
        j12 = l2*np.sin(q1 + q2) + l3*np.sin(q1 + q2 + q3)
        j13 = l3*np.sin(q1 + q2 + q3)

        j21 = -l1*np.cos(q1) - l2*np.cos(q1 + q2) - l3*np.cos(q1 + q2 + q3)
        j22 = -l2*np.cos(q1 + q2) - l3*np.cos(q1 + q2 + q3)
        j23 = -l3*np.cos(q1 + q2 + q3)

        return np.array([[j11, j12, j13], [j21, j22, j23], [0, 0, 0]])

    def forward_kinematics_B(self, q):
        """Modelo espacial (como el segundo código)"""
        l1, l2, l3 = self.lB
        q1, q2, q3 = q
        x = - (l2 * np.cos(q2) + l3 * np.cos(q2+q3)) * np.cos(q1)
        y = - (l2 * np.cos(q2) + l3 * np.cos(q2+q3)) * np.sin(q1)
        z = - l2 * np.sin(q2) - l3 * np.sin(q2+q3) + l1
        return np.array([x, y, z])

    def jacobian_B(self, q):
        """Jacobiano para robot B (espacial)"""
        l2, l3 = self.lB[1], self.lB[2]
        q1, q2, q3 = q

        j11 = -(-l2*np.cos(q2) - l3*np.cos(q2 + q3)) * np.sin(q1)
        j12 = (l2*np.sin(q2) + l3*np.sin(q2 + q3)) * np.cos(q1)
        j13 = l3*np.sin(q2 + q3) * np.cos(q1)

        j21 = (-l2*np.cos(q2) - l3*np.cos(q2 + q3)) * np.cos(q1)
        j22 = (l2*np.sin(q2) + l3*np.sin(q2 + q3)) * np.sin(q1)
        j23 = l3*np.sin(q1) * np.sin(q2 + q3)

        j31 = 0.0
        j32 = -l2*np.cos(q2) - l3*np.cos(q2 + q3)
        j33 = -l3*np.cos(q2 + q3)

        return np.array([[j11, j12, j13], [j21, j22, j23], [j31, j32, j33]])

    # ====================== ACTUALIZACIÓN ======================
    def update_ik(self, q, target, fwd_fn, jac_fn):
        current = fwd_fn(q)
        error = target - current
        if np.linalg.norm(error) < self.tolerance:
            return q

        J = jac_fn(q)
        JtJ = J.T @ J
        damping = self.damping * np.eye(3)
        dq = np.linalg.solve(JtJ + damping, J.T) @ error
        q += dq * self.step_size
        return q

    # ====================== CALLBACKS ======================
    def cb_targetA(self, msg):
        self.targetA = np.array([msg.x, msg.y, msg.z])
        self.get_logger().info(f"New target A: {self.targetA}")

    def cb_targetB(self, msg):
        self.targetB = np.array([msg.x, msg.y, msg.z])
        self.get_logger().info(f"New target B: {self.targetB}")

    def timer_callback(self):
        # Actualizar robot A
        self.qA = self.update_ik(self.qA, self.targetA, self.forward_kinematics_A, self.jacobian_A)
        # Actualizar robot B
        self.qB = self.update_ik(self.qB, self.targetB, self.forward_kinematics_B, self.jacobian_B)

        # Publicar ambos estados
        self.publish_joints(self.pubA, ['A_q1', 'A_q2', 'A_q3'], self.qA)
        self.publish_joints(self.pubB, ['B_q1', 'B_q2', 'B_q3'], self.qB)

    def publish_joints(self, publisher, names, q):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = names
        msg.position = q.tolist()
        publisher.publish(msg)

# ====================== MAIN ======================
def main(args=None):
    rclpy.init(args=args)
    node = InverseKinematicsDual()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
