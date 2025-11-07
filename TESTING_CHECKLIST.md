# Automation Testing Checklist

Follow this checklist to verify the automation is working correctly before going live.

## Pre-Test Setup

### 1. Verify GitHub Repositories

- [ ] repository.silvo is published to GitHub
  - URL: https://github.com/MikeSiLVO/repository.silvo
- [ ] script.skin.info.service is published to GitHub
  - URL: https://github.com/MikeSiLVO/script.skin.info.service
- [ ] Both repos are public (required for GitHub Pages)

### 2. Verify GitHub Pages

- [ ] GitHub Pages enabled on repository.silvo
  - Settings → Pages → Source: Deploy from branch `main`
- [ ] Installation page loads:
  - https://mikesilvo.github.io/repository.silvo/

### 3. Verify PAT Setup

- [ ] Personal Access Token (PAT) created
- [ ] PAT added to script.skin.info.service secrets as `REPO_SILVO_PAT`
  - Check: Repo Settings → Secrets and variables → Actions
  - Should see: REPO_SILVO_PAT (Updated X days ago)

### 4. Verify Workflow Files

- [ ] Deploy workflow exists in script.skin.info.service:
  - `.github/workflows/deploy-to-repo.yml`
- [ ] Generate workflow exists in repository.silvo:
  - `.github/workflows/release.yml`

## Test 1: Pre-Release Channel (Beta Version)

### Step 1: Create Beta Version

```bash
cd /mnt/c/Kodi\ -\ Piers/portable_data/addons/script.skin.info.service

# Edit addon.xml
# Change version="2.0.0" to version="2.0.0~beta.1"
```

- [ ] Version updated in addon.xml with `~beta.1` suffix

### Step 2: Commit and Push

```bash
git add addon.xml
git commit -m "Test: automation beta deployment"
git push
```

- [ ] Pushed to GitHub successfully

### Step 3: Monitor Addon Deployment

1. Go to: https://github.com/MikeSiLVO/script.skin.info.service/actions
2. Watch "Deploy to repository.silvo" workflow

**Expected Results:**
- [ ] Workflow starts within 30 seconds
- [ ] "Extract addon metadata" step shows: addon_id, version, channel=pre-release
- [ ] "Package addon" step creates zip file
- [ ] "Clone repository.silvo" step succeeds
- [ ] "Copy files to repository" step copies zip and metadata
- [ ] "Commit and push" step pushes to repository.silvo
- [ ] Workflow completes successfully (green checkmark)

**If workflow fails:**
- Click on failed step to see error
- Common issues: Missing PAT, wrong secret name, invalid addon.xml

### Step 4: Verify Repository Update

1. Go to: https://github.com/MikeSiLVO/repository.silvo
2. Check recent commits

**Expected Results:**
- [ ] New commit appears: "Auto-deploy: script.skin.info.service v2.0.0~beta.1"
- [ ] Commit is from "GitHub Actions Bot"
- [ ] Check pre-release folder has new files:
  - `pre-release/script.skin.info.service/script.skin.info.service-2.0.0~beta.1.zip`
  - `pre-release/script.skin.info.service/addon.xml`
  - `pre-release/script.skin.info.service/icon.png`

### Step 5: Monitor Repository Generation

1. Go to: https://github.com/MikeSiLVO/repository.silvo/actions
2. Watch "Generate Repository Files" workflow

**Expected Results:**
- [ ] Workflow triggers automatically (within 1 minute)
- [ ] "Generate addons.xml files" step runs successfully
- [ ] New commit appears: "Auto-generate repository files [skip ci]"
- [ ] Check files updated:
  - `pre-release/addons.xml`
  - `pre-release/addons.xml.md5`

### Step 6: Verify GitHub Pages Deployment

Wait 2-3 minutes for GitHub Pages to deploy.

**Check addons.xml:**
```bash
curl https://mikesilvo.github.io/repository.silvo/pre-release/addons.xml
```

**Expected Results:**
- [ ] File loads successfully (no 404 error)
- [ ] Contains `<addon id="script.skin.info.service" version="2.0.0~beta.1"`
- [ ] XML is well-formed

**Check addon zip:**
```bash
curl -I https://mikesilvo.github.io/repository.silvo/pre-release/script.skin.info.service/script.skin.info.service-2.0.0~beta.1.zip
```

**Expected Results:**
- [ ] Returns `200 OK` (not 404)
- [ ] Content-Type: application/zip

### Step 7: Test in Kodi

1. Install repository.silvo in Kodi (if not already)
2. Go to Add-ons → My add-ons → Program add-ons
3. Look for script.skin.info.service

**Expected Results:**
- [ ] Shows version 2.0.0~beta.1
- [ ] Can install/update successfully
- [ ] Addon runs without errors

## Test 2: Testing Channel (Side-by-Side Version)

### Step 1: Create Testing Branch

```bash
cd /mnt/c/Kodi\ -\ Piers/portable_data/addons/script.skin.info.service

git checkout -b test-automation
```

- [ ] New branch created

### Step 2: Modify for Testing

Edit addon.xml:
```xml
<!-- Change ID -->
id="script.skin.info.service.test"

<!-- Change version -->
version="2.0.0~test.1"
```

- [ ] Addon ID has `.test` suffix
- [ ] Version has `~test.1` suffix

### Step 3: Commit and Push

```bash
git add addon.xml
git commit -m "Test: automation testing channel deployment"
git push -u origin test-automation
```

