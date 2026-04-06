Validation Date and Time : 26/04/06 Friday 13:30:00

# DDS Concourse KeyVault Workflow Notes

## Status
- No code changes were made.
- mannually added the required varibales (Azure login creds).

## Important Auth Setup Note
- Azure `tenant-id`, `client-id`, and `subscription-id` were maintained as secrets in another place previously.
- For this workflow file, values are now being handled through GitHub Actions variables (manually added for this file’s mapping flow).
- Keep this mapping consistent with the selected `AZURESUB` input to avoid authentication mismatches.

## GitHub Actions YAML Testing Link
- https://github.com/ms-pwc/adomg-test/actions/workflows/DDS-consourse.yml
