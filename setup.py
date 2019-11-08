from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


# class PostDevelopCommand(develop):
#     """Post-installation for development mode."""
#     def run(self):
#         # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
#         develop.run(self)
#
# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#     def run(self):
#         # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
#         install.run(self)
setup(
    name='traffic_conditioner',
    version='1.0',
    packages=['tc', 'test'],
    url='192.168.88.102:5000',
    license='',
    author='andi',
    author_email='hw@rebelalliance.it',
    description='Traffic Conditioner application', install_requires=['ifaddr']
    # cmdclass={
    #         'develop': PostDevelopCommand,
    #         'install': PostInstallCommand,
    #     },
)
