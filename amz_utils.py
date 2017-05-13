# -*- coding: utf-8 -*-
# @Author: Tianxiao Yang
# @Date:   2017-05-13 13:43:46
# @Last Modified by:   Tianxiao Yang
# @Last Modified time: 2017-05-13 14:29:24


import subprocess
import sys

import os
import signal
import time

DEBUG = False
START_TIME = time.time()
# print processing message
def log(line):
    global DEBUG
    global START_TIME
    if DEBUG:
        print "DEBUG: " + str(round(float(time.time() - START_TIME), 3)) + "s - " + str(line)

# print error message and exit program with errorcode 1
def elog(line):
    sys.stderr.write(line + "\n")
    sys.exit(1)

# function execute:
# description: execute a single command 
# params: 
#       cmd: command as string to be executed
# return: will return (stdout, None) if successfully executed, return (None, stderr) if not
# issue: timeout is not available to use
def execute(cmd, timeout=None):
    try:
        pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               shell=True, preexec_fn=os.setsid) 
        output, error = pro.communicate()

        if timeout is not None:
            time.sleep(timeout)
            log("kill command: \n\t{0}".format(cmd))
            os.killpg(pro.pid, signal.SIGTERM)
            return (output, error)

        if output:
            # log("successfully executed command: \n\t{0}".format(cmd))
            return (output, None)
        if error:
            log("error occurred when excuting command: \n\t{0}".format(cmd)) 
            return (None, error)
        return ("", None)

    except OSError, oserror:
        return (None, oserror)