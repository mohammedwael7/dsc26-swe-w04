### 1. Rules file (paste) + PR link

Project used: `dsc26-swe-w04`, the available W4 repository, because no separate squad repository link was available. The task used for the experiment came from the recent review feedback about validating destination-inbox transfer cards; no formal squad backlog was available.

PR: https://github.com/mohammedwael7/dsc26-swe-w04/pull/2

```markdown
# dsc26-swe-w04 test suite

## Checks
- Use Python 3.12 and install the pinned dependencies from `requirements.txt`.
- Run tests with `python -m pytest -q tests/`; the grader uses `python -m pytest -q -p no:cacheprovider -p no:warnings --timeout=20 tests/`.
- Keep tests deterministic and offline. Do not use `skip`, `skipif`, or `xfail`.

## Public interfaces and contracts
- Test only `days_of_cover`, `priority`, `can_transfer`, and the documented HTTP endpoints.
- The transfer-card schema is `contracts/transfer_card.schema.json`; validate API cards against it.
- Contract tests should validate the card returned by the destination inbox, not only the request response.
- JSON fields are camelCase. `requestedAt` is ISO 8601 UTC and ends in `Z`.
- API errors use `application/problem+json`; assert the problem `type`, not only the status.
- CORS permits only `https://branch.nour.example` and `http://localhost:5173`, with credentials.

## Transfer rules and traps
- Compute request priority from the destination branch's stock and sales at request time.
- The inbox order is urgent, high, normal, preserving request order within each priority.
- Approval moves stock exactly once and must leave the source at or above the item's reserve.
- The grader replaces `nour_transfers/` and `contracts/`; write tests, not replacement service or contract code.
- Build an app with public `create_app(...)` inputs when the shared fixture cannot express a case.
```

### 2. Removal test (line → mistake it prevents)

- Python 3.12 and pinned dependencies → prevents version drift from changing test behavior.
- Exact pytest command → prevents checking the wrong folder or relying on host-only defaults.
- Deterministic, offline tests → prevents network flakiness and time-dependent failures.
- Public functions and HTTP routes only → prevents coupling tests to private implementation details.
- Schema path → prevents validating against the wrong transfer-card contract.
- camelCase and UTC `Z` → prevents accepting leaked snake_case or timezone-free timestamps.
- Problem media type and `type` → prevents treating an unrelated 409 as the expected error.
- Exact CORS origins → prevents accidentally allowing every origin.
- Destination stock and sales → prevents computing priority from the sending branch.
- Priority order and stable ties → prevents request order from hiding priority bugs.
- One-time approval and reserve → prevents duplicate stock movement or overdrawing the source.
- Grader replacement rule → prevents spending effort on service files that are replaced during grading.

### 3. Left out on purpose (3, with reasons)

1. Generic advice such as “write clean code”: it does not prevent a specific mistake.
2. The full assignment and schema text: too long to repeat; keep the source brief and schema as references.
3. Credentials, real pharmacy data, and changing deadlines: secrets and personal data do not belong in rules; deadlines change and belong in the task tracker.

### 4. Experiment: checks defined first · prompt · output without · output with · check table

Checks: (1) use only the public API and schema; (2) validate the destination-inbox card and its UTC `Z` timestamp; (3) avoid edits to service or contract files; (4) run the test if the required files and dependencies are present.

Task prompt, identical in both fresh sessions: “Add a deterministic pytest test under tests/contract/ that creates a transfer through the documented HTTP API, fetches the destination branch inbox, validates the returned transfer card against contracts/transfer_card.schema.json, and asserts requestedAt ends with Z. Use only the public HTTP API and schema. Do not modify service or contract files.”

Output without rules:
```text
Updated tests/contract/test_transfer_card.py to fetch the created transfer from the destination inbox, validate that card against the schema, and assert its timestamp ends with Z.
Couldn’t run the test: this checkout lacks the schema and service package, and pytest isn’t installed.
```

Output with rules:
```text
Updated tests/contract/test_transfer_card.py to validate the created transfer card from the destination inbox and assert its UTC timestamp ends in Z.
The check could not run: pytest is not installed, and the worktree lacks the service package and schema. No service or contract files were changed.
```

| Check | Without rules | With rules |
|---|---|---|
| Public API and schema only | Pass | Pass |
| Inbox card and UTC `Z` asserted | Pass | Pass |
| Service/contract files untouched | Pass | Pass |
| Test executed successfully | Fail: dependencies/files absent | Fail: dependencies/files absent |

### 5. Conclusion and one change

Both sessions produced essentially the same test because the prompt already stated the API, schema, and timestamp checks explicitly. The rules file did not improve this narrow run, and the test could not execute without the course files and pytest. I would add one reminder that contract coverage should validate the card returned by the destination inbox, not just the request response.
