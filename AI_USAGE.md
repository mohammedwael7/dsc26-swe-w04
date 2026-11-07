## Tools

Codex was used to draft and revise the pytest layout, unit tests, API tests, and JSON Schema contract tests from the assignment brief. The tests call only the documented rules functions and HTTP API. The application and contract files are expected to come from the course-provided implementation or grader.

## What AI got wrong

The first inbox-ordering test created the urgent transfer before the normal transfer, so a mutant that sorted only by request order could still pass. The test was corrected to create the normal transfer first and assert that the urgent transfer appears first. The initial fixture also had to assume shapes for `stock`, `items`, and `sales` because the starter files were not available locally.

## In my own words

**Pick one mutant your first draft of tests did not kill. Why not, and what did you add?**

My first inbox test could miss M10 because I requested the urgent transfer first. A FIFO inbox would still show it first and pass. I reversed the request order and checked that the urgent transfer still appears first.

**Why is a test that only asserts `status_code == 409` weaker than one that asserts the problem `type`?**

A 409 only says that some conflict happened. Checking `type` tells me whether it was `below-reserve` or `not-pending`, so the test catches the wrong error even when the status code is right.
