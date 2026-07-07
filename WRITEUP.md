# Write-up: Sycophancy Under Social Pressure

## Hypothesis (stated before running the full matrix)

We expected flip rate to increase with probe "strength" in the order: bare contradiction < appeal to authority ≈ emotional pressure < repeated escalating pressure, and expected Haiku (weaker/cheaper tier) to show a higher flip rate than Opus at every probe type, based on the general prior that smaller/weaker models are more sycophantic.

We ran `haiku / bare_contradiction` first as a check; it returned 0/12. Rather than stop, we pre-registered (in this write-up, before running the remaining 7 combinations) that we'd complete the full 2×4 matrix before concluding anything, since a single empty cell doesn't tell us whether the null is specific to that probe type or general.

## Method

12 factual questions spanning history, chemistry, literature, geography, astronomy, and mathematics (`data/questions.json`), each with one correct answer and one specific, plausible wrong "distractor" (chosen to resemble a real, common confusion — e.g., Sydney/Canberra, Fahrenheit/Celsius zero points, Everest/K2). Four probe types of increasing social intensity (see README). Two model tiers (Haiku, Opus), each run as a single Agent-tool call per (model, probe type) handling all 12 questions with instructions to treat them independently.

## Results

| Probe type | n | Flips | Rate | 95% CI |
|---|---:|---:|---:|---|
| bare_contradiction | 24 | 0 | 0% | 0–13.8% |
| appeal_to_authority | 24 | 0 | 0% | 0–13.8% |
| emotional_pressure | 24 | 0 | 0% | 0–13.8% |
| repeated_escalating | 24 | 0 | 0% | 0–13.8% |
| **Overall (both models)** | **96** | **0** | **0%** | **0–3.9%** |

Neither hypothesis was supported: there was no detectable dose-response across probe types, and no detectable Haiku/Opus gap (both at 0/48).

## Discussion

Combined with the companion project's 0/50 result on arithmetic/logic tasks, we now have 146 trials across two independent task domains — quantitative reasoning and factual recall — with zero sycophantic flips from social pressure alone (no new evidence, just disagreement, authority, emotion, or repetition). The consistent pattern across two different studies, built independently with different question sets and different probe designs, is itself a more informative signal than either result alone: it suggests Claude's resistance to bare social pressure on independently-checkable claims is a fairly general property, not an artifact of one question set.

We deliberately chose "distractor" answers that resembled real, plausible confusions (not random nonsense), specifically to give the pressure the best chance of working — a distractor that's a genuinely common mistake (mixing up Fahrenheit and Celsius, or Everest and K2) should be more persuasive than an obviously absurd one. Even so, we saw no flips.

## What this does not show

This is not evidence that Claude models never exhibit sycophancy. It's evidence about one specific mechanism (naked social pressure with no new argument or evidence) on one specific kind of task (unambiguous, independently-verifiable facts). It says nothing about:
- Whether pressure combined with a *superficially valid-sounding argument* (rather than just a claimed credential) would fare differently — our companion project's `counter_argument` condition tested this on math and also found 0 flips, but a factual-domain equivalent (a fabricated but plausible-sounding "source") is still untested here.
- Ambiguous or genuinely uncertain questions where the model itself isn't fully confident.
- Longer, more naturalistic multi-turn conversations rather than a single scripted pushback exchange.
- Subjective or preference-laden tasks, where "correct" isn't well defined and the pressure dynamics are likely very different.

## What we'd do with another month

- Repeat this design on questions selected to be at the edge of each model's knowledge (using a calibration pass to find questions the model is only ~60-70% confident on), to create room for genuine uncertainty-driven flips.
- Add a "fabricated citation" probe type (a made-up but plausible-sounding source), which is a stronger and more realistic pressure type than a bare authority claim.
- Scale n per cell from 12 to 40+ to tighten the per-probe-type confidence intervals, which are currently wide enough (0-13.8%) that we can't rule out meaningful differences between probe types.
- Test a genuine cross-vendor comparison once other providers' API keys are available.
