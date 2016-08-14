#!/usr/bin/python
# Copyright header....

DOCUMENTATION = '''
---
# Documentation is yaml file, template: https://github.com/ansible/ansible/blob/devel/examples/DOCUMENTATION.yml.
# If a key doesn't apply to your module (ex: choices, default, or
# aliases) you can use the word 'null', or an empty list, [], where
# appropriate.
module: modulename
short_description: This is a sentence describing the module
description:
    - Longer description of the module
    - You might include instructions
version_added: "X.Y"
author: "Your AWESOME name, @awesome-github-id"
notes:
    - Other things consumers of your module should know
requirements:
    - list of required things
    - like the factor package
    - or a specific platform
options:
# One or more of the following
    option_name:
        description:
            - Words go here
            - that describe
            - this option
        required: true or false
        default: a string or the word null
        choices: [list, of, choices]
        aliases: [list, of, aliases]
version_added: 1.X
'''

EXAMPLES = '''
- action: modulename opt1=arg1 opt2=arg2

### play.yml
- hosts: localhost
  tasks:
    - name: Test that my module works
      github_repo:
      register: result

    - debug: var=result
### ansible-playbook play.yml
'''

RETURN = '''
dest:
    description: destination file/path
    returned: success
    type: string
    sample: "/path/to/file.txt"
src:
    description: source file used for the copy on the target machine
    returned: changed
    type: string
    sample: "/home/httpd/.ansible/tmp/ansible-tmp-1423796390.97-147729857856000/source"
md5sum:
    description: md5 checksum of the file after running copy
    returned: when supported
    type: string
    sample: "2a5aeecc61dc98c4d780b14b330e3282"
...
'''


from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec = dict(
            state     = dict(default='present', choices=['present', 'absent']),
            name      = dict(required=True),
            enabled   = dict(required=True, type='bool'),
            something = dict(aliases=['whatever'])
        )
    )
    response = {"hello":"world"}
    module.exit_json(changed=False, meta=response)
    #module.exit_json(changed=True, something_else=12345)
    #module.fail_json(msg="Something fatal happened")

if __name__ == '__main__':
    main()

