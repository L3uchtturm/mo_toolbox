from setuptools import setup

setup(
    name='mo_toolbox',
    version='0.1.0',
    packages=['tools'],
    install_requires=['shapely>=2.0.6', 'geopandas>=1.0.1', 'pandas>=2.2.2', 'ttkwidgets>=0.13.0'],
    url='http://10.195.64.254:81/mombrei/mo_toolbox.git',
    author='Axel Mombrei',
    author_email='axel.mombrei@dlr.rlp.de',
    description='Private Toolsammlung'
)

