"""
Ansible + Python Exercises - Solutions
=======================================
Complete solutions for all 20 exercises in ansible-python-exercises.md
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Optional imports - install as needed
try:
    import yaml
except ImportError:
    yaml = None
    print("Note: Install pyyaml for YAML exercises: pip install pyyaml")

try:
    from jinja2 import Environment, FileSystemLoader, Template
except ImportError:
    Environment = FileSystemLoader = Template = None
    print("Note: Install jinja2 for template exercises: pip install jinja2")

try:
    import ansible_runner
except ImportError:
    ansible_runner = None
    print("Note: Install ansible-runner for execution exercises: pip install ansible-runner")


# =============================================================================
# Exercise 1: Parse YAML Inventory
# =============================================================================

def ex01_parse_inventory(filepath: str) -> dict:
    """
    Parse an Ansible inventory file (YAML format) and return hosts/groups.
    
    Example inventory.yml:
        all:
          children:
            webservers:
              hosts:
                web1.example.com:
                web2.example.com:
            dbservers:
              hosts:
                db1.example.com:
    """
    if yaml is None:
        raise ImportError("pyyaml required: pip install pyyaml")
    
    with open(filepath, 'r') as f:
        inventory = yaml.safe_load(f)
    
    def extract_hosts(data, group_name="all"):
        """Recursively extract hosts from inventory structure."""
        results = {}
        
        if isinstance(data, dict):
            # Check for hosts in this group
            if 'hosts' in data:
                results[group_name] = list(data['hosts'].keys())
            
            # Check for child groups
            if 'children' in data:
                for child_name, child_data in data['children'].items():
                    results.update(extract_hosts(child_data, child_name))
        
        return results
    
    groups = extract_hosts(inventory.get('all', inventory))
    
    # Print results
    print("Inventory Groups and Hosts:")
    print("-" * 40)
    for group, hosts in groups.items():
        print(f"\n[{group}]")
        for host in hosts:
            print(f"  - {host}")
    
    return groups


# =============================================================================
# Exercise 2: Generate Playbook from Python
# =============================================================================

def ex02_generate_playbook(
    hosts: str = "localhost",
    task_name: str = "Example task",
    module: str = "debug",
    module_args: dict = None,
    output_file: str = "generated_playbook.yml"
) -> str:
    """
    Generate an Ansible playbook YAML file from parameters.
    """
    if yaml is None:
        raise ImportError("pyyaml required: pip install pyyaml")
    
    if module_args is None:
        module_args = {"msg": "Hello from generated playbook!"}
    
    playbook = [
        {
            "name": f"Generated playbook for {hosts}",
            "hosts": hosts,
            "gather_facts": False,
            "tasks": [
                {
                    "name": task_name,
                    module: module_args
                }
            ]
        }
    ]
    
    with open(output_file, 'w') as f:
        yaml.dump(playbook, f, default_flow_style=False, sort_keys=False)
    
    print(f"Playbook generated: {output_file}")
    return output_file


# =============================================================================
# Exercise 3: Jinja2 Template Rendering
# =============================================================================

def ex03_jinja_render(template_string: str = None, variables: dict = None) -> str:
    """
    Render a Jinja2 template with given variables.
    """
    if Template is None:
        raise ImportError("jinja2 required: pip install jinja2")
    
    if template_string is None:
        template_string = """
