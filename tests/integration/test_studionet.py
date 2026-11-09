"""Public Studionet proof: deterministic no-evidence and AI comparison cases."""
import json
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


def confirmed(call, name):
    receipt = call.transact(consensus_max_rotations=4, wait_interval=10000, wait_retries=50)
    assert tx_execution_succeeded(receipt), f"{name} failed: {receipt.get('hash', '')}"
    print(f"{name}_TX={receipt.get('hash', '')}", flush=True)


def test_real_studionet(default_account):
    c = get_contract_factory("EcoClaim").deploy(
        account=default_account, consensus_max_rotations=4)
    address = str(c.address)
    assert address.startswith("0x") and len(address) == 42
    print(f"ECOCLAIM_EXPLORER=https://explorer-studio.genlayer.com/address/{address}", flush=True)

    confirmed(c.register(args=[
        "public-eco-empty-001", "Plastic container",
        "All of our packaging is made using recycled material.",
        "Current packaging for the product in 2026", ""
    ]), "ECOCLAIM_REGISTER_NO_EVIDENCE")
    confirmed(c.check(args=["public-eco-empty-001"]), "ECOCLAIM_CHECK_NO_EVIDENCE")
    assert json.loads(c.get_claim(args=["public-eco-empty-001"]).call())["finding"] == "NO_EVIDENCE"

    confirmed(c.register(args=[
        "public-eco-text-002", "Recycled notebook",
        "This notebook contains 50 percent recycled paper by weight.",
        "Paper composition of the notebook in its 2026 batch",
        "The submitted supplier summary reports 50 percent recycled paper by weight for the notebook in 2026."
    ]), "ECOCLAIM_REGISTER_TEXT")
    confirmed(c.check(args=["public-eco-text-002"]), "ECOCLAIM_CHECK_AI")
    result = json.loads(c.get_claim(args=["public-eco-text-002"]).call())
    assert result["finding"] in {"CONSISTENT", "CONFLICTING", "UNCLEAR"}
    print(f"ECOCLAIM_FINAL_FINDING={result['finding']}", flush=True)
