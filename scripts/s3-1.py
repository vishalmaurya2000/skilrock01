#!/usr/bin/python3

import boto3
import sys
import time
import argparse

session=boto3.Session(profile_name="default", region_name="af-south-1") #boto3 session, aws profile
s3=session.client('s3')

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="objects file name")
args = parser.parse_args()

f = open(args.file,encoding = 'utf-8')
bucket = 'inq-elastic-snapshots'

for line in f:
    file_name = line.rstrip('\n')
    print(file_name)
    response = s3.list_object_versions(
        Bucket=bucket,
        Prefix=file_name,
    )
    main_file_version = ''
    delete_marker_version = ''
    
    if 'DeleteMarkers' in response:
        delete_marker = response['DeleteMarkers']
        delete_marker_version = response['DeleteMarkers'][0]['VersionId']

    if 'Versions' in response: 
        version = response['Versions']
        main_file_version = response['Versions'][0]['VersionId']
    
    print(f'Main File Vesion = {main_file_version}')
    print(f'Delete Marker Version = {delete_marker_version}')
    print(f'File Name = {file_name}')

    response = s3.delete_objects(
        Bucket=bucket,
        Delete={
            'Objects': [
                {
                    'Key': file_name,
                    'VersionId': delete_marker_version
                },
                {
                   'Key': file_name,
                    'VersionId': main_file_version
                },
            ]
        }
    )
