#!/usr/bin/env python
#from setuptools import setup
from distutils.core import setup
#import setuptools
import os,glob,sys

DIR= os.path.dirname(__file__)
if DIR:
	os.chdir(DIR)


print (required)
setup(
	name='delay_and_cache',
	version='0.1',
	packages=[
'.'
#        'delay_and_cache',
             ],
    include_package_data=True,    
	license='MIT',
	author='Feng Geng',
	author_email='shouldsee.gem@gmail.com',
	long_description=open('README.md').read(),
	install_requires=[
		x.strip() for x in open("requirements.txt","r") 
        	if x.strip() and not x.strip().startswith("#") 
	],

)


