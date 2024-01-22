import psutil
import json
import time

p = psutil.pids()
cron_map = {}
active_cron_jobs = []


def modify_cron_tree(active_crons, cron_command):
    # if cron_command in cron_map.keys():
    #     # 
    # else:
    #     # set it to the current one
    print("nothing")

def modify_cron_map(active_crons):
    print(json.dumps(active_crons, indent=2))

    # iterate over this response to get all the cron jobs currently running
    # active_crons_lenghth = active_crons.length
    active_crons_identifier = []
    for curr_active_cron in active_crons:
        active_crons_identifier.append(curr_active_cron['command'][-1])
        modify_cron_tree(active_crons, curr_active_cron['command'][-1])
    print(active_crons_identifier)

def find_cron_pid():
    for process in psutil.process_iter(['pid', 'name', 'ppid']):
        if (process.info['name']=='cron' or process.info['name']=='crond') and process.info['ppid']==1:
            return process.info['pid']

cron_process_id = find_cron_pid()

def processes_to_ignore():
    return ['sleep']

# Create a json format here to create a tree kind of structure for the currently running processes

def get_child_processes(parent_pid):
    try:
        parent_process = psutil.Process(parent_pid)
        child_processes = parent_process.children(recursive=False)
        response = []

        for child in child_processes:
            #print(f"Child PID: {child.pid}, Name: {child.name()}, Parent PID: {parent_pid}")
            #print(child, " ", parent_process.cmdline(), " ", child.cmdline())
            if child.name() in processes_to_ignore():
                continue
            child_response = get_child_processes(child.pid)
            new_resp = {
                "id": child.pid,
                "name": child.name(),
                "command": child.cmdline(),
                "children": child_response,
                "status": "active"
            }
            response.append(new_resp)
            #print(new_resp)
        return response
    except psutil.NoSuchProcess:
        print(f"Process with PID {parent_pid} not found.")
        return []

def get_cron_tree():
    # Replace 'your_parent_pid' with the actual PID of the process you're interested in
    parent_pid = cron_process_id
    response = get_child_processes(parent_pid)
    active_cron_jobs = response
    # print(json.dumps(response, indent=2))
    # print(response)
    modify_cron_map(response[0]['children'])
    return response

def return_cron_tree():
    return cron_map

def get_active_cron_tree():
    return active_cron_jobs

def refresh_active_cron():
    while True:
        get_cron_tree()
        time.sleep(0.005)

# if __name__ == '__main__':
# refresh_active_cron()