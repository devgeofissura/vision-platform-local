# Skill Spectator (NVIDIA SkillSpector) — vault entry

## Purpose

Answer one question before you install an agent skill: *should I install this
at all?* Skills execute with the same privileges as the agent — file system,
shell, network and environment access — yet most are loaded on trust.
SkillSpector detects 64 vulnerability patterns across 16 categories (prompt
injection, data exfiltration, privilege escalation, supply-chain, excessive
agency, system prompt leakage, MCP tool poisoning and more) using static
analysis plus optional LLM semantic evaluation.

Research behind the tool ("Agent Skills in the Wild") found 26.1% of skills
contain at least one vulnerability and 5.2% show likely malicious intent —
skills with executable scripts are 2.12x more likely to be vulnerable.

## Prerequisites

- Python 3.12+ with uv (or pip + virtualenv)
- The skill or repository you want to scan
- (Optional) an LLM API key for the semantic analysis stage

## Usage

### 1. Install SkillSpector

```bash
uv tool install skillspector
skillspector --help
```

### 2. Scan a skill before installing it

```bash
# Scan a directory
skillspector scan /path/to/skill

# Scan a single SKILL.md
skillspector scan /path/to/skill/SKILL.md

# Scan a zip archive
skillspector scan ./downloaded-skill.zip

# Scan a remote repository
skillspector scan https://github.com/user/skill-repo
```

### 3. Generate reports for review or CI

```bash
skillspector scan /path/to/skill --format json --output ./report.json
skillspector scan /path/to/skill --format markdown --output ./report.md
skillspector scan /path/to/skill --format sarif --output ./report.sarif
```

### 4. Use the Python API

```python
from skillspector import graph

result = graph.invoke({
    "input_path": "/path/to/skill",
    "output_format": "json",
    "use_llm": False,  # True enables semantic evaluation
})
print(result["risk_score"], result["findings"])
```

### 5. Integrate with this kit's marketplace

Before publishing or installing any asset through `core/marketplace`, run
SkillSpector on the skill directory and gate on the risk score:

```bash
skillspector scan ./assets/skills/new-skill --format json \
  | jq -r '.risk_score' | tee ./risk.txt
```

## Examples

### Example 1: Vet a skill from a marketplace

```bash
uv tool install skillspector
skillspector scan ./downloaded-skill.zip --format markdown --output ./vetting.md
less ./vetting.md
```

### Example 2: CI gate that fails on high risk

```bash
score=$(skillspector scan ./assets/skills/my-skill --format json | jq -r '.risk_score')
if [ "$score" -gt 60 ]; then
  echo "SKILL BLOCKED: risk score $score" >&2
  exit 1
fi
```

### Example 3: Semantic review with an LLM backend

```bash
skillspector scan ./plugin --use-llm --format terminal
```

## Notes

- SkillSpector is static analysis; it cannot detect runtime behavior.
- Encrypted or compiled payloads cannot be analyzed.
- Combine with this kit's `core/security/secret-scan.sh` for credential
  leakage and `core/security/dependency-audit.sh` for supply-chain checks.
- Treat scores above 60 as a blocker for automatic installs.
