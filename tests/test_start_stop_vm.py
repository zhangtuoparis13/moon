import novaclient
from novaclient.v1_1 import client
import time

# TEST = "Test_intra_tenant_it"
# TEST = "Test_intra_tenant_rh"
TEST = "Test_inter_tenant_it->tenant_rh"


def get_nova(project="tenant_it", user="admin"):
    auth_url = "http://192.168.119.113:5000/v2.0"
    user = user
    password = "P4ssw0rd"
    project = project
    region = "RegionOne"
    service = "compute"

    nova = client.Client(user, password, project, auth_url, region_name=region, service_type=service)
    return nova

# results = nova.servers.list(detailed=True)
# for image in results:
#     print image.id, image.name, image.status
    # print(dir(image))
nova = None
image_id = None
if TEST == "Test_intra_tenant_it":
    nova = get_nova(project="tenant_it", user="admin")
    image_id = "bdeb5442-4673-435a-b1d0-a09cb4027e00"
elif TEST == "Test_intra_tenant_rh":
    nova = get_nova(project="tenant_rh", user="admin")
    image_id = "2b1904b9-0776-4d6b-bc7d-48515ef424ab"
elif TEST == "Test_inter_tenant_it->tenant_rh":
    nova = get_nova(project="tenant_it", user="admin")
    image_id = "2b1904b9-0776-4d6b-bc7d-48515ef424ab"

# image_id = "5388f7cf-ab31-476d-a95d-a270240e6e55"
# image_id = "95528176-2ec6-47e6-9c7d-6c02deb5225b"
# image_id = "afe5dc2f-eec6-44d4-8e2f-b94dfb2b7f89"

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


# image_id = "0924da4b-f29b-4a6c-bf37-27aee96fd71c"
# image = nova.servers.get(server=image_id)
# print(image)
#
# if image.status == "SHUTOFF":
#     print("Starting server")
#     image.start()
#     while True:
#         time.sleep(5)
#         image = nova.servers.get(server=image_id)
#         print("\t"+image.status)
#         if image.status == "ACTIVE":
#             break
# else:
#     print("Stopping server")
#     image.stop()
#     while True:
#         time.sleep(5)
#         image = nova.servers.get(server=image_id)
#         print("\t"+image.status)
#         if image.status == "SHUTOFF":
#             break
#
#     print("Starting server")
#     image.start()