# Automation Setup Guide

This guide will help you set up the cross-repository automation so that pushing to addon repos automatically deploys to repository.silvo.

## Overview

When you push changes to an addon repository (like script.skin.info.service), the automation will:
1. Detect version changes in addon.xml
2. Package the addon into a zip file
3. Deploy to the appropriate channel in repository.silvo
4. Trigger repository.silvo to regenerate addons.xml
5. Deploy to GitHub Pages for user updates

## Prerequisites

- [x] repository.silvo is published to GitHub
- [x] GitHub Pages is enabled on repository.silvo
- [ ] Create GitHub Personal Access Token (PAT)
- [ ] Add PAT to each addon repository
- [ ] Push addon repos to GitHub (if not already done)

## Step 1: Create GitHub Personal Access Token (PAT)

The PAT allows addon repositories to push to repository.silvo automatically.

### Create the Token

1. Go to GitHub.com and sign in as **MikeSiLVO**
2. Click your profile picture (top right) → **Settings**
3. Scroll down to **Developer settings** (bottom of left sidebar)
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**

### Configure the Token

**Note:** `Repository automation for repository.silvo`

**Expiration:** Choose **No expiration** (or 1 year if you prefer)

**Select scopes:** Check only these:
- ✅ **repo** (Full control of private repositories)
  - This includes: repo:status, repo_deployment, public_repo, repo:invite, security_events

**Click:** Generate token

### Save the Token

⚠️ **IMPORTANT:** Copy the token immediately! You won't be able to see it again.

The token will look like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

Save it somewhere secure (password manager, encrypted note, etc.)

## Step 2: Add PAT as Secret to Addon Repositories

You need to add this token to **each addon repository** that will auto-deploy to repository.silvo.

### For script.skin.info.service

1. Go to: https://github.com/MikeSiLVO/script.skin.info.service
2. Click **Settings** tab (top of repo page)
3. Click **Secrets and variables** → **Actions** (left sidebar)
4. Click **New repository secret**
5. **Name:** `REPO_SILVO_PAT`
6. **Secret:** Paste your PAT token
7. Click **Add secret**

### For skin.aeon.nox.silvo (and any other addons)

Repeat the same process:
1. Go to the addon's GitHub repository
2. Settings → Secrets and variables → Actions
3. New repository secret
4. Name: `REPO_SILVO_PAT`
5. Paste token
6. Add secret

## Step 3: Add Deployment Workflow to Addon Repos

The workflow file has already been created for script.skin.info.service at:
```
script.skin.info.service/.github/workflows/deploy-to-repo.yml
```

### For Other Addons

Copy the template from repository.silvo:

```bash
# From repository.silvo directory
cp _addon_deploy_workflow.yml /path/to/your-addon/.github/workflows/deploy-to-repo.yml
```

Or manually create `.github/workflows/deploy-to-repo.yml` in each addon repo using the template.

## Step 4: Commit and Push

### For script.skin.info.service

```bash
cd /mnt/c/Kodi\ -\ Piers/portable_data/addons/script.skin.info.service

# Add the workflow file
git add .github/workflows/deploy-to-repo.yml
git commit -m "Add automated deployment to repository.silvo"
git push
```

### For repository.silvo

```bash
cd /mnt/c/Kodi\ -\ Piers/portable_data/addons/repository.silvo

# Commit updated workflow
git add .github/workflows/release.yml
git commit -m "Update repository generation workflow"
git push
```

## Step 5: Test the Automation

### Test with script.skin.info.service

1. Make a small change to script.skin.info.service
2. Update version in addon.xml: `2.0.0` → `2.0.1~beta.1`
3. Commit and push:
   ```bash
   git commit -am "Test: bump version for automation test"
   git push
   ```

4. Watch the GitHub Actions:
   - Go to: https://github.com/MikeSiLVO/script.skin.info.service/actions
   - You should see "Deploy to repository.silvo" workflow running
   - Click on it to watch progress

5. After 2-3 minutes, check repository.silvo:
   - Go to: https://github.com/MikeSiLVO/repository.silvo
   - Look for automated commit: "Auto-deploy: script.skin.info.service v2.0.1~beta.1"
   - Check pre-release folder has the new zip

6. Verify GitHub Pages:
   - Wait 2-3 more minutes for Pages to deploy
   - Visit: https://mikesilvo.github.io/repository.silvo/pre-release/addons.xml
   - Should show your updated version

## Troubleshooting

### Workflow fails with "Permission denied"
- PAT not added to addon repo secrets
- PAT has wrong name (must be exactly `REPO_SILVO_PAT`)
- Solution: Double-check Step 2

### Workflow doesn't trigger
- Version doesn't have pre-release suffix (~beta, ~rc, ~alpha)
- Not pushing to main/master branch
- Solution: Add ~beta.1 to version, ensure correct branch

### Repository.silvo doesn't update
- Wait 5 minutes - there can be delays
- Check GitHub Actions on repository.silvo repo
- Ensure workflow file has [skip ci] in commit message to prevent loops

### "No changes to commit" in repository.silvo
- This is normal if addons.xml hasn't changed
- Means your addon was already up to date

## Your New Workflow

Once setup is complete, your workflow is:

```
1. Edit addon code in Kodi addons folder
2. Bump version in addon.xml (manual): 2.0.0 → 2.1.0~beta.1
3. git commit -am "Add new feature"
4. git push
5. ☕ Wait 3-5 minutes
6. Done! Users receive update within 24 hours
```

## Channel Selection

The automation automatically chooses the channel based on version/ID:

| Version/ID | Channel | Example |
|------------|---------|---------|
| Contains `~beta` | pre-release | `2.1.0~beta.1` |
| Contains `~rc` | pre-release | `2.1.0~rc.1` |
| Contains `~alpha` | pre-release | `2.1.0~alpha.1` |
| ID has `.test` suffix | testing | `addon.id.test` |
| No pre-release suffix | Skipped | `2.1.0` (stable) |

**Note:** Stable versions (no tilde) are **not** deployed to repository.silvo. Those should go to official Kodi repository only.

## Security Notes

- Never commit the PAT token to git
- PAT is stored securely in GitHub Secrets (encrypted)
- Only GitHub Actions can access the secret
- Workflows run in isolated containers
- You can revoke/regenerate the PAT anytime

## Next Steps

After setup:
1. ✅ Commit and push changes to script.skin.info.service
2. ✅ Test the automation with a beta version
3. ⏭️ Copy workflow to other addon repos (skin.aeon.nox.silvo)
4. ⏭️ Share repository.silvo URL with users for feedback

## Support

If you encounter issues:
1. Check GitHub Actions logs (click on failed workflow)
2. Verify PAT is added correctly with right permissions
3. Ensure repository names match (MikeSiLVO/repository.silvo)
4. Check that GitHub Pages is enabled on repository.silvo

---

**Setup completed?** Try the test in Step 5 to verify everything works!
