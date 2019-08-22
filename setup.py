#!/usr/bin/env python
#from setuptools import setup
from distutils.core import setup
#import setuptools
import os,glob,sys

DIR= os.path.dirname(__file__)
if DIR:
	os.chdir(DIR)

FILE =  'requirements.txt'
required = [ x.strip() for x in open( FILE,'r')  if not x.strip().startswith('#') ] 
required = [ x.strip() for x in required if x.find(' @ ')==-1 and x ] 
required = [ x.strip() for x in required if x.find('git+')==-1 and x ] 


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
	install_requires = required,
    
#   entry_points = {
#           'console_scripts': [
#               'command-name = pymisca.directory_hashmirror_0520:main',                  
#           ],              
#       },
#     scripts = glob.glob('bin/*.py') ,
#     package_data={'pymisca': ['*.sh','*.json','*.csv','*.tsv','*.npy','*.pk',
#                               'templates/*.html',
# #                              'resources/*','genomeConfigs/*',
#                              ],
# #                  'runtime_data':['wraptool/*.{ext}'.format(**locals()) 
# #                                  for ext in 
# #                                  ['json','csv','tsv','npy','pk']],
#                  },
)


