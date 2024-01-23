import os
import psutil

def get_status(process_id):

  try:
      # Wait for the child process to exit
      process_id, exit_status = os.waitpid(process_id, 0)

      # Check if the child process terminated normally
      if os.WIFEXITED(exit_status):
          exit_code = os.WEXITSTATUS(exit_status)
          print(f"Child process {process_id} exited with status {exit_code}")
      else:
          print(f"Child process {process_id} terminated abnormally")

  except ChildProcessError as e:
      print(f"Error waiting for child process {process_id}: {e}")

def later(proc):
    print(proc)
    print(proc.__dir__())
    print(proc.pid,", ",proc.returncode, ", ",proc._exitcode)
    # help(proc)
    print("ended")

def get_status_of_processes(process_ids):
    print("Getting exit status")
    print(process_ids)
    # processes = [psutil.Process(process_id) for process_id in process_ids[1:]]
    processes = psutil.Process(process_ids[0]).children()
    print(processes)

    # gone, alive = psutil.wait_procs(processes, timeout=5, callback=later)
    gone, alive = psutil.wait_procs(processes, callback=later)

    print(gone)
    print(alive)
    # print(alive[0].returncode)


    # for process_id in process_ids:
    #     get_status(process_id)