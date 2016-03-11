# rackspace-backup
python script to easily configure and schedule a cloudbackup on rackspace

## Prerequisites
* python2.7
* pip
* Rackspace account
* Rackspace user / apikey with the following REQUIRED privileges:
  * Backup (Creator): View, Create, Edit
  * Files (Admin): View, Create, Edit, Delete
  * Next Generation Servers (Creator): View, Create, Edit

## Install
1. `git clone git@github.com:avatarnewyork/rackspace-backup.git`
2. move to project dir
3. `sudo pip install -r requirements.txt`

### Configuration
* creds.json - copy creds.json.example to creds.json and edit with your rackspace username / apikey
* backup_config.json.tmpl - edit the `backup_config.json.tmpl` file with your specific requirements (especially the excludes / includes / schedule)

### Install the agent
This is required if you don't already have this automated as part of your bootstrap or config managment
* [install the backup agent on the cloudserver](https://support.rackspace.com/how-to/rackspace-cloud-backup-install-the-agent-on-linux/)

### Obtain the Machine ID
This can be done various ways (for example using the nova client) but the most basic is below:
* Login to [mycloud.rackspace.com](http://mycloud.rackspace.com) and navigate to **Backups > Systems**
* Click on the system you installed the backup agent on and note the last digits in the URL.  This is the `machine_id` needed to create the backup.  Note this.

## Usage
Running this command will create a scheduled backup (Based on the template) and run an inital backup on your cloudserver.  You can watch in real-time the status on the machine under Backups > Systems > [CLOUD_SERVER].  For large systems it can take while to run.

`export PYTHONWARNINGS="ignore"; python cloud-backup.py --name=[SERVER_NAME] --id=[MACHINE_ID] --region=[REGION] --email=[EMAIL_NOTIFICATION]`

## Example
export PYTHONWARNINGS="ignore"; python cloud-backup.py --name=myserver-web2 --id=123456 --region=ord --email='gmailuser@gmail.com'

## Addtional Notes
* The `export PYTHONWARNINGS="ignore";` before the command is needed to avoid an SSL Cert warning that occurs.  For more information, please see the extended open thread for details: https://github.com/shazow/urllib3/issues/497


