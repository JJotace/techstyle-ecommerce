# Contributing to TechStyle

This document defines the Git workflow and release process for the
TechStyle e-commerce project.

## Branching Strategy: GitHub Flow

We use **GitHub Flow** rather than Git Flow or pure Trunk-Based Development.

**Why GitHub Flow for TechStyle:**
- Small team / solo-friendly — no need to maintain a long-lived `develop` branch
- Pairs naturally with our CI pipeline (Day 04): every PR triggers automated
  build/test checks before merge
- Simple mental model: `main` is always deployable, all work happens in
  short-lived feature branches
- Faster feedback loop than Git Flow, more structure than pure trunk-based
  (still uses PRs and reviews, which trunk-based often skips)

### Branch Structure

- `main` — always deployable production code
- `feature/xyz` — new features (e.g. `feature/wishlist`)
- `bugfix/xyz` — non-urgent bug fixes
- `hotfix/xyz` — urgent production fixes
- `release/vX.X.X` — optional, used only when a release needs final
  stabilization before tagging

## Merge Strategy

| Situation | Strategy | Why |
|---|---|---|
| Feature branch with clean, atomic commits | **Merge commit** | Preserves history and shows when features landed |
| Feature branch with messy "WIP" commits | **Squash merge** | Keeps `main` history clean and readable |
| Small, single-commit hotfix | **Fast-forward** | No merge noise needed for trivial changes |
| Rebasing local work before opening a PR | **Rebase** (local only, never on shared branches) | Keeps a linear history before merge |

## Pull Request Requirements

- All changes to `main` go through a Pull Request — no direct pushes
- At least **1 review/approval** required before merging (2 for solo work,
  self-review using the PR diff view before merging)
- PR description must include: what changed, why, and how it was tested
- CI checks (lint + tests) must pass before merge is allowed

## Commit Message Format

We use **Conventional Commits**:

<type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, test, chore

Examples:
feat(cart): add quantity selector
fix(checkout): handle empty cart edge case
docs(readme): update installation steps

## Release & Tagging Process

- Releases follow Semantic Versioning (MAJOR.MINOR.PATCH)
- Tags are created from main once a set of features is stable, using:
  git tag -a vX.X.X -m "Release description"
  git push origin vX.X.X
- A corresponding GitHub Release is published with release notes
  (features, fixes, technical notes)
- Anyone merging to main may propose a release; the release itself is
  tagged after confirming main is stable and CI is green

## Conflict Handling

- The person opening the PR is responsible for resolving merge conflicts
  with main before requesting review
- Conflicts are resolved locally (git merge main or git rebase main
  inside the feature branch), never edited directly on GitHub's web UI
  for non-trivial conflicts
- If a conflict resolution changes logic (not just formatting), it should
  be called out in the PR description for the reviewer's attention
