# Artifact Strategy Decision — TechStyle

## Context

Historically, TechStyle struggled to manage software updates efficiently.
Every time a feature or bugfix was implemented, developers had to manually
check which build results were current and which versions were safe to
reuse. This led to inconsistencies and production errors. This document
records the decision on how build artifacts will be managed going forward.

## Options Evaluated

**Option 1 — Temporary workflow artifact** (`actions/upload-artifact`)
Build output is attached to a single CI run, downloadable for a limited
retention period. No persistent index, no `pip install` from outside CI.

**Option 2 — Self-hosted PyPI registry** (`pypiserver`)
Build output is published to a versioned, persistent package index.
Any project/environment can install a specific version with
`pip install --index-url ... techstyle==X.Y.Z`.

## Decision

**TechStyle will use Option 2 (pypiserver) for any package consumed by
more than one project or environment, and Option 1 for short-lived
debugging/handoff artifacts only.**

### Reasoning

- The original problem — "which build results were current, which
  versions were safe to reuse" — is exactly what a temporary artifact
  cannot solve. Workflow artifacts expire, aren't versioned beyond a
  single CI run, and can't be pulled by another project without going
  through the Actions UI manually.
- A registry gives TechStyle exactly what was missing: `pip install
  techstyle==1.4.2` is unambiguous and reproducible, whether it's run by
  a teammate, a staging environment, or another internal project.
- Temporary artifacts remain useful for their original purpose: a
  developer wants to grab today's build to debug locally, without
  publishing a "real" release.

## When Each Option Applies

| Situation | Option |
|---|---|
| One-off debug build, single developer, single use | Option 1 (upload-artifact) |
| Package needed by multiple environments/projects | Option 2 (pypiserver) |
| Need to `pip install` a specific historical version later | Option 2 (pypiserver) |
| CI run just needs to pass build output to a later job in the same workflow | Option 1 (upload-artifact) |

## Trade-offs and Consequences

**Operations:** Option 2 requires running and maintaining a server
(currently an EC2 instance via Terraform). This is infrastructure
TechStyle now owns and must patch, monitor, and pay for — unlike Option 1,
which has zero operational footprint beyond GitHub Actions itself.

**Security:** The current pypiserver demo setup has no authentication
(`demo`/`demo`). Before any real/production use, this needs real
credentials, TLS (currently plain HTTP, which required
`--trusted-host` to bypass pip's security warning), and ideally IP
restriction rather than the current open `0.0.0.0/0` SSH/HTTP rule.

**Versioning:** Registry usage only pays off if versions are bumped
consistently (SemVer). Without discipline here, Option 2 just becomes a
more complex version of Option 1's problem — an inconsistent set of
uploaded packages nobody trusts.

**Reusability:** Option 2 is what actually enables the original goal —
other projects and environments can depend on a specific, trusted
TechStyle package version without manual coordination.

## Managed-Feed Alternative (Azure DevOps Artifacts)

A managed feed (e.g. Azure DevOps Artifacts) would provide the same
versioned/reproducible benefits as Option 2 without TechStyle operating
its own server — patching, TLS, and auth would be handled by the
provider. The trade-off is vendor lock-in and less control over the
underlying infrastructure. For a team without dedicated ops capacity,
a managed feed may be the more pragmatic long-term choice over
self-hosting pypiserver.

## Quality Gates Before Publishing

Before any package is published to the registry, it must pass:
- Automated tests (pytest) — already enforced in `ci.yml`
- Linting (flake8) — already enforced in `ci.yml`
- A version bump — no re-publishing an already-released version
  (pypiserver already rejects duplicate uploads, confirmed during testing)

## Conclusion

TechStyle will default to Option 1 for temporary/debug artifacts and
adopt Option 2 (pypiserver, or a managed feed if migrating away from
self-hosting) once a package needs to be consumed outside a single CI
run. The operational and security gaps identified above (authentication,
TLS, SemVer discipline) must be addressed before Option 2 is used for
anything beyond internal testing.
