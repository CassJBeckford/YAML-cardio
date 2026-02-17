# Ansible Practice Exercises

## Setup
Before starting, ensure Ansible is installed:
```bash
pip install ansible
```

## Exercise 1: Hello World Playbook
**Goal:** Create your first playbook that prints a message

Create a file called `01-hello.yml` that:
- Targets localhost
- Uses the `debug` module to print "Hello from Ansible!"

<details>
<summary>Hint</summary>
Use `hosts: localhost` and `connection: local`
</details>

**Learn more:** [Ansible Playbooks Introduction](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html)

---

## Exercise 2: Create a File
**Goal:** Use Ansible to create a file on your system

Create `02-create-file.yml` that:
- Creates a file at `/tmp/ansible-test.txt` (or `C:\temp\ansible-test.txt` on Windows)
- Sets the content to "Created by Ansible"
- Uses the `copy` module with `content` parameter

**Learn more:** [Copy Module Documentation](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html)

---

## Exercise 3: Variables
**Goal:** Learn to use variables in playbooks

Create `03-variables.yml` that:
- Defines a variable called `app_name` with value "MyApp"
- Defines a variable called `app_version` with value "2.0"
- Uses `debug` to print both variables

**Learn more:** [Using Variables](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html)

---

## Exercise 4: Multiple Tasks
**Goal:** Chain multiple tasks together

Create `04-multiple-tasks.yml` that:
- Creates a directory
- Creates a file inside that directory
- Prints a success message

**Learn more:** [Tasks in Playbooks](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html#tasks-list)

---

## Exercise 5: Loops
**Goal:** Use loops to repeat tasks

Create `05-loops.yml` that:
- Creates 3 files named `file1.txt`, `file2.txt`, `file3.txt`
- Uses `loop` to avoid repeating code

**Learn more:** [Loops Documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html)

---

## Exercise 6: Conditionals
**Goal:** Run tasks based on conditions

Create `06-conditionals.yml` that:
- Sets a variable `environment` to either "dev" or "prod"
- Prints different messages based on the environment value
- Uses `when` condition

**Learn more:** [Conditionals Documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_conditionals.html)

---

## Exercise 7: Inventory File
**Goal:** Work with inventory files

Create an inventory file `inventory.ini` with:
- A group called `[local]` containing localhost
- Set `ansible_connection=local`

Then create a playbook that uses this inventory.

**Learn more:** [Ansible Inventory Documentation](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html)

---

## Exercise 8: Handlers
**Goal:** Use handlers for triggered actions

Create `08-handlers.yml` that:
- Creates a config file
- Notifies a handler when the file changes
- Handler prints "Configuration updated!"

**Learn more:** [Ansible Handlers Documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html)

---

## Exercise 9: Templates
**Goal:** Use Jinja2 templates

Create a template file and a playbook that:
- Uses variables in a template (application / version / environemnt)
- Deploys the template to a file

**Learn more:** [Ansible Templates Documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_templating.html)

---

## Exercise 10: Full Playbook
**Goal:** Combine everything you've learned

Create a playbook that:
- Uses variables
- Creates directory structure
- Deploys configuration files
- Uses conditionals
- Has handlers
- Uses loops

**Learn more:** [Playbook Best Practices](https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html)

---

## Exercise 11: Roles
**Goal:** Organise tasks into reusable roles

Create a role called `webserver`:
- Use `ansible-galaxy init roles/webserver` to scaffold
- Add tasks that create an `/var/www/html` directory and deploy an `index.html`
- Call the role from `11-roles.yml`

**Learn more:** [Ansible Roles Documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)

---

## Exercise 12: Registered Variables
**Goal:** Capture task output and use it later

Create `12-register.yml` that:
- Runs `hostname` (or `$env:COMPUTERNAME` on Windows) using the `command` module
- Registers the result to a variable called `host_info`
- Prints `host_info.stdout` with `debug`

**Learn more:** [Registered Variables](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#registering-variables)

---

## Exercise 13: Include & Import
**Goal:** Split playbooks into smaller files

Create three files:
1. `tasks/install.yml` – a task list that prints "Installing…"
2. `tasks/configure.yml` – a task list that prints "Configuring…"
3. `13-include.yml` – includes both task files with `include_tasks` or `import_tasks`

**Learn more:** [Including and Importing](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse.html)

---

## Exercise 14: Blocks and Rescue
**Goal:** Handle errors gracefully

Create `14-blocks.yml` that:
- Wraps tasks in a `block`
- Intentionally fails one task (e.g., copy to a non-existent path)
- Uses `rescue` to print "Task failed, running recovery"
- Uses `always` to print "Cleanup complete"

**Learn more:** [Blocks Documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_blocks.html)

---

## Exercise 15: Facts and Gathering
**Goal:** Use system facts in playbooks

Create `15-facts.yml` that:
- Gathers facts automatically (default behaviour)
- Prints `ansible_os_family`, `ansible_distribution`, and `ansible_hostname`

Try running with `gather_facts: false` and observe the difference.

**Learn more:** [Discovering Variables: Facts](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_vars_facts.html)

---

## Exercise 16: Vault Basics
**Goal:** Encrypt sensitive data

1. Create a vars file `secret_vars.yml` with `db_password: supersecret`
2. Encrypt it: `ansible-vault encrypt secret_vars.yml`
3. Create `16-vault.yml` that includes the encrypted file and prints `db_password`
4. Run with `--ask-vault-pass`

**Learn more:** [Ansible Vault Documentation](https://docs.ansible.com/ansible/latest/vault_guide/index.html)

---

## Exercise 17: Tags
**Goal:** Run selective parts of a playbook

Create `17-tags.yml` with three tasks:
- Task 1 tagged `setup`
- Task 2 tagged `deploy`
- Task 3 tagged `cleanup`

Run only one tag: `ansible-playbook 17-tags.yml --tags deploy`

**Learn more:** [Tags Documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tags.html)

---

## Exercise 18: Ansible Lint
**Goal:** Validate playbook quality

Install ansible-lint:
```bash
pip install ansible-lint
```

Run it against any playbook:
```bash
ansible-lint 10-full.yml
```

Fix at least two warnings or errors it reports.

**Learn more:** [Ansible Lint Documentation](https://ansible.readthedocs.io/projects/lint/)

---

## Exercise 19: Dynamic Inventory Script
**Goal:** Generate inventory at runtime

Create `inventory.py` (or `.ps1` on Windows) that outputs JSON:
```json
{
  "local": {
    "hosts": ["localhost"],
    "vars": { "ansible_connection": "local" }
  }
}
```

Run: `ansible-playbook -i inventory.py 07_inventory_files.yml`

**Learn more:** [Dynamic Inventory](https://docs.ansible.com/ansible/latest/inventory_guide/intro_dynamic_inventory.html)

---

## Exercise 20: Multi-Play Playbook
**Goal:** Combine multiple plays in one file

Create `20-multi-play.yml` containing two plays:
1. Play 1 targets `localhost`, prints "Setting up localhost"
2. Play 2 targets a group called `webservers` (define in inventory), prints "Deploying to webservers"

Use a single inventory file that defines both `localhost` and `webservers`.

---

## Running Your Playbooks

Basic command:
```bash
ansible-playbook playbook.yml
```

With inventory:
```bash
ansible-playbook -i inventory.ini playbook.yml
```

Verbose mode (for debugging):
```bash
ansible-playbook playbook.yml -v
```

## Tips
- Start simple and test each playbook
- Use `--check` flag for dry-run mode
- Use `-v`, `-vv`, or `-vvv` for increasing verbosity
- YAML is sensitive to indentation (use 2 spaces)
