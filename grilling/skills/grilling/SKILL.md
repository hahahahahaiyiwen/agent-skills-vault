---
name: grilling
description: Conduct a probing interview about the user's plan, decision, idea, or understanding. Use when the user wants to answer challenging questions and refine their thinking through an ongoing conversation. Questions are directed to the user, not to the agent for self-review.
---

# Grilling

## Scope

Interview the user about the requested subject; clarify the scope if needed.
Probe assumptions, rationale, evidence, tradeoffs, and failure cases that could
materially change the shared understanding. Challenge ideas, not the person,
and do not invent questions merely to prolong the conversation.

## Rounds

- Track material open questions, their dependencies, settled decisions, and
  explicit unknowns. An exhaustive design tree is not required.
- Default to one high-value question. Group a few related questions only when
  their answers do not depend on one another. Defer downstream questions until
  their prerequisites are known.
- Use the host's user-question tool when available; otherwise ask concise,
  numbered questions. Wait for the user's actual answers. Never supply answers
  on their behalf or continue through unanswered dependent questions.
- Integrate each answer and ask the next useful question without repeatedly
  asking permission to continue. Follow up on contradictions or ambiguity.
  "I don't know," a skipped question, or a deferred choice remains unresolved,
  not an established fact. Reopen settled issues only when new information
  materially changes them.
- Offer a recommendation or alternatives when helpful and supported, labeling
  assumptions and tradeoffs. Do not attach a recommended answer automatically
  to every question.

## Evidence and waiting

Inspect relevant, accessible evidence with the smallest useful direct lookup.
Ask the user for facts only they know or information that cannot be retrieved.
Keep genuinely unknown facts explicit rather than inventing them. Delegate
only when that capability is available and the work meaningfully benefits.

A necessary investigation still running or blocked leaves its question open.
Ask independent ready questions, wait for a pending result, or explain a blocker
and ask whether to defer it. An empty set of ready questions is not completion.

## Completion

If the user asks to pause, stop, or wrap up, stop questioning and summarize the
current understanding and unresolved items.

Otherwise, when the scoped issues are resolved or explicitly deferred, present
a concise summary of decisions, assumptions, and remaining uncertainties before
asking whether it accurately reflects the shared understanding. Address
corrections, then end the interview on confirmation.

Confirmation of understanding is not permission to implement. Return the
summary and stop; implementation requires separate authorization.
