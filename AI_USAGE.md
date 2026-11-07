## Tools

Codex was used to draft and revise the pytest layout, unit tests, API tests, and JSON Schema contract tests from the assignment brief. The tests call only the documented rules functions and HTTP API. The application and contract files are expected to come from the course-provided implementation or grader.

## What AI got wrong

The first inbox-ordering test created the urgent transfer before the normal transfer, so a mutant that sorted only by request order could still pass. The test was corrected to create the normal transfer first and assert that the urgent transfer appears first. The initial fixture also had to assume shapes for `stock`, `items`, and `sales` because the starter files were not available locally.

## In my own words

*Draft answers based on this work. Review and confirm or rewrite them in your own words before submission.*

**Pick one mutant your first draft of tests did not kill. Why not, and what did you add?**

In my view, the inbox-priority mutant could survive my first draft because I requested the urgent transfer first, so sorting by request order gave the same result. I changed the test to request the normal transfer first and the urgent one second, then check that the urgent card is still listed first. That makes the test show the priority rule more clearly.

**Why is a test that only asserts `status_code == 409` weaker than one that asserts the problem `type`?**

I think checking only for 409 is too general: several different problems can produce that status. Checking the problem `type` tells me the API returned the particular conflict I expected, such as `below-reserve` or `not-pending`, instead of an unrelated conflict with the same status.
