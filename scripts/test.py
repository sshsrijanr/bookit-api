import os
import django
import sys
'''
Run this script from the project dir using 
--> python scripts/test.py 

add all the required model structure from func you want to test independent from everything else here.
'''
PROJECT_ROOT_DIR = os.path.abspath("")
sys.path.insert(0, PROJECT_ROOT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()