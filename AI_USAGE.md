## Tools

Codex was used to draft and revise the pytest layout, unit tests, API tests, and JSON Schema contract tests from the assignment brief. The tests call only the documented rules functions and HTTP API. The application and contract files are expected to come from the course-provided implementation or grader.

## What AI got wrong

The first inbox-ordering test created the urgent transfer before the normal transfer, so a mutant that sorted only by request order could still pass. The test was corrected to create the normal transfer first and assert that the urgent transfer appears first. The initial fixture also had to assume shapes for `stock`, `items`, and `sales` because the starter files were not available locally.

## In my own words

**Pick one mutant your first draft of tests did not kill. Why not, and what did you add?**

My first inbox-priority test would have missed M10. I created the urgent transfer first and the normal transfer second, so even a broken inbox that kept request order would put the urgent card first and pass. I changed the test to request the normal transfer first, then the urgent one, and assert that the urgent card still appears first. That makes request order disagree with priority, so the test can catch the mutant.

**Why is a test that only asserts `status_code == 409` weaker than one that asserts the problem `type`?**

A 409 only tells me that the server reported some conflict. Both `below-reserve` and `not-pending` are supposed to return 409, but they mean different things and require different client behavior. I also assert the problem `type` so the test fails if the API returns the right status for the wrong reason or maps the error to the wrong documented case.
