#!/usr/bin/env python
# coding: utf-8

import boto3
import datetime
import argparse
import time
import yaml

def mkdate(datestr):
  try:
    return time.strptime(datestr, '%Y-%m-%d')
  except ValueError:
    raise argparse.ArgumentTypeError(datestr + ' is not a proper date string')

parser = argparse.ArgumentParser()
parser.add_argument('xDate',type=mkdate)
args = parser.parse_args()

with open('aws-config.yaml', 'r') as file:
    aws_service = yaml.safe_load(file)

BUCKET = aws_service['aws']['bucket_name']
access_key_id = aws_service['aws']['aws_access_key_id']
secret_access_key = aws_service['aws']['aws_secret_access_key']
prefix = aws_service['aws']['prefix']
YEAR = args.xDate.tm_year
MONTH = args.xDate.tm_mon
DAY = args.xDate.tm_mday

session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

s3 = session.resource('s3')
my_bucket = s3.Bucket(BUCKET)
for my_bucket_object in my_bucket.objects.filter(Prefix=prefix):
    if my_bucket_object.last_modified.replace(tzinfo = None) > datetime.datetime(YEAR, MONTH, DAY, tzinfo=None):
        print(my_bucket_object.key, my_bucket_object.last_modified)
        my_bucket.download_file(my_bucket_object.key, my_bucket_object.key)