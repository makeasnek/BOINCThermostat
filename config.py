##########################################################################################################################################
##############      BOINC CONTROLLER. EDIT THESE IF YOU WANT TO CONTROL THE BOINC CLIENT                                    ##############
##########################################################################################################################################
control_boinc=True # Set to True to use this as your BOINC manager and directly manage the BOINC client. You can still use BOINC Manager/boinctui to monitor its progress. Default: True
enable_temp_control=True # Enable controlling BOINC based on temp. Default: True
start_temp=50 # Start crunching if temp > this number, whole numbers only! Default: 50.
stop_temp=75 # Stop crunching is temp > this number, whole numbers only! Default: 75
# Methods of fetching temp data, only use one!
temp_url=None # URL to fetch temperature data from, Default: None. # Note this will check temperature quite frequently. This is fine for your smart thermostats on a local IP but not great for publicly-accesible data points. Example: 'https://mytempcheck.com'
temp_command=None # Shell command to run to check temp data. Must use absolute paths ie '/bin/bash /home/user/tempcheck.sh'.
# If you want to write a custom function to retrieve temperature information, put it here. It must return a string value such as '70' or None
def temp_function():
    # blah blah blah your code here, return some int value
    return None

temp_regex=r'\d*' # Regular expression used to scrape temp from command, URL, or other specified source. This just grabs the first sequence of numbers it finds. Default: r'\d*'. Examples: https://www.dataquest.io/blog/regex-cheatsheet/
temp_sleep_time=10 # If we should stop crunching due to temp, sleep this many minutes before checking again. Default: 10
##########################################################################################################################################
##############                ADVANCED SETTINGS. DO NOT EDIT THESE IF YOU DON'T UNDERSTAND THEIR IMPLICATIONS               ##############
##########################################################################################################################################
boinc_data_dir=None # Example: '/var/lib/boinc-client' or 'C:\\ProgramData\\BOINC\\'. Only needed if in a non-standard location, otherwise None.
log_level='ERROR' # Options are: 'DEBUG','INFO','WARNING','ERROR', default is 'WARNING'
max_logfile_size_in_mb=1 # Default: 10
# these are not fully implemented yet, but would theoretically allow you to control a non-local BOINC client. They may or may not work idk.
boinc_ip='127.0.0.1' # defaults to '127.0.0.1' with quotes
boinc_username=None # defaults to None without quotes
boinc_password=None # defaults to None, password to the BOINC rpc
boinc_port=31416