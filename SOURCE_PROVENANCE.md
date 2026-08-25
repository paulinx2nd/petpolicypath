# Source Provenance

## Collection behavior

No live source collection occurs. Policy text and pet profile are public declarations. Evidence notes are public references and are not authenticated off chain.

The contract performs no live web request, does not scrape a page, and does not silently claim that a label or URL authenticates its publisher. This avoids validator drift from changing pages. If an application needs live retrieval, that retrieval belongs in a separately reviewed mechanism whose validators independently fetch and normalize the same source.

## Integrity bindings

- Contract source SHA-256: `cbae291ada4c1e9b87dd9659dc42b8eb5811dc549a23c2a250cd58f89d96c0b7`
- ABI SHA-256: `c949503011c10fb84fc837434761fe92f4a404100bf8db429e9fa12986cc987e`
- Frozen text and canonical JSON records are hashed inside the contract where the workflow needs a content binding.
- Human-readable source references, when present, are expressly marked unverified.

## Fixture policy

Tests use synthetic public fixtures written for this repository. They are not copied production records and do not represent real people.
