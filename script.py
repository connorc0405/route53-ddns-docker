#! /bin/env python3

import subprocess
import os
import json
import time
from ipaddress import ip_address, IPv4Address


zone_id = os.environ['ZONEID']
domain = os.environ['DOMAIN']

listed_ip = None


def get_listed_ip():
    output = subprocess.check_output(["aws", "route53", "list-resource-record-sets", "--hosted-zone-id", zone_id])
    jsony = json.loads(output)
    for resource_record_set in jsony['ResourceRecordSets']:
        if resource_record_set['Type'] == 'A' and resource_record_set['Name'] == domain + '.':
            return resource_record_set['ResourceRecords'][0]['Value']


def get_public_ip():
    output = subprocess.check_output(["curl", "checkip.amazonaws.com"])
    public_ip = output.decode().rstrip('\n')
    return public_ip


def change_listed_ip(new_ip):
    with open("/change.json", 'r') as change_file:
        jsony = json.load(change_file)
        jsony['Changes'][0]['ResourceRecordSet']['Name'] = domain
        if type(ip_address(new_ip)) is not IPv4Address:
            jsony['Changes'][0]['ResourceRecordSet']['Type'] = 'AAAA'
        jsony['Changes'][0]['ResourceRecordSet']['ResourceRecords'][0]['Value'] = new_ip
        with open("/change_final.json", 'w') as change_final_file:
            json.dump(jsony, change_final_file)
        output = subprocess.check_output(['aws', 'route53', 'change-resource-record-sets', '--hosted-zone', zone_id, '--change-batch', 'file:///change_final.json'])
        jsony = json.loads(output)
        if jsony["ChangeInfo"]["Status"] != "PENDING":
            raise Exception("DDNS update did not succeed")


while True:
    if listed_ip is None:
        listed_ip = get_listed_ip()
    public_ip = get_public_ip()
    if public_ip != listed_ip:
        print(f"Updating DDNS IP from {listed_ip} to {public_ip}")
        try:
            change_listed_ip(public_ip)
            listed_ip = public_ip
            print("Update succeeded")
        except Exception as e:
            print("Update failed")

    time.sleep(60)
