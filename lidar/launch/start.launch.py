from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='sc_mini',
            executable='sc_mini',
            name='sc_mini',
            output='screen',
            parameters=[
                {'frame_id': 'laser_link'},
                {'port': '/dev/sc_mini'},
                {'baud_rate': 115200}
            ]
        )
    ])
