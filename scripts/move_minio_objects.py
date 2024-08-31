from minio import Minio
from minio.commonconfig import CopySource
from instance.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY

def move_objects(object_list):
    for obj in object_list:
        modified_date = obj.last_modified
        new_path = f"raw_data/{modified_date.year}/{modified_date.month}/{modified_date.day}/{obj.object_name.removeprefix('raw_data/')}"
        client.copy_object("highjump", new_path, CopySource("highjump", obj.object_name))
        # client.remove_object("highjump", obj.object_name)

if __name__ == "__main__":

    client = Minio(MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, secure=False)
    object_list = client.list_objects("highjump", prefix="raw_data/")
    move_objects(object_list)