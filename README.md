# Ansible Learning Exercises

A hands-on collection of 20 exercises covering Ansible fundamentals through to intermediate concepts.

## Files

| File | Description |
|------|-------------|
| `ansible-exercises.md` | Exercise instructions and goals |
| `ansible-python-exercises.md` | Python + Ansible integration exercises |
| `solutions.md` | Complete solutions for all exercises |
| `ansible_python_solutions.py` | Python solutions for all 20 Python exercises |
| `solution_attempts.md` | Your working attempts |

## Topics Covered

### Beginner (Exercises 1–6)

| # | Topic | Key Concepts |
|---|-------|--------------|
| 1 | Hello World | `hosts`, `connection`, `debug` module |
| 2 | File Creation | `copy` module, `content`, `dest` |
| 3 | Variables | `vars`, Jinja2 `{{ }}` syntax |
| 4 | Multiple Tasks | Task sequencing, `file` module, `state: directory` |
| 5 | Loops | `loop`, `{{ item }}` |
| 6 | Conditionals | `when`, boolean expressions |

### Intermediate (Exercises 7–10)

| # | Topic | Key Concepts |
|---|-------|--------------|
| 7 | Inventory Files | INI format, groups, `ansible_connection` |
| 8 | Handlers | `notify`, `handlers` section, triggered tasks |
| 9 | Templates | Jinja2 `.j2` files, `template` module |
| 10 | Full Playbook | Combining variables, loops, conditionals, handlers |

### Advanced Beginner (Exercises 11–15)

| # | Topic | Key Concepts |
|---|-------|--------------|
| 11 | Roles | `ansible-galaxy init`, role structure, reusability |
| 12 | Registered Variables | `register`, `stdout`, capturing task output |
| 13 | Include & Import | `include_tasks`, `import_tasks`, modular playbooks |
| 14 | Blocks & Rescue | `block`, `rescue`, `always`, error handling |
| 15 | Facts | `gather_facts`, `ansible_os_family`, system info |

### Intermediate+ (Exercises 16–20)

| # | Topic | Key Concepts |
|---|-------|--------------|
| 16 | Vault | `ansible-vault encrypt`, `--ask-vault-pass`, secrets |
| 17 | Tags | `tags`, `--tags`, `--skip-tags`, selective execution |
| 18 | Ansible Lint | `ansible-lint`, FQCN, code quality |
| 19 | Dynamic Inventory | Python/JSON inventory scripts |
| 20 | Multi-Play Playbooks | Multiple plays, different host groups |

## Python + Ansible Exercises

The `ansible-python-exercises.md` file contains 20 exercises for automating Ansible with Python:

| # | Topic | Key Concepts |
|---|-------|-------------|
| 1–5 | Parsing & Generation | YAML parsing, playbook generation, Jinja2, dynamic inventory |
| 6–10 | Execution & Analysis | `ansible-runner`, facts collection, task counting, variable extraction |
| 11–15 | Tooling | Role scaffolding, vault helpers, linting, report generation |
| 16–20 | Advanced | Module docs, playbook merging, connection testing, full framework |

**Required libraries:**
```bash
pip install pyyaml jinja2 ansible-runner click rich
```

## Quick Reference

### Running Playbooks

```bash
# Basic run
ansible-playbook playbook.yml

# With inventory file
ansible-playbook -i inventory.ini playbook.yml

# Dry run (check mode)
ansible-playbook playbook.yml --check

# Verbose output
ansible-playbook playbook.yml -vvv

# Run specific tags
ansible-playbook playbook.yml --tags deploy

# With vault password
ansible-playbook playbook.yml --ask-vault-pass
```

### Common Modules

| Module | Purpose |
|--------|---------|
| `debug` | Print messages/variables |
| `copy` | Copy content or files |
| `file` | Manage files/directories |
| `template` | Deploy Jinja2 templates |
| `command` | Run shell commands |
| `include_tasks` | Include task files |

### YAML Syntax Tips

- Use 2-space indentation
- Lists start with `-`
- Key-value pairs use `:`
- Strings with special chars need quotes
- Variables: `{{ var_name }}`

## Prerequisites

```bash
pip install ansible ansible-lint
```

## Resources

- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Galaxy](https://galaxy.ansible.com/)
- [YAML Specification](https://yaml.org/spec/)