server_name: {{ server_name }}
port: {{ port }}
environment: {{ env }}
debug_mode: {{ debug | default('false') }}
"""
    
    if variables is None:
        variables = {
            "server_name": "web-server-01",
            "port": 8080,
            "env": "production"
        }
    
    template = Template(template_string)
    rendered = template.render(**variables)
    
    print("Rendered template:")
    print("-" * 40)
    print(rendered)
    
    return rendered


# =============================================================================
# Exercise 4: YAML Validator
# =============================================================================

def ex04_yaml_validator(filepath: str) -> tuple[bool, list]:
    """
    Validate an Ansible playbook YAML file.
    Returns (is_valid, list of errors).
    """
    if yaml is None:
        raise ImportError("pyyaml required: pip install pyyaml")
    
    errors = []
    
    # Check file exists
    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"]
    
    # Try to parse YAML
    try:
        with open(filepath, 'r') as f:
            content = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return False, [f"Invalid YAML syntax: {e}"]
    
    # Validate Ansible structure
    if content is None:
        return False, ["Empty playbook"]
    
    if not isinstance(content, list):
        errors.append("Playbook must be a list of plays")
        return False, errors
    
    for i, play in enumerate(content):
        if not isinstance(play, dict):
            errors.append(f"Play {i+1}: Must be a dictionary")
            continue
        
        # Check required keys
        if 'hosts' not in play:
            errors.append(f"Play {i+1}: Missing required 'hosts' key")
        
        if 'tasks' not in play and 'roles' not in play:
            errors.append(f"Play {i+1}: Must have 'tasks' or 'roles'")
        
        # Validate tasks
        if 'tasks' in play:
            if not isinstance(play['tasks'], list):
                errors.append(f"Play {i+1}: 'tasks' must be a list")
            else:
                for j, task in enumerate(play['tasks']):
                    if not isinstance(task, dict):
                        errors.append(f"Play {i+1}, Task {j+1}: Must be a dictionary")
    
    is_valid = len(errors) == 0
    
    if is_valid:
        print(f"✓ {filepath} is valid")
    else:
        print(f"✗ {filepath} has errors:")
        for error in errors:
            print(f"  - {error}")
    
    return is_valid, errors


# =============================================================================
# Exercise 5: Dynamic Inventory Script
# =============================================================================

def ex05_dynamic_inventory(args: list = None) -> str:
    """
    Generate dynamic inventory JSON for Ansible.
    Supports --list and --host <hostname> arguments.
    """
    if args is None:
        args = sys.argv[1:] if len(sys.argv) > 1 else ["--list"]
    
    inventory = {
        "webservers": {
            "hosts": ["web1.example.com", "web2.example.com"],
            "vars": {
                "http_port": 80,
                "ansible_user": "deploy"
            }
        },
        "dbservers": {
            "hosts": ["db1.example.com"],
            "vars": {
                "db_port": 5432
            }
        },
        "all": {
            "children": ["webservers", "dbservers"]
        },
        "_meta": {
            "hostvars": {
                "web1.example.com": {"ansible_host": "192.168.1.10"},
                "web2.example.com": {"ansible_host": "192.168.1.11"},
                "db1.example.com": {"ansible_host": "192.168.1.20"}
            }
        }
    }
    
    if "--list" in args:
        output = json.dumps(inventory, indent=2)
    elif "--host" in args:
        try:
            host_index = args.index("--host") + 1
            hostname = args[host_index]
            hostvars = inventory["_meta"]["hostvars"].get(hostname, {})
            output = json.dumps(hostvars, indent=2)
        except (IndexError, KeyError):
            output = json.dumps({})
    else:
        output = json.dumps(inventory, indent=2)
    
    print(output)
    return output


# =============================================================================
# Exercise 6: Run Ansible Playbook from Python
# =============================================================================

def ex06_run_playbook(playbook_path: str, inventory_path: str = None) -> dict:
    """
    Execute an Ansible playbook using ansible-runner.
    """
    if ansible_runner is None:
        raise ImportError("ansible-runner required: pip install ansible-runner")
    
    kwargs = {"playbook": playbook_path}
    
    if inventory_path:
        kwargs["inventory"] = inventory_path
    else:
        kwargs["inventory"] = "localhost,"
    
    r = ansible_runner.run(**kwargs)
    
    result = {
        "status": r.status,
        "rc": r.rc,
        "stats": r.stats
    }
    
    print(f"Playbook: {playbook_path}")
    print(f"Status: {r.status}")
    print(f"Return code: {r.rc}")
    
    if r.stats:
        print("\nStats:")
        for host, stats in r.stats.items():
            print(f"  {host}: {stats}")
    
    return result


# =============================================================================
# Exercise 7: Host Facts Collector
# =============================================================================

def ex07_facts_collector(host: str = "localhost") -> dict:
    """
    Collect Ansible facts for a host and extract key information.
    """
    cmd = [
        "ansible", host, "-m", "setup",
        "-c", "local" if host == "localhost" else "ssh",
        "--one-line"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Parse the JSON output (after the "host | SUCCESS => " prefix)
        output = result.stdout
        json_start = output.find("{")
        if json_start != -1:
            facts_json = output[json_start:]
            facts = json.loads(facts_json)
            ansible_facts = facts.get("ansible_facts", facts)
            
            # Extract key info
            info = {
                "hostname": ansible_facts.get("ansible_hostname", "N/A"),
                "os_family": ansible_facts.get("ansible_os_family", "N/A"),
                "distribution": ansible_facts.get("ansible_distribution", "N/A"),
                "distribution_version": ansible_facts.get("ansible_distribution_version", "N/A"),
                "kernel": ansible_facts.get("ansible_kernel", "N/A"),
                "architecture": ansible_facts.get("ansible_architecture", "N/A"),
                "memory_mb": ansible_facts.get("ansible_memtotal_mb", "N/A"),
                "processor_count": ansible_facts.get("ansible_processor_count", "N/A"),
                "python_version": ansible_facts.get("ansible_python_version", "N/A"),
            }
            
            print("Host Facts:")
            print("-" * 40)
            for key, value in info.items():
                print(f"  {key}: {value}")
            
            return info
    except subprocess.TimeoutExpired:
        print("Timeout collecting facts")
    except json.JSONDecodeError:
        print("Failed to parse facts JSON")
    except FileNotFoundError:
        print("Ansible not found. Install with: pip install ansible")
    
    return {}


# =============================================================================
# Exercise 8: Inventory Diff Tool
# =============================================================================

def ex08_inventory_diff(file1: str, file2: str) -> dict:
    """
    Compare two inventory files and report differences.
    """
    if yaml is None:
        raise ImportError("pyyaml required: pip install pyyaml")
    
    def get_all_hosts(inv_data):
        """Extract all hosts from inventory."""
        hosts = set()
        
        def extract(data):
            if isinstance(data, dict):
                if 'hosts' in data:
                    hosts.update(data['hosts'].keys() if isinstance(data['hosts'], dict) else data['hosts'])
                for v in data.values():
                    extract(v)
            elif isinstance(data, list):
                for item in data:
                    extract(item)
        
        extract(inv_data)
        return hosts
    
    # Load inventories
    with open(file1, 'r') as f:
        inv1 = yaml.safe_load(f)
    with open(file2, 'r') as f:
        inv2 = yaml.safe_load(f)
    
    hosts1 = get_all_hosts(inv1)
    hosts2 = get_all_hosts(inv2)
    
    diff = {
        "added": list(hosts2 - hosts1),
        "removed": list(hosts1 - hosts2),
        "unchanged": list(hosts1 & hosts2)
    }
    
    print("Inventory Diff:")
    print("-" * 40)
    print(f"Added hosts ({len(diff['added'])}):")
    for h in diff['added']:
        print(f"  + {h}")
    print(f"\nRemoved hosts ({len(diff['removed'])}):")
    for h in diff['removed']:
        print(f"  - {h}")
    print(f"\nUnchanged hosts: {len(diff['unchanged'])}")
    
    return diff


# =============================================================================
# Exercise 9: Playbook Task Counter
# =============================================================================

def ex09_task_counter(playbook_path: str) -> dict:
    """
    Analyse playbook complexity - count tasks, handlers, modules used.
    """
    if yaml is None:
        raise ImportError("pyyaml required: pip install pyyaml")
    
    with open(playbook_path, 'r') as f:
        playbook = yaml.safe_load(f)
    
    stats = {
        "plays": 0,
        "tasks": 0,
        "handlers": 0,
        "modules": set()
    }
    
    # Known Ansible keywords (not modules)
    keywords = {
        'name', 'hosts', 'vars', 'vars_files', 'tasks', 'handlers',
        'roles', 'become', 'become_user', 'gather_facts', 'when',
        'register', 'notify', 'tags', 'block', 'rescue', 'always',
        'loop', 'with_items', 'include_tasks', 'import_tasks',
        'include_role', 'import_role', 'environment', 'ignore_errors'
    }
    
    def count_tasks(tasks_list):
        count = 0
        for task in tasks_list:
            if isinstance(task, dict):
                count += 1
                # Find module (first key that's not a keyword)
                for key in task.keys():
                    if key not in keywords:
                        stats["modules"].add(key)
                        break
                # Handle blocks
                if 'block' in task:
                    count += count_tasks(task['block']) - 1
                if 'rescue' in task:
                    count += count_tasks(task['rescue'])
                if 'always' in task:
                    count += count_tasks(task['always'])
        return count
    
    if isinstance(playbook, list):
        stats["plays"] = len(playbook)
        for play in playbook:
            if 'tasks' in play:
                stats["tasks"] += count_tasks(play['tasks'])
            if 'handlers' in play:
                stats["handlers"] += count_tasks(play['handlers'])
    
    stats["modules"] = sorted(stats["modules"])
    
    print(f"Playbook Analysis: {playbook_path}")
    print("-" * 40)
    print(f"  Plays: {stats['plays']}")
    print(f"  Tasks: {stats['tasks']}")
    print(f"  Handlers: {stats['handlers']}")
    print(f"  Modules used: {', '.join(stats['modules'])}")
    
    return stats


# =============================================================================
# Exercise 10: Variable Extractor
# =============================================================================

def ex10_var_extractor(playbook_path: str) -> dict:
    """
    Extract all variables from a playbook and check if they're defined.
    """
    if yaml is None:
        raise ImportError("pyyaml required: pip install pyyaml")
    
    with open(playbook_path, 'r') as f:
        content = f.read()
    
    # Find all {{ variable }} patterns
    pattern = r'\{\{\s*([\w\.]+)(?:\s*\|[^}]*)?\s*\}\}'
    matches = re.findall(pattern, content)
    
    # Get unique variables (base name only)
    variables = set()
    for match in matches:
        var_name = match.split('.')[0]  # Get base variable name
        variables.add(var_name)
    
    # Parse YAML to find defined variables
    playbook = yaml.safe_load(content)
    defined_vars = set()
    
    def extract_defined(data):
        if isinstance(data, dict):
            if 'vars' in data:
                defined_vars.update(data['vars'].keys())
            for v in data.values():
                extract_defined(v)
        elif isinstance(data, list):
            for item in data:
                extract_defined(item)
    
    extract_defined(playbook)
    
    # Built-in variables
    builtins = {'item', 'ansible_hostname', 'ansible_os_family', 
                'inventory_hostname', 'hostvars', 'groups', 'group_names'}
    
    undefined = variables - defined_vars - builtins
    
    result = {
        "all_variables": sorted(variables),
        "defined": sorted(defined_vars),
        "undefined": sorted(undefined),
        "builtin": sorted(variables & builtins)
    }
    
    print(f"Variable Analysis: {playbook_path}")
    print("-" * 40)
    print(f"Variables found: {', '.join(result['all_variables'])}")
    print(f"Defined in vars: {', '.join(result['defined']) or 'None'}")
    print(f"Built-in/special: {', '.join(result['builtin']) or 'None'}")
    print(f"Potentially undefined: {', '.join(result['undefined']) or 'None'}")
    
    return result


# =============================================================================
# Exercise 11: Role Scaffolder
# =============================================================================

def ex11_role_scaffold(role_name: str, base_path: str = "roles") -> str:
    """
    Create Ansible role directory structure with placeholder files.
    """
    if yaml is None:
        raise ImportError("pyyaml required: pip install pyyaml")
    
    role_path = Path(base_path) / role_name
    
    # Define structure
    dirs = ['tasks', 'handlers', 'templates', 'files', 'vars', 'defaults', 'meta']
    
    # Create directories
    for d in dirs:
        (role_path / d).mkdir(parents=True, exist_ok=True)
    
    # Create main.yml files with placeholder content
    yaml_files = {
        'tasks/main.yml': [{"name": f"Main tasks for {role_name}", "debug": {"msg": "Role tasks here"}}],
        'handlers/main.yml': [{"name": "Restart service", "debug": {"msg": "Handler triggered"}}],
        'vars/main.yml': {f"{role_name}_version": "1.0"},
        'defaults/main.yml': {f"{role_name}_enabled": True},
        'meta/main.yml': {
            "galaxy_info": {
                "author": "your_name",
                "description": f"Role for {role_name}",
                "license": "MIT",
                "min_ansible_version": "2.9"
            },
            "dependencies": []
        }
    }
    
    for filepath, content in yaml_files.items():
        full_path = role_path / filepath
        with open(full_path, 'w') as f:
            yaml.dump(content, f, default_flow_style=False, sort_keys=False)
    
    # Create README
    readme_content = f"""# {role_name}

