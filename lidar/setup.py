from setuptools import find_packages, setup
import os, glob

package_name = 'lidar'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),        
        # Include your RViz configuration file
        (os.path.join('share', package_name, 'launch'),( glob.glob(os.path.join('launch', '*launch.py')))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='skh',
    maintainer_email='tls3162@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [            
            'sc_mini = lidar.sc_mini:main',
        ],
    },
)
