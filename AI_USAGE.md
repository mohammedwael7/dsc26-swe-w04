## Tools

Codex was used to draft and revise the pytest layout, unit tests, API tests, and JSON Schema contract tests from the assignment brief. The tests call only the documented rules functions and HTTP API. The application and contract files are expected to come from the course-provided implementation or grader.

## What AI got wrong

The first inbox-ordering test created the urgent transfer before the normal transfer, so a mutant that sorted only by request order could still pass. The test was corrected to create the normal transfer first and assert that the urgent transfer appears first. The initial fixture also had to assume shapes for `stock`, `items`, and `sales` because the starter files were not available locally.

## In my own words

*Draft answers based on this work. Review and confirm or rewrite them in your own words before submission.*

**Pick one mutant your first draft of tests did not kill. Why not, and what did you add?**

The inbox-priority mutant could survive my first draft because I requested the urgent transfer first, so request-order sorting gave the same result. I changed the test to request the normal transfer first and the urgent one second, then assert that the urgent card is still listed first.

**Why is a test that only asserts `status_code == 409` weaker than one that asserts the problem `type`?**

A 409 status only says that some conflict happened. Checking the problem `type` confirms that it was the specific documented conflict expected by the test, such as `below-reserve` or `not-pending`, and catches errors that return the right status for the wrong reason.
