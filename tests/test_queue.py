from parallel import *


command=['echo','blah']

queue_jobs([Command(command)],2)
