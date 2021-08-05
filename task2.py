#!/usr/bin/env python

# Python ver. 3.8.10

"""
2. Run user-selected command on many servers (user-provided as param) with ssh in parallel,
collect output from all nodes. The script should print collected output from all nodes on stdout,
w/o using temp files.
"""


import ipaddress
import subprocess
import sys
import threading


def remote_run(host,command):
  # Default command to run
  cmd = ['ssh', '0.0.0.0', 'some command']
  # Set IP address
  cmd[1] = host
  # Set command to run
  cmd[2] = command
  try:
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
  except subprocess.CalledProcessError as e:
    print(f"An error occured {e.stderr}")


if __name__ == "__main__":

  if len(sys.argv) == 1:
    print("Please provide IP blank-separated list to run command remotely")
    exit

  # Validate IP addresses and remove not valid from list
  ip_list = sys.argv[1:]
  for ip in ip_list:
    try:
      ipaddress.ip_address(ip)
    except:
      if ValueError:
        ip_list.remove(ip)

  thread_list = []

  for ip in ip_list:
    thread = threading.Thread(target=remote_run, args=(ip, 'cat /var/log/syslog'))
    thread_list.append(thread)
  
  for thread in thread_list:
    thread.start()
  
  for thread in thread_list:
    thread.join()
