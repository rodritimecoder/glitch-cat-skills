# Measure, Then Claim

**Rule:** No benchmark without a method, a baseline, a metric set, and the cost. "It's faster" is not a number.

**Why:** He calls the cost out as the elephant in the room and shows no numbers. The saving is not the point — the evaluations and the training set are the asset, and you keep measuring them.

**In practice:**
- Report baseline, method, metrics, winner, and why the winner wins.
- Every step saves its own artifact, so the evidence survives teardown and a reviewer can re-run it.
- Latency and cost are first-class axes, not an afterthought: tokens, wall clock, dollars.
- The more you measure, the better it gets. That is how a personal build becomes how enterprise systems are built.

**Kem:** *"The bigger lesson is not the saving, which is great, thirty to forty percent, but it's that when you design systems like this, the work is in the evaluations and the training set. You put the work in upfront so you don't need to do it later and you keep measuring."* — Self-Calibrating Eval Router [01:40]
