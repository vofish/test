#!/usr/bin/env python

# Python ver. 3.8.10

"""
2. Run user-selected command on many servers (user-provided as param) with ssh in parallel,
collect output from all nodes. The script should print collected output from all nodes on stdout,
w/o using temp files.
"""


import subprocess
import sys
import threading
from argparse import ArgumentParser


def remote_run(host,command):
  # Default command to run
  cmd = ['ssh', '-o ConnectTimeout=2', '0.0.0.0', 'some command']
  # Set IP address
  cmd[2] = host
  # Set command to run
  cmd[3] = command
  try:
    result = subprocess.run(cmd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(f"Output from {host}\n", result.stdout)
  except subprocess.SubprocessError as e:
    print(e.stderr)

if __name__ == "__main__":

  parser = ArgumentParser()
  parser.add_argument("-c", dest='Command', type = str,
                      help="command to run on remote servers, if there is a blank in it use quotes")
  parser.add_argument("-s", dest='Servers',
                      help="IP address of server, blank-separated if many", nargs='+')

  args = parser.parse_args()
  
  if len(sys.argv) <= 3:
    parser.print_help(sys.stderr)
    sys.exit(1)
    
  serv_list = args.Servers
  
  thread_list = []

  for ip in serv_list:
    thread = threading.Thread(target=remote_run, args=(ip, str(args.Command)))
    thread_list.append(thread)
  
  for thread in thread_list:
    thread.start()
  
  for thread in thread_list:
    thread.join()
