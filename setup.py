#from distutils.core import setup
from setuptools import setup,find_packages
# from setuptools import setup

setup(
	name='PASDAC',
	version='0.1.dev',
	packages=find_packages(),
	include_package_data=True, 
	# use MANIFEST.in during install
	url='https://github.com/HAbitsLab/PASDAC',
	description='Time Series Classification Pipeline',
	author=['Shibo Zhang', 'Zach King', 'Rawan M Alharbi','Sal Aguinaga','Nabil Alshurafa'],
	author_email='nabil@northwestern.edu',
	maintainer='Sal Aguinaga',
	maintainer_email='salvador.aguinaga@gmail.com',
	license='MIT',
	long_description=open('README.md').read(),
    install_requires=[],

)
