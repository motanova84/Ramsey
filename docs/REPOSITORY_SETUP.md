# Repository Setup Instructions

This document provides instructions for completing the repository setup, particularly for configurations that require GitHub web interface access.

## Adding Repository Topics/Tags

Repository topics improve discoverability on GitHub. Follow these steps to add the recommended topics:

### Via GitHub Web Interface

1. Navigate to https://github.com/motanova84/Ramsey
2. Click on the ⚙️ (gear icon) next to "About" in the right sidebar
3. In the "Topics" field, add the following tags:
   - `ramsey-theory`
   - `z3`
   - `verification`
   - `resonance`
   - `semialgebraic`
   - `frequency-logic`
   - `graph-theory`
   - `combinatorics`
   - `sat-solver`
   - `mathematical-verification`
   - `polynomial-bounds`
   - `vibrational-theory`
4. Click "Save changes"

### Recommended Topics (Spanish)

If targeting Spanish-speaking audience, also consider:
- `teoria-ramsey`
- `matematicas`
- `teoria-grafos`

### Via GitHub CLI (Alternative)

If you have GitHub CLI (`gh`) installed:

```bash
gh repo edit motanova84/Ramsey \
  --add-topic ramsey-theory \
  --add-topic z3 \
  --add-topic verification \
  --add-topic resonance \
  --add-topic semialgebraic \
  --add-topic frequency-logic \
  --add-topic graph-theory \
  --add-topic combinatorics \
  --add-topic sat-solver \
  --add-topic mathematical-verification \
  --add-topic polynomial-bounds \
  --add-topic vibrational-theory
```

### Via GitHub API (Advanced)

Using curl with a personal access token:

```bash
curl -X PUT \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.mercy-preview+json" \
  https://api.github.com/repos/motanova84/Ramsey/topics \
  -d '{
    "names": [
      "ramsey-theory",
      "z3",
      "verification",
      "resonance",
      "semialgebraic",
      "frequency-logic",
      "graph-theory",
      "combinatorics",
      "sat-solver",
      "mathematical-verification",
      "polynomial-bounds",
      "vibrational-theory"
    ]
  }'
```

## Publishing to Zenodo

To generate a DOI for the repository:

### Step 1: Enable Zenodo Integration

1. Visit https://zenodo.org/account/settings/github/
2. Log in with your GitHub account
3. Find "motanova84/Ramsey" in the list
4. Toggle the switch to enable Zenodo integration

### Step 2: Create a Release

1. Go to https://github.com/motanova84/Ramsey/releases/new
2. Tag version: `v1.0.0`
3. Release title: `Vibrational Ramsey Theory v1.0.0`
4. Description:
   ```markdown
   # Vibrational Ramsey Theory v1.0.0

   First stable release of the Vibrational Ramsey Theory implementation.

   ## Features
   - Complete Z3-based verification tools
   - Precomputed table of R_ψ(r,s,ε) values
   - Comprehensive test suite (16 tests)
   - Full documentation and examples
   - CITATION.cff for proper attribution

   ## What's New
   - ✅ Z3 verification script (z3/ramsey_verifier.py)
   - ✅ Usage documentation (z3/README.md)
   - ✅ Precomputed values table (docs/table.md)
   - ✅ Citation metadata (CITATION.cff)
   - ✅ All syntax errors fixed
   - ✅ All tests passing

   ## Getting Started
   ```bash
   pip install -r requirements.txt
   python z3/ramsey_verifier.py --r 3 --s 3
   ```

   See README.md for full documentation.
   ```
5. Click "Publish release"

### Step 3: Update CITATION.cff

After Zenodo generates the DOI:

1. Copy the DOI from Zenodo (format: `10.5281/zenodo.XXXXXXX`)
2. Update `CITATION.cff`:
   ```yaml
   identifiers:
     - type: doi
       value: "10.5281/zenodo.XXXXXXX"  # Replace with actual DOI
       description: "Zenodo DOI"
   ```
3. Commit and push the change

## Converting PR from Draft to Ready

Once all the above steps are complete and you've verified the changes:

### Via GitHub Web Interface

1. Go to https://github.com/motanova84/Ramsey/pulls
2. Find PR #24 (or current PR)
3. Scroll to the bottom
4. Click "Ready for review" button

### Via GitHub CLI

```bash
gh pr ready <PR_NUMBER>
```

### Via GitHub API

```bash
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/motanova84/Ramsey/pulls/<PR_NUMBER>/ready_for_review
```

## Repository Description

Update the repository description (About section) to:

```
Vibrational Ramsey Theory: Frequency-based graph coloring achieving polynomial bounds O(√(rs)·ln(rs)). Includes Z3 verification tools and comprehensive documentation.
```

## Social Preview Image

Consider adding a social preview image:

1. Create an image (1280x640 pixels recommended)
2. Go to repository Settings → Options → Social preview
3. Upload the image

## Additional Configuration

### Enable GitHub Pages (Optional)

If you want to publish documentation as a website:

1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: main (or your preferred branch)
4. Folder: / (root) or /docs
5. Click Save

### Branch Protection

Consider enabling branch protection for `main`:

1. Go to Settings → Branches → Branch protection rules
2. Add rule for `main`
3. Enable:
   - Require a pull request before merging
   - Require status checks to pass before merging
   - Require conversation resolution before merging

## Verification Checklist

After completing setup, verify:

- [ ] Repository has appropriate topics/tags
- [ ] Zenodo integration is enabled
- [ ] Release v1.0.0 is published
- [ ] DOI is generated and added to CITATION.cff
- [ ] PR is marked as "Ready for review"
- [ ] Repository description is updated
- [ ] All tests pass: `python run_tests.py`
- [ ] Z3 verifier works: `python z3/ramsey_verifier.py --r 3 --s 3`
- [ ] README badges are accurate
- [ ] License is MIT (already present)

## Support

For issues or questions about repository setup:
- Open an issue: https://github.com/motanova84/Ramsey/issues
- Contact: motanova84@example.com

---

**Last Updated**: 2025-01-16  
**Version**: 1.0
