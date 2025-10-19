# Branch Protection Configuration

This document describes the branch protection rules that should be configured for the `main` branch.

## GitHub Branch Protection Settings

To configure branch protection for the `main` branch:

1. Go to: `https://github.com/ajdelaguila/opml-news-feeds/settings/branches`
2. Click "Add branch protection rule"
3. Configure the following settings:

### Branch name pattern
```
main
```

### Protection Rules

#### Require a pull request before merging
- ✅ **Enable**: Require a pull request before merging
- ✅ **Require approvals**: 1 approval required
- ✅ **Dismiss stale pull request approvals when new commits are pushed**
- ✅ **Require review from Code Owners**

#### Require status checks to pass before merging
- ✅ **Enable**: Require status checks to pass before merging
- ✅ **Require branches to be up to date before merging**
- Add status check: `build-and-release` (will appear after first workflow run)

#### Other restrictions
- ✅ **Require conversation resolution before merging**
- ✅ **Require signed commits** (optional, recommended)
- ✅ **Require linear history** (optional, keeps history clean)
- ✅ **Include administrators** (applies rules to you as well)

#### Allow bypassing the above settings
- ✅ **Allow specified actors to bypass required pull requests**
  - Add: `@ajdelaguila`

### Recommended Settings Summary

```yaml
Branch Protection Rule for 'main':
  - Require pull request before merging: Yes
  - Required approvals: 1
  - Dismiss stale reviews: Yes
  - Require review from Code Owners: Yes
  - Require status checks: Yes
  - Require branches up to date: Yes
  - Required status checks: build-and-release
  - Require conversation resolution: Yes
  - Require signed commits: Optional
  - Require linear history: Optional
  - Include administrators: Yes
  - Allow bypass by: @ajdelaguila
```

## CODEOWNERS File

The `CODEOWNERS` file has been created at the root of the repository with the following configuration:

- All files are owned by `@ajdelaguila`
- Specific ownership for critical directories:
  - `.github/workflows/*`
  - `scripts/*`
  - `bundles/*`
  - `*.opml.xml`

## How It Works

1. **Creating a PR**: Any changes to `main` must go through a pull request
2. **Automatic Review Request**: You will be automatically requested as a reviewer (via CODEOWNERS)
3. **Status Checks**: The GitHub Action workflow must pass successfully
4. **Your Authority**: As the owner, you can:
   - Approve and merge PRs
   - Bypass branch protection rules when necessary
   - Push directly to `main` (if bypass is enabled)

## Testing the Setup

After configuring branch protection:

1. Create a feature branch: `git checkout -b test/branch-protection`
2. Make a change to any file
3. Push: `git push origin test/branch-protection`
4. Create a PR on GitHub
5. Verify that:
   - You are automatically requested as reviewer
   - CI checks run automatically
   - Merge is blocked until checks pass
   - You can approve and merge as owner

## CLI Configuration (Alternative)

You can also configure branch protection using GitHub CLI:

```bash
gh api repos/ajdelaguila/opml-news-feeds/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["build-and-release"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"dismissal_restrictions":{},"dismiss_stale_reviews":true,"require_code_owner_reviews":true,"required_approving_review_count":1}' \
  --field restrictions=null
```

## Quick Links

- **Branch Protection Settings**: https://github.com/ajdelaguila/opml-news-feeds/settings/branches
- **CODEOWNERS Documentation**: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- **Branch Protection Documentation**: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
