from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient

credential = AzureCliCredential()

subscription_id = "YOUR_SUBSCRIPTION_ID"
resource_group = "my-resource-group"
vm_name = "my-vm"

client = ComputeManagementClient(credential, subscription_id)

client.virtual_machines.begin_start(resource_group, vm_name)
print("VM starting")

client.virtual_machines.begin_power_off(resource_group, vm_name)
print("VM stopping")
