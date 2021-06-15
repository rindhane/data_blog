#! /usr/bin/env python

# Imports the Google Cloud client library
from google.cloud import storage
from google.oauth2.service_account import Credentials
import json
from google.api_core import exceptions 

def get_OauthCreds_from_serviceAccount(json_file_path=None, service_account_creds=None):
    #HELP : https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html#module-google.oauth2.service_account
    data=None
    if json_file_path:
        with open(json_file_path,'r') as fp:
            data=json.load(fp)
    if data is None and isinstance(service_account_creds,dict):
        data=service_account_creds
    #make sure env variable GOOGLE_APPLICATION_CREDENTIALS is set
    if data is None:
        import os
        #make sure env variable GOOGLE_APPLICATION_CREDENTIALS is set
        tmp= os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if tmp is None:
            raise Exception('credentials have not been provided')
        return get_OauthCreds_from_serviceAccount(json_file_path=tmp) 
    return Credentials.from_service_account_info(data)

def create_client(OauthCreds):
    # Instantiates a client
    storage_client = storage.Client(credentials=OauthCreds)
    return storage_client

def create_bucket_class_location(client,bucket_name,**kwargs):
    """Create a new bucket in specific location with storage class"""
    bucket = client.bucket(bucket_name)
    bucket.storage_class = "COLDLINE"
    # Creates the new bucket
    new_bucket = client.create_bucket(bucket, location="us")
    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket

def get_bucket(client,bucketName):
    #bucketName is a string
    return client.get_bucket(bucketName)

def print_bucket_metadata(bucket):
    #bucket is bucket object     
    print("ID: {}".format(bucket.id))
    print("Name: {}".format(bucket.name))
    print("Storage Class: {}".format(bucket.storage_class))
    print("Location: {}".format(bucket.location))
    print("Location Type: {}".format(bucket.location_type))
    print("Cors: {}".format(bucket.cors))
    print(
        "Default Event Based Hold: {}".format(bucket.default_event_based_hold)
    )
    print("Default KMS Key Name: {}".format(bucket.default_kms_key_name))
    print("Metageneration: {}".format(bucket.metageneration))
    print(
        "Retention Effective Time: {}".format(
            bucket.retention_policy_effective_time
        )
    )
    print("Retention Period: {}".format(bucket.retention_period))
    print("Retention Policy Locked: {}".format(bucket.retention_policy_locked))
    print("Requester Pays: {}".format(bucket.requester_pays))
    print("Self Link: {}".format(bucket.self_link))
    print("Time Created: {}".format(bucket.time_created))
    print("Versioning Enabled: {}".format(bucket.versioning_enabled))
    print("Labels:")
    print(bucket.labels)
    return True

def get_a_blob(bucket,blob_name):
    return bucket.blob(blob_name)

def list_bucketBlob(bucket):
    #bucket is bucket-object
    blobs = bucket.list_blobs()
    ans=list()
    for blob in blobs:
        ans.append(blob.name)
    return ans

def upload_content_blob(blob,content):
    blob.upload_from_string(content)
    return blob

def upload_a_file(bucket,destination_name,filePath):
    #bucket object
    blob=bucket.blob(destination_name)
    blob.upload_from_filename(filePath)
    return blob

def blobDownload_to_file(blob,filePath):
    blob.download_to_filename(filePath)
    return True

def blobDownload_as_bytes(blob):
    return blob.download_as_bytes()

def blobDownload_as_text(blob):
    return blob.download_as_text()

def blobDelete(blob):
    blob.delete()
    return True

def blobExists(blob):
    return blob.exists()