- [ ] Pushed to GitHub

### Step 4: Monitor Deployment

Go to: https://github.com/MikeSiLVO/script.skin.info.service/actions

**Expected Results:**
- [ ] Workflow detects `.test` in addon ID
- [ ] Channel shows: testing (not pre-release)
- [ ] Files copied to `testing/script.skin.info.service.test/`
- [ ] Workflow completes successfully

### Step 5: Verify Testing Channel

Check repository.silvo:

**Expected Results:**
- [ ] New commit for testing channel deployment
- [ ] `testing/addons.xml` updated
- [ ] `testing/addons.xml.md5` updated
- [ ] Contains `<addon id="script.skin.info.service.test" version="2.0.0~test.1"`

### Step 6: Verify in Kodi

1. Check Kodi add-ons list
2. Should see **both versions:**
   - script.skin.info.service (production)
   - script.skin.info.service.test (testing)

**Expected Results:**
- [ ] Both versions appear separately
- [ ] Can install both simultaneously
- [ ] Each has its own settings/data directory

## Test 3: Stable Version (Should Not Deploy)

### Step 1: Remove Pre-Release Suffix

```bash
cd /mnt/c/Kodi\ -\ Piers/portable_data/addons/script.skin.info.service

git checkout main

# Edit addon.xml
# Change version="2.0.0~beta.1" to version="2.0.0" (no ~beta)
```

- [ ] Version is stable (no tilde)

### Step 2: Commit and Push

```bash
git add addon.xml
git commit -m "Test: stable version should not auto-deploy"
git push
```

### Step 3: Verify Workflow Behavior

Go to: https://github.com/MikeSiLVO/script.skin.info.service/actions

**Expected Results:**
- [ ] Workflow runs
- [ ] "Extract addon metadata" step detects stable version
- [ ] Logs show: "Skipping deployment - only pre-release versions are deployed"
- [ ] Workflow completes but doesn't push to repository.silvo
- [ ] No new commits in repository.silvo

## Test 4: Multiple Addons

Once script.skin.info.service works, test with skin:

### Step 1: Add Workflow to Skin Repo

```bash
# Copy workflow file from repository.silvo
cp /mnt/c/Kodi\ -\ Piers/portable_data/addons/repository.silvo/_addon_deploy_workflow.yml \
   /path/to/skin.aeon.nox.silvo/.github/workflows/deploy-to-repo.yml
```

- [ ] Workflow file added to skin repo

### Step 2: Add PAT Secret

1. Go to skin.aeon.nox.silvo repo on GitHub
2. Settings → Secrets → Actions → New repository secret
3. Name: `REPO_SILVO_PAT`
4. Value: (paste your PAT)

- [ ] Secret added

### Step 3: Test Skin Deployment

```bash
cd /path/to/skin.aeon.nox.silvo

# Update version to beta
# Edit addon.xml: version="x.y.z~beta.1"

git commit -am "Test: skin auto-deployment"
git push
```

**Expected Results:**
- [ ] Skin workflow triggers
- [ ] Deploys to repository.silvo
- [ ] Both script.skin.info.service and skin appear in addons.xml
- [ ] No conflicts or overwrites

## Final Verification

### Repository Structure

Check that repository.silvo has proper structure:

```
pre-release/
├── addons.xml
├── addons.xml.md5
└── script.skin.info.service/
    ├── addon.xml
    ├── icon.png
    ├── fanart.jpg
    └── script.skin.info.service-2.0.0~beta.1.zip

testing/
├── addons.xml
├── addons.xml.md5
└── script.skin.info.service.test/
    ├── addon.xml
    ├── icon.png
    ├── fanart.jpg
    └── script.skin.info.service.test-2.0.0~test.1.zip
```

- [ ] Structure matches expected layout
- [ ] All required files present
- [ ] No extra/duplicate files

### Kodi Update Check

1. Wait 24 hours (or force update check)
2. Kodi should detect new versions automatically

**Expected Results:**
- [ ] Update notification appears for beta versions
- [ ] Can update directly from Kodi
- [ ] No errors during update

## Cleanup After Testing

Once all tests pass:

```bash
cd /mnt/c/Kodi\ -\ Piers/portable_data/addons/script.skin.info.service

# Return to stable version (or your actual beta)
# Edit addon.xml with real version

git checkout main
git branch -D test-automation  # Delete test branch

git commit -am "Restore production version"
git push
```

- [ ] Test branches removed
- [ ] Version numbers corrected
- [ ] Ready for production use

## Success Criteria

Automation is working correctly when:

- ✅ Pushing beta versions auto-deploys to pre-release channel
- ✅ Pushing .test versions auto-deploys to testing channel
- ✅ Stable versions do NOT auto-deploy
- ✅ addons.xml regenerates automatically
- ✅ GitHub Pages serves updated files
- ✅ Users receive updates in Kodi
- ✅ Multiple addons can deploy without conflicts
- ✅ No manual intervention needed after push

## If Tests Fail

1. Check GitHub Actions logs for specific errors
2. Verify PAT permissions and name match exactly
3. Ensure repository names are correct (MikeSiLVO/repository.silvo)
4. Check addon.xml is valid XML
5. Verify GitHub Pages is enabled and deploying
6. Review AUTOMATION_SETUP.md for missed steps

---

**All tests passed?** You're ready to use the automation for real beta releases!

Document any issues or unexpected behavior for future reference.
