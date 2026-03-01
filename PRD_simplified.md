TITLE: GHCP-BOOTSTRAP SPEC (Simplified) — Experiment Platform Setup

PURPOSE
Build a reproducible platform that lets GitHub Copilot CLI run an experiment matrix and deploy each run to Azure Container Apps while capturing logs, metrics, and manifests.

GOALS
- Provision Azure infrastructure (ACR + Container Apps environment + web/api apps).
- Create a GitHub repo with a deterministic web+api skeleton and tiered specs.
- Run an experiment matrix: 2 models × 5 conditions × 4 tiers (40 runs).
- Persist per-run artifacts: manifests, logs, build/test results, and deployment URLs.

NON-GOALS
- Building a full production app beyond the tier specs.
- Adding databases or extra services unless explicitly required by a tier.

CONSTRAINTS
- Use only public documentation links in comments/docs.
- Never print or commit secrets; use GitHub Secrets for sensitive values.
- Keep runs deterministic: fixed repo structure, fixed prompts, fixed K slices (K ∈ {3,5,7}).

ASSUMPTIONS
- User has GitHub access with Copilot enabled.
- User has Azure subscription permissions.
- Local machine has: gh, az, git, Node.js 22+, and (optional) Docker.

REQUIRED INPUTS (USER-PROVIDED)
Set locally (environment variables or equivalent):
- EXP_PREFIX
- GH_ORG_OR_USER
- REPO_NAME
- AZ_SUBSCRIPTION_ID
- AZ_LOCATION
- AZ_RG
- AZ_ACR
- AZ_ACA_ENV
- AZ_WEB_APP
- AZ_API_APP
Optional:
- RUN_SCOPE (shared | per-run)
- RETENTION_DAYS

DELIVERABLES
- GitHub repo with:
  - apps/web (React+Vite)
  - apps/api (FastAPI)
  - specs/base_prd.md
  - specs/tiers/tier0.md .. tier3.md
  - scripts/ (split/integrate/metrics stubs)
  - .github/workflows/experiment.yml
- Azure resources:
  - Resource group, ACR, ACA environment, web app, api app
- Per-run artifacts:
  - run_manifest.json, logs, build/test output, deployment URLs

REPO STRUCTURE (CANONICAL)
/
  apps/
    web/
    api/
  specs/
    base_prd.md
    tiers/
      tier0.md
      tier1.md
      tier2.md
      tier3.md
  scripts/
  .github/workflows/

WORKFLOW BEHAVIOR (REQUIRED)
Trigger: workflow_dispatch
Matrix:
- model: [gpt-5.3-codex, claude-opus-latest]
- condition: [single, single_plan, k3, k5, k7]
- tier: [tier0, tier1, tier2, tier3]

Condition logic:
- single: implement full spec directly.
- single_plan: generate plan, then implement.
- k3/k5/k7: split into K slices, implement in parallel, integrate, test, deploy.

PHASE 1 (MINIMUM VIABLE)
- Single job runs matrix and captures artifacts.
- k3/k5/k7 may only split (no parallel implementers yet).

PHASE 2 (REQUIRED FOR FINAL)
Implement true parallelism for k3/k5/k7:
- Job A: split and upload slices artifact.
- Job B: implement_slice matrix (one job per slice).
- Job C: integrate_and_test (merge slices deterministically).
- Job D: deploy (web + api).

ARTIFACTS & METRICS
Each run must include:
- run_manifest.json (run key, model, condition, tier, app identifiers)
- Stage timings (start/end timestamps)
- Build/test results (web + api)
- Copilot CLI usage/context info (best-effort)
- Deployment URLs (web + api)

ACCEPTANCE CRITERIA
- Repo structure matches the canonical layout.
- Experiment workflow runs a full matrix.
- All runs produce artifacts and manifests.
- Azure deployments complete with stable URLs.
- No secrets printed or committed.
- Deterministic prompts and slice counts are enforced.

REFERENCE LINKS (PUBLIC)
- Copilot CLI command reference: https://docs.github.com/en/copilot/reference/cli-command-reference
- Copilot CLI in Actions: https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-with-actions
- Copilot CLI getting started: https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-getting-started
- Workflow artifacts: https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts
- Azure Container Apps GitHub Actions: https://learn.microsoft.com/azure/container-apps/github-actions
