import subprocess
import time
proc=subprocess.Popen('tar -c coke.jpg | ssh ubuntu@40.122.47.160 "tar -x -C tf_files/"', shell=True, stdout=subprocess.PIPE, )
proc.communicate()
time.sleep(3)
proc=subprocess.Popen('ssh ubuntu@40.122.47.160 "cat tf_files/log.txt"', shell=True, stdout=subprocess.PIPE, )
response=proc.communicate()[0]
print response