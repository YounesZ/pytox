from os import walk, path, sep
from typing import List, Dict, Optional, Tuple, Any
from minio.error import InvalidResponseError


# Function to upload a folder to MinIO
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


def empty_bucket(bucket_name: str,
                 client: Any):

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