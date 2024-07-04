from os import walk, path, getenv
from minio import Minio, S3Error
from dotenv import load_dotenv
from typing import Union, Optional, Tuple, Any
from minio.error import InvalidResponseError
from ..utils.decorators import validate_arguments
from apps.lib.localvars import MINIO_SERVER_URL, MINIO_SECURE_CLIENT, PATH_TO_CODE


# GET KEY
load_dotenv(PATH_TO_CODE)
MINIO_ACCESS_KEY = getenv('AWS_ACCESS_KEY_ID')
MINIO_SECRET_KEY = getenv('AWS_SECRET_ACCESS_KEY')


@validate_arguments
def create_minio_client() -> Union[Minio, None]:
    try:
        client = Minio(endpoint=MINIO_SERVER_URL,
                       access_key=MINIO_ACCESS_KEY,
                       secret_key=MINIO_SECRET_KEY,
                       secure=MINIO_SECURE_CLIENT)
        return client
    except (Exception, S3Error) as e:
        print(e)
        return None


# Function to upload a folder to MinIO
@validate_arguments
def upload_object(local_folder: str,
                  minio_bucket: str,
                  minio_client: Any,
                  prefix: Optional[str] = '') -> Tuple[int, int, int]:

    # Make sure it's not already in
    lsobj = minio_client.list_objects(minio_bucket)
    lsobn = [i_.object_name for i_ in lsobj]
    upldd = 0
    alrdy = 0
    errtr = 0

    for root, dirs, files in walk(local_folder):
        for file in files:
            local_file_path = path.join(root, file)
            object_name = path.join(prefix, path.relpath(local_file_path, local_folder))

            if file not in lsobn:
                try:
                    minio_client.fput_object(
                        minio_bucket,
                        object_name,
                        local_file_path
                    )
                    upldd += 1
                    print(f"Uploaded {local_file_path} to {minio_bucket}/{object_name}")
                except InvalidResponseError as err:
                    print(err)
                    errtr += 1

            else:
                alrdy += 1

    return upldd, alrdy, errtr


@validate_arguments
def create_bucket(bucket_name: str,
                  client: Any) -> str:
    try:
        # Check if the bucket already exists
        if not client.bucket_exists(bucket_name):
            # Create the bucket
            client.make_bucket(bucket_name)
            out_msg = f"Bucket '{bucket_name}' created successfully."
        else:
            out_msg = f"Bucket '{bucket_name}' already exists."
        print(out_msg)
    except S3Error as e:
        print(f"Error occurred: {e}")
    return out_msg


@validate_arguments
def empty_bucket(bucket_name: str,
                 client: Any) -> None:

    # TODO: type minio client

    try:
        # List all objects in the bucket
        objects = client.list_objects(bucket_name, recursive=True)

        # Remove each object from the bucket
        for obj in objects:
            client.remove_object(bucket_name, obj.object_name)

        print(f"All objects in the bucket '{bucket_name}' have been removed.")
    except InvalidResponseError as err:
        print(f"Error: {err}")
    return


@validate_arguments
def delete_bucket(bucket_name: str,
                  client: Any) -> str:
    try:
        # Check if the bucket exists
        if client.bucket_exists(bucket_name):
            # Ensure the bucket is empty before attempting to remove it
            objects = client.list_objects(bucket_name, recursive=True)
            for obj in objects:
                client.remove_object(bucket_name, obj.object_name)

            # Remove the bucket
            client.remove_bucket(bucket_name)
            out_msg = f"Bucket '{bucket_name}' removed successfully."
        else:
            out_msg = f"Bucket '{bucket_name}' does not exist."
    except S3Error as e:
        print(f"Error occurred: {e}")
    return out_msg