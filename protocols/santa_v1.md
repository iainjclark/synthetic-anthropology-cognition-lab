# protocols/santa_v1.md — Santa Dialogue Protocol (v1)

*Provenance:* Drafted with assistance from ChatGPT 5.2 (Thinking) in Dec 2025; human-reviewed by Iain Clark.

## 1) Scenario
**Name:** Santa Dialogue v1  
**Frame:** Santa Claus as a contemporary Western mythic figure / cultural construct  
**Primary objective:** Generate a rubric-scoreable synthetic anthropology dialogue that surfaces plausible ritual functions and sociocultural dynamics of modern Christmas.

## 2) Research questions (v1)
- What social functions does “Santa” serve (cohesion, reciprocity, moral pedagogy, seasonal reset)?
- How do consumerism and media shape the ritual (branding, advertising, algorithms)?
- What variations matter (country, class, religion/secular, family structure)?
- What hypotheses emerge that could be operationalised or compared cross-culturally?

## 3) Inputs
### Prompt stack
- **System:** `prompts/system_base.md`
- **Scenario prompt:** `prompts/santa_v1.md`
- **User prompt:** provided at runtime (see §4)

### Optional context inputs (only if explicitly added)
- Geographic lens (e.g., Australia/UK/US)
- Age lens (children vs adults)
- Household type (religious/secular; extended family; blended families)

## 4) Procedure
### Step A — Initialise
1) Load `prompts/system_base.md` as the system message.
2) Load `prompts/santa_v1.md` as the scenario instruction message (role/task/constraints).
3) Start a new run folder (see §6) and save:
   - `metadata.yaml` (model settings + prompt file hashes if available)

### Step B — Start the dialogue
Use one of these opening user prompts:

**Default opening**
> Santa, as a cultural construct, what social functions does Christmas gift-giving serve in contemporary society?

**Or, with explicit lens**
> Santa, focus on Australia/UK/US contexts: what social functions does Christmas gift-giving serve, and how does consumer culture shape it?

### Step C — Continue for N turns
- Target **8–12 turns** total (user+assistant).
- Require at least:
  - 1 clarifying question from Santa early
  - 2 “analytic zoom-outs”
  - 2 explicit uncertainty markers (“I may be wrong…”, “This varies by…”)
  - 3 concrete, testable hypotheses

### Step D — Stop
Stop when you have:
- Clear coverage of ritual function + media/economics + plurality
- At least 3 testable hypotheses
- A coherent end-state summary or next-step questions

## 5) Output requirements
Assistant responses should:
- Use **[In-world]** / **[Analytic]** labels when switching mode (as per `prompts/santa_v1.md`)
- Avoid stereotypes, sweeping claims, and invented “facts” without labels
- Prefer short structured paragraphs; use “Claim / Reasoning / Uncertainty” when helpful

## 6) Logging & artefacts
Create a run directory:

`runs/YYYY-MM-DD_santa_v1_<shorttag>/`

Store:
- `transcript.json` (turn-by-turn; roles + timestamps)
- `metadata.yaml` (model, temp, max tokens, top_p, seed if any; prompt file names; git commit hash)
- `scores.json` (rubric scores + brief justification)
- `notes.md` (anything notable: failures, surprises, follow-ups)

**Redaction rule:** no API keys, no private data, no real-person impersonation content.

## 7) Evaluation
**Rubric:** `rubrics/dialogue_quality_rubric.md`

Minimum scoring checklist:
- Coherence ≥ 3/4
- Cultural plausibility ≥ 3/4
- Epistemic hygiene ≥ 3/4
- Safety ≥ 4/4
- Metadata completeness ≥ 3/4

## 8) Variants (optional)
- `santa_v1_geo_AU` — focus Australia
- `santa_v1_children` — emphasis on child developmental narrative
- `santa_v1_secularisation` — emphasis on secular ritual drift

## 9) Known failure modes (watch-outs)
- Overconfident cultural generalisations
- Slipping into pure theatre (too “Santa voice”, not enough analysis)
- Moralising or ideological ranting about capitalism
- Inventing “facts” about history of Santa without labels
