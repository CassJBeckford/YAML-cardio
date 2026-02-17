#1

```yaml
---
  - host: localhost
    connection: local 
    task:
      -name: Hello Ansible 
      debug:
        msg: "Hello Ansible"
```

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
```

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
```

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
```
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
```
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
```

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
```

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
```

#9

template.j2:
```
Appliation: {{ app_name }} 
Version: {{ app_version }} 
Environment: {{ env }}
```

Playbook (09_Jinja_template.yml)
```yaml 
---
  - host: localHost 
    connection: local
    vars:
      app_name: "template.js"
      app_version: 2.0
      env: production
    tasks:
      - name: Deply template 
        template: 
          src: template.j2
          dest: 
```

#10

```yml 
---

  - host: LocalHost
    connection: local 
    vars:
      app_name: "example name"
      app_version: "2.0"
      env:
      - dev
      - prod
      - other 
      create_backup: true 
    tasks:
      - name: Create directory  
        file: 
          path: tmp/{{ app_name }}/{{ item }}
          state: directory
        loop: "{{ environments }}"
      
      - name: Create config files
        copy:
          content: "config files"
          dest: tmp/{{ app_name }}/{{ item }}/config.txt
        loop: "{{ environments }}"
        notiy: config_creation

      - name: Print summary 
        debug:
          msg: "{{ app_name }} version {{ app_version }} has been deployed to {{ environments | length }} environments."

      - name: Create Backup
        copy:
          content: "backup created"
          dest: tmp/{{ item }}/backup.txt
        when: create_backup == true

    handler:
      - name: config_creation
        debug:
          msg: "all configurations have been deployed "
      
```

#11

'ansible-galaxy init roles/webserver'

(
  webserver/ 
    task/ 
      main.yaml
    default/
      main.yaml
)

role/webserver/task/main.yml:
```yaml 
---
      - name: Create web root directory
        file: 
          path: /var/www/html
          state: directory 

      - name: deploy html folder
        copy: 
          content: "<p>test<p>"
          dir: /var/www/html/index.html
```

role/webserver/default/main.yml:
```yaml
---
  server_name: "test_server"
```

Playbook (11_roles.yml)
```yaml 
---
  - host: localHost
    connection: local
    roles: 
      - webserver
```

#12

```yaml
---
  - host: localHost
    connection: local
    task:

    - name:
      command: hostname 
      register: host_info 

    - name:
      debug:
        msg: "message: {{ host_info.stdout }}"
```

#13

tasks/install.yml
```yaml
---
  - name: "Install"
    debug:
      msg: "Installing…"
```

tasks/configure.yml
```yaml
---
  - name: "configure"
    debug:
      msg: "Configuring..."
```

Playbook (13_include_and_import)
```yaml
---
  - hosts: localHost
    connection: local 
    tasks:
      - name: "Include install"
        include_tasks:
            file: tasks/install.yml

      - name: "Include config"
        include_tasks:
            file: tasks/configure.yml
```