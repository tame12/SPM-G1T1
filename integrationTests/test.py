import sys
  
# append the path of the
# parent directory
sys.path.append("..")
  
# import method from sibling 
# module
from backend import hello
  
# call method
hello()