import os,sys
DIR= os.path.join(os.path.dirname(os.path.realpath(__file__)),'test_temp')
if not os.path.isdir(DIR):
    os.makedirs(DIR)
os.chdir(DIR)

import delay_and_cache

#os.chdir(os.path.dirname(os.path.realpath(__file__)))
exec(open(DIR+"/../delay_and_cache.py").read())
exec(open(DIR+"/../example.py").read())
exec(open(DIR+"/../test_cls.py").read())
#execfile(DIR + "/../delay_and_cache.py")
#execfile(DIR + "/../example.py")
