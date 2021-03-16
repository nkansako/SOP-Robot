from setuptools import setup

package_name = 'head_tilt'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vagrant',
    maintainer_email='vagrant@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = head_tilt.head_tilt_data_publisher:main',
            'listener = head_tilt.head_tilt_action_client:main',
        ],
    },
)
