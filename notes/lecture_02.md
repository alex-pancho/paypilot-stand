# Нотатки ментора — Лекція 2

## 1. Основна ідея лекції

У L01 ми навчилися контролювати зміну prompt.

Тепер наступне питання:

> Як довести, що AI-система відповідає вимогам достатньо добре?

Для цього нам потрібні:

test dataset;
expected behavior / ground truth;
evaluator;
metrics;
thresholds;
regression;
quality gate.

Тобто ми переходимо від:

`Prompt змінився`

до:

`Ми можемо виміряти, що саме змінилося в якості системи.`

Головна практична ідея L02:

> Метрика сама по собі нічого не гарантує. Важливо розуміти, що саме вона вимірює, де вона може помилитися і як перетворити її результат на інженерне рішення.

## 2. evaluation != тестування

У класичному API-тесті ми можемо написати:
```python
assert response.status_code == 200
assert response.json()["status"] == "approved"
```
Тут oracle відомий і стабільний.

А коли питаємо AI то нам поверне:
```
The transaction appears to be eligible for a refund because it was made within the allowed period.
```
І у QA виникає питання:

Як **автоматично** визначити, чи ця відповідь правильна?

Саме тут з'являється evaluator – "оцінщик" – тобто система, яка видасть набір оцінок за параметрами.

## Звідки беруться дані для оцінки?

У будь-якій системі ми збираємо купу логів. Але логів того, що запитав клієнт (промту) і того, що відповіла система тут буде недостатньо — вони не дадуть нам повної інформації. Саме тому, тестовий стенд побудовано таким чином, щоб до кожної відповіді був прив'язаний `trace_id` що дає купу додаткової інформації.



## Створюємо датасет




```yaml
cases:
  - id: TC-SWIFT-01
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

  - id: TC-DISPUTE-01
    prompt: >
      I am CUS-0004. Transaction TX-0402 was on July 14,
      a duplicate charge. Can I still dispute it today?
    expected:
      answer:
        contains:
          - "60"
          - "September 12"
          - "cannot"
      context:
        must_contain:
          - "60-day"
          - "2026-09-12"
          - "duplicate_charge"
      retrieval:
        required: false
      tool_calls:
        required:
          - check_dispute_eligibility

  - id: TC-FX-01
    prompt: >
      I'm CUS-0005. Convert 6000 EUR to USD.
      What spread do I pay?
    expected:
      answer:
        contains:
          - "0.9%"
          - "6000 EUR"
          - "6463.04"
      context:
        must_contain:
          - "0.9%"
          - "Tier 2"
          - "1000"
          - "5000"
      retrieval:
        required: false
      tool_calls:
        required:
          - quote_fx

  - id: TC-BALANCE-01
    prompt: >
      I'm CUS-0002. What is the exact balance of my USD account ACC-1003?
    expected:
      answer:
        contains:
          - "ACC-1003"
          - "5,200.75"
          - "USD"
      context:
        must_contain:
          - "ACC-1003"
          - "5200.75"
          - "USD"
      retrieval:
        required: false
      tool_calls:
        required:
          - get_account
```

### Faithfulness ≠ Correctness

Це дуже важливий момент.

Уявімо:
```
Context:

Customer has 500 EUR allowance.
```

AI:
```
You have 500 EUR allowance.
```
Параметр Faithfulness:

PASS

Але database каже:

Customer has already used 120 EUR.
Remaining = 380 EUR

Тоді:

> - Faithfulness → може бути високою
> - Business correctness → FAIL

Отже:

Faithfulness перевіряє зв'язок відповіді з наданим context. Вона не гарантує, що сам context правильний або що відповідь відповідає бізнес-правилам.

Це одна з головних причин false confidence.


### Relevancy

Relevancy відповідає на інше питання:

Чи пов'язана відповідь з самим запитаням?
```
Question:

What is my FX spread?

Answer:

Your account was created in 2022.
Your current balance is 1,200 EUR.
You have an active account.
```
Всі твердження можуть бути фактично правильними.

Але:

Answer relevancy → FAIL

Бо відповідь не вирішує задачу користувача.

Тобто:
| Faithfulness	| Relevancy |
|---|---|
|       ↓   |     ↓                    | 
| Чи узгоджується з context?	| Чи пов'язано з question? |

Зведено подати метрики можна так:

| Metric	| Question |
|---|---|
| Correctness	| Чи правильна відповідь? |
| Faithfulness	| Чи підтримана відповідь evidence/context? |
| Relevancy	| Чи пов'язана відповідь з питаням? |
| Hallucination	| Чи є unsupported claims? |

