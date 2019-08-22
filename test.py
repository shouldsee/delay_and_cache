import os,sys
DIR= os.path.join(os.path.dirname(os.path.realpath(__file__)),'test_temp')
os.makedirs(DIR)
os.chdir(DIR)

#os.chdir(os.path.dirname(os.path.realpath(__file__)))
execfile("delay_and_cache.py")
