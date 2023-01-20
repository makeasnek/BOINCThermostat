import asyncio,logging,os,shlex,subprocess,config,re
from time import sleep
from libs.pyboinc._parse import parse_generic
from libs.pyboinc import init_rpc_client
import libs.pyboinc
from typing import Union,Dict,List,Tuple,Any
import xml.etree.ElementTree as ET
import logging.handlers
loop = asyncio.get_event_loop()
enable_temp_control=True
temp_sleep_time=10
# Translates BOINC's CPU and GPU Mode replies into English. Note difference between keys integer vs string.
CPU_MODE_DICT = {
    1: 'always',
    2: 'auto',
    3: 'never'
}
GPU_MODE_DICT = {
    '1': 'always',
    '2': 'auto',
    '3': 'never'
}

# import user settings
from config import *

# setup logging
handler = logging.handlers.RotatingFileHandler(os.environ.get("LOGFILE", "debug.log"),maxBytes=max_logfile_size_in_mb*1024*1024,backupCount=1)
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
log = logging.getLogger()
log.setLevel(os.environ.get("LOGLEVEL", log_level))
log.addHandler(handler)

async def setup_connection(boinc_ip:str=boinc_ip,boinc_password:str=boinc_password,port:int=31416)->libs.pyboinc.rpc_client:
    """
    Sets up a BOINC RPC client connection
    """
    rpc_client = await init_rpc_client(boinc_ip, boinc_password, port=port)
    return rpc_client
def print_and_log(msg:str,log_level:str)->None:
    """
    Print a message and add it to the log at log_level. Valid log_levels are DEBUG, INFO, WARNING, ERROR
    """
    print(msg)
    if log_level=='DEBUG':
        log.debug(msg)
    elif log_level=='WARNING':
        log.warning(msg)
    elif log_level=='INFO':
        log.info(msg)
    elif log_level=='ERROR':
        log.error(msg)
    else:
        print('Being asked to log at an unknown level: {}'.format(log_level))
def temp_check()->bool:
    """
    Returns True if we should keep crunching based on temperature, False otherwise
    """
    if not enable_temp_control:
        return True
    match=None
    text=''
    if temp_url:
        import requests as req
        try:
            text=req.get(temp_url).text
        except Exception as e:
            print('Error checking temp: {}'.format(e))
            log.error('Error checking temp: {}'.format(e))
            return True
    elif temp_command:
        command=shlex.split(temp_command)
        try:
            text=subprocess.check_output(command)
        except Exception as e:
            print('Error checking temp: {}'.format(e))
            log.error('Error checking temp: {}'.format(e))
            return True
    command_output=config.temp_function()
    if command_output:
        text=str(command_output)
        pattern=re.compile(temp_regex)
        match = re.search(pattern, text)
    if match:
        found_temp=int(match.group(0))
        log.debug('Found temp {}'.format(found_temp))
        if found_temp > stop_temp or found_temp < start_temp:
            return False
    else:
        print('No temps found!')
        log.error('No temps found!')
        return True
    return True
async def run_rpc_command(rpc_client:libs.pyboinc.rpc_client,command:str,arg1:Union[str,None]=None,arg1_val:Union[str,None]=None,arg2:Union[str,None]=None,arg2_val:Union[str,None]=None)->Union[str,Dict[Any,Any]]:
    """
    Runs command on BOINC client via RPC
    Example: run_rpc_command(rpc_client,'project_nomorework','http://project.com/project')
    """
    full_command='{} {} {} {}'.format(command,arg1,arg1_val,arg2,arg2_val) # added for debugging purposes
    log.debug('Running BOINC rpc request '+full_command)
    req = ET.Element(command)
    if arg1 is not None:
        a = ET.SubElement(req, arg1)
        if arg1_val is not None:
            a.text = arg1_val
    if arg2 is not None:
        b = ET.SubElement(req, arg2)
        if arg2_val is not None:
            b.text = arg2_val
    response = await rpc_client._request(req)
    parsed = parse_generic(response)
    if not str(parsed):
        print('Warning: Error w RPC command {}: {}'.format(full_command,parsed))
        log.error('Warning: Error w RPC command {}: {}'.format(full_command, parsed))
    return parsed
def boinc_loop(dev_loop:bool=False,rpc_client=None,client_rpc_client=None,time:int=0):
    """
    Main routine which manages BOINC
    :param dev_loop: set to True if we are crunching for developer
    :param rpc_client BOINC rpc client. Pass in developer client if crunching for developer
    :param client_rpc_client client BOINC rpc client, as it must be accessed in dev mode and kept in suspend
    :param time How long to crunch for. Only used by dev mode at the moment
    """
    if not client_rpc_client:
        client_rpc_client=rpc_client
    # these variables are referenced outside the loop (or in recursive calls of the loop) so should be made global
    global combined_stats
    global final_project_weights
    global total_preferred_weight
    global total_mining_weight
    global highest_priority_projects
    global priority_results
    global dev_project_weights
    global DEV_BOINC_PASSWORD
    global DEV_LOOP_RUNNING
    while True:
        # Re-authorize in case we have become de-authorized since last run
        authorize_response = loop.run_until_complete(rpc_client.authorize())
        # Get BOINC's starting CPU and GPU modes
        existing_mode_info = loop.run_until_complete(run_rpc_command(rpc_client, 'get_cc_status'))
        existing_cpu_mode = existing_mode_info['task_mode']
        existing_gpu_mode = str(existing_mode_info['gpu_mode'])
        if existing_cpu_mode in CPU_MODE_DICT:
            existing_cpu_mode = CPU_MODE_DICT[existing_cpu_mode]
        else:
            print_and_log('Error: Unknown cpu mode {}'.format(existing_cpu_mode),'ERROR')
        if existing_gpu_mode in GPU_MODE_DICT:
            existing_gpu_mode = GPU_MODE_DICT[existing_gpu_mode]
        else:
            print_and_log('Error: Unknown gpu mode {}'.format(existing_gpu_mode),"ERROR")

        # If temp is too high:
        if not temp_check():
            while True: # Keep sleeping until we pass a temp check
                print_and_log('Sleeping due to temperature','INFO')
                # Put BOINC into sleep mode, automatically reverting if script closes unexpectedly
                sleep_interval=str(int(((60*temp_sleep_time)+60)))
                loop.run_until_complete(
                    run_rpc_command(rpc_client, 'set_run_mode', 'never', sleep_interval))
                loop.run_until_complete(
                    run_rpc_command(rpc_client, 'set_gpu_mode', 'never', sleep_interval))
                sleep(60*temp_sleep_time)
                if temp_check():
                    # Reset to initial crunching modes now that temp is satisfied
                    print_and_log('Crunching again due to temperature', 'INFO')
                    loop.run_until_complete(
                        run_rpc_command(rpc_client, 'set_run_mode', existing_cpu_mode))
                    loop.run_until_complete(
                        run_rpc_command(rpc_client, 'set_gpu_mode', existing_gpu_mode))
                    break
        else:
            print('Temperature is good, crunching...')
        sleep(temp_sleep_time)

if __name__=='__main__':
    print('Setting up BOINC connection...')
    rpc_client = loop.run_until_complete(setup_connection(boinc_ip,boinc_password,boinc_port)) # setup BOINC RPC connection
    print('Starting BOINC control...')
    boinc_loop(False,rpc_client)