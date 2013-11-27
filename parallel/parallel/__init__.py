SUBPROCESS_FAILED_EXIT=10
import os
import subprocess
import sys
import Queue
from threading import Thread
# Simple class to represent command and stdout
#
class Command:
    def __init__(self,command,stdout=None):
        # command represented as a list for application e.g
        # 
        if(type(command) == str):
            command = command.split()
        self.command = command
        self.stdout = command

def run_subprocess(command,stdout=None):
        try:
            if(stdout is None):
                exit_code = subprocess.Popen(command)
            else:
            # find out what kind of exception to try here
                if(hasattr(stdout,'read')):

                    exit_code = subprocess.Popen(command,stdout=stdout)
                else:
                    stdout=open(stdout,'w')
                    exit_code = subprocess.Popen(command,stdout=stdout)
                    stdout.close()
        except:
            raise Exception("failed to run " +' '.join(command))
            sys.exit(SUBPROCESS_FAILED_EXIT)
        exit_code.wait()
        if(exit_code.returncode != 0):
            raise Exception(" return code != 0 for " +  ' '.join(command))

def __queue_worker__(q):
    stdout=None
    while True:
        queue_item=q.get()
        if (isinstance(queue_item,tuple)):
            cmd=queue_item[0]
            stdout=queue_item[1]
        else:
            cmd=queue_item
        try:
            run_subprocess(cmd,stdout=stdout)
        except SystemExit:
            logger.error(tool_name + " : Failed to run in thread ")
            sys.exit(SUBPROCESS_FAILED_EXIT)
    q.task_done()

    
def queue_jobs(commands,threads):
    q = Queue.Queue()
    for i in range(int(threads)):
        t = Thread(target=__queue_worker__,args=[q])
        t.daemon = True
        t.start()
    for item in (commands):
        t.put(item.command,item.stdout)
    q.join()

