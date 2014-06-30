import novaclient
from novaclient.v1_1 import client
import time


def get_nova(project="admin"):
    auth_url = "http://192.168.119.113:5000/v2.0"
    user = "admin"
    password = "P4ssw0rd"
    project = project or "admin"
    region = "RegionOne"
    service = "compute"

    nova = client.Client(user, password, project, auth_url, region_name=region, service_type=service)
    return nova

# results = nova.servers.list(detailed=True)
# for image in results:
#     print image.id, image.name, image.status
    # print(dir(image))
nova = get_nova()

image_id = "5388f7cf-ab31-476d-a95d-a270240e6e55"

image = nova.servers.get(server=image_id)
print(image)

if image.status == "SHUTOFF":
    print("Starting server")
    image.start()
    while True:
        time.sleep(5)
        image = nova.servers.get(server=image_id)
        print("\t"+image.status)
        if image.status == "ACTIVE":
            break
else:
    print("Stopping server")
    image.stop()
    while True:
        time.sleep(5)
        image = nova.servers.get(server=image_id)
        print("\t"+image.status)
        if image.status == "SHUTOFF":
            break

    print("Starting server")
    image.start()


image_id = "0924da4b-f29b-4a6c-bf37-27aee96fd71c"
image = nova.servers.get(server=image_id)
print(image)

if image.status == "SHUTOFF":
    print("Starting server")
    image.start()
    while True:
        time.sleep(5)
        image = nova.servers.get(server=image_id)
        print("\t"+image.status)
        if image.status == "ACTIVE":
            break
else:
    print("Stopping server")
    image.stop()
    while True:
        time.sleep(5)
        image = nova.servers.get(server=image_id)
        print("\t"+image.status)
        if image.status == "SHUTOFF":
            break

    print("Starting server")
    image.start()