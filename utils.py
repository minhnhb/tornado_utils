import sys
import os.path

##################################################
# Get execution path
################################################################################

def execution_path(filename):
    """Get execution path of the current running code
    by Stephen McDonald http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/496889"""
    return os.path.join(os.path.dirname(sys._getframe(1).f_code.co_filename), filename)
