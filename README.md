# EcoClaim v2 — Quantified green-claim arithmetic on GenLayer

**A fundamentally new mechanism, replacing the earlier three-label text-consistency assessment.**

EcoClaim now tests **numerical environmental marketing claims** against a fixed public baseline and a current measurement. AI consensus performs exactly **one bounded extraction**: a single claimed integer percentage reduction from the marketing statement. **The smart contract itself**, not the AI model, calculates actual reduction in basis points and deterministically decides whether the advertised reduction exceeds the reported measurements.

## Example

A packaging producer publicly reports 1,000 kg CO2e in 2025 and 750 kg in 2026, but advertises a **40% reduction**.

- Deterministic reduction: `(1000 - 750) * 10000 // 1000 = 2500` basis points = **25%**.
- Independent GenLayer validators must agree the marketing statement claims **40%**.
- The contract concludes `OVERSTATED_VS_INPUTS`, because `40 * 100 > 2500`.
- A 25% claim with those same inputs concludes `NOT_OVERSTATED_VS_INPUTS`.
- No clear explicit single whole-number reduction → `UNQUANTIFIED`.

These are **deterministic arithmetic conclusions about caller-supplied data**, not AI-generated three-way credibility judgments.

## Contract methods

- `register(report_id, product, metric, baseline_period, current_period, baseline_units, current_units, marketing_claim, source_note)`: commit two nonidentical reporting periods, public metrics, immutable measurements, and marketing text. Supported units: `CO2E_KG`, `WATER_L`, `ENERGY_KWH`.
- `audit_percentage(report_id)`: author-only, once; GenLayer validators independently extract the same integer claimed reduction. The on-chain code computes arithmetic and stores the outcome, not an AI verdict.
- `get_report(report_id)`: publicly inspect all values, extracted percentage, arithmetic and outcome.

Controls: strict bounds, no zero baseline, no different-metric comparisons, duplicates and replay blocked, malformed or unbounded AI extraction rejected. Basis points avoid rounding errors from floats. No payments or token escrow.

## Difference from earlier submitted work

The previous EcoClaim prototype asked an AI to decide if environmental text was consistent with supporting text—similar to pre-existing claim-verification contracts. **That implementation has been replaced.** This version is a concrete numeric accounting primitive: validator-agreed semantic **number extraction** followed by a transparent and deterministic on-chain percentage comparison. It has neither source fetching nor AI-selected final verdict.

**Important limits:** Both baseline and current measurements and the source note are **self-reported, not authenticated**. `NOT_OVERSTATED_VS_INPUTS` is NEVER environmental certification or proof of real-world improvement. Missing denominators, unit conversion, changing output volumes, time windows or scope changes may make input comparisons misleading. Do not advertise findings as verified emissions reductions.

## Local Direct and GenVM checks

```bash
python -m pip install 'genlayer-py @ git+https://github.com/genlayerlabs/genlayer-py@v0.18' 'genlayer-test @ git+https://github.com/genlayerlabs/genlayer-testing-suite@v0.29' 'genvm-linter @ git+https://github.com/genlayerlabs/genvm-linter@main' pytest
python -m pytest -q tests/test_direct_sdk.py
genvm-lint check contracts/EcoClaim.py
```

**Evidence:** Previous EcoClaim v1 Studionet receipts are historical; they are **not** proof for this new source. This version needs a new contract deployment and Explorer link before Portal submission.
