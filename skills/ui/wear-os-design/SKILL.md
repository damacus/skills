---
name: wear-os-design
description: Design, implement and verify native Wear OS screens and navigation with Wear Compose Material 3. Use for round-watch layouts, touch feedback, rotary scrolling, swipe-back, phone companions and physical-watch checks.
---

# Wear OS design and navigation

Design for a short interaction on a wrist. Establish the user's task, entry
point and successful exit before choosing components. Inspect the actual watch
module, protocol and selected visual reference; a missing screenshot need not
block exploratory concepts. Distinguish proposed screens from existing features.

## Screen and interaction decisions

- Give each screen one obvious primary action. Use a shallow list-to-detail flow
  when selecting an item; avoid inserting a menu between routine actions.
- Keep the primary action in the owner's chosen comfortable position. An edge
  button is a platform option, not a reason to override an approved central pill.
- Use the round safe area, readable semantic typography and restrained colour.
  Verify long names and large system fonts on the smallest supported viewport.
- Start with one expressive moment, such as an outlined pill filling on press.
  Preserve text contrast in resting, pressed, disabled and focused states.
- Separate press feedback from activation. A cancelled press does not activate;
  keyboard and accessibility activation must still work. Filling on touch is
  not progress toward a clinical write or a hold-to-confirm gesture unless the
  owner explicitly chose that behaviour.
- Make the action label match its effect. A preview must identify sample data
  and simulated results; do not imply a dose was saved or a device is connected
  without evidence. Honour reduced motion and avoid continuous decoration.

## Implementation

Use Wear-specific Compose Material 3 components rather than phone navigation
chrome. Read the selected components' current official samples before coding.
Check published Maven metadata and the project's compiler/SDK constraints;
choose stable compatible versions and pin them through existing project tooling.
Do not copy old version claims or obsolete widgets from a third-party skill.

For new navigation, inspect the current stable Wear Navigation 3 guidance and
its swipe-dismiss scene strategy. Existing Wear Navigation applications can
retain their supported host unless migration is part of the task. Use one
application scaffold and screen scaffolds; pass screen padding into scrollable
content. Use Wear scrolling lists, position feedback and rotary handling.
Preserve back-stack and selected-item state across recreation. Keep swipe-back
available rather than intercepting it with a horizontal application gesture.

Use semantic theme colours and typography, native labelled controls and generous
touch targets. Prefer component defaults; use at least 48 dp interactive targets
for this workflow. Screens that can overflow with larger fonts must scroll.

Keep phone-companion transport separate from watch presentation. Inspect what
the protocol actually carries before wiring screens. Never move account
credentials onto a companion watch or add direct server transport merely to
make a mockup work. Authentication, expiry and domain writes retain their owning
application checks. A UI preview is a separate development entry point.

## Verify and deliver

Use the repository's tasks and meaningful tests for navigation state, cancellation
and action results. Preserve dependency, permission and credential-boundary gates
when adding Compose. Check fresh launch, list/detail/back, rotary input, long
text, font scaling and press cancellation. Report untested interactions plainly.

For an authorised physical watch, list ADB devices and select its exact serial.
Wireless connection and pairing use different ports; request the current pairing
endpoint/code only if needed. Never scan unrelated network devices. Installing an
update must preserve existing app data; do not uninstall to bypass a signing
mismatch. Capture only the app under test, avoid personal notifications, and keep
private screenshots out of commits. Distinguish build, install, observed device
behaviour, backend acceptance and publication.

## Sources and maintenance

Original synthesis, informed by these sources; check their current guidance when
API or platform details matter:

- [Google Wear Compose M3 skill][wear]: Wear components, scaffolds, scrolling
  and Navigation 3.
- [Wear Compose navigation][navigation]: platform host and back-stack integration;
  compare its versioned guidance with current samples.
- [Material 3 Expressive skill][expressive]: visual hierarchy, purposeful
  shape/colour and restrained motion.
- [Add Wear OS app skill][companion]: separate native watch module and phone
  Data Layer boundaries. Its older version and component examples are not
  dependency guidance.
- [Navigation Event skill][events]: prefer the navigation library's existing
  back handling over introducing duplicate low-level handlers.

These sources guide implementation choices; they do not authorise connecting,
installing, publishing, deploying or performing live domain actions.

[wear]: https://github.com/android/skills/tree/main/wear/wear-compose-m3
[navigation]: https://developer.android.com/training/wearables/compose/navigation
[expressive]: https://skills.sh/albermonte/android-skills/material-3-expressive
[companion]: https://skills.sh/khadinakbarlabs/expo-mobile-app-builder/add-wear-os-app
[events]: https://skills.sh/android/skills/navigation-event
