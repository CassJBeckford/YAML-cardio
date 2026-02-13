# Ansible Exercise Solutions

## Exercise 1: Hello World
```yaml
---
- hosts: localhost
  connection: local
  tasks:
    - name: Print hello message
      debug:
        msg: "Hello from Ansible!"
```

## Exercise 2: Create a File
```yaml
---
- hosts: localhost
  connection: local
  tasks:
    - name: Create a test file
      copy:
        content: "Created by Ansible"
        dest: /tmp/ansible-test.txt
```

## Exercise 3: Variables
```yaml
---
- hosts: localhost
  connection: local
  vars:
    app_name: "MyApp"
    app_version: "2.0"
  tasks:
    - name: Print app name
      debug:
        msg: "Application: {{ app_name }}"
    
    - name: Print app version
      debug:
        msg: "Version: {{ app_version }}"
```

## Exercise 4: Multiple Tasks
```yaml
---
- hosts: localhost
  connection: local
  tasks:
    - name: Create directory
      file:
        path: /tmp/ansible-demo
        state: directory
    
    - name: Create file in directory
      copy:
        content: "Demo file"
        dest: /tmp/ansible-demo/demo.txt
    
    - name: Print success message
      debug:
        msg: "Directory and file created successfully!"
```

## Exercise 5: Loops
```yaml
---
- hosts: localhost
  connection: local
  tasks:
    - name: Create multiple files
      copy:
        content: "File {{ item }}"
        dest: "/tmp/{{ item }}.txt"
      loop:
        - file1
        - file2
        - file3
```

## Exercise 6: Conditionals
```yaml
---
- hosts: localhost
  connection: local
  vars:
    environment: "dev"
  tasks:
    - name: Print message for dev
      debug:
        msg: "Running in DEVELOPMENT environment"
      when: environment == "dev"
    
    - name: Print message for prod
      debug:
        msg: "Running in PRODUCTION environment"
      when: environment == "prod"
```

## Exercise 7: Inventory File

inventory.ini:
```ini
[local]
localhost ansible_connection=local
```

Playbook (07-inventory.yml):
```yaml
---
- hosts: local
  tasks:
    - name: Test inventory
      debug:
        msg: "Connected using inventory file!"
```

Run: `ansible-playbook -i inventory.ini 07-inventory.yml`

## Exercise 8: Handlers
```yaml
---
- hosts: localhost
  connection: local
  tasks:
    - name: Create config file
      copy:
        content: "config_value=123"
        dest: /tmp/app.conf
      notify: config_updated
  
  handlers:
    - name: config_updated
      debug:
        msg: "Configuration updated!"
```

## Exercise 9: Templates

template.j2:
```
Application: {{ app_name }}
Version: {{ app_version }}
Environment: {{ env }}
```

Playbook (09-templates.yml):
```yaml
---
- hosts: localhost
  connection: local
  vars:
    app_name: "MyApp"
    app_version: "3.0"
    env: "production"
  tasks:
    - name: Deploy template
      template:
        src: template.j2
        dest: /tmp/config.txt
```

## Exercise 10: Full Playbook
```yaml
---
- hosts: localhost
  connection: local
  vars:
    app_name: "FullApp"
    version: "1.0"
    environments:
      - dev
      - staging
      - prod
    create_backup: true
  
  tasks:
    - name: Create application directories
      file:
        path: "/tmp/{{ app_name }}/{{ item }}"
        state: directory
      loop: "{{ environments }}"
    
    - name: Deploy config files
      copy:
        content: "Config for {{ item }}"
        dest: "/tmp/{{ app_name }}/{{ item }}/config.txt"
      loop: "{{ environments }}"
      notify: configs_deployed
    
    - name: Create backup
      copy:
        content: "Backup created"
        dest: "/tmp/{{ app_name }}/backup.txt"
      when: create_backup == true
    
    - name: Print summary
      debug:
        msg: "{{ app_name }} v{{ version }} deployed to {{ environments | length }} environments"
  
  handlers:
    - name: configs_deployed
      debug:
        msg: "All configurations have been deployed!"
```

## Exercise 11: Roles

Directory structure (created with `ansible-galaxy init roles/webserver`):
```
roles/
  webserver/
    tasks/
      main.yml
    defaults/
      main.yml
```

roles/webserver/tasks/main.yml:
```yaml
---
- name: Create web root directory
  file:
    path: /var/www/html
    state: directory

- name: Deploy index.html
  copy:
    content: "<h1>Welcome to {{ server_name }}</h1>"
    dest: /var/www/html/index.html
```

roles/webserver/defaults/main.yml:
```yaml
---
server_name: "MyWebServer"
```

Playbook (11-roles.yml):
```yaml
---
- hosts: localhost
  connection: local
  roles:
    - webserver
```

## Exercise 12: Registered Variables
```yaml
---
- hosts: localhost
  connection: local
  tasks:
    - name: Get hostname
      command: hostname
      register: host_info

    - name: Print hostname
      debug:
        msg: "Hostname is: {{ host_info.stdout }}"
```

## Exercise 13: Include & Import

tasks/install.yml:
```yaml
---
- name: Install step
  debug:
    msg: "Installing..."
```

tasks/configure.yml:
```yaml
---
- name: Configure step
  debug:
    msg: "Configuring..."
```

Playbook (13-include.yml):
```yaml
---
- hosts: localhost
  connection: local
  tasks:
    - name: Run install tasks
      include_tasks: tasks/install.yml

    - name: Run configure tasks
      include_tasks: tasks/configure.yml
```

## Exercise 14: Blocks and Rescue
```yaml
---
- hosts: localhost
  connection: local
  tasks:
    - name: Error handling example
      block:
        - name: This task will succeed
          debug:
            msg: "Starting operation..."

        - name: This task will fail
          command: /nonexistent/path/script.sh

        - name: This will not run
          debug:
            msg: "This should not appear"

      rescue:
        - name: Handle the failure
          debug:
            msg: "Task failed, running recovery"

      always:
        - name: Always run this
          debug:
            msg: "Cleanup complete"
```

## Exercise 15: Facts and Gathering
```yaml
---
- hosts: localhost
  connection: local
  gather_facts: true
  tasks:
    - name: Print OS family
      debug:
        msg: "OS Family: {{ ansible_os_family }}"

    - name: Print distribution
      debug:
        msg: "Distribution: {{ ansible_distribution }}"

    - name: Print hostname
      debug:
        msg: "Hostname: {{ ansible_hostname }}"
```

## Exercise 16: Vault Basics

secret_vars.yml (before encryption):
```yaml
---
db_password: supersecret
```

Encrypt: `ansible-vault encrypt secret_vars.yml`

Playbook (16-vault.yml):
```yaml
---
- hosts: localhost
  connection: local
  vars_files:
    - secret_vars.yml
  tasks:
    - name: Print secret (not recommended in real use!)
      debug:
        msg: "DB Password is: {{ db_password }}"
```

Run: `ansible-playbook 16-vault.yml --ask-vault-pass`

## Exercise 17: Tags
```yaml
---
- hosts: localhost
  connection: local
  tasks:
    - name: Setup task
      debug:
        msg: "Running setup..."
      tags: setup

    - name: Deploy task
      debug:
        msg: "Deploying application..."
      tags: deploy

    - name: Cleanup task
      debug:
        msg: "Cleaning up..."
      tags: cleanup
```

Run examples:
- `ansible-playbook 17-tags.yml --tags deploy`
- `ansible-playbook 17-tags.yml --skip-tags cleanup`

## Exercise 18: Ansible Lint

Install:
```bash
pip install ansible-lint
```

Run against a playbook:
```bash
ansible-lint 10-full.yml
```

Common fixes:
- Add `name:` to all tasks
- Use FQCN (e.g., `ansible.builtin.debug` instead of `debug`)
- Fix trailing whitespace
- Correct indentation

## Exercise 19: Dynamic Inventory Script

inventory.py:
```python
#!/usr/bin/env python3
import json

inventory = {
    "local": {
        "hosts": ["localhost"],
        "vars": {
            "ansible_connection": "local"
        }
    },
    "_meta": {
        "hostvars": {}
    }
}

print(json.dumps(inventory))
```

Make executable: `chmod +x inventory.py`

Run: `ansible-playbook -i inventory.py 07-inventory.yml`

## Exercise 20: Multi-Play Playbook

inventory-multi.ini:
```ini
[local]
localhost ansible_connection=local

[webservers]
webserver1 ansible_connection=local
webserver2 ansible_connection=local
```

Playbook (20-multi-play.yml):
```yaml
---
- name: Setup localhost
  hosts: localhost
  connection: local
  tasks:
    - name: Localhost message
      debug:
        msg: "Setting up localhost"

- name: Deploy to webservers
  hosts: webservers
  tasks:
    - name: Webserver message
      debug:
        msg: "Deploying to webservers"
```

Run: `ansible-playbook -i inventory-multi.ini 20-multi-play.yml`