Ansible role for {role_name}.

## Requirements

None.

## Role Variables

See `defaults/main.yml` and `vars/main.yml`.

## Example Playbook

```yaml
- hosts: servers
  roles:
    - {role_name}
```
"""
    with open(role_path / "README.md", 'w') as f:
        f.write(readme_content)
    
    print(f"Role created: {role_path}")
    print("Structure:")
    for d in dirs:
        print(f"  {role_name}/{d}/")
    
    return str(role_path)


# =============================================================================
# Exercise 12: Encrypted Vars Handler
# =============================================================================

def ex12_vault_helper(action: str, filepath: str, password: str = None) -> bool:
    """
    Helper for Ansible Vault operations (encrypt, decrypt, view).
    """
    import getpass
    
    if password is None:
        password = getpass.getpass("Vault password: ")
    
    # Write password to temp file for ansible-vault
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(password)
        pass_file = f.name
    
    try:
        if action == "encrypt":
            cmd = ["ansible-vault", "encrypt", filepath, "--vault-password-file", pass_file]
        elif action == "decrypt":
            cmd = ["ansible-vault", "decrypt", filepath, "--vault-password-file", pass_file]
        elif action == "view":
            cmd = ["ansible-vault", "view", filepath, "--vault-password-file", pass_file]
        else:
            print(f"Unknown action: {action}")
            return False
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if action == "view":
            print(result.stdout)
        
        if result.returncode == 0:
            print(f"Vault {action} successful: {filepath}")
            return True
        else:
            print(f"Vault {action} failed: {result.stderr}")
            return False
    finally:
        os.unlink(pass_file)


# =============================================================================
# Exercise 13: Playbook Linter
# =============================================================================

def ex13_playbook_linter(playbook_path: str) -> list:
    """
    Simple playbook linter checking for common issues.
    """
    if yaml is None:
        raise ImportError("pyyaml required: pip install pyyaml")
    
    with open(playbook_path, 'r') as f:
        content = f.read()
    
    playbook = yaml.safe_load(content)
    warnings = []
    
    def check_tasks(tasks, play_num):
        for i, task in enumerate(tasks, 1):
            if not isinstance(task, dict):
                continue
            
            task_id = f"Play {play_num}, Task {i}"
            
            # Check for name
            if 'name' not in task:
                warnings.append(f"{task_id}: Missing 'name' field")
            
            # Check shell vs command
            if 'shell' in task:
                shell_cmd = task['shell']
                if isinstance(shell_cmd, str) and '|' not in shell_cmd and '>' not in shell_cmd:
                    warnings.append(f"{task_id}: Consider using 'command' instead of 'shell'")
            
            # Check for hardcoded passwords
            task_str = str(task)
            if re.search(r'password["\']?\s*[:=]\s*["\']?\w+', task_str, re.I):
                warnings.append(f"{task_id}: Possible hardcoded password detected")
            
            # Check become for privileged modules
            privileged_modules = ['apt', 'yum', 'dnf', 'package', 'service', 'systemd', 'user', 'group']
            for mod in privileged_modules:
                if mod in task and 'become' not in task:
                    warnings.append(f"{task_id}: '{mod}' module may require 'become: true'")
            
            # Check blocks recursively
            for block_type in ['block', 'rescue', 'always']:
                if block_type in task:
                    check_tasks(task[block_type], play_num)
    
    if isinstance(playbook, list):
        for i, play in enumerate(playbook, 1):
            if 'tasks' in play:
                check_tasks(play['tasks'], i)
    
    print(f"Lint Results: {playbook_path}")
    print("-" * 40)
    if warnings:
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
        print("  ✓ No issues found")
    
    return warnings


# =============================================================================
# Exercise 14: Execution Report Generator
# =============================================================================

def ex14_report_generator(results: dict, output_file: str = "report.md") -> str:
    """
    Generate a Markdown report from Ansible execution results.
    """
    from datetime import datetime
    
    report = f"""# Ansible Execution Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

