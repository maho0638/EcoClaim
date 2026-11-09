"""Public Studionet proof: consensus-extracted numbers, deterministic final arithmetic."""
import json
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


def confirmed(call, tag, consensus=False):
    kwargs = dict(wait_interval=10000, wait_retries=100)
    if consensus:
        kwargs["consensus_max_rotations"] = 4
    receipt = call.transact(**kwargs)
    assert tx_execution_succeeded(receipt), f"{tag}: {receipt.get('hash', '')}"
    print(f"{tag}_TX={receipt.get('hash', '')}", flush=True)
    return receipt


def report(contract, key):
    return json.loads(str(contract.get_report(args=[key]).call()))


def test_live_quantified_claims(default_account):
    contract = get_contract_factory("EcoClaim").deploy(
        account=default_account, consensus_max_rotations=4,
    )
    assert len(str(contract.address)) == 42
    print(f"ECOCLAIM_V2_EXPLORER=https://explorer-studio.genlayer.com/address/{contract.address}", flush=True)
    cases = [
        ("public-reduction-25", 25, "NOT_OVERSTATED_VS_INPUTS"),
        ("public-reduction-40", 40, "OVERSTATED_VS_INPUTS"),
    ]
    for key, advertised_percent, expected_outcome in cases:
        marketing = (
            f"This packaging line reduced CO2e emissions by {advertised_percent} "
            "percent from 2025 to 2026."
        )
        confirmed(contract.register(args=[
            key, "Recycled packaging line",
            "CO2E_KG", "2025", "2026", 1000, 750,
            marketing,
            "Caller-reported totals based on equal units of packaging output.",
        ]), f"ECOCLAIM_V2_REGISTER_{advertised_percent}")
        initial = report(contract, key)
        assert initial["observed_reduction_basis_points"] == 2500
        assert initial["outcome"] == "PENDING"
        confirmed(contract.audit_percentage(args=[key]),
                  f"ECOCLAIM_V2_AUDIT_{advertised_percent}", consensus=True)
        final = report(contract, key)
        assert final["extracted_claim_percent"] == advertised_percent
        assert final["observed_reduction_basis_points"] == 2500
        assert final["outcome"] == expected_outcome
        print(
            f"ECOCLAIM_V2_CASE_{advertised_percent}="
            f"CLAIMED_{advertised_percent}_ACTUAL_25_{expected_outcome}", flush=True,
        )
    print("ECOCLAIM_V2_TWO_CONTRASTING_LIVE_CASES=PASS", flush=True)
