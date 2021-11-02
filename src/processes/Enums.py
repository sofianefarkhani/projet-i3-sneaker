

from enum import Enum

class TaskType(Enum):
    """A TaskType caracterizes a Task sent to a BlackBox. It allows it to know how to behave."""
    PROCESS = 0
    END     = 1
     

class AnswerType(Enum):
    """An AnswerType caracterizes an Answer sent by a BlackBox. It informs the main about what happened."""
    BOXENDSERVICE = 1 # sent by the BlackBox to the main when its service ends, after recieving a Task typed: END.

class LoaderTaskType(Enum):
    """A LoaderTaskType caracterizes a Task sent to the Loader. It allows it to know how to behave."""
    LOAD      = 0 # signal for the loader to load more images.
    TERMINATE = 1 # signal that the loader should exit its run method.
    
class LoaderAnswerType(Enum):
    """A LoaderAnswerType caracterizes an Answer sent by the Loader. It informs the main about what happened."""
    LOADDONE = 0 # sent when the loader ends a LOAD task 
    NOMORE   = 1 # sent when the loader reaches the end of the db.
    END      = 2 # sent when the loader exits its run method.  
    
