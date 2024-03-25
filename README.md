# SC2 Arcade Hosts Patch

This is a patcher script which retrieves the alive arcade lobbies on America server, extract the img tags and the domains within them, and then update the hosts file with the domains.

## How to use

Download from releases, run the executable file as administrator.

Or you can clone the repository, run the following command to install the dependencies, and then run the script. (Make sure your command line is running as administrator)

```bash
pip install -r requirements.txt
python -u patcher.py
```
