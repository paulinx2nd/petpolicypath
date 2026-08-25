"""Direct tests for clause selection and split-role task completion."""

import json


DOCUMENT = {
    "clauses": [
        {"id": "VACCINE", "condition": "The application concerns a dog that will use shared indoor areas.", "task": "Provide the current vaccination record reference.", "responsible": "APPLICANT"},
        {"id": "MEET", "condition": "A dog is proposed for regular residence at the property.", "task": "Record the manager's introductory meeting outcome.", "responsible": "MANAGER"},
    ]
}
PROFILE = "The application is for one adult dog that will live at the property and pass through shared indoor corridors each day. Vaccination documents and a manager meeting can be supplied."


def _policy(contract, direct_vm, publisher):
    direct_vm.sender = publisher
    return contract.publish_policy("BUILDING-A", "Shared-property pet policy", DOCUMENT)


def _application(contract, direct_vm, applicant, manager, policy_id):
    direct_vm.sender = applicant
    return contract.open_application(policy_id, "PET-1", manager, PROFILE)


def _compile(contract, direct_vm, applicant, application_id, clauses):
    direct_vm.sender = applicant
    direct_vm.mock_llm(
        r".*Select which frozen pet-policy clauses apply.*",
        json.dumps({"applicable_clause_ids": clauses}),
    )
    contract.compile_tasks(application_id)


def test_policy_is_stored_in_independent_ledger(contract, direct_vm, direct_alice):
    policy_id = _policy(contract, direct_vm, direct_alice)
    policy = contract.get_policy(policy_id)
    assert policy["active"] is True
    assert policy["document_sha256"].startswith("sha256:")
    assert contract.get_policy_count() == 1


def test_manager_must_be_distinct(contract, direct_vm, direct_bob):
    policy_id = _policy(contract, direct_vm, direct_bob)
    with direct_vm.expect_revert("manager_must_be_distinct"):
        contract.open_application(policy_id, "BAD", direct_bob, PROFILE)


def test_consensus_compiles_role_bound_tasks(contract, direct_vm, direct_alice, direct_bob):
    policy_id = _policy(contract, direct_vm, direct_alice)
    application_id = _application(contract, direct_vm, direct_alice, direct_bob, policy_id)
    _compile(contract, direct_vm, direct_alice, application_id, ["VACCINE", "MEET"])
    application = contract.get_application(application_id)
    assert application["status"] == "TASKS_READY"
    assert application["applicable_mask"] == 3


def test_each_task_enforces_assigned_actor(contract, direct_vm, direct_alice, direct_bob):
    policy_id = _policy(contract, direct_vm, direct_alice)
    application_id = _application(contract, direct_vm, direct_alice, direct_bob, policy_id)
    _compile(contract, direct_vm, direct_alice, application_id, ["VACCINE", "MEET"])
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("wrong_task_actor"):
        contract.complete_task(application_id, "VACCINE", "Manager cannot submit the applicant's vaccination reference.")


def test_completed_tasks_enable_manager_decision(contract, direct_vm, direct_alice, direct_bob):
    policy_id = _policy(contract, direct_vm, direct_alice)
    application_id = _application(contract, direct_vm, direct_alice, direct_bob, policy_id)
    _compile(contract, direct_vm, direct_alice, application_id, ["VACCINE", "MEET"])
    contract.complete_task(application_id, "VACCINE", "Vaccination record reference VR-2026-104 is attached to the public application.")
    direct_vm.sender = direct_bob
    contract.complete_task(application_id, "MEET", "Manager meeting completed with the handling expectations reviewed and acknowledged.")
    contract.decide_application(application_id, True, "All applicable clause tasks are complete and the application is approved.")
    application = contract.get_application(application_id)
    assert application["status"] == "APPROVED"
    assert application["completed_mask"] == 3
    assert len(application["task_evidence"]) == 2


def test_unknown_model_clause_fails_closed(contract, direct_vm, direct_alice, direct_bob):
    policy_id = _policy(contract, direct_vm, direct_alice)
    application_id = _application(contract, direct_vm, direct_alice, direct_bob, policy_id)
    direct_vm.mock_llm(
        r".*Select which frozen pet-policy clauses apply.*",
        json.dumps({"applicable_clause_ids": ["INVENTED"]}),
    )
    with direct_vm.expect_revert("unknown_clause_id"):
        contract.compile_tasks(application_id)
    assert contract.get_application(application_id)["status"] == "OPEN"


def test_only_publisher_can_deactivate_policy(contract, direct_vm, direct_alice, direct_bob):
    policy_id = _policy(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_policy_publisher"):
        contract.deactivate_policy(policy_id)
