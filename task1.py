#!/usr/bin/env python

# Python ver. 3.8.10

"""
1. Detect locally mounted disk (make sure it is local) with at least X MB free space, create Z files of size Y,
run Z “dd” processes which where each process will fill the selected file with Data and print time took to complete the work.
"""


import psutil
import time
import threading
import subprocess
import os

x = 200   # free space on disk in MB
y = 15    # file size in MB
z = 10    # numbers of files

# Default command to run
cmd = ['dd', 'if=/dev/zero', 'of=file.dat', 'bs=2M', 'count=1', 'status=none']


def dd_func(file_size,file_number,path):
  # Default command to run
  cmd = ['dd', 'if=/dev/zero', 'of=file.dat', 'bs=2M', 'count=1', 'status=none']
  # Update file name
  cmd[2] = 'of='+ path + 'var/tmp/file' + str(file_number) + '.dat'
  # Update file size
  cmd[3] = 'bs=' + str(file_size) + 'M'
  try:
    subprocess.run(cmd, check=True, capture_output=True)
  except subprocess.CalledProcessError as e:
    print(f"An error occured {e.stderr}")
    os._exit(e.returncode)
      

def get_free_space(partition):
    # Convert free space to MB and round
    free_space = round(psutil.disk_usage(partition).free/1024.0/1024.0)
    return free_space

if __name__ == "__main__":
  start_time = time.time()

  thread_list = []

  # Get all mounted partitions
  partitions = psutil.disk_partitions(all=False)
  # Check free space on each local device
  for p in partitions:
    if p.fstype not in ('nfs', 'smb') and get_free_space(p.mountpoint) >= x:
      print(f"Disk {p.device} has free {get_free_space(p.mountpoint)}MB")
      print(f"Creating {z} file(s) in {p.mountpoint}var/tmp folder")
      
      for i in range(z):
        thread = threading.Thread(target=dd_func, args=(y,i,p.mountpoint))
        thread_list.append(thread)
      
      for thread in thread_list:
        thread.start()
      
      for thread in thread_list:
        thread.join()
      
      break
  else:
    print("Partion with enough free space not found")
  end_time = time.time()

  print(f"Time took to complete the work {round(end_time - start_time, 5)} seconds")
