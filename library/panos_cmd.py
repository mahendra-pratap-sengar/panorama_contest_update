#!/usr/bin/python3

'''
@author: mahendra.pratap.sengar@kyndryl.com
@date: 03rd Jan. 2025
@description: This module runns all the OP&CMD xml based commands on Panorama or paloalto devices.
'''

import base64
import urllib3
import requests
import xml.etree.ElementTree as ET
from ansible.module_utils.basic import AnsibleModule

def xml_to_dict(element):
    """Convert an XML element to a dictionary."""
    if len(element) == 0:
        return element.text.strip() if element.text else None
    
    result = {}
    for child in element:
        if child.tag not in result:
            result[child.tag] = []
        result[child.tag].append(xml_to_dict(child))
    
    for key in result:
        if len(result[key]) == 1:
            result[key] = result[key][0]
    
    return result

def get_system_info(url, headers):
    """API request and return system info in dictionary format"""
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        # Parsing XML
        root = ET.fromstring(response.content)
        result_dict = xml_to_dict(root)
        return result_dict
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def run_module():
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True), 
        fw_ip_address=dict(type='list', required=True),
        xml_command=dict(type='str', required=True),
        xml_elements=dict(type='list', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    username = module.params['username']
    password = module.params['password']
    fw_ip_address = module.params['fw_ip_address']
    xml_command = module.params['xml_command']
    xml_elements = module.params['xml_elements']
    
    credentials = f"{username}:{password}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {b64_credentials}'
    }

    # results = {}

    try:
        for ip in fw_ip_address:
            api_url = f"https://{ip}/api/?type=op&cmd={xml_command}"
            urllib3.disable_warnings()
            api_request = requests.get(url=api_url, headers=headers, verify=False)
            api_response = api_request.text
            
            # Parse XML response
            xml_tree_root = ET.fromstring(api_response)

            firewall_data = {}
            for tag in xml_elements:
                for leaf in xml_tree_root.iter(tag):
                    if leaf.tag == tag:
                        firewall_data[tag] = xml_to_dict(leaf)

            # results[ip] = firewall_data

        module.exit_json(changed=False, json_output=firewall_data)

    except Exception as e:
        module.fail_json(msg=f"ERROR: Connection Error. Check the Firewall IP Address List and API Key. {str(e)}")

def main():
    run_module()

if __name__ == '__main__':
    main()