## Tools

Codex was used to draft the test layout and test cases from the assignment brief. The tests target only the documented public rules and HTTP API; the implementation and contract files are expected to come from the course grader or starter package.

## What AI got wrong

The brief preview does not include the concrete shapes of the `stock`, `items`, and `sales` inputs or the exact response envelope. The initial fixture uses a straightforward mapping shape and may need adjustment to match the course reference implementation.

## In my own words

**Pick one mutant your first draft of tests did not kill. Why not, and what did you add?**

> [Your answer: review the first run and explain one surviving mutant and the test you added.]

**Why is a test that only asserts `status_code == 409` weaker than one that asserts the problem `type`?**

> [Your answer: explain how checking the problem type verifies which documented conflict occurred, rather than accepting any unrelated conflict.]
