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

Саме тут з'являється evaluator – "оцінщк" – тобто система, яка видасть набір оцінок за параметрами.

## Створюємо датасет

Тут основна логіка побудови проста:
єлементи з all повинні бути у відповіді, елементи з any можуть бути, і нарешті  те що в not - бути не повинно. 

```yaml
testdata:
  forex_policy:
    promt: "I'm {customer}. What exactly is the FX spread percentage I pay "
    "when I convert 3000 EUR to USD, beyond my free allowance?"
    all: ["FX_SPREAD", "EUR", "USD"]
    any: ["commission", "rate", "policy"]
    not: []
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

