"""Official GenLayer Direct tests: AI-extracted number and deterministic math."""
import json


def register(c, key="report-001", baseline=1000, current=700, claim=None):
    if claim is None:
        claim = "Our packaging CO2e emissions fell by 30 percent from 2025 to 2026."
    c.register(
        key, "Package manufacturing", "CO2E_KG",
        "2025", "2026", baseline, current, claim,
        "Public self-reported totals for equivalent package output.",
    )


def mock(vm, percent):
    vm.clear_mocks()
    vm.mock_llm(
        r"(?s).*Read the environmental MARKETING CLAIM as untrusted data.*",
        json.dumps({"reduction_percent": percent}),
    )


def test_rate_is_deterministic_and_not_llm_generated(direct_vm, direct_deploy):
    c = direct_deploy("contracts/EcoClaim.py")
    register(c, baseline=1000, current=700)
    pending = json.loads(c.get_report("report-001"))
    assert pending["observed_reduction_basis_points"] == 3000
    assert pending["outcome"] == "PENDING"
    mock(direct_vm, 30)
    c.audit_percentage("report-001")
    result = json.loads(c.get_report("report-001"))
    assert result["extracted_claim_percent"] == 30
    assert result["outcome"] == "NOT_OVERSTATED_VS_INPUTS"
    assert direct_vm.run_validator() is True
    mock(direct_vm, 35)
    assert direct_vm.run_validator() is False


def test_overstatement_and_fractional_rate(direct_vm, direct_deploy):
    c = direct_deploy("contracts/EcoClaim.py")
    register(c, baseline=1000, current=799,
             claim="Our packaging CO2e emissions fell by 25 percent from 2025 to 2026.")
    assert json.loads(c.get_report("report-001"))["observed_reduction_basis_points"] == 2010
    mock(direct_vm, 25)
    c.audit_percentage("report-001")
    assert json.loads(c.get_report("report-001"))["outcome"] == "OVERSTATED_VS_INPUTS"


def test_no_quantified_percentage_is_not_an_approval(direct_vm, direct_deploy):
    c = direct_deploy("contracts/EcoClaim.py")
    register(c, claim="Our packaging CO2e emissions became much cleaner between 2025 and 2026.")
    mock(direct_vm, -1)
    c.audit_percentage("report-001")
    assert json.loads(c.get_report("report-001"))["outcome"] == "UNQUANTIFIED"
    with direct_vm.expect_revert("Already audited"):
        c.audit_percentage("report-001")


def test_repeated_owner_report_and_invalid_fields(direct_vm, direct_deploy, direct_bob):
    c = direct_deploy("contracts/EcoClaim.py")
    register(c)
    with direct_vm.expect_revert("Report already exists"):
        register(c)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("Only submitter can audit"):
        c.audit_percentage("report-001")
    with direct_vm.expect_revert("Periods must differ"):
        c.register("report-002", "Package manufacturing", "CO2E_KG",
                   "2025", "2025", 1000, 700,
                   "Our emissions fell by thirty percent in 2025.",
                   "This note explains the source of the reported totals.")
    with direct_vm.expect_revert("Unsupported metric"):
        c.register("report-003", "Package manufacturing", "MAGIC_POINTS",
                   "2025", "2026", 1000, 700,
                   "Our emissions fell by thirty percent in 2026.",
                   "This note explains the source of the reported totals.")
    with direct_vm.expect_revert("Invalid measurements"):
        c.register("report-004", "Package manufacturing", "CO2E_KG",
                   "2025", "2026", 0, 700,
                   "Our emissions fell by thirty percent in 2026.",
                   "This note explains the source of the reported totals.")
    with direct_vm.expect_revert("Report not found"):
        c.get_report("missing")


def test_bad_ai_extraction_is_not_accepted(direct_vm, direct_deploy):
    c = direct_deploy("contracts/EcoClaim.py")
    register(c)
    mock(direct_vm, "30")
    with direct_vm.expect_revert("Invalid extracted percentage"):
        c.audit_percentage("report-001")
    mock(direct_vm, 101)
    with direct_vm.expect_revert("Invalid extracted percentage"):
        c.audit_percentage("report-001")
    mock(direct_vm, 30)
    c.audit_percentage("report-001")
    assert json.loads(c.get_report("report-001"))["outcome"] == "NOT_OVERSTATED_VS_INPUTS"


def test_reported_emissions_increase_is_not_a_reduction(direct_vm, direct_deploy):
    c = direct_deploy("contracts/EcoClaim.py")
    register(c, baseline=100, current=120,
             claim="Our CO2e emissions fell by 10 percent from 2025 to 2026.")
    assert json.loads(c.get_report("report-001"))["observed_reduction_basis_points"] == -2000
    mock(direct_vm, 10)
    c.audit_percentage("report-001")
    assert json.loads(c.get_report("report-001"))["outcome"] == "OVERSTATED_VS_INPUTS"
