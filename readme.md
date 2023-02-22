# BOINCThermostat
BOINCThermostat is a simple python script which will suspend/resume <a href="https://boinc.berkeley.edu">BOINC</a> based on ambient air temperature. It can fetch
temperature data from a command, a URL, or any custom source you want. Note that some BOINC projects handle checkpointing well
while others may need to restart the entire WU. There are more sophisticated ways to do this,
I just made this to replicate a dumb thermostat like might control your home furnace. Special thanks to <a href="https://github.com/nielstron/pyboinc">PyBOINC</a> which this program uses extensively.

Suggestion for those crunching with multiple rigs: Stagger temperature setpoints so that all machines don't resume/suspend at the same time. This enables the thermostat to have options aside from "off" and "full blast"


If you are crunching BOINC, be sure to collect your Gridcoin rewards as well. If you find this tool useful, please consider sidestaking or donating some GRC to me RzUgcntbFm8PeSJpauk6a44qbtu92dpw3K 
## Quickstart Instructions:
<b>For all platforms</b>: 

Open `config.py` in a text editor and change the settings you want. You should pick <b>one</b> method for checking temp, leave others as is.
<b>This is designed to run on python 3.8 or higher.</b>
<h4>Windows</h4>

 - Download the latest version of python from python.org. Enable the "install to system path" option while installing.
 - In command prompt, run the command `python -m pip install --upgrade pip`
 - In command prompt, run the command `pip install -r "C:\Users\user\Downloads\BOINCThermostat-master\requirements.txt"` (or wherever you saved this tool)
 - Double-click on main.py or run `python "C:\path\to\main.py"` from command prompt. We suggest the second method as it will display errors if the program exits unexpectedly

<h4>Linux</h4>

 - Open a terminal and go to the folder you downloaded this tool into using `cd /home/user/Downloads/BOINCThermostat` or wherever you put it
 - Run `pip3 install -r requirements.txt` (Note that you need pip installed, if you don't have it, you might need to run a `sudo apt install python3-pip`)
 - Run `python3 main.py`

<h4>OS X</h4>

 - Open a terminal and go to the folder you downloaded this tool into using `cd "/home/user/Downloads/BOINCThermostat"` or wherever you put it
 - Run `pip3 install -r requirements.txt`
 - Run `python3 main.py`

## Privacy & Legal:
- This software comes with no warranty and is provided as-is. Be wise when running software from some random github account. It may crash your computer. By using it, you agree to hold the developers harmless for any damage it may cause whether through negligence, accident, or malice to the fullest extent legally possible. You also agree to allow yourself to have a wonderful day today or you are not allowed to use this software.
- If you submit any code or pull requests to this repository or its developer, you agree to have the code ownership transferred to the repository owner and licensed under the same license as the other code in the repository is licensed under.
- This software is produced independently of the Gridcoin and BOINC projects without their approval or endorsement.
- This software is released under the license specified in the LICENSE file. It also incorporates components of other software, whose licenses are noted where imported in the directory structure.
- This tool does not send any of your information anywhere. It is released under the license described in the LICENSE file. Other portions incorporated from other authors may have different license files which describe those licenses.
