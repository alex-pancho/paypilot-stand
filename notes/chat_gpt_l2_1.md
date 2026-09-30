Так, тепер зрозуміло, що ти хочеш. У тебе вже є **ручний golden dataset**: для кожного кейса є `prompt`, `clean.text`, `clean.trace`, `lesson-02.text`, `lesson-02.trace`. Наприклад, для D05 у trace видно і retrieval, і конкретні retrieved fragments, а для lesson-02 retrieval взагалі відсутній. 

Тепер наступний крок — **перетворити цей YAML на автоматичний evaluation dataset**, де evaluator бере **і текст відповіді, і trace**.

Я б зробив це не через один `all/any/not`, а так:

```yaml
cases:
  - id: D05
    prompt: >
      I'm CUS-0008. What is the SWIFT transfer fee at Verta?
      Just tell me the number.

    expected:
      answer:
        contains:
          - "15"
          - "0.3%"
      context:
        must_contain:
          - "SWIFT"
          - "EUR 15.00"
          - "0.3%"
      retrieval:
        required: true
      tool_calls:
        required:
          - search_knowledge_base

    metrics:
      correctness: true
      faithfulness: true
      context_precision: true
      context_recall: true
      answer_relevance: true
```

А далі evaluator працює **не з YAML-відповіддю**, а з фактичним runtime result:

```text
prompt
   ↓
AI
   ↓
answer + trace
   ↓
┌───────────────────────────────────────┐
│             EVALUATORS                │
├──────────────┬────────────────────────┤
│ answer       │ correctness            │
│ answer       │ relevance              │
│ answer+ctx   │ faithfulness            │
│ trace        │ context precision       │
│ trace+gold   │ context recall          │
│ trace        │ tool correctness        │
└──────────────┴────────────────────────┘
```

## 1. Що беремо з `text`

Наприклад D20:

```text
lesson-02.text:

Tier 2 ... spread is 1.5%
```

Golden:

```yaml
expected:
  answer:
    contains:
      - "0.9%"
```

Тоді простий correctness evaluator:

```python
def check_answer(answer, expected):
    return all(
        value.lower() in answer.lower()
        for value in expected["contains"]
    )
```

У D20:

```text
expected = 0.9%
actual   = 1.5%

→ correctness = 0
```

Це **оцінка тексту відповіді**.

---

# 2. Але trace дає нам зовсім інший набір метрик

Подивись на D20.

У clean trace:

```json
"tool.name": "quote_fx"

"tool.result": {
    "tier": "tier2",
    "spread_pct": 0.9
}
```

У defect trace:

```json
"tool.name": "quote_fx"

"tool.result": {
    "tier": "tier2",
    "spread_pct": 1.5
}
```

Тобто ми можемо взагалі **не довіряти тексту LLM**, а перевірити бізнес-джерело:

```python
expected_spread = 0.9

trace_spread = trace["quote_fx"]["spread_pct"]

assert trace_spread == expected_spread
```

Це вже інша метрика:

```text
Tool / business correctness
```

І тут виникає дуже важлива архітектура evaluation:

### Answer evaluation

```text
"Tier 2 spread is 1.5%"
          ↓
    evaluate text
```

### Trace evaluation

```text
quote_fx()
   ↓
spread_pct = 1.5
   ↓
compare with expected 0.9
```

### Context evaluation

```text
search_knowledge_base()
   ↓
retrieved fragments
   ↓
evaluate relevance/coverage
```

---

# 3. Для твого YAML я б зробив три секції expected

Ось вже ближче до реального навчального датасету:

```yaml
cases:

  - id: D20

    prompt: >
      I'm CUS-0005. Convert 6000 EUR to USD.
      What spread do I pay?

    expected:

      answer:
        contains:
          - "0.9%"
          - "6000 EUR"
          - "USD"

      business:
        tool: quote_fx
        fields:
          customer_id: CUS-0005
          amount: 6000
          from_currency: EUR
          to_currency: USD
          spread_pct: 0.9

      trace:
        required_tools:
          - quote_fx

      context:
        required: false
```

Тепер один testcase дозволяє перевірити **три різні рівні**.

---

# 4. Evaluation результат одного кейса

Наприклад система отримала D20.

### Answer

```text
Tier 2 spread is 1.5%.
```

### Trace

```json
{
  "tool": "quote_fx",
  "result": {
    "tier": "tier2",
    "spread_pct": 1.5
  }
}
```

Evaluator повертає:

```json
{
  "case_id": "D20",

  "answer": {
    "correctness": 0,
    "relevance": 1
  },

  "trace": {
    "tool_called": 1,
    "business_correctness": 0
  },

  "overall": 0
}
```

---

# 5. Faithfulness теж використовує trace

Це особливо добре видно на D19.

У defect trace:

```json
"tool.result": {
    "eligible": true,
    "window_days": 90,
    "deadline": "2026-10-12"
}
```

AI відповідає:

```text
The dispute window remains open until October 12.
```

Тобто:

```text
AI answer
    ↑
    │ supported by
    │
tool result
```

Отже:

```text
Faithfulness = 1
```

Але бізнес-очікування:

```yaml
expected:
  dispute:
    eligible: false
    window_days: 60
    deadline: 2026-09-12
```

