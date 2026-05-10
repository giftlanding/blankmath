---
name: spacelift-logs
description: Inspect Spacelift stack runs and logs for this repo using spacectl. Use when Codex needs to check Spacelift/OpenTofu run status, fetch run logs, diagnose failed plans, retry runs, or confirm whether Spacelift is running from the correct project root.
---

# Spacelift Logs

Use this skill to inspect and diagnose Spacelift runs for this repository.

## Assumptions

- `spacectl` is installed locally.
- The repo has an ignored `.env.local` file with:

```sh
export SPACELIFT_API_KEY_ENDPOINT="https://giftlanding.app.spacelift.io"
export SPACELIFT_API_KEY_ID="..."
export SPACELIFT_API_KEY_SECRET="..."
export SPACELIFT_STACK_ID="blankmath"
```

Always run Spacelift commands through:

```sh
source .env.local && spacectl ...
```

Spacelift commands require network access and may need elevated sandbox permission.

## Basic Checks

Authenticate:

```sh
source .env.local && spacectl whoami
```

Show stack configuration:

```sh
source .env.local && spacectl stack show --id "$SPACELIFT_STACK_ID"
```

List recent runs:

```sh
source .env.local && spacectl stack run list --id "$SPACELIFT_STACK_ID"
```

Fetch run logs:

```sh
source .env.local && spacectl stack logs --id "$SPACELIFT_STACK_ID" --run RUN_ID
```

Retry a failed run:

```sh
source .env.local && spacectl stack retry --id "$SPACELIFT_STACK_ID" --run RUN_ID
```

## Common Diagnoses

- If OpenTofu says `No changes` and no providers are installed, Spacelift probably ran from the repo root instead of `terraform/`.
- Check `Project root` in `spacectl stack show`.
- This repo should configure project root through `.spacelift/config.yml`:

```yaml
version: "2"

stacks:
  blankmath:
    project_root: terraform
    terraform_workflow_tool: OPEN_TOFU
    opentofu_version: "1.11.6"
```

- If OpenTofu reports missing variables such as `cloudflare_account_id`, Spacelift needs `TF_VAR_cloudflare_account_id`, not only `CLOUDFLARE_ACCOUNT_ID`.
- Set Terraform variable aliases with:

```sh
source .env.local && spacectl stack environment setvar --id "$SPACELIFT_STACK_ID" --write-only TF_VAR_cloudflare_account_id VALUE
source .env.local && spacectl stack environment setvar --id "$SPACELIFT_STACK_ID" --write-only TF_VAR_cloudflare_zone_id VALUE
```

Use write-only for secrets and sensitive identifiers unless there is a clear reason not to.

## Current Project Notes

- Stack ID: `blankmath`
- Expected project root: `terraform`
- Expected OpenTofu version: `1.11.6`
- The first real plan should install AWS, Cloudflare, random, and archive providers.
- An unconfirmed run means the plan succeeded and is waiting for approval/apply.
