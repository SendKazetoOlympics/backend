from minio import Minio
from minio.commonconfig import CopySource
from instance.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY

def move_objects(object_list):
    for obj in object_list:
        og_name = obj.object_name
        if og_name[19:23] == '2024':
            new_path = f"raw_data/{og_name[19:23]}/{og_name[23:25]}/{og_name[25:27]}/{og_name[19:]}"
            client.copy_object("highjump", new_path, CopySource("highjump", obj.object_name))
        # client.remove_object("highjump", obj.object_name)

if __name__ == "__main__":

    client = Minio(MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, secure=False)
    object_list = client.list_objects("highjump", prefix="raw_data/",recursive=True)
    move_objects(object_list)