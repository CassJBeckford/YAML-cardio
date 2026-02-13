#1

```yaml
---
  - host: localhost
    connection: local 
    task:
      -name: Hello Ansible 
      debug:
        msg: "Hello Ansible"
---

#2

```yaml
---
  - host: localHost 
    connection: local 
    task:
      -name: Create file 
      copy: 
        content: "Created by Ansible"
        dest: /tmp/ansible-test.txt
---

#3

```yaml
---
  - host: localHost 
    connection: local 
    vars:
      app_name: MyApp
      app_version: 2.0
    task: 
      -name: print varibales 
      debug:
        msg: "app name: {{ app_name }}. version: {{ app_version }}"
---

#4

```yaml
---
  - host: localHost 
    connection: local 
    task: 
      - name: create directory 
        file:
          path: /tmp/ansible-demo
          state: directory

      - name: create file in directory 
        copy: 
          content: "create file in directory"
          dest: /tmp/ansible-demo/ansible-test.txt
      
      - name: print success 
        debug:
          msg: "Directory successfully created"
---
#5

```yaml
---
  - host: localHost
    connection: local 
    task: 
      - name: create multiple files 
        copy: 
          content: "loop files"
          dest: /tmp/ansible-demo/{{ item }}.txt
        loop: 
          - file1
          - file2
          - file3
---
#6

```yaml
---
  - hosts: localHost
    connection: local 
    vars: 
      environment: "dev"
    tasks:
      - name: return conditonal 
        debug:
          msg: "dev"
        when: environment == "dev"  
      - name: return conditonal 
        debug:
          msg: "prod"
        when: environment == "prod"
---

#7

inventory.ini:
```ini
[local]
localHost
[local:vars]
ansible_connection=local
```
Playbook (07_inventory_files.yml):
```yaml
---
  - host: local 
    task: 
    - name: "return success"
      debug:
        msg: "inventory file created"
---

Run: "ansible-playbook -i inventory.ini 07_inventory_files.yml "

#8

```yaml
---
  - hosts: localHost
    connection: local 
    tasks:
      - name: "create file"
        copy:
          content: "file with changes"
          dest: /tmp/ansible-demo/example.conf
        notify: config_change
    handlers: 
    - name: config_change
      debug:
        msg: "changes detected"
---

#9


