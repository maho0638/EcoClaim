"""GenLayer SDK Direct checks for EcoClaim's public receipts and consensus."""
import json


def create(c, key="environment-001", evidence=None):
    if evidence is None:
        evidence = "The provided report describes recycled content as 40% by mass in the 2025 product batch."
    c.register(
        key, "Reusable packaging",
        "Our packaging contains 40 percent recycled material by mass.",
        "Packaging material in the 2025 production batch", evidence
    )


def mock(vm, finding):
    vm.clear_mocks()
    vm.mock_llm(r"(?s).*Compare an environmental marketing statement ONLY.*",
                json.dumps({"finding": finding}))


def test_register_and_read_immutable_claim_text(direct_deploy):
    c = direct_deploy("contracts/EcoClaim.py")
    create(c)
    entry = json.loads(c.get_claim("environment-001"))
    assert entry["finding"] == "PENDING"
    assert entry["product"] == "Reusable packaging"


def test_missing_evidence_is_deterministically_not_certified(direct_vm, direct_deploy):
    c = direct_deploy("contracts/EcoClaim.py")
    create(c, evidence="")
    c.check("environment-001")
    assert json.loads(c.get_claim("environment-001"))["finding"] == "NO_EVIDENCE"
    with direct_vm.expect_revert("Already checked"):
        c.check("environment-001")


def test_nondeterministic_verdict_checks_validator_agreement(direct_vm, direct_deploy):
    c = direct_deploy("contracts/EcoClaim.py")
    create(c)
    mock(direct_vm, "CONSISTENT")
    c.check("environment-001")
    assert json.loads(c.get_claim("environment-001"))["finding"] == "CONSISTENT"
    assert direct_vm.run_validator() is True
    mock(direct_vm, "CONFLICTING")
    assert direct_vm.run_validator() is False


def test_authorization_replay_and_input_validation(direct_vm, direct_deploy, direct_bob):
    c = direct_deploy("contracts/EcoClaim.py")
    create(c)
    owner = direct_vm.sender
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("Only submitter can check"):
        c.check("environment-001")
    direct_vm.sender = owner
    with direct_vm.expect_revert("Claim already exists"):
        create(c)
    with direct_vm.expect_revert("Invalid text length"):
        c.register("environment-002", "Box", "A claim too short", "year", "some evidence")
    with direct_vm.expect_revert("Disallowed control characters"):
        c.register("environment-003", "Packaging", "Packaging is recycled material.", "2026 packaging batch", "Invisible control.\u202e")
    with direct_vm.expect_revert("Claim not found"):
        c.get_claim("missing")
