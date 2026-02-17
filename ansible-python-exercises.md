# Ansible + Python Exercises

These exercises combine Python programming with Ansible automation concepts.

## Setup
```bash
pip install ansible ansible-runner pyyaml jinja2
```

---

## Exercise 1: Parse YAML Inventory
**Goal:** Read and parse an Ansible inventory file with Python

Write a Python script `01_parse_inventory.py` that:
- Reads an inventory file (INI or YAML format)
- Prints all hosts and their groups
- Uses the `pyyaml` library for YAML parsing

```python
# Starter code
import yaml

def parse_inventory(filepath):
    # Your code here
    pass
```

**Learn more:** 
- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Ansible Inventory Format](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html)
- [Python File I/O](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)

---

## Exercise 2: Generate Playbook from Python
**Goal:** Dynamically create an Ansible playbook using Python

Write `02_generate_playbook.py` that:
- Takes user input for: target hosts, task name, module to use
- Generates a valid YAML playbook
- Saves it to a `.yml` file

**Learn more:** 
- [PyYAML: Dumping YAML](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Ansible Playbook Structure](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html)
- [Python input() Function](https://docs.python.org/3/library/functions.html#input)

---

## Exercise 3: Jinja2 Template Rendering
**Goal:** Use Python to render Ansible-style templates

Write `03_jinja_render.py` that:
- Loads a Jinja2 template file
- Accepts variables as a dictionary
- Renders and outputs the result

```python
from jinja2 import Environment, FileSystemLoader

# Template example (save as templates/config.j2):
# server_name: {{ server_name }}
# port: {{ port }}
# environment: {{ env }}
```

**Learn more:** 
- [Jinja2 Documentation](https://jinja.palletsprojects.com/en/3.1.x/)
- [Jinja2 API](https://jinja.palletsprojects.com/en/3.1.x/api/)
- [Ansible Templates](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_templating.html)

---

## Exercise 4: YAML Validator
**Goal:** Validate Ansible playbook syntax

Write `04_yaml_validator.py` that:
- Reads a YAML file
- Checks for valid YAML syntax
- Validates required Ansible keys (`hosts`, `tasks`)
- Reports errors clearly

**Learn more:** 
- [PyYAML safe_load](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)
- [Ansible Playbook Structure](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html)

---

## Exercise 5: Dynamic Inventory Script
**Goal:** Create a dynamic inventory for Ansible

Write `05_dynamic_inventory.py` that:
- Outputs JSON in Ansible's dynamic inventory format
- Supports `--list` and `--host <hostname>` arguments
- Returns host groups and variables

```python
#!/usr/bin/env python3
import json
import argparse

def get_inventory():
    return {
        "webservers": {
            "hosts": ["web1.example.com", "web2.example.com"],
            "vars": {"http_port": 80}
        },
        "_meta": {
            "hostvars": {}
        }
    }

# Add argument parsing for --list and --host
```

**Learn more:** 
- [Dynamic Inventory](https://docs.ansible.com/ansible/latest/inventory_guide/intro_dynamic_inventory.html)
- [Python argparse](https://docs.python.org/3/library/argparse.html)
- [Python json Module](https://docs.python.org/3/library/json.html)

---

## Exercise 6: Run Ansible Playbook from Python
**Goal:** Execute playbooks programmatically

Write `06_run_playbook.py` that:
- Uses `ansible-runner` to execute a playbook
- Captures and prints the output
- Handles success/failure status

```python
import ansible_runner

def run_playbook(playbook_path, inventory_path):
    r = ansible_runner.run(
        playbook=playbook_path,
        inventory=inventory_path
    )
    print(f"Status: {r.status}")
    print(f"Return code: {r.rc}")
```

**Learn more:** 
- [ansible-runner Documentation](https://ansible.readthedocs.io/projects/runner/en/stable/)
- [ansible-runner Python API](https://ansible.readthedocs.io/projects/runner/en/stable/python_interface.html)

---

## Exercise 7: Host Facts Collector
**Goal:** Collect and process Ansible facts with Python

Write `07_facts_collector.py` that:
- Runs `ansible -m setup` against localhost
- Parses the JSON output
- Extracts and displays: OS, memory, CPU info

**Learn more:** 
- [Ansible Facts](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_vars_facts.html)
- [Python subprocess Module](https://docs.python.org/3/library/subprocess.html)
- [Setup Module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/setup_module.html)

---

## Exercise 8: Inventory Diff Tool
**Goal:** Compare two inventory files

Write `08_inventory_diff.py` that:
- Reads two inventory files
- Compares hosts and groups
- Reports: added hosts, removed hosts, changed groups

**Learn more:** 
- [Python Sets](https://docs.python.org/3/tutorial/datastructures.html#sets)
- [Ansible Inventory](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html)
- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)

---

## Exercise 9: Playbook Task Counter
**Goal:** Analyse playbook complexity

Write `09_task_counter.py` that:
- Reads a playbook YAML file
- Counts: total tasks, handlers, plays
- Lists all modules used
- Outputs a summary report

**Learn more:** 
- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Python Collections](https://docs.python.org/3/library/collections.html)
- [Ansible Playbook Structure](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html)

---

## Exercise 10: Variable Extractor
**Goal:** Extract all variables from playbooks

Write `10_var_extractor.py` that:
- Scans a playbook for `{{ variable }}` patterns
- Lists all unique variables used
- Checks if they're defined in `vars:` section
- Reports undefined variables

```python
import re
import yaml

def extract_variables(playbook_path):
    # Use regex to find {{ var }} patterns
    pattern = r'\{\{\s*(\w+)\s*\}\}'
    # Your code here
```

**Learn more:** 
- [Python Regular Expressions](https://docs.python.org/3/library/re.html)
- [Ansible Variables](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html)
- [regex101 (Testing Tool)](https://regex101.com/)

---

## Exercise 11: Role Scaffolder
**Goal:** Create Ansible role directory structure

Write `11_role_scaffold.py` that:
- Takes a role name as input
- Creates the standard role directory structure:
  ```
  roles/
  └── <role_name>/
      ├── tasks/main.yml
      ├── handlers/main.yml
      ├── templates/
      ├── files/
      ├── vars/main.yml
      ├── defaults/main.yml
      └── meta/main.yml
  ```
- Adds placeholder content to YAML files

**Learn more:** 
- [Ansible Roles](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)
- [Python os.makedirs](https://docs.python.org/3/library/os.html#os.makedirs)
- [Python pathlib](https://docs.python.org/3/library/pathlib.html)

---

## Exercise 12: Encrypted Vars Handler
**Goal:** Work with Ansible Vault in Python

Write `12_vault_helper.py` that:
- Uses `ansible-vault` CLI via subprocess
- Provides functions to: encrypt, decrypt, view vault files
- Handles password input securely

```python
import subprocess
import getpass

def encrypt_file(filepath):
    password = getpass.getpass("Vault password: ")
    # Use subprocess to run ansible-vault encrypt
```

**Learn more:** 
- [Ansible Vault](https://docs.ansible.com/ansible/latest/vault_guide/index.html)
- [Python subprocess Module](https://docs.python.org/3/library/subprocess.html)
- [Python getpass Module](https://docs.python.org/3/library/getpass.html)

---

## Exercise 13: Playbook Linter
**Goal:** Build a simple playbook linter

Write `13_playbook_linter.py` that checks for:
- Tasks without `name` field
- Use of `shell` module when `command` would work
- Missing `become` for privileged operations
- Hardcoded passwords in plain text

**Learn more:** 
- [ansible-lint](https://ansible.readthedocs.io/projects/lint/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html)
- [Python Pattern Matching](https://docs.python.org/3/library/re.html)

---

## Exercise 14: Execution Report Generator
**Goal:** Parse Ansible output and create reports

Write `14_report_generator.py` that:
- Parses Ansible JSON callback output
- Generates an HTML or Markdown report
- Shows: passed/failed/skipped tasks per host
- Includes timestamps and duration

**Learn more:** 
- [Ansible Callback Plugins](https://docs.ansible.com/ansible/latest/plugins/callback.html)
- [Python json Module](https://docs.python.org/3/library/json.html)
- [Python datetime Module](https://docs.python.org/3/library/datetime.html)

---

## Exercise 15: Host Pattern Matcher
**Goal:** Implement Ansible-style host patterns

Write `15_pattern_matcher.py` that:
- Takes an inventory and a pattern (e.g., `web*`, `!db*`, `web:&staging`)
- Returns matching hosts
- Supports: wildcards, negation, intersection

```python
def match_hosts(inventory, pattern):
    # Implement Ansible-style pattern matching
    pass

# Examples:
# match_hosts(inv, "web*")  -> all hosts starting with 'web'
# match_hosts(inv, "all:!db")  -> all except db hosts
```

**Learn more:** 
- [Ansible Patterns](https://docs.ansible.com/ansible/latest/inventory_guide/intro_patterns.html)
- [Python fnmatch Module](https://docs.python.org/3/library/fnmatch.html)
- [Python Set Operations](https://docs.python.org/3/library/stdtypes.html#set)

---

## Exercise 16: Module Documentation Parser
**Goal:** Extract module info from Ansible

Write `16_module_docs.py` that:
- Uses `ansible-doc -j <module>` to get module documentation
- Parses the JSON output
- Displays: description, parameters, examples

**Learn more:** 
- [ansible-doc Command](https://docs.ansible.com/ansible/latest/cli/ansible-doc.html)
- [Python subprocess Module](https://docs.python.org/3/library/subprocess.html)
- [Python json Module](https://docs.python.org/3/library/json.html)

---

## Exercise 17: Playbook Merger
**Goal:** Combine multiple playbooks

Write `17_playbook_merger.py` that:
- Takes multiple playbook files as input
- Merges them into a single playbook
- Handles duplicate variable names
- Outputs the combined playbook

**Learn more:** 
- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Python Deep Copy](https://docs.python.org/3/library/copy.html)
- [Ansible Playbook Structure](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html)

---

## Exercise 18: Connection Tester
**Goal:** Test connectivity to inventory hosts

Write `18_connection_tester.py` that:
- Reads an inventory file
- Tests SSH/WinRM connectivity to each host
- Uses `ansible -m ping`
- Reports reachable/unreachable hosts

**Learn more:** 
- [Ansible Ping Module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/ping_module.html)
- [Python subprocess Module](https://docs.python.org/3/library/subprocess.html)
- [Ansible Connection Methods](https://docs.ansible.com/ansible/latest/plugins/connection.html)

---

## Exercise 19: Config File Generator
**Goal:** Generate ansible.cfg programmatically

Write `19_config_generator.py` that:
- Accepts configuration options as arguments or prompts
- Generates a valid `ansible.cfg` file
- Includes: inventory path, remote user, SSH settings

**Learn more:** 
- [Ansible Configuration File](https://docs.ansible.com/ansible/latest/reference_appendices/config.html)
- [Python configparser Module](https://docs.python.org/3/library/configparser.html)
- [Python argparse](https://docs.python.org/3/library/argparse.html)

---

## Exercise 20: Full Automation Framework
**Goal:** Build a mini automation framework

Create a Python package `ansible_helper/` with:
```
ansible_helper/
├── __init__.py
├── inventory.py      # Inventory parsing/generation
├── playbook.py       # Playbook creation/validation
├── runner.py         # Execute playbooks
├── reporter.py       # Generate reports
└── cli.py            # Command-line interface
```

Build a CLI that can:
- Generate playbooks from templates
- Run playbooks with custom options
- Generate execution reports

**Learn more:** 
- [Click Documentation](https://click.palletsprojects.com/)
- [Python Packages](https://docs.python.org/3/tutorial/modules.html#packages)
- [ansible-runner API](https://ansible.readthedocs.io/projects/runner/en/stable/python_interface.html)
- [Rich Library](https://rich.readthedocs.io/en/stable/)

---

## Tips

- Use `subprocess` to call Ansible CLI commands
- Parse YAML with `pyyaml` or `ruamel.yaml`
- Use `ansible-runner` for programmatic execution
- Handle errors gracefully with try/except
- Test with small inventories first

## Useful Libraries

```bash
pip install pyyaml ruamel.yaml jinja2 ansible-runner click rich
```

- `pyyaml` / `ruamel.yaml` - YAML parsing
- `jinja2` - Template rendering
- `ansible-runner` - Run Ansible from Python
- `click` - Build CLI tools
- `rich` - Beautiful terminal output
