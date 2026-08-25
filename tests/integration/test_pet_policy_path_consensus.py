"""Five-validator GLSim flow for policy-clause task compilation."""

import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


DOCUMENT = {"clauses": [{"id": "VACCINE", "condition": "The application concerns a dog that will use shared indoor areas.", "task": "Provide the current vaccination record reference.", "responsible": "APPLICANT"}, {"id": "MEET", "condition": "A dog is proposed for regular residence at the property.", "task": "Record the manager's introductory meeting outcome.", "responsible": "MANAGER"}]}


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _context():
    validators = get_validator_factory().batch_create_mock_validators(
        5,
        mock_llm_response={"nondet_exec_prompt": {"Select which frozen pet-policy clauses apply": json.dumps({"applicable_clause_ids": ["VACCINE", "MEET"]})}},
    )
    return {"validators": [validator.to_dict() for validator in validators]}


def test_five_validator_clause_tasks_and_manager_decision():
    publisher_account, applicant_account, manager_account = create_accounts(3)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "pet_policy_path.py")
    deployed = factory.deploy_contract_tx(args=[], account=publisher_account, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(deployed)
    address = extract_contract_address(deployed)
    publisher = factory.build_contract(address, account=publisher_account)
    applicant = factory.build_contract(address, account=applicant_account)
    manager = factory.build_contract(address, account=manager_account)
    policy_id = f"{str(publisher_account.address).lower()}:BUILDING-A"
    application_id = f"{str(applicant_account.address).lower()}:PET-1"
    _ok(publisher.publish_policy(args=["BUILDING-A", "Shared-property pet policy", DOCUMENT]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(applicant.open_application(args=[policy_id, "PET-1", manager_account.address, "The application is for one adult dog that will live at the property and pass through shared indoor corridors each day. Vaccination documents and a manager meeting can be supplied."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(applicant.compile_tasks(args=[application_id]).transact(transaction_context=_context(), wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(applicant.complete_task(args=[application_id, "VACCINE", "Vaccination record reference VR-2026-104 is attached to the public application."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(manager.complete_task(args=[application_id, "MEET", "Manager meeting completed with handling expectations reviewed and acknowledged."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(manager.decide_application(args=[application_id, True, "All applicable clause tasks are complete and the application is approved."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert applicant.get_application(args=[application_id]).call()["status"] == "APPROVED"
