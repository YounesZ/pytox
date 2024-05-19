import time
from os import path, environ
from typing import Tuple, Dict
from dotenv import load_dotenv
from google.cloud import compute_v1
from google.oauth2 import service_account
from apps.lib.localvars import PATH_TO_CODE

load_dotenv()


def gcp_prepare_client() -> Tuple[compute_v1.InstancesClient, Dict]:

    # TODO: type GCP request

    # Initialize the Compute Engine client
    sak_path = path.join(PATH_TO_CODE, environ.get('SERVICE_ACCOUNT_KEY'))
    credentials = service_account.Credentials.from_service_account_file(sak_path)
    compute_client = compute_v1.InstancesClient(credentials=credentials)

    # Prepare requests
    request = {
            "project": environ.get('GCP_INSTANCE_PROJECT'),
            "zone": environ.get('GCP_INSTANCE_ZONE'),
            "instance": environ.get('GCP_INSTANCE_NAME')
        }
    return compute_client, request


def start_instance(gcp_client: compute_v1.InstancesClient,
                   request: Dict) -> str:

    # Get status
    status = instance_status(gcp_client, request)
    timeAd = 60
    timeSt = time.time()

    if status == 'RUNNING':
        print('Instance is already running - nothing to do')
        return status

    while (status in ['PROVISIONING', 'STAGING', 'STOPPING', 'SUSPENDING']) and ((time.time() - timeSt)<timeAd):
        time.sleep(10)
        status = instance_status(gcp_client, request)

    if status in ['STOPPED', 'SUSPENDED', 'TERMINATED']:
        # Boot the instance
        response = gcp_client.start(request=request)
        time.sleep(60)
        status = instance_status(gcp_client, request) # MAKE SURE BUFFER IS SUFFICIENT TO FIRE UP INSTANCE
    elif status != 'RUNNING':
        print('Waited 60sec for instance to stabilize - timed out')
    else:
        print('Unknown instance state')
        pass

    return status


def stop_instance(gcp_client: compute_v1.InstancesClient,
                  request: Dict) -> str:
    # Get status
    status = instance_status(gcp_client, request)
    timeAd = 60
    timeSt = time.time()

    if status == 'STOPPED':
        print('Instance is already stopped - nothing to do')
        response = None
        return response

    if status == 'TERMINATED':
        print('Instance is terminated - nothing to do')
        response = None
        return response

    while (status in ['PROVISIONING', 'STAGING', 'STOPPING', 'SUSPENDING']) and ((time.time() - timeSt) < timeAd):
        time.sleep(10)
        status = instance_status(gcp_client, request)

    if status == 'RUNNING':
        # Stop the instance
        response = gcp_client.stop(request=request)
        time.sleep(30)      # MAKE SURE BUFFER IS SUFFICIENT TO KILL INSTANCE

    elif status in ['STOPPED', 'SUSPENDED']:
        print('Instance was stopping - complete')
        response = None
    else:
        print('Unknown instance state')
        response = None
        pass

    return response


def instance_status(gcp_client: compute_v1.InstancesClient,
                    request: Dict) -> str:

    # Get the status of the instance
    instance = gcp_client.get(project=request['project'],
                              zone=request['zone'],
                              instance=request['instance'])
    print(f"Instance {request['instance']} status: {instance.status}")
    return instance.status


# Example usage
#start_instance(project, zone, instance_name)
# stop_instance(project, zone, instance_name)