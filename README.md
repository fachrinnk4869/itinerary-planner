# Project README — PoC Autonomous Vacation Planner

## Requirements
- python 3.11
- uv [download link](https://docs.astral.sh/uv/getting-started/installation/)

# 1. Quick start — Run app (step-by-step)

1. Clone repo

   ```bash
   git clone <your-repo-url>
   cd <repo>
   ```

2. Install all library/dependencies
```python
uv sync
```

3. Fill environment variables in .env (see below)
```bash
cp .env.example .env
```

4. Run application

```python
uv run uvicorn app:app --reload
```

5. Access:

   * API root: `http://127.0.0.1:8000/`
   * Swagger UI: `http://127.0.0.1:8000/docs`
   * Itinerary endpoint: `GET /itinerary`

---

# 2. Folder structure (recommended PoC layout)

```
/.
├─ utils/
│  └─ helpers.py              
├─ schemas/
│  └─ booking.py              
│  └─ common.py              
│  └─ finaltripplan.py              
│  └─ intent.py              
│  └─ plan.py              
│─ settings.py
│─ .env.example
│─ state.py
│─ graph.py
│─ nodes.py
│─ edges.py
│─ prompt.py
├─ README.md
│─ app.py # <-- Fast API 
```

---

# 3. How the app is used (minimal)

* `GET /itinerary` user message → LangGraph workflow runs nodes: `intent_extraction` → `planning` → `booking` → `payment` if `auto_booking` true → `final_response`. returns last generated `FinalTripPlan`.
* Payment: if `auto_booking` true

---

# 4. Problems found during PoC (short)

* **State type mismatch** — `MessagesPlaceholder` expected `List[BaseMessage]`, but calendar provided as `dict` → ValueError.
* **Putting structured objects into `messages`** — appended Pydantic result directly into `messages` (must wrap into `AIMessage` or keep structured state separate).
* **LLM hallucination / malformed structured output** — LLM sometimes returns invalid JSON or wrong fields; need strict Pydantic validation + regenerate on failure.
* **Payment: don't store raw card data** — must use provider tokenization; PoC uses provider wrapper only.

---

# 5. Architecture (ASCII)
[architecture]()
---

# 6. Tech stack

* uv
* Python 3.11+
* FastAPI (HTTP server)
* Uvicorn (ASGI)
* LangGraph / LangChain (workflow / agents) — or minimal orchestrator if not available
* Pydantic (schema validation)
* Git

---

# 7. Demo video (how to produce)

[Demo Video]()

---

# 8. Risks & Vulnerabilities (detailed)

> For each risk: (1) attack scenario, (2) likelihood & impact, (3) mitigations (budget-conscious), (4) monitoring

### 1) LLM hallucination → incorrect bookings / charges

1. **Scenario:** LLM outputs wrong dates/amounts; booking/payment executed.
2. **Likelihood/Impact:** Medium-high / High (financial + reputational).
3. **Mitigation:** restrict LLM → produce structured output only; enforce Pydantic validation; require explicit user confirmation before charge; cap per-transaction amounts.
4. **Monitoring:** Log all charge proposals; alert if amount > threshold or if LLM output fails validation.

### 2) Prompt injection

1. **Scenario:** Malicious input tries to override system instructions to trigger charges.
2. **Likelihood/Impact:** High / High.
3. **Mitigation:** keep system prompts immutable; separate LLM (NLP) from action-executor (business logic); sanitize inputs; never include untrusted content in system prompt.
4. **Monitoring:** watch for injection patterns and spikes in validation rejections.

### 3) Unauthorized payment use (session theft)

1. **Scenario:** Stolen session or compromised token used to trigger bookings.
2. **Likelihood/Impact:** Medium / High.
3. **Mitigation:** require 2FA or re-confirmation for payments; store only tokenized payment_method_id from provider; short-lived session tokens.
4. **Monitoring:** detect unusual IP/device changes; alert on payment without recent user interaction.

### 4) Personal data leak (calendar, itinerary)

1. **Scenario:** Logs or backups contain PII (travel dates/locations).
2. **Likelihood/Impact:** Medium / Very high (privacy + safety).
3. **Mitigation:** mask PII in logs; encrypt persisted data; limit retention.
4. **Monitoring:** scan logs for PII patterns; audit access logs.

### 5) Third-party API dependency / outages

1. **Scenario:** Payment or booking provider outage causes failed bookings or duplicate attempts.
2. **Likelihood/Impact:** Medium / Medium-high.
3. **Mitigation:** retry with backoff; idempotency keys; graceful degradation (create itinerary and notify user rather than charge).
4. **Monitoring:** track provider error rates & latency; alert if SLA exceeded.

### 6) Over-broad autonomous booking consent

1. **Scenario:** User grants wide permission; system books beyond intended scope.
2. **Likelihood/Impact:** Medium / Medium-high.
3. **Mitigation:** require per-item confirmation OR single-use granular consent; code-enforced budgets and destination locks.
4. **Monitoring:** log consent events; alert when bookings happen without fresh user action.

### 7) LLM output validation bypass (malformed fields / code injection)

1. **Scenario:** LLM outputs malicious strings in structured fields.
2. **Likelihood/Impact:** High / Medium-high.
3. **Mitigation:** strict Pydantic validation; sandbox any downstream use of LLM output; never `eval` strings.
4. **Monitoring:** count validation failures; log rejected outputs (sanitized).

### 8) Memory store leakage

1. **Scenario:** Conversation memory contains payment tokens or PII and gets exfiltrated.
2. **Likelihood/Impact:** Medium / High.
3. **Mitigation:** encrypt memory, mask tokens, limit retention; never store raw card data.
4. **Monitoring:** alert on unusual read/export patterns; bucket-level access logs.

---

# 9. Where to expand for production

* Replace mock payment with real provider SDK (Stripe/PayPal/Xendit) and use tokenization.
* Harden auth (OAuth2, session policies).
* Centralized audit & observability (Prometheus + Grafana + Sentry).
* CI/CD with security scans & unit/integration tests for flows (billing, refunds).
* Add privacy-preserving defaults (data minimization).
