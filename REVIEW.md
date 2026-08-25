# Reviewer Guide

## Mechanism in one sentence

A reusable clause-task ledger where validators select applicable policy clauses and each resulting task can be completed only by its assigned applicant or manager role.

## What consensus actually decides

Validators independently agree on the exact applicable-clause bitmask for the frozen policy and pet profile.

## What code settles afterward

Separate storage ledgers track policy fields, application fields, masks, and per-clause evidence; all selected tasks must complete before a manager decision.

## Why this is distinct

It uses per-field ledgers and a split-role clause checklist rather than the shared JSON-record lifecycle that caused the prior rejection.

## Fast review path

1. Confirm the pinned dependency on the first source line.
2. Inspect the custom validator and verify it reruns the substantive task.
3. Trace role checks and terminal-state guards in each write method.
4. Run lint, strict type checking, seven direct tests, and the five-validator integration test.
5. Compare `abi.json` and the StudioNet manifest to the committed source hash.

## Known limitations

Publisher, applicant, and manager wallets are not real-world identity proofs. The contract does not determine legal compliance or animal safety.
