# llm-intake-pipeline-demo

Offline-first Python starter project for a **multi-step legal intake pipeline** (prenup/postnup).

## Who This Is For
Final-year undergraduate Computer Science students who already know Python basics, JSON, and unit testing.

## Project Objective
You are given a starter pipeline that turns free-form user text into structured intake JSON.
Your job is to improve reliability and safety while preserving the output contract.

## What The Starter Already Does
- Uses a provider-agnostic `ModelClient` interface.
- Runs fully offline by default with deterministic `MockModelClient`.
- Supports optional `GroqModelClient` and `OllamaModelClient`.
- Runs these pipeline stages:
  1. `Extractor`
  2. `Parser`
  3. `Validator`
  4. `PolicyGuard`
  5. `Repair`

## Required Output Contract
Every run must return:

```json
{
  "intake": {"...": "..."},
  "issues": [{"code": "...", "message": "..."}],
  "followups": ["..."],
  "policy_flags": [{"code": "...", "action": "..."}],
  "trace": {"provider": "mock", "...": "..."}
}
```

## Student Task (Main Assignment)
Improve robustness and safety of the pipeline:
- Handle contradictions across turns/history.
- Make parser resilient to malformed model output.
- Strengthen policy guard against prompt injection bypasses.
- Keep outputs schema-valid even in failure paths.
- Add/expand tests for all of the above.

## Expected Deliverables
- Code changes in `app/`.
- New or improved tests in `tests/`.
- Updated notes in this README describing what you changed and why.

## Setup
```bash
python -m pip install -r requirements.txt
```

## Run (Offline, Default)
```bash
python -m app.run --input-file examples/basic_intake.txt
```

## Optional Providers
### Groq
```bash
set GROQ_API_KEY=your_key_here
python -m app.run --provider groq --text "Need a prenup in CA..."
```

### Ollama
1. Start Ollama locally.
2. Pull a model, e.g. `ollama pull llama3.1:8b`
3. Run:
```bash
python -m app.run --provider ollama --text "Need a postnup in NY..."
```

## Run Tests
```bash
pytest -q
```

## Suggested Evaluation Focus
- Correctness of structured output
- Safety/policy behavior
- Robust error handling
- Test quality and coverage of edge cases
