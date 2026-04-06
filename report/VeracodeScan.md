# **Last Updated:** April 6, 2026  

## Repository Settings & Secrets Configuration

### Added Variables in Settings (Repo Level)
- **ado_pat** - Azure DevOps Personal Access Token variable
- **ado_org** - Azure DevOps Organization name variable  
- **ado_assigned_to** - Azure DevOps user to assign work items to

**Location:** Repository Settings → Secrets and Variables → Actions Variables

---

## GitHub Secrets Management

### Updated/Changed Secrets
- **GIT_PAT** - GitHub Personal Access Token (changed)
  - Used at: [Line 29](../.github/workflows/Veracode-Scan.yml#L29) - Repository checkout authentication
  - Scope: Read access to target repositories

- **ADO_PAT** - Azure DevOps Personal Access Token (added)
  - Used at: [Line 141](../.github/workflows/Veracode-Scan.yml#L141) - Environment variable for Azure DevOps API calls
  - Scope: Create work items in Azure DevOps


---

## Error Handling & Try-Catch Implementation (Line 65+)

### Python Exception Handling - Repository JSON Parsing
**Location:** [Lines 60-72](../.github/workflows/Veracode-Scan.yml#L60-L72)

```python
try:
    repos = json.loads(raw_repos)
except Exception:
    # Fallback for loose formats like [Search-API] or comma-separated text.
    trimmed = raw_repos.strip('[]')
    repos = [p.strip().strip('"\'') for p in trimmed.split(',') if p.strip()]
```

**Improvements:**
- Added try-catch block for JSON parsing
- Graceful fallback to manual parsing for malformed JSON
- Handles various input formats: `["repo"]`, `[repo]`, or `repo1, repo2`
- Strips extra quotes and whitespace for robustness

---

## Azure DevOps Work Item Creation Script

### Script Enhancements

#### Location: Lines 135-170 - Create Azure DevOps work item on failure

**Changes Made:**

1. **Removed HTML Entity Encoding (%27)**
   - Removed hardcoded `%27` single quote encodings
   - Simplified string literals in JSON operations
   
2. **Added Comma Separators in JSON Operations**
   - Fixed JSON patch operations array structure
   - Added proper commas between operations for valid JSON formatting

---
**Github repo:** `https://github.com/ms-pwc/adomg-test/actions/workflows/Veracode-Scan.yml`
