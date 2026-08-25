# PetPolicyPath

A reusable clause-task ledger where validators select applicable policy clauses and each resulting task can be completed only by its assigned applicant or manager role.

## Why GenLayer

Validators independently agree on the exact applicable-clause bitmask for the frozen policy and pet profile. Separate storage ledgers track policy fields, application fields, masks, and per-clause evidence; all selected tasks must complete before a manager decision.

## Roles

- policy publisher
- applicant
- designated manager
- GenLayer validators

## Lifecycle

publish clause document -> open application -> consensus clause mask -> role-bound task completion -> manager decision

## Contract interface

- Constructor: none
- Write methods: compile_tasks, complete_task, deactivate_policy, decide_application, open_application, publish_policy, withdraw_application
- View methods: get_application, get_application_count, get_application_id, get_policy, get_policy_count, get_policy_id
- Runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

## Public-data warning

All contract inputs, evidence, notes, addresses, model results, and state are public. Do not submit secrets, private documents, personal contact information, or confidential identifiers.

## Source model

No live source collection occurs. Policy text and pet profile are public declarations. Evidence notes are public references and are not authenticated off chain.

## Verification

```text
genvm-lint check contracts/pet_policy_path.py
genvm-lint typecheck contracts/pet_policy_path.py --strict
python -m pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
python -m pytest tests/integration -q -s
```

The repository contains seven direct tests and one full five-validator GLSim flow. StudioNet evidence is recorded separately under `deployments/` after network execution.

## Limitations

Publisher, applicant, and manager wallets are not real-world identity proofs. The contract does not determine legal compliance or animal safety.

Licensed under MIT. See `LICENSE`.
