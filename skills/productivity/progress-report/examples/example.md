---
project: Example care application
report: Migration progress · illustrative example
headline: Core workflows are published; the release rehearsal remains
updated: 6 October 2026 at 14:00 UK time · fictional sample
---

## Overview

The replacement application can sign users in and record care activity. The foundation has been accepted. The latest shared-care work passes locally and is published, but its hosted checks are still running.

**Keep the existing application in production.** The saved-state rollback rehearsal is still required before the first release.

## Release boundary

The first release requires the application runner, sign-in, shared-care recording and a saved-state rollback rehearsal. Offline capture remains in the full goal and is deferred from this release.

Whole-slice acceptance, merging and deployment remain visible in each checklist. Release approval also requires the completed rehearsal and an agreed operating plan.

## Slice foundation | Application foundation

### Details

Accepted: passed @foundation
Closes: Run the replacement through its normal entry point and record independent acceptance of the published runner.

### runner | Start the replacement application

Scope: first-release
Implementation: complete @foundation
Local checks: passed @foundation
Publication: published @foundation
Hosted checks: passed @foundation
Acceptance: passed @foundation
Merge: merged @foundation
Deployment: not-deployed
Works: The normal entry point starts the replacement and serves its pages.
Remaining: None
Next: None

## Slice care | Sign-in and shared care

### Details

Accepted: pending
Closes: Accept all sign-in and care journeys, including withdrawn access, repeated requests and offline replay for the full goal.

### sign-in | Sign users in

Scope: first-release
Implementation: complete @accounts
Local checks: passed @accounts
Publication: published @accounts
Hosted checks: passed @accounts
Acceptance: pending
Merge: unmerged
Deployment: not-deployed
Works: Users can sign in, recover access and end a session.
Remaining: Independent whole-slice acceptance remains.
Next: Include the published account journeys in the final care review.

### care-record | Record shared care activity

Scope: first-release
Implementation: complete @care
Local checks: passed @care
Publication: published @care
Hosted checks: pending @care
Acceptance: pending
Merge: unmerged
Deployment: not-deployed
Works: Current members can record care activity; withdrawn members are denied.
Remaining: The hosted run for the published revision has not finished.
Next: Inspect the hosted result for example-care-02 and resolve any failures.

### offline | Capture care activity while offline

Scope: full-goal
Implementation: in-progress @offline
Local checks: pending
Publication: unpublished
Hosted checks: pending
Acceptance: pending
Merge: unmerged
Deployment: not-deployed
Works: A local draft stores activity while disconnected.
Remaining: Replay, conflict handling and withdrawn-access checks remain.
Next: Complete replay through the same authorised care operation.

## Slice release | Release and rollback

### Details

Accepted: pending
Closes: Restore independent saved data, run the existing application and record the complete release rehearsal.

### restore | Rehearse restoration of saved data

Scope: first-release
Implementation: not-started
Local checks: pending
Publication: unpublished
Hosted checks: not-required @rehearsal-scope
Acceptance: pending
Merge: unmerged
Deployment: not-deployed
Works: None
Remaining: Restoration and operation on the saved state are unproved.
Next: Restore the agreed snapshot in an isolated environment and record the result.

## Evidence

### foundation | Runner publication and acceptance

Observed: 6 October 2026 at 10:00 UK time · fictional
Revision: example-foundation-01
Source: https://example.org/foundation
Note: Illustrative evidence for implementation, local and hosted checks, publication, acceptance and merging. No deployment is recorded.

### accounts | Published account journeys

Observed: 6 October 2026 at 11:00 UK time · fictional
Revision: example-accounts-01
Source: https://example.org/accounts
Note: Illustrative evidence for implemented journeys, passing local and hosted checks and publication. Whole-slice acceptance remains pending.

### care | Published shared-care work with a pending hosted run

Observed: 6 October 2026 at 13:00 UK time · fictional
Revision: example-care-02
Source: https://example.org/care
Note: Illustrative evidence for implementation, passing local checks, publication and a pending hosted run. This item earns no point yet.

### offline | Local offline draft

Observed: 6 October 2026 at 13:30 UK time · fictional
Revision: example-offline-draft
Source: https://example.org/offline
Note: Illustrative in-progress implementation; no complete replay checks or publication.

### rehearsal-scope | Agreed restore rehearsal scope

Observed: 6 October 2026 at 09:00 UK time · fictional
Revision: example-release-plan-01
Source: https://example.org/release-plan
Note: Hosted checks do not apply to this manually observed restore rehearsal. A published rehearsal record and passing local checks are still required.

## Limitations

This is a fictional format example, not a live MedTracker status report. Evidence URLs are placeholders. The retained MedTracker HTML supplies the design reference only.

The first-release column counts its explicitly required items. It does not declare the release approved or deployed. Full-goal deferrals remain in the slice denominators.
