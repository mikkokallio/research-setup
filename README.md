# GHCP-BOOTSTRAP Experiment Platform

This repo scaffolds a deterministic web + api app and a GitHub Actions workflow that runs an experiment matrix and deploys to Azure Container Apps. It matches the simplified PRD in PRD_simplified.md.

## Defaults
- `AZ_LOCATION` is fixed to `swedencentral`.
- `RUN_SCOPE` is `shared` with per-run revision suffixes.
- `RETENTION_DAYS` is 30.

## Required GitHub Secrets
Set these as **Secrets** in the repo:
- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`

## Required GitHub Variables
Set these as **Variables** in the repo:
- `EXP_PREFIX` (default: `exp`)
- `GH_ORG_OR_USER` (default: `mikkokallio`)
- `REPO_NAME` (default: `copilot-mas`)
- `AZ_SUBSCRIPTION_ID`
- `AZ_LOCATION` (must be `swedencentral`)
- `AZ_RG`
- `AZ_ACR`
- `AZ_ACA_ENV`
- `AZ_WEB_APP`
- `AZ_API_APP`
- `RUN_SCOPE` (`shared`)
- `RETENTION_DAYS` (default: `30`)

## Local Env Example
See .env.example for a local reference.

## Notes
- The workflow uses Container Apps revisions to provide per-run URLs without creating 40 separate apps.
- Keep resources and naming consistent across runs.

## Public References
- https://docs.github.com/en/copilot/reference/cli-command-reference
- https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-with-actions
- https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-getting-started
- https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts
- https://learn.microsoft.com/azure/container-apps/github-actions
