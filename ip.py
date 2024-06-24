import boto3
import csv

def list_elastic_ips():
    # Create a session using Boto3
    session = boto3.Session()
    
    # Create EC2 client
    ec2_client = session.client('ec2')
    
    # Describe Elastic IPs
    elastic_ips = ec2_client.describe_addresses()
    
    # Create a list to hold the data
    data = []
    
    # Fetch all NAT Gateways to create a lookup
    nat_gateways = ec2_client.describe_nat_gateways()
    nat_gateway_ids = {nat['NatGatewayAddresses'][0]['NetworkInterfaceId']: nat['NatGatewayId'] for nat in nat_gateways['NatGateways']}

    # Iterate through Elastic IPs
    for address in elastic_ips['Addresses']:
        allocation_id = address.get('AllocationId')
        public_ip = address.get('PublicIp')
        instance_id = address.get('InstanceId')
        network_interface_id = address.get('NetworkInterfaceId')
        
        if instance_id:
            resource_type = 'EC2 Instance'
            resource_id = instance_id
        elif network_interface_id and network_interface_id in nat_gateway_ids:
            resource_type = 'NAT Gateway'
            resource_id = nat_gateway_ids[network_interface_id]
        else:
            resource_type = 'Not Assigned'
            resource_id = 'N/A'
        
        data.append([allocation_id, public_ip, resource_type, resource_id])
    
    # Define CSV file path
    csv_file_path = '/home/cloudshell-user/ips.csv'  # CloudShell's home directory
    
    # Write data to CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['AllocationId', 'PublicIp', 'ResourceType', 'ResourceId'])
        writer.writerows(data)
    
    print(f"Elastic IPs data has been written to {csv_file_path}")

if __name__ == "__main__":
    list_elastic_ips()