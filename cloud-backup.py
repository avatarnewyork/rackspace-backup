from rcbu.client.client import Client
from rcbu.client.connection import Connection
import rcbu.client.backup_configuration as backup_config
import pprint
import string
import time

import simplejson as json
import sys, getopt

def main(argv):    

    hostname=''
    machineid=0
    region='ord'
    configfile='backup_config.json'
    configtmpl='backup_config.json.tmpl'
    try:
        opts, args = getopt.getopt(argv,"hn:i:r",["name=","id=","region=","region="])
    except getopt.GetoptError:
        print 'deploy.py --name=<name> --id=<id> --region=<region>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'deploy.py --name=<name> --id=<id> --region=<region>'
            sys.exit()
        elif opt in ("-n", "--name"):
            hostname = arg
        elif opt in ("-i", "--id"):
            machineid = arg
        elif opt in ("-r", "--region"):
            region = arg


    d={'HOSTNAME':hostname, 
       'MACHINEID':machineid}

    filein = open(configtmpl)
    src = string.Template(filein.read())
    result = src.substitute(d)

    fileout = open(configfile, "w")
    fileout.write(result)
    fileout.close()

    #pprint.pprint(myconf)

    # Import username and API key from a separate JSON file
    creds = json.loads(open('creds.json').read())
    
    conn = Connection(creds["user"], region,
                      apikey=creds["key"])
    client = Client(conn)
    
    myconf = backup_config.from_file(configfile, conn)
    #print machineid
    #print vars(myconf)
    #sys.exit(-1)
    
    # Upload a new backup configuration to the Backup API
    myconf.create()
    
    backup = client.create_backup(myconf)
    time.sleep(5)
    status = backup.start()
    
    # block here until the backup completes
    # polls once a minute by default
    backup.wait_for_completion(poll_interval=.5)
    
    # easy reporting and checking for success
    report = backup.report
    report.raise_if_not_ok()

if __name__ == '__main__':
    main(sys.argv[1:])
