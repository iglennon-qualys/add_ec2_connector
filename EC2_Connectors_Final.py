
#
# Author: Sean Nicholson
# Purpose: Automate the adding of EC2 connectors via the Qualys API
# version: 1.0.0
# date: 11.20.2018
#
#
#

import sys
import requests
import os
import time
import csv
import base64
import argparse
import getpass


def post_call(username: str, password: str, url: str, data_connector: str):

    usr_pass = str(username)+':'+str(password)
    usr_pass_bytes = bytes(usr_pass, "utf-8")
    b64val = base64.b64encode(usr_pass_bytes).decode("utf-8")
    headers = {
        'Accept': '*/*',
        'content-type': 'text/xml',
        'X-Requested-With': 'curl',
        'Authorization': "Basic %s" % b64val

    }

    r = requests.post(url, data=data_connector, headers=headers)
    return r.raise_for_status()


def add_aws_ec2_connector(username: str, passwd: str, url: str, add_to_cloudview: bool, debug: bool, csvfile: str):
    url = url + "/qps/rest/2.0/create/am/awsassetdataconnector"

    print('------------------------------AWS Connectors--------------------------------')
    if debug:
        if not os.path.exists("debug"):
            os.makedirs("debug")
        debug_file_name = "debug/debug_file" + time.strftime("%Y%m%d-%H%M%S") + ".txt"
        debug_file = open(debug_file_name, "w")
        debug_file.write('------------------------------AWS Connectors--------------------------------' + '\n')

    with open(csvfile, 'rt') as f:
        reader = csv.DictReader(f)
        csv_content = list(reader)
        f.close()
    counter = 0
    for csv_row in csv_content:
        counter += 1

        arn = csv_row['ARN']
        ext = csv_row['EXTID']
        name = csv_row['NAME']
        module = csv_row['MODULE']
        region = csv_row['REGION']
        print(str(counter) + ' : AWS Connector')
        print('---' + 'ARN : ' + str(arn))
        print('---' + 'EXT : ' + str(ext))
        # print '---' + 'DESC : ' + str(DESC)
        print('---' + 'NAME : ' + str(name))
        print('---' + 'REGION : ' + str(region))
        print('---' + 'MODULE : ' + str(module))
        if debug:
            debug_file.write(str(counter) + ' : AWS Connector' + '\n')
            debug_file.write('---' + 'ARN : ' + str(arn) + '\n')
            debug_file.write('---' + 'EXT : ' + str(ext) + '\n')
            debug_file.write('---' + 'NAME : ' + str(name) + '\n')
            debug_file.write('---' + 'REGION : ' + str(region) + '\n')
            debug_file.write('---' + 'MODULE : ' + str(module) + '\n')

        module_list = csv_row['MODULE'].split()
        activate_module = ""
        activate_region = ""
        for m in module_list:
            activate_module += "<ActivationModule>{0}</ActivationModule>".format(str(m))

        if csv_row['REGION'] != "ALL":
            region_list = csv_row['REGION'].split()
            for r in region_list:
                activate_region += "<AwsEndpointSimple><regionCode>{0}</regionCode></AwsEndpointSimple>".format(str(r))
            xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><ServiceRequest><data><AwsAssetDataConnector><name>{0}" \
                  "</name><arn>{1}</arn><externalId>{2}</externalId><endpoints><add>{3}</add></endpoints>" \
                  "<disabled>false</disabled><activation><set>{4}</set></activation><useForCloudView>{5}" \
                  "</useForCloudView></AwsAssetDataConnector></data></ServiceRequest>".format(csv_row['NAME'], csv_row['ARN'],
                                                                                              csv_row['EXTID'],
                                                                                              activate_region,
                                                                                              activate_module,
                                                                                              add_to_cloudview)
        else:
            xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><ServiceRequest><data><AwsAssetDataConnector>" \
                  "<name>{0}</name><arn>{1}</arn><externalId>{2}</externalId><disabled>false</disabled>" \
                  "<allRegions>true</allRegions><activation><set>{3}</set></activation><useForCloudView>{4}" \
                  "</useForCloudView></AwsAssetDataConnector></data></ServiceRequest>".format(csv_row['NAME'],
                                                                                              csv_row['ARN'],
                                                                                              csv_row['EXTID'],
                                                                                              activate_module,
                                                                                              add_to_cloudview)

        try:
            post_call(username, passwd, url, xml)
            print(str(counter) + ' : Connector Added Successfully')
            print('-------------------------------------------------------------')
            if debug:
                debug_file.write(str(counter) + ' : Connector Added Successfully' + '\n')

        except requests.exceptions.HTTPError as e:  # This is the correct syntax
            print(str(counter) + ' : Failed to Add AWS Connector')
            print(e)
            print('-------------------------------------------------------------')
            if debug:
                debug_file.write(str(counter) + ' : Failed to Add AWS Connector' + '\n')
                debug_file.write(str(e) + '\n')
                debug_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('username', help='Qualys Username')
    parser.add_argument('api_endpoint', help='Qualys API FQDN (e.g. qualysapi.qualys.com')
    parser.add_argument('input_file', help='CSV Input File')
    parser.add_argument('-c', '--cloudview', help='Also add Cloud View connector with the same details',
                        action='store_true')
    parser.add_argument('-d', '--debug', help='Enable debug output to file', action='store_true')

    args = parser.parse_args()

    if args.username:
        qualys_user = str(args.username)
        qualys_pass = getpass.getpass('Enter password for \'%s\'' % qualys_user)
    else:
        print('ERROR: Username not specified')
        sys.exit(1)

    add_aws_ec2_connector(username=qualys_user, passwd=qualys_pass, url=args.api_endpoint,
                          add_to_cloudview=args.cloudview, debug=args.debug, csvfile=args.input_file)
