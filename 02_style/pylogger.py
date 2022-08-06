# STYLE ***************************************************************************
# content = assignment
#
# date    = 2022-08-06
# email   = contact@alexanderrichtertd.com
#************************************************************************************

# original: logging.init.py

def findCaller(self):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    
    currentFrame = currentframe() #On some versions of IronPython, currentframe() returns None if IronPython isn't run with -X:Frames.
    
    if currentFrame is not None:
    
        frame = currentFrame.f_back
    
    rv = "(unknown file)", 0, "(unknown function)"
    
    while hasattr(frame, "f_code"):
        
        frameCode = frame.f_code
        
        filename = os.path.normcase(frameCode.co_filename)
        
        if filename == _srcfile:
        
            frame = frame.f_back
        
            continue
        
        rv = (frameCode.co_filename, frame.f_lineno, frameCode.co_name)
        
        break
    
    return rv


