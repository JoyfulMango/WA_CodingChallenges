import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

class MergeArraysNode(Node):
    def __init__(self):
        super().__init__('merge_arrays_node')
        self.subscription1 = self.create_subscription(
            Int32MultiArray,
            '/input/array1',
            self.array1_callback,
            10)
        self.subscription2 = self.create_subscription(
            Int32MultiArray,
            '/input/array2',
            self.array2_callback,
            10)
        self.publisher = self.create_publisher(Int32MultiArray, '/output/array', 10)
        self.array1 = []
        self.array2 = []

    def array1_callback(self, msg):
        self.array1 = msg.data
        self.try_merge_and_publish()

    def array2_callback(self, msg):
        self.array2 = msg.data
        self.try_merge_and_publish()

    def try_merge_and_publish(self):
        if self.array1 and self.array2:
            merged_array = sorted(self.array1 + self.array2)
            msg = Int32MultiArray()
            msg.data = merged_array
            self.publisher.publish(msg)
            self.get_logger().info(f'Published merged array: {merged_array}')

def main(args=None):
    rclpy.init(args=args)
    merge_arrays_node = MergeArraysNode()
    rclpy.spin(merge_arrays_node)
    merge_arrays_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()