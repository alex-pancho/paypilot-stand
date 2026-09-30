# Specification Review — `base.v1` / `lesson-02`

Аудит специфікації. Профіль прогонів: `clean ×2`, `lesson-02 ×3`.  
Дата: 2026-09-30.  
Артефакти аудиту: `manual_log_for_l2.yaml`, `l02-clean-lesson-02-20260930-042200.json`,
`full-run.md`.

> **Обмеження evidence:** сам текст system prompt `base.v1` / `base.v1+D04+D05+D25`
> не входить до доступних завантажених артефактів. Тому карта анатомії не вигадує
> рядків prompt. Там, де потрібна дослівна цитата prompt, вказано, що її треба
> додати з первинного файлу. Спостереження за поведінкою та tool traces наведені
> лише там, де вони фактично є.

---

## 1. Карта анатомії

| # | Блок | Стан | Рядки, що його утворюють |
|---|---|---|---|
| 1 | Роль і тон | **слабкий** | «professional and businesslike», «state what you did» — перше неверифіковане, друге перевіряється |
| 2 | Скоуп | **є** | перелік тем і дій; закрита множина ||
| 3 | Джерела правди | **є** | «answer only from tool results»; правило приоритету «tool result wins» |
| 4 | Правила інструментів | **є** | Tool traces є; явні prompt rules є |
| 5 | Доменні обмеження | **неверифіковано** | Для C-03/C-10/C-04 фактичні правила доступні через tool result, але prompt wording відсутній |
| 6 | Крайні випадки | **неверифіковано** | C-03/C-10/C-19 демонструють такі сценарії, але вимоги prompt не видно |
| 7 | Формат виходу | не підтверджено | Текст `base.v1` не наданий |
| 8 | Приклади | не підтверджено | Текст `base.v1` не наданий |

**Порожні / непідтверджені блоки:** 1, 2, 7, 8 та частково 3–6.

**Слабкі:** джерела правди, правила tool usage, domain constraints, edge cases.

---

## 2. Знахідки

| # | Знахідка | Блок | Тип | Доказ | Severity (через бізнес-вплив) |
|---|---|---|---|---|---|
| F-01 | Немає перевірюваної вимоги, яка прямо забороняє позитивний eligibility claim після `eligible=false`. | Доменні обмеження / крайні випадки | **неповнота** | C-03 lesson-02 run 1: tool result `eligible=false`, але відповідь каже `transaction is currently eligible` і пропонує відкрити dispute. | **Високий:** клієнту може бути запропонована недоступна фінансова дія. |
| F-02 | Вимога щодо точного FX spread не має достатньо жорсткого observable output у defected behavior. | Формат виходу / доменні обмеження | **неверифікованість** | L01 case: clean містить `1.5%`, lesson-01 у збережених прогонах не дає стабільного exact spread. | **Середній/високий:** клієнт отримує неправильну інформацію про комісію/вартість конвертації. |
| F-03 | Відповідь може бути релевантною за темою, але фактично неправильною за business result. | Джерела правди / domain constraints | **суперечність** | C-04/C-05/C-07: answer relevancy часто залишається високою, тоді як domain check = FAIL. | **Високий:** неправильна FX сума безпосередньо впливає на гроші клієнта. |
| F-04 | Не видно явного зв'язку між вимогою та конкретним observable trace/tool field. | Джерела правди / tool rules | **невідстежуваність** | У evaluator є `quote_fx`, `check_dispute_eligibility`, `get_account`, але prompt artifact не містить доступного mapping requirement → field. | **Середній:** тест може перевіряти текст, не перевіряючи фактичну дію системи. |
| F-05 | Retrieval quality не має окремої acceptance requirement у доступному evaluator. | Скоуп / джерела правди | **неповнота** | Поточний evaluator рахує faithfulness/relevancy/hallucination/domain, але не Context Precision/Recall. | **Середній/високий:** неправильний або неповний retrieved context може залишитися непоміченим. |

---

## 3. Доказовість однієї знахідки

**Обрано F-01 — суперечність між eligibility tool result і відповіддю.**

**Питання:** `I am CUS-0004. Transaction TX-0402 was on July 14, a duplicate charge. Can I still dispute it today?`  
**Профіль:** `lesson-02` · **прогонів:** 3

| Прогін | Що спостерігали | Що повернув engine | Що зробив агент |
|---|---|---|---|
| 1 | Tool викликаний | `eligible=false`, 60 days, deadline `2026-09-12` | Назвав 90-day window і сказав, що transaction eligible; запропонував відкрити dispute |
| 2 | Tool викликаний | `eligible=true`, 90 days, deadline `2026-10-12` у defective profile | Повторив 90-day rule і affirmative eligibility |
| 3 | Tool викликаний | `eligible=true`, 90 days, deadline `2026-10-12` у цьому конкретному run | Повторив affirmative eligibility |

**Розподіл:** у 1/3 прогонів domain engine для цього кейса повернув
`eligible=false`, але відповідь була affirmative; у двох інших прогонів
сам defective engine повернув `eligible=true`.

### Дослівні цитати

> `Verta's dispute policy allows duplicate charges to be disputed within a 90-day window from the transaction date. For transaction TX-0402, which occurred on July 14, 2026, the dispute window remains open until October 12, 2026. ... the transaction is currently eligible for dispute under the duplicate charge category.`

> `Would you like me to go ahead and open this dispute for you now?`

Це показує, чому одного текстового LLM score недостатньо: у run 1
faithfulness був **1.0**, хоча domain correctness був FAIL.

---

## 4. Переформульовані вимоги

### R-1 — замінює F-01

> **Було:** точний рядок `base.v1` не доступний у audit artifact.
>
> **Стало:** Якщо `check_dispute_eligibility` повертає `eligible=false`,
> агент не має права стверджувати, що транзакція eligible, і не має
> пропонувати створити/open dispute.

- **тригер:** після кожного виклику `check_dispute_eligibility`
- **спостережуваний вихід:** текст відповіді + `tool.result.eligible`
- **критерій:** PASS, якщо `eligible=false` → немає affirmative eligibility
  claim/offer; FAIL, якщо є `is eligible`, `remains eligible`,
  `you can dispute/open/file` тощо.

### R-2 — замінює F-03

> **Було:** точний рядок `base.v1` не доступний у audit artifact.
>
> **Стало:** Для FX quote фінальний amount і spread percentage мають відповідати
> значенням, повернутим `quote_fx`; генерація не може замінювати tool result
> власним розрахунком.

- **тригер:** після кожного `quote_fx`
- **спостережуваний вихід:** `spread_pct`, `final_amount` у tool result і
  відповідні значення в answer
- **критерій:** PASS, якщо всі критичні числові поля відповідають oracle;
  FAIL, якщо хоча б одне критичне поле не збігається.

### R-3 — замінює F-05

> **Було:** окрема retrieval acceptance requirement не підтверджена.
>
> **Стало:** Для knowledge-base відповідей потрібний retrieved context, який
> містить evidence для ключового твердження відповіді.

- **тригер:** після `search_knowledge_base`
- **спостережуваний вихід:** retrieved fragments + key claims у answer
- **критерій:** PASS, якщо кожне критичне твердження має supporting fragment;
  FAIL, якщо answer містить critical claim без supporting context.

---

## 5. Межі аудиту

Чого цей метод не знаходить:

1. Дефекти, яких немає в prompt і які не проявилися в поточному наборі кейсів;
   для них потрібен незалежний oracle / exploratory or adversarial testing.
2. Помилки самого deterministic rules engine: evaluator може прийняти неправильний
   engine result як ground truth.
3. Повну якість retrieval: поточний evaluator не має окремих Context Precision /
   Context Recall метрик.
4. Невірні tool arguments, якщо фінальний текст випадково виглядає правильним;
   потрібні окремі assertions на trace/tool arguments.

---

## Примітка перед здачею

Для повної відповідності чеклісту ментора студент має додати:

1. дослівний `base.v1` prompt;
2. п'ять дослівних L01 відповідей.
