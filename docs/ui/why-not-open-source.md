# Why Aren't the Workshop and Courtroom UIs Open Source?

**Short answer:** Because they are governance instruments, not UI components.

---

## 1. These interfaces encode separation of powers

The UIs are not generic dashboards. They are **enforcement surfaces** that embody legal and operational boundaries.

Publishing them without the kernel:
- encourages misimplementation
- dilutes accountability guarantees
- invites unsafe forks

---

## 2. The UIs are kernel-coupled by design

Without the governance kernel:
- workflows appear incomplete
- decisions appear blocked
- evidence appears inaccessible

This is intentional.

Open sourcing them prematurely would misrepresent the system.

---

## 3. Transparency ≠ source availability

We provide:
- architectural documentation
- UI walkthroughs
- screenshots
- invariants and guarantees

What we do not provide (yet):
- mutable enforcement surfaces
- partial governance implementations

---

## 4. When will this change?

We plan to publish:
- frozen UI snapshots
- read-only reference implementations
- governance UI kits

**Only after:**
- kernel contracts are stable
- invariants are externally validated
- misinterpretation risk is minimized

---

## 5. What should reviewers evaluate today?

Reviewers should focus on:
- separation of powers
- fail-closed behavior
- receipt immutability
- evidence verifiability

All of these are documented and observable without source access.

---

## Closing Statement

> Governance is not a theme.
> It is a constraint system.
> Constraints must be proven before they are shared.

