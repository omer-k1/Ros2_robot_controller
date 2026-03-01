from setuptools import find_packages, setup

package_name = 'gazebo_turtle_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='omerk',
    maintainer_email='omerk@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "robot_controller=gazebo_turtle_controller.turtle_controller:main",
            "robot_controller1=gazebo_turtle_controller.turtle_controller1:main",
            "robot_controller2=gazebo_turtle_controller.turtle_controller2:main"
        ],
    },
)
