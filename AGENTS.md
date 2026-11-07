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
