# Workflow Changes Summary

1. Permissions block was moved to the top.
2. Conditions are applied at job level rather than step level.
3. Variable group alignment was added by resolving environment-specific values before execution.
4. Common variables are defined once at global level instead of repeating in each step.
5. For multi-key flow, variables and secrets were added manually in the GitHub repo.
