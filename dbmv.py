import json
import os
import logging

TARGET_HOST = 'localhost'
TARGET_PORT = '5433'

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

with open('params.json') as json_file:
    data = json.load(json_file)
 
for i in data:
    dump_cmd = 'PGPASSWORD=' + i['src_password'] + ' pg_dump -h '\
            + i['src_host'] + ' -U ' + i['src_user'] + ' -d '\
            + i['src_db'] + '  -c -O --if-exists > /tmp/' + i['src_db']
    
    logging.info('Creating dump from %s', i['src_db'])
    if os.system(dump_cmd) != 0:
        logging.warning('Failed to create dump from %s!', i['src_db'])
        continue
    logging.info('Done creating dump')
    
    restore_cmd = 'PGPASSWORD=' + i['dst_password'] + ' psql -h '\
            + TARGET_HOST + ' -p ' + TARGET_PORT + ' -U ' + i['dst_user'] + ' -d ' + i['dst_db'] + ' -f /tmp/' + i['src_db']  
    
    logging.info('Resoring dump from %s to %s', i['src_db'], i['dst_db'])
    if os.system(restore_cmd) != 0:
        logging.warning('Failed to restore dump from %s to %s!', i['src_db'], i['dst_db'])
        continue
    logging.info('Resoring dump done') 
   
    del_cmd = 'rm /tmp/' + i['src_db']
    logging.info('Deleting dump %s', i['src_db']) 
    os.system(del_cmd)
