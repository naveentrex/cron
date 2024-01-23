import psutil
import json
import time
import catch_status

p = psutil.pids()
cron_map = {}
active_cron_jobs = []
active_process_ids = []

def create_new_process_object(current_process_object, original_process_object):
    # compare among the childrens
    # If the current_process_object child is not in original_process_object just append it at the end
    # And, if the current_process_object child is in the original_process_object then compare their children iteratively

    new_object = original_process_object
    new_object['status'] = 'active'
    original_childrens = {}
    original_childrens_index = {}
    new_childs_to_append = []
    index = 0
    for x in original_process_object['children']:
        original_childrens[" ".join(x['command'])] = x
        original_childrens_index[" ".join(x['command'])] = index
        index = index + 1

    # print(original_childrens)
    # print(original_childrens_index)


    for current_child in current_process_object['children']:
        # print(current_child)
        current_child_command = " ".join(current_child['command'])
        # if current_child_command in original_childrens.keys():
        if current_child_command in original_childrens:
            # now iteratively compare both the twins
            # print("ORIGINAL PROCESS OBJECT")
            # print(original_process_object)
            new_child_object = create_new_process_object(current_child, original_childrens[current_child_command])
            new_object['children'][original_childrens_index[current_child_command]] = new_child_object
        else:
            # just append it to the end of the original_process_object
            new_childs_to_append.append(current_child)
    
    new_object['children'] += new_childs_to_append
    return new_object

def modify_cron_tree(curr_active_cron, cron_command):
    if cron_command in cron_map.keys():
        cron_map_child = (x['command'][-1] for x in cron_map[cron_command]['children'])
        # print(cron_map_child)

        # This entry is present in cron map, we just need to add something new if it comes up in curr_active_cron
        # one thing that we could do is that create a whole new cron_map for curr_active_cron and replace it with the old one at the end
        
        new_curr_active_cron = create_new_process_object(curr_active_cron, cron_map[cron_command])
        cron_map[cron_command] = new_curr_active_cron
    else:
        cron_map[cron_command] = curr_active_cron
    print("nothing")

def modify_cron_map(active_crons):
    # print(json.dumps(active_crons, indent=2))

    # iterate over this response to get all the cron jobs currently running
    # active_crons_lenghth = active_crons.length
    active_crons_identifier = []
    for curr_active_cron in active_crons:
        # print(curr_active_cron['command'])
        # print(curr_active_cron['command'][-1])
        active_crons_identifier.append(curr_active_cron['command'][-1])
        modify_cron_tree(curr_active_cron, curr_active_cron['command'][-1])
    # print(active_crons_identifier)

def find_cron_pid():
    for process in psutil.process_iter(['pid', 'name', 'ppid']):
        if (process.info['name']=='cron' or process.info['name']=='crond') and process.info['ppid']==1:
            return process.info['pid']

cron_process_id = find_cron_pid()

def processes_to_ignore():
    return ['sleep']

# Create a json format here to create a tree kind of structure for the currently running processes

def get_child_processes(parent_pid, level=0):
    try:
        parent_process = psutil.Process(parent_pid)
        active_process_ids.append(parent_pid)
        print(active_process_ids)
        child_processes = parent_process.children(recursive=False)
        response = []

        for child in child_processes:
            #print(f"Child PID: {child.pid}, Name: {child.name()}, Parent PID: {parent_pid}")
            #print(child, " ", parent_process.cmdline(), " ", child.cmdline())
            if child.name() in processes_to_ignore():
                continue
            child_response = get_child_processes(child.pid, level+1)
            new_resp = {
                "id": child.pid,
                "name": child.name(),
                "command": child.cmdline(),
                "children": child_response,
                "status": "active"
            }
            if level<1:
                response.append(child_response[0])
                # print("PRINTING CHILD RESPONSE")
                # print(child_response[0])
                # print("PRINTED CHILD RESPONSE")
            else:
                response.append(new_resp)
            #print(new_resp)
        return response
    except psutil.NoSuchProcess:
        print(f"Process with PID {parent_pid} not found.")
        return []

def set_process_status(process, status):
    process['status'] = status
    for child in process['children']:
        set_process_status(child, status)

def check_for_active(map_process, active_process):
    map_process['status'] = 'active'
    # map_process_child_map = {}
    map_process_child_map_index = {}
    index = 0
    for map_child_process in map_process['children']:
        # map_process_child_map[" ".join(map_child_process['command'])] = map_child_process
        map_process_child_map_index[" ".join(map_child_process['command'])] = index
        index = index + 1

    for active_child_process in active_process['children']:
        active_process_command = " ".join(active_child_process['command'])
        map_process['children'][map_process_child_map_index[active_process_command]]['status'] = 'active'
        check_for_active(map_process['children'][map_process_child_map_index[active_process_command]], active_child_process)


def set_current_active(active_processes):
    # iterate over all the active_processes
    print("PRINTING CRON MAP")
    print(cron_map)
    for active_process in active_processes:
        # active_process_command = active_process['command'][-1]
        # active_process_in_map = cron_map[active_process_command]
        # set_process_status(active_process_in_map, 'active')
        active_process_command = active_process['command'][-1]
        active_process_in_map = cron_map[active_process_command]
        check_for_active(active_process_in_map, active_process)

def get_cron_tree():
    # Replace 'your_parent_pid' with the actual PID of the process you're interested in
    parent_pid = cron_process_id

    # active_process_ids = []

    response = get_child_processes(parent_pid, 0)
    print(active_process_ids)
    active_cron_jobs = response

    modify_cron_map(response)

    # if len(response)>0:
    #     print("PRINTING RESPONSE CHILDREN")
    #     print(response[0]['children'])
    #     modify_cron_map(response[0]['children'])
    for entry in cron_map.values():
        set_process_status(entry, 'inactive')

    # for entry in cron_map.values():
    set_current_active(response)

    print("GOING TO PRINT EXIT STATUS")
    print(active_process_ids)
    # catch_status.get_status_of_processes(active_process_ids)

    # need to merge cron_map with active cron job and return new response

    print(cron_map)
    return [x for x in cron_map.values()]

def return_cron_tree():
    return cron_map

def get_active_cron_tree():
    return active_cron_jobs

# def refresh_active_cron():
#     while True:
#         get_cron_tree()
#         time.sleep(0.01)

# if __name__ == '__main__':
#     refresh_active_cron()