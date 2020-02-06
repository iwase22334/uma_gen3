#!/usr/bin/env python3

import sys
import os
import boto3
from boto3.session import Session

if __name__ == "__main__":
    args = sys.argv

    if len(args) != 3:
        print("usage: s3_upload.py <src> <dst>")
        exit()

    access_key = os.environ.get('UMA_AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('UMA_AWS_SECRET_ACCESS_KEY')
    region = os.environ.get('UMA_AWS_REGION')
    bucket_name = os.environ.get('UMA_TRAINER_STATISTICS_BUCKET')

    session = Session(aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      region_name=region)

    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    #bucket.upload_file(args[1], args[2], ExtraArgs={'ACL':'public-read'})
    bucket.upload_file(args[1], args[2])

