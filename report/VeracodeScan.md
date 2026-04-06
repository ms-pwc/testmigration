# Veracode Scan Workflow - Changes Documentation

## Summary
This document outlines all changes made to the GitHub Actions Veracode-Scan workflow and associated Azure DevOps integration.

---

## 1. Repository Settings & Secrets Configuration

### Added Variables in Settings (Repo Level)
- **ado_pat** - Azure DevOps Personal Access Token variable
- **ado_org** - Azure DevOps Organization name variable  
- **ado_assigned_to** - Azure DevOps user to assign work items to

**Location:** Repository Settings → Secrets and Variables → Actions Variables

---

## 2. GitHub Secrets Management

### Updated/Changed Secrets
- **GIT_PAT** - GitHub Personal Access Token (changed)
  - Used at: [Line 29](../.github/workflows/Veracode-Scan.yml#L29) - Repository checkout authentication
  - Scope: Read access to target repositories

- **ADO_PAT** - Azure DevOps Personal Access Token (added)
  - Used at: [Line 141](../.github/workflows/Veracode-Scan.yml#L141) - Environment variable for Azure DevOps API calls
  - Scope: Create work items in Azure DevOps

### New Token Added
- **APTA_TOKEN** - Additional authentication token (newly added)
  - Purpose: Secondary authentication or backup token for Azure DevOps operations
  - Status: Ready for use in workflow

**Location:** Repository Settings → Secrets and Variables → Actions Secrets

---

## 3. Workflow Environment Variables

### Environment Variables Configuration (Line 140-143)
```yaml
env:
  ADO_PAT: ${{ secrets.ADO_PAT }}
  ADO_ORG: ${{ vars.ADO_ORG }}
  ADO_ASSIGNED_TO: ${{ vars.ADO_ASSIGNED_TO }}
```

**Changes Made:**
- Added explicit environment variable declarations for Azure DevOps integration
- Separated secrets from variables (vars vs secrets prefix)
- ADO_PAT pulls from secrets (secure storage)
- ADO_ORG and ADO_ASSIGNED_TO pull from repository variables (non-sensitive)

---

## 4. Error Handling & Try-Catch Implementation (Line 65+)

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

## 5. Azure DevOps Work Item Creation Script

### Script Enhancements

#### Location: Lines 135-170 - Create Azure DevOps work item on failure

**Changes Made:**

1. **Removed HTML Entity Encoding (%27)**
   - Removed hardcoded `%27` single quote encodings
   - Simplified string literals in JSON operations
   
2. **Added Comma Separators in JSON Operations**
   - Fixed JSON patch operations array structure
   - Added proper commas between operations for valid JSON formatting

**Script Improvements:**
```yaml
ops = [
    {'op': 'add', 'path': '/fields/System.Title', 'value': 'ConcourseSearch Veracode Backend Scan Pipeline Failing'},
    {'op': 'add', 'path': '/fields/System.AreaPath', 'value': project},
    {'op': 'add', 'path': '/fields/System.IterationPath', 'value': project},
    {'op': 'add', 'path': '/fields/System.Tags', 'value': 'Build ${{ github.run_number }}'},
    {'op': 'add', 'path': '/fields/System.Description', 'value': '<br/>'.join(description_lines)}
]
```

**Authentication:**
- Uses Base64 encoding for PAT token
- Implements proper HTTP Authorization header
- Sets correct Content-Type: `application/json-patch+json`

---

## 6. Step-by-Step Implementation Checklist

- [x] Added ADO environment variables to workflow step
- [x] Created ADO_PAT secret in GitHub repository
- [x] Added ADO_ORG repository variable
- [x] Added ADO_ASSIGNED_TO repository variable
- [x] Updated GIT_PAT secret with new token
- [x] Implemented try-catch for JSON parsing (line 65+)
- [x] Removed %27 HTML entity codes from work item script
- [x] Added proper comma separators in JSON operations
- [x] Added APTA_TOKEN for secondary authentication
- [x] Updated Base64 authentication token generation
- [x] Tested Azure DevOps API endpoint: `/_apis/wit/workitems/$Issue?api-version=7.1`

---

## 7. API Endpoint Details

### Azure DevOps Work Item Creation Endpoint
- **URL:** `https://dev.azure.com/{org}/{project}/_apis/wit/workitems/$Issue?api-version=7.1`
- **Method:** POST
- **Content-Type:** `application/json-patch+json`
- **Authentication:** Basic Auth (Base64 encoded PAT)
- **Project:** `testmigration`

---

## 8. Configuration Reference

### Required Repository Variables
```
ADO_ORG=<Azure DevOps Organization Name>
ADO_ASSIGNED_TO=<User Email or ID>
```

### Required Repository Secrets
```
GIT_PAT=<GitHub Personal Access Token>
ADO_PAT=<Azure DevOps Personal Access Token>
APTA_TOKEN=<Additional Authentication Token>
VERACODE_API_ID=<Veracode API ID>
VERACODE_API_KEY=<Veracode API Key>
```

---

## 9. Testing & Validation

- Workflow uses `exit 1` to simulate failure for testing
- Work item creation triggers on `if: failure()` condition
- JSON patch operations validated for Azure DevOps API format
- Exception handling tested with various JSON input formats

---

## 10. Impact & Benefits

✅ **Improved Security:** Proper secret management separation  
✅ **Better Error Handling:** Graceful fallback for JSON parsing  
✅ **Cleaner Code:** Removed unnecessary HTML entities  
✅ **Valid JSON:** Proper comma separators in operations array  
✅ **Automation:** Automatic work item creation on pipeline failures  
✅ **Flexibility:** Support for multiple input formats  

---

**Last Updated:** April 6, 2026  
**Workflow File:** `.github/workflows/Veracode-Scan.yml`
