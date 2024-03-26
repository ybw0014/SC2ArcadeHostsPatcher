# SC2 Arcade Hosts Patch

This is a patcher script which retrieves the alive arcade lobbies on America server, extract the img tags and the domains within them, and then update the hosts file with the domains.

UPDATE on March 26: NA server is patched and the img tags no longer works. The script is no longer useful.

## How to use

Download from releases, run the executable file as administrator.

Or you can clone the repository, run the following command to install the dependencies, and then run the script. (Make sure your command line is running as administrator)

```bash
pip install -r requirements.txt
python -u patcher.py
```

## Disclaimer

Hosts file patch is a temporary solution for avoiding game being stalled, until Blizzard takes action to fix this issue.

The attackers may add some commonly used domains (such as google.com, youtube.com, bing.com) in their attack maps in the future. I have added a confirmation prompt before updating the hosts file, so you can check the domains before updating.

If you confirm, you are responsible for the consequences of updating the hosts file.
