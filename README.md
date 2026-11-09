# EcoClaim — Environmental marketing consistency on GenLayer

A small GenLayer Intelligent Contract for comparing the text of an environmental marketing claim with a **caller-disclosed** evidence excerpt and its scope.

**Different from earlier projects:** EcoClaim focuses on the wording and boundaries of environmental marketing claims, rather than contract-language equivalence, shipment monitoring, or general cryptographic source authentication.

## Contract API

- `register(claim_id, product, marketing_claim, scope, evidence_excerpt)`: records the original marketing statement, its scope, and caller-supplied evidence. Each ID is unique.
- `check(claim_id)`: submitter-only, one-time review. If evidence is empty, result is deterministically `NO_EVIDENCE`. Otherwise independent GenLayer validators must agree on `CONSISTENT`, `CONFLICTING`, or `UNCLEAR`.
- `get_claim(claim_id)`: anyone can read the public claim and outcome.

The contract rejects duplicates, missing records, unauthorized reviews, replayed reviews, malformed model outputs and unsafe text controls. A conclusion of `CONSISTENT` means only that the **submitted excerpt** aligns with the submitted wording. It is *not* independent evidence that the environmental claim is true.

**Limitations:** The contract does not retrieve or authenticate documents, measurement equipment, ESG records, certificates, real-world products or supplier reports. Claim data and source excerpts are public on-chain. No regulatory or sustainability certification, financial settlement or payments are provided.

## Verification

```bash
python -m pip install 'genlayer-py @ git+https://github.com/genlayerlabs/genlayer-py@v0.18' 'genlayer-test @ git+https://github.com/genlayerlabs/genlayer-testing-suite@v0.29' 'genvm-linter @ git+https://github.com/genlayerlabs/genvm-linter@main' pytest
python -m pytest -q tests/test_direct_sdk.py
genvm-lint check contracts/EcoClaim.py
```

The workflow `.github/workflows/checks.yml` runs Direct SDK + GenVM lint tests; optional manual public Studionet proof is in `.github/workflows/studionet.yml`. Direct tests alone do not prove finalized public consensus.

See [SUBMISSION.md](SUBMISSION.md) for the GenLayer Portal narrative and evidence links.
