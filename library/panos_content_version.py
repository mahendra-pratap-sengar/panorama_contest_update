#!/usr/bin/python3

'''
@author: mahendras.tulipit@gmail.com
@date: 03rd Jan. 2025
@description: This module is developed specifically for this use case where the information is required to be filterd from json input.
'''

import json
from ansible.module_utils.basic import AnsibleModule

def check_updates(json_data, target_version):
    """Check for updates with the specified version."""
    # Load JSON data
    data = json.loads(json_data)

    updates_with_version = []

    # Iterate over entries
    for entry in data.get("content-updates", {}).get("entry", []):
        version = entry.get("version")

        # Check if the version matches the target version
        if version == target_version:
            updates_with_version.append(entry)

    return updates_with_version

def run_module():
    module_args = dict(
        json_data=dict(type='str', required=True),
        target_version=dict(type='str', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    json_data = module.params['json_data']
    target_version = module.params['target_version']

    try:
        updates_found = check_updates(json_data, target_version)
        
        if updates_found:
            module.exit_json(changed=False, updates=updates_found)
        else:
            module.exit_json(changed=False, updates=[])

    except Exception as e:
        module.fail_json(msg=f"ERROR: {str(e)}")

def main():
    run_module()

if __name__ == '__main__':
    main()