| Metric | Value |
|--------|-------|
| Status | {results.get('status', 'N/A')} |
| Return Code | {results.get('rc', 'N/A')} |

## Host Results

"""
    
    stats = results.get('stats', {})
    for host, host_stats in stats.items():
        report += f"### {host}\n\n"
        report += "| Task Type | Count |\n"
        report += "|-----------|-------|\n"
        for stat_name, count in host_stats.items():
            emoji = "✓" if stat_name == "ok" else "✗" if stat_name == "failures" else "○"
            report += f"| {emoji} {stat_name} | {count} |\n"
        report += "\n"
    
    if not stats:
        report += "_No statistics available_\n"
    
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"Report generated: {output_file}")
    return report


# =============================================================================
# Exercise 15: Host Pattern Matcher
# =============================================================================

def ex15_pattern_matcher(inventory: dict, pattern: str) -> list:
    """
    Match hosts using Ansible-style patterns.
    
    Supports:
    - Wildcards: web*
    - Negation: !dbservers
    - Intersection: webservers:&staging
    - Union: webservers:dbservers
    """
    import fnmatch
    
    # Collect all hosts
    all_hosts = set()
    group_hosts = {}
    
    def collect_hosts(data, group="all"):
        if isinstance(data, dict):
            if 'hosts' in data:
                hosts = list(data['hosts'].keys()) if isinstance(data['hosts'], dict) else data['hosts']
                group_hosts[group] = set(hosts)
                all_hosts.update(hosts)
            if 'children' in data:
                for child_name, child_data in data['children'].items():
                    collect_hosts(child_data, child_name)
    
    collect_hosts(inventory.get('all', inventory))
    group_hosts['all'] = all_hosts
    
    def resolve_pattern(pat):
        pat = pat.strip()
        
        # Negation
        if pat.startswith('!'):
            return all_hosts - resolve_pattern(pat[1:])
        
        # Group name
        if pat in group_hosts:
            return group_hosts[pat]
        
        # Wildcard pattern
        if '*' in pat or '?' in pat:
            return {h for h in all_hosts if fnmatch.fnmatch(h, pat)}
        
        # Single host
        if pat in all_hosts:
            return {pat}
        
        return set()
    
    # Handle compound patterns
    result = set()
    
    # Split by : for union/intersection
    parts = pattern.split(':')
    
    for part in parts:
        if part.startswith('&'):
            # Intersection
            result = result & resolve_pattern(part[1:])
        elif part.startswith('!'):
            # Exclusion
            result = result - resolve_pattern(part[1:])
        else:
            # Union
            if not result:
                result = resolve_pattern(part)
            else:
                result = result | resolve_pattern(part)
    
    matched = sorted(result)
    print(f"Pattern '{pattern}' matched: {matched}")
    return matched


# =============================================================================
# Exercise 16: Module Documentation Parser
# =============================================================================

def ex16_module_docs(module_name: str) -> dict:
    """
    Get and parse Ansible module documentation.
    """
    cmd = ["ansible-doc", "-j", module_name]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            docs = json.loads(result.stdout)
            module_doc = docs.get(module_name, {}).get('doc', {})
            
            info = {
                "name": module_name,
                "short_description": module_doc.get('short_description', 'N/A'),
                "description": module_doc.get('description', []),
                "options": list(module_doc.get('options', {}).keys()),
                "author": module_doc.get('author', 'N/A')
            }
            
            print(f"Module: {module_name}")
            print("-" * 40)
            print(f"Description: {info['short_description']}")
            print(f"Author: {info['author']}")
            print(f"Parameters: {', '.join(info['options'][:10])}...")
            
            return info
        else:
            print(f"Module not found: {module_name}")
            return {}
    except subprocess.TimeoutExpired:
        print("Timeout getting module docs")
        return {}
    except FileNotFoundError:
        print("ansible-doc not found. Install Ansible first.")
        return {}


# =============================================================================
# Exercise 17: Playbook Merger
# =============================================================================

def ex17_playbook_merger(playbook_files: list, output_file: str = "merged_playbook.yml") -> str:
    """
    Merge multiple playbooks into one.
    """
    if yaml is None:
        raise ImportError("pyyaml required: pip install pyyaml")
    
    merged_plays = []
    all_vars = {}
    
    for filepath in playbook_files:
        with open(filepath, 'r') as f:
            playbook = yaml.safe_load(f)
        
        if isinstance(playbook, list):
            for play in playbook:
                # Merge vars
                if 'vars' in play:
                    all_vars.update(play['vars'])
                merged_plays.append(play)
    
    # Add merged vars to first play if any
    if all_vars and merged_plays:
        if 'vars' not in merged_plays[0]:
            merged_plays[0]['vars'] = {}
        merged_plays[0]['vars'].update(all_vars)
    
    with open(output_file, 'w') as f:
        yaml.dump(merged_plays, f, default_flow_style=False, sort_keys=False)
    
    print(f"Merged {len(playbook_files)} playbooks into: {output_file}")
    print(f"Total plays: {len(merged_plays)}")
    
    return output_file


# =============================================================================
# Exercise 18: Connection Tester
# =============================================================================

def ex18_connection_tester(inventory_path: str) -> dict:
    """
    Test connectivity to all hosts in inventory using ansible ping.
    """
    cmd = ["ansible", "all", "-i", inventory_path, "-m", "ping", "--one-line"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        reachable = []
        unreachable = []
        
        for line in result.stdout.splitlines():
            if "SUCCESS" in line:
                host = line.split()[0]
                reachable.append(host)
            elif "UNREACHABLE" in line or "FAILED" in line:
                host = line.split()[0]
                unreachable.append(host)
        
        for line in result.stderr.splitlines():
            if "UNREACHABLE" in line:
                parts = line.split()
                if parts:
                    unreachable.append(parts[0])
        
        results = {
            "reachable": reachable,
            "unreachable": unreachable
        }
        
        print("Connection Test Results:")
        print("-" * 40)
        print(f"Reachable ({len(reachable)}):")
        for h in reachable:
            print(f"  ✓ {h}")
        print(f"\nUnreachable ({len(unreachable)}):")
        for h in unreachable:
            print(f"  ✗ {h}")
        
        return results
    except subprocess.TimeoutExpired:
        print("Connection test timed out")
        return {"reachable": [], "unreachable": [], "error": "timeout"}
    except FileNotFoundError:
        print("Ansible not found. Install with: pip install ansible")
        return {}


# =============================================================================
# Exercise 19: Config File Generator
# =============================================================================

def ex19_config_generator(
    inventory: str = "./inventory",
    remote_user: str = "ansible",
    private_key: str = None,
    host_key_checking: bool = False,
    output_file: str = "ansible.cfg"
) -> str:
    """
    Generate an ansible.cfg configuration file.
    """
    config = f"""[defaults]
