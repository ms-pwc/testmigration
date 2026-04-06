Valiadted & Updated: 2026-04-06 Monday 9:00pm

## Variables

- Required identity variables are stored manually in GitHub repository variables for OIDC login:
  - `AZURE_CLIENT_ID`
  - `AZURE_TENANT_ID`
  - `AZURE_SUBSCRIPTION_ID`
- Environment-specific values are loaded from variable groups defined in `global.yaml`.
- `SearchApi` and `SearchService` handling from `global.yaml` is unchanged as requested.

## Changes Done
1. Combined update for output transfer reliability:
- Change done to pass loaded variables as a safe transport payload between jobs.
- Instead of depending only on direct JSON output, encoded payload handling is used to avoid output parsing/breakage issues.

2. Python output handling update:
- Python now suggests and uses base64 for workflow output transport.
- Change done in the load step to generate encoded output:
  - Added `import base64`
  - Added JSON-to-base64 conversion
  - Wrote encoded value to workflow output key

3. Code-level update details (combined technical changes):
- `encode` logic added to the Python loader step.
- Output key added for encoded payload (`all_vars_b64`).
- Apply step updated with decode flow:
  - Read encoded payload first
  - Decode base64 to JSON
  - Parse JSON into key-value map
  - Export variables into `GITHUB_ENV`
- Fallback retained to handle non-encoded payload when needed.

4. Apply Variables step with description:
- Change done in Apply Variables to make variable export robust and predictable.
- Added payload selection logic:
  - `payload_b64`: preferred encoded payload
  - `payload_json`: fallback plain payload
- Why this is used:
  - Previous step values were not loading correctly in some runs.
  - Encoded payload avoids format/escaping issues across step/job output boundaries.
- Multiline environment values are still handled correctly with heredoc-style export blocks.


## Added/Updated Code (Before and After)

### 1) Setup job output key

Before:
```yaml
outputs:
  all_vars: ${{ steps.load.outputs.all_vars }}
```

After:
```yaml
outputs:
  all_vars_b64: ${{ steps.load.outputs.all_vars_b64 }}
```

### 2) Python loader imports and output write

Before:
```python
import yaml, os, json, subprocess
...
with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
  f.write('all_vars=' + json.dumps(result) + '\n')
```

After:
```python
import yaml, os, json, subprocess, base64
...
with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
  encoded = base64.b64encode(json.dumps(result).encode('utf-8')).decode('utf-8')
  f.write('all_vars_b64=' + encoded + '\n')
```

### 3) Apply Variables env inputs

Before:
```yaml
env:
  ALL_VARS: ${{ needs.setup_variables.outputs.all_vars }}
```

After:
```yaml
env:
  ALL_VARS: ${{ needs.setup_variables.outputs.all_vars }}
  ALL_VARS_B64: ${{ needs.setup_variables.outputs.all_vars_b64 }}
```

### 4) Apply Variables payload decode and fallback

Before:
```python
import json, os
with open(os.environ['GITHUB_ENV'], 'a') as env_file:
  for k, v in json.loads(os.environ.get('ALL_VARS', '{}')).items():
    val = str(v)
    if '\n' in val:
      env_file.write(k + '<<__ENV_EOF__\n' + val + '\n__ENV_EOF__\n')
    else:
      env_file.write(k + '=' + val + '\n')
```

After:
```python
import json, os, base64
payload_b64 = (os.environ.get('ALL_VARS_B64') or '').strip()
payload_json = (os.environ.get('ALL_VARS') or '').strip()

if payload_b64:
  all_vars = json.loads(base64.b64decode(payload_b64).decode('utf-8'))
elif payload_json:
  all_vars = json.loads(payload_json)
else:
  all_vars = {}

with open(os.environ['GITHUB_ENV'], 'a') as env_file:
  for k, v in all_vars.items():
    val = str(v)
    if '\n' in val:
      env_file.write(k + '<<__ENV_EOF__\n' + val + '\n__ENV_EOF__\n')
    else:
      env_file.write(k + '=' + val + '\n')
```

### Why this code change was required

- Previous step outputs were not loading correctly every time in downstream jobs.
- Base64 payload made transfer stable across workflow output boundaries.
- Fallback kept compatibility if only plain JSON is available.

---
GitHub test workflow: https://github.com/ms-pwc/adomg-test/actions/workflows/searchCreateSrc.yml
