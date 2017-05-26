import requests
import argparse
import json
from pygments import highlight, lexers, formatters
import os
import sys

SpotinstApiToken = "Bearer " + os.environ['SPOTINSTTOKEN']

headers = {"Authorization": SpotinstApiToken}

parser = argparse.ArgumentParser()

parser.add_argument("-g", action="store", dest='ElasticGroupName', help="set elasticgroup name to fetch", type=str)
parser.description ='List elasticgroups on spotinst or dump a single group json config'
args = parser.parse_args()

try:
    SpotinstRequest = requests.get('https://api.spotinst.io/aws/ec2/group', headers=headers)
    if SpotinstRequest.status_code is not 200:
        print(SpotinstRequest.status_code)
        sys.exit(1)
except Exception as e:
    print(e)
    sys.exit(1)

SpotResponse = SpotinstRequest.json()


if args.ElasticGroupName:
    for ElasticGroup in SpotResponse['response']['items']:
        if ElasticGroup['name'] == args.ElasticGroupName:
            formatted_json = json.dumps(ElasticGroup,sort_keys=True, indent=4)
            colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
            print(colorful_json)

else:
    for ElasticGroup in SpotResponse['response']['items']:
        print(ElasticGroup['name'])