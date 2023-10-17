## bbpp

This module monitors any BitBucket repository and sends an OS notification whenever is any status change in the last 10 pipelines of the repo.
It will stop notifying every 10 seconds after the first notification and will keep doing that until the script is exited with ctrl+c.

## Prerequisites

You will need your BitBucket credentials, which you can get from your BitBucket account settings.

### Username

You can find your username in the BitBucket settings page. Click on the cogwheel / Personal BitBucket settings / Account settings / Username.

### Password

The password in this script is an APP password. Click on the cogwheel / Personal BitBucket settings / App passwords / Create app password. 
Give it a name and grant next permissions:
* Account read
* Projects read
* Repositories read
* Pipelines read

## Installation

### macos
```
pip install bbpp
```

### Windows
* Install python from the Microsoft Store
* Install pip
```
python -m ensurepip --upgrade
```
* Install bbpp
```
pip install bbpp
```

Read the installation warning
```
WARNING: The script bbpp.exe is installed in 'C:Users...' which is not on PATH. Consider adding this directory to PATH or, if your prefer to suppress this warning, use --no-warn-script-location.
export PATH with where the script bbpp is available.
```
You will need to edit your PATH to include the installation directory mentioned on the warning.

### Linux

This hasn't been tested on Linux yet, the installation should work but the notifications will surely fail.
Feel free to open a PR including the notification support for Linux. :)

## Configuration

Configure credentials:
```
bbpp config -u username -p apikey -w workspace
```

Where username and apikey are the credentials obtained from the prerequisites section and workspace is the name of the workspace you want to monitor the pipelines from.

This would write a json configuration file at ~/.bbpp/bbpp.conf (Windows users sorry about that)

You can also customize the sound played with the macos nofitication.


## How to use?
```
bbpp -r regex
```
where regex is part of the repository name you want to monitor. It will try to match to /.*regex.*/ if there is more than one match it will exit and you will need to provide a more specific regex.

## Contribute
Contributions are more than welcomed!

## License
BSD