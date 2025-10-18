from setuptools import find_packages, setup

package_name = 'sensor_network'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'tutorial_interfaces'],
    zip_safe=True,
    maintainer='nath',
    maintainer_email='nath@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'sensor_1_node = sensor_network.sensor_1_node:main',
            'sensor_2_node = sensor_network.sensor_2_node:main',
            'sensor_3_node = sensor_network.sensor_3_node:main',
            'node_compiler = sensor_network.node_compiler:main',
            'node_display = sensor_network.node_display:main',
        ],
    },
)