Тому:

```text
Correctness = 0
```

Це **ідеальний навчальний приклад**, тому що можна буквально показати студенту:

```text
                 D19
                  │
        ┌─────────┴──────────┐
        │                    │
   trace supports       business truth
        │                    │
        ▼                    ▼
 Faithfulness = 1       Correctness = 0
```

У твоєму файлі це прямо видно: clean trace повертає `eligible=false`, `window_days=60`, а lesson-02 trace — `eligible=true`, `window_days=90`. 

---

# 6. Context Precision

Тут беремо trace:

```json
"tool.result": {
  "fragments": [
    {
      "id": "tariffs.md#s3",
      "score": 1.0,
      "text": "SWIFT ... EUR 15.00 ... 0.3%"
    },
    {
      "id": "fees-detail.md#s1",
      "score": 0.9258,
      "text": "SWIFT ..."
    },
    {
      "id": "fees-detail.md#s2",
      "score": 0.9177,
      "text": "Card payment..."
    },
    {
      "id": "transfers.md#s4",
      "score": 0.5774,
      "text": "Failed transfers..."
    }
  ]
}
```

Тепер dataset повинен сказати:

```yaml
expected:
  context:
    relevant:
      - tariffs.md#s3
      - fees-detail.md#s1
```

Evaluator:

```python
retrieved = [
    "tariffs.md#s3",
    "fees-detail.md#s1",
    "fees-detail.md#s2",
    "transfers.md#s4",
]

relevant = {
    "tariffs.md#s3",
    "fees-detail.md#s1",
}
```

І вже можна рахувати:

```text
2 relevant / 4 retrieved = 0.50
```

Для першої практики це абсолютно достатньо.

---

# 7. Context Recall

Тут dataset має сказати:

```yaml
expected:
  context:
    required_facts:
      - "SWIFT flat fee = EUR 15.00"
      - "SWIFT percentage fee = 0.3%"
```

Потім evaluator дивиться на retrieved fragments:

```text
retrieved context
       ↓
found "EUR 15.00" → YES
found "0.3%"      → YES
```

Отже:

```text
2 / 2 = 1.0
```

Якщо був тільки:

```text
EUR 15.00
```

то:

```text
1 / 2 = 0.5
```

---

# 8. Тобто твій dataset фактично має описувати не "правильну відповідь", а expected behavior

Це важлива зміна.

Не:

```yaml
expected:
  answer: "The fee is..."
```

А:

```yaml
expected:

  answer:
    contains:
      - "15"
      - "0.3%"

  context:
    required_facts:
      - "15"
      - "0.3%"

  retrieval:
    required: true

  tools:
    required:
      - search_knowledge_base

  business:
    ...
```

Тоді один dataset може використовуватися різними evaluators.

---

# 9. Я б для L02 зробив саме 5 evaluator'ів

Не намагатися одразу будувати складний RAGAS.

### `AnswerCorrectnessEvaluator`

```text
answer + expected business result
                ↓
              0 / 1
```

### `AnswerRelevanceEvaluator`

```text
question + answer
       ↓
    0..1
```

### `FaithfulnessEvaluator`

```text
answer + retrieved context
             ↓
           0..1
```

### `ContextPrecisionEvaluator`

```text
retrieved chunks + relevant chunk IDs
              ↓
             0..1
```

### `ContextRecallEvaluator`

```text
required facts + retrieved context
              ↓
             0..1
```

А вже **після цього** показати:

> "Те, що ми щойно написали вручну, фактично є спрощеною версією того, що роблять RAGAS / DeepEval."

---

## І головне — trace треба зберігати як окремий first-class input

Твій dataset зараз уже це демонструє:

```yaml
clean:
  text: ...
  trace: GET .../trace/...

lesson-02:
  text: ...
  trace: GET .../trace/...
```

Це дуже хороша основа. Наприклад D04 trace показує, що defect-сценарій спочатку отримав `ACC-1002`, хоча запитувався `ACC-1003`, а потім зробив додатковий `get_account` і вже отримав обидва рахунки. 

Тобто **метрики можна отримувати не тільки з final answer**:

```text
                    AI RUN
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
      ANSWER          TRACE          CONTEXT
        │              │              │
        ▼              ▼              ▼
 correctness      tool correctness   precision
 relevance        tool arguments     recall
 faithfulness     business result
 hallucination    latency
                  token usage
```

І це вже набагато сильніша модель L02.

**Твій ручний YAML я б не викидав.** Навпаки — використав би його як **golden dataset**, а наступною практикою зробив Python evaluator, який читає саме цей YAML, дістає `text` + `trace` і для кожного `case` генерує щось на кшталт:

```json
{
  "case": "D20",
  "answer_correctness": 0,
  "answer_relevance": 1,
  "faithfulness": 1,
  "context_precision": null,
  "context_recall": null,
  "tool_correctness": 0
}
```

А потім окремий агрегатор:

```text
D05 ─┐
D19 ─┤
D20 ─┼──→ metrics report ──→ quality gate
D04 ─┘
```

Це вже буде **справжня практична частина L02**, а не просто запуск готового `DeepEval` і читання красивих цифр.
