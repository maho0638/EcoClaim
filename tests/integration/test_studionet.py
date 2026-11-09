"""Manual public Studionet proof for EcoClaim v2 (new implementation)."""
import json
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


def confirmed(call, tag):
    receipt = call.transact(consensus_max_rotations=4, wait_interval=10000, wait_retries=50)
    assert tx_execution_succeeded(receipt), f"{tag}: {receipt.get('hash', '')}"
    print(f"{tag}_TX={receipt.get('hash', '')}", flush=True)


def test_live_quantitative_claim(default_account):
    c = get_contract_factory("EcoClaim").deploy(
        account=default_account, consensus_max_rotations=4,
    )
    address = str(c.address)
    assert address.startswith("0x") and len(address) == 42
    print(f"ECOCLAIM_V2_EXPLORER=https://explorer-studio.genlayer.com/address/{address}", flush=True)
    confirmed(c.register(args=[
        "public-reduction-001", "Recycled packaging line",
        "CO2E_KG", "2025", "2026", 1000, 750,
        "This packaging line reduced CO2e emissions by 25 percent from 2025 to 2026.",
        "Caller-reported totals based on equal units of packaging output.",
    ]), "ECOCLAIM_V2_REGISTER")
    initial = json.loads(c.get_report(args=["public-reduction-001"]).call())
    assert initial["observed_reduction_basis_points"] == 2500
    assert initial["outcome"] == "PENDING"
    confirmed(c.audit_percentage(args=["public-reduction-001"]), "ECOCLAIM_V2_AUDIT")
    final = json.loads(c.get_report(args=["public-reduction-001"]).call())
    p = final["extracted_claim_percent"]
    expected = ("UNQUANTIFIED" if p == -1 else
                "OVERSTATED_VS_INPUTS" if p * 100 > 2500 else
                "NOT_OVERSTATED_VS_INPUTS")
    assert final["outcome"] == expected
    print(f"ECOCLAIM_V2_FINAL_PERCENT={p}", flush=True)
    print(f"ECOCLAIM_V2_OUTCOME={expected}", flush=True)