inventory = {inventory}
remote_user = {remote_user}
host_key_checking = {str(host_key_checking).lower()}
retry_files_enabled = false
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 3600

[privilege_escalation]
become = true
become_method = sudo
become_user = root
become_ask_pass = false

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
pipelining = true
"""
    
    if private_key:
        config = config.replace(
            "retry_files_enabled",
            f"private_key_file = {private_key}\nretry_files_enabled"
        )
    
    with open(output_file, 'w') as f:
        f.write(config)
    
    print(f"Config generated: {output_file}")
    return output_file


# =============================================================================
# Exercise 20: Full Automation Framework (CLI Entry Point)
# =============================================================================

def ex20_cli():
    """
    Command-line interface for the automation framework.
    This ties together all the previous exercises.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ansible Helper - Python Automation Framework"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate a playbook")
    validate_parser.add_argument("playbook", help="Path to playbook")
    
    # Lint command
    lint_parser = subparsers.add_parser("lint", help="Lint a playbook")
    lint_parser.add_argument("playbook", help="Path to playbook")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a playbook")
    gen_parser.add_argument("--hosts", default="localhost", help="Target hosts")
    gen_parser.add_argument("--output", default="playbook.yml", help="Output file")
    
    # Scaffold command
    scaffold_parser = subparsers.add_parser("scaffold", help="Create role structure")
    scaffold_parser.add_argument("role_name", help="Name of the role")
    
    # Inventory command
    inv_parser = subparsers.add_parser("inventory", help="Dynamic inventory")
    inv_parser.add_argument("--list", action="store_true", help="List all hosts")
    inv_parser.add_argument("--host", help="Get vars for a host")
    
    args = parser.parse_args()
    
    if args.command == "validate":
        ex04_yaml_validator(args.playbook)
    elif args.command == "lint":
        ex13_playbook_linter(args.playbook)
    elif args.command == "generate":
        ex02_generate_playbook(hosts=args.hosts, output_file=args.output)
    elif args.command == "scaffold":
        ex11_role_scaffold(args.role_name)
    elif args.command == "inventory":
        if args.host:
            ex05_dynamic_inventory(["--host", args.host])
        else:
            ex05_dynamic_inventory(["--list"])
    else:
        parser.print_help()


