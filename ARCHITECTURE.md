# Architecture

## Boundary

- Frontend or backend: wallet UX, indexing, private drafts, non-authoritative previews, notifications, and optional off-chain source retrieval.
- GenLayer contract: Validators independently agree on the exact applicable-clause bitmask for the frozen policy and pet profile. Separate storage ledgers track policy fields, application fields, masks, and per-clause evidence; all selected tasks must complete before a manager decision.
- External world: No live source collection occurs. Policy text and pet profile are public declarations. Evidence notes are public references and are not authenticated off chain.

## Event path

publish clause document -> open application -> consensus clause mask -> role-bound task completion -> manager decision

## Actors

- policy publisher
- applicant
- designated manager
- GenLayer validators

## Consensus design

The leader produces a normalized bounded result. Each validator independently reruns the substantive task from the same frozen public inputs. Validators compare the decision fields that change state, not merely JSON shape. Invalid model output raises `[LLM_ERROR]` so a broken leader is not accepted.

## Deterministic layer

Separate storage ledgers track policy fields, application fields, masks, and per-clause evidence; all selected tasks must complete before a manager decision. Identifiers, bounds, access checks, ordering, counters, masks, hashes, and terminal-state guards are computed deterministically.

## Persistence

State uses GenLayer storage types only. Public composite records are serialized as canonical JSON where appropriate. Source SHA-256 at evidence generation: `cbae291ada4c1e9b87dd9659dc42b8eb5811dc549a23c2a250cd58f89d96c0b7`.