# =============================================================================
# Main - Demo/Test Functions
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Ansible + Python Exercises - Solutions")
    print("=" * 60)
    print("\nAvailable functions:")
    print("  ex01_parse_inventory(filepath)")
    print("  ex02_generate_playbook(hosts, task_name, module, ...)")
    print("  ex03_jinja_render(template_string, variables)")
    print("  ex04_yaml_validator(filepath)")
    print("  ex05_dynamic_inventory(args)")
    print("  ex06_run_playbook(playbook_path, inventory_path)")
    print("  ex07_facts_collector(host)")
    print("  ex08_inventory_diff(file1, file2)")
    print("  ex09_task_counter(playbook_path)")
    print("  ex10_var_extractor(playbook_path)")
    print("  ex11_role_scaffold(role_name)")
    print("  ex12_vault_helper(action, filepath, password)")
    print("  ex13_playbook_linter(playbook_path)")
    print("  ex14_report_generator(results, output_file)")
    print("  ex15_pattern_matcher(inventory, pattern)")
    print("  ex16_module_docs(module_name)")
    print("  ex17_playbook_merger(playbook_files, output_file)")
    print("  ex18_connection_tester(inventory_path)")
    print("  ex19_config_generator(...)")
    print("  ex20_cli()")
    print("\nRun individual exercises by importing this module:")
    print("  from ansible_python_solutions import ex01_parse_inventory")
    print("\nOr run the CLI:")
    print("  python ansible_python_solutions.py validate playbook.yml")
    
    # Quick demo
    print("\n" + "=" * 60)
    print("Demo: Exercise 3 - Jinja2 Template Rendering")
    print("=" * 60)
    ex03_jinja_render()
    
    print("\n" + "=" * 60)
    print("Demo: Exercise 5 - Dynamic Inventory")
    print("=" * 60)
    ex05_dynamic_inventory(["--list"])
