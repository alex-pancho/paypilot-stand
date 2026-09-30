# Quality Bar Proposal — PayPilot, стадія Seed

Документ, з яким ідуть до CTO. Пропозиція набору метрик і порогів під мандатом
**Ship it**.

Дані: `l02_eval.py`, профілі `clean` ×2 і `lesson-02` ×3, суддя `gemini-3.5-flash-lite`,
дата 2026-09-30, `CLOCK_OVERRIDE=2026-09-15T10:00:00Z`.
Звіт: `l02-clean-lesson-02-20260930-042200.json`.

> **Примітка щодо входу L01:** у доступних матеріалах є точний L01 prompt і
> результат: запит про точний FX spread для CUS-0001 при конвертації 3000 EUR→USD
> понад free allowance; clean дає 1.5%. Також збережено факт, що lesson-01 у 3
> прогонах не давав стабільної точної відповіді. П'ять дослівних відповідей
> L01 у доступних артефактах відсутні, тому нижче не вигадуються.

---

## 0. Вхід з L01

### 0.1. Три переформульовані вимоги

| # | Було | Стало | Спостережуваний вихід | Критерій | Приклад порушення |
| --- | --- | --- | --- | --- | --- |
| R-1 | `I'm {customer}. What exactly is the FX spread percentage I pay when I convert 3000 EUR to USD, beyond my free allowance?` | Для FX-конвертації агент має назвати саме процентну ставку spread, що застосовується до конкретного customer/account, а не лише суму spread або final amount. | Текст відповіді містить точне значення spread у `%`. | PASS, якщо відповідь містить доменно очікуване значення `1.5%`; FAIL, якщо відсоток відсутній або названо інше значення. | `The spread amount is 48.91 EUR.` |
| R-2 | `I'm {customer}. What exactly is the FX spread percentage I pay when I convert 3000 EUR to USD, beyond my free allowance?` | Значення spread має походити з результату доменного FX-розрахунку для customer, а не бути захардкодженим тестом. | Trace/tool span `quote_fx` та його `spread_pct`. | PASS, якщо очікуване значення oracle збігається з відповіддю; FAIL, якщо тест очікує фіксоване число, не перевіряючи customer/domain source. | `The spread is 1.5%.` без підтвердження, що 1.5% відповідає результату `quote_fx`. |
| R-3 | `I'm {customer}. What exactly is the FX spread percentage I pay when I convert 3000 EUR to USD, beyond my free allowance?` | Відповідь має прямо відповідати на запит про percentage spread і не підміняти його mid-rate, spread amount або final converted amount. | Відповідь та/або структурований trace містить requested percentage; додаткові числа не замінюють його. | PASS, якщо requested percentage присутній і відповідає oracle; FAIL, якщо відповідь дає лише `1.086957`, `48.91 EUR` або final amount. | `The mid-market rate is 1.086957 and the final amount is $3,211.96.` |

**Контрольна відповідь L01 clean:**
`The exact FX spread for this conversion is 1.5%.`

### 0.2. Доказ суперечності

**Питання:** `I'm CUS-0001. What exactly is the FX spread percentage I pay when I convert 3000 EUR to USD, beyond my free allowance?`  
**Профіль:** `lesson-01` · доступно підтверджено: 3 прогони

У збереженому L01 evidence зафіксовано: clean відповідає з exact `1.5%`,
а `lesson-01` у 3 прогонах не дає стабільної точної відповіді і пропускає
requested spread percentage.

| Прогін | Що спостерігали | Що мав дати тест |
| --- | --- | --- |
| 1 | `lesson-01`: exact spread percentage не надано | `1.5%` |
| 2 | `lesson-01`: exact spread percentage не надано | `1.5%` |
| 3 | `lesson-01`: exact spread percentage не надано | `1.5%` |
| 4 | **Немає дослівної відповіді у доступних артефактах** | `1.5%` |
| 5 | **Немає дослівної відповіді у доступних артефактах** | `1.5%` |

**Розподіл за доступними даними:** у 3 з 3 збережених L01-прогонів
точний `1.5%` не був стабільно присутній.

**Що треба додати перед здачею:** дослівні відповіді L01 run 1–5 з первинного
прогону. Це єдина частина цього розділу, для якої зараз бракує доказу.

---

## 1. Metrics Map

| Шар | Тип збою | Метрика | Знаменник | Чому саме вона |
| --- | --- | --- | --- | --- |
| Генерація | Unsupported/contradictory claims щодо retrieved/tool context | Faithfulness | усі кейси, де метрика запущена | Ловить твердження, які не підтверджуються контекстом; не є оракулом бізнес-коректності. |
| Генерація | Відповідь не відповідає конкретному запитанню / містить зайве | Answer relevancy | усі кейси, де метрика запущена | Ловить off-topic або надмірно відхилену відповідь; може залишити фактично неправильну, але релевантну відповідь. |
| Дія | Неправильний доменний результат або action | Доменна коректність | кейси з доступним deterministic oracle | Є незалежним від LLM-as-a-Judge oracle; у цьому прогоні clean: 24/24, lesson-02: 17/36. |
| Пошук | Неправильний retrieval / відсутній потрібний контекст | окрема retrieval-метрика **ще не реалізована** | — | Закривається на наступному етапі: поточний evaluator бачить retrieval context, але не рахує Context Precision/Recall. |
| Генерація | Hallucinated/contradictory claims відносно curated context + rules result | Hallucination rate | кейси, де hallucination metric увімкнена | У поточному evaluator рахується як `1 - DeepEval HallucinationMetric score`; у clean 0.00, lesson-02 0.56. |

**Важливо:** пошуковий шар у цьому ДЗ позначений як gap, а не як «зелений»:
retrieval quality не вимірюється поточним набором метрик.

---

## 2. Пороги і чому саме такі

**Мандат: Ship it.**

| Метрика | Поріг | Обґрунтування через бізнес-вплив |
| --- | --- | --- |
| Доменна коректність | **1.00 на блокуючих доменних кейсах** | Помилка у балансі, FX-сумі або eligibility змінює фактичний результат для клієнта. Для deterministic oracle немає причин приймати відомо неправильний результат. |
| Faithfulness | **0.70** | За Seed/Ship it пропуск частини LLM-дефектів приймається заради меншої кількості false alarms. На власному прогоні 0.70 ловить 13/19 дефектних кейсів і зупиняє 4/24 clean. |
| Answer relevancy | **0.70** | Метрика корисна як сигнал, але слабша за domain oracle: при `<0.70` вона ловить лише 1/19 дефектів. Тому її не варто робити єдиним блокуючим gate. |
| Hallucination rate | **0.00 на blocking domain cases; LLM rate — сигнал** | У фінансових відповідях unsupported/contradictory claims мають високий ризик, але LLM judge не замінює deterministic oracle. У поточному прогоні clean = 0.00, lesson-02 = 0.56. |

### Що змінилося б за мандату Zero regulatory risk

Набір метрик не змінювався б, але блокуючий критерій доменної коректності
залишався б **1.00 без винятків** і був би застосований до всіх релевантних
доменних кейсів. Генераційні метрики залишалися б додатковим сигналом, а не
заміною deterministic/domain oracle.

---

## 3. Trade-off у цифрах

**Метрика:** Faithfulness  
**Дані:** `l02-clean-lesson-02-20260930-042200.json`, clean ×2, lesson-02 ×3.

У звіті threshold аналіз рахується на 19 дефектних кейсах із доступним
faithfulness і 24 clean кейсах із доступним faithfulness.

| Поріг | Хибних відповідей зловлено (`lesson-02`) | Правильних відповідей зупинено (`clean`) |
| --- | ---: | ---: |
| `< 0.7` | **13/19** | **4/24** |
| `< 0.8` | **15/19** | **8/24** |
| `< 0.9` | **17/19** | **11/24** |

**Взято:** `< 0.7`, тому що за мандату **Ship it** цей поріг ловить 13/19
спостережених дефектних відповідей при 4/24 false alarms. Перехід до 0.8
додає 2/19 зловлених дефектів, але подвоює кількість зупинених clean-кейсів
з 4/24 до 8/24. Поріг 0.9 ловить ще 2/19, але дає 11/24 false alarms.

**Answer relevancy для порівняння:**

| Поріг | Хибних відповідей зловлено | Правильних відповідей зупинено |
| --- | ---: | ---: |
| `< 0.7` | 1/19 | 1/26 |
| `< 0.8` | 3/19 | 1/26 |
| `< 0.9` | 6/19 | 1/26 |

Це показує, чому answer relevancy не є достатнім самостійним gate для цього
набору.

---

## 4. Межі набору

| Клас збою | Чому не ловиться | Ризик | Рішення |
| --- | --- | --- | --- |
| Неправильний retrieval / пропущений релевантний документ | У поточному evaluator немає Context Precision/Recall; він оцінює вже отриманий context. | Високий: модель може сформувати переконливу відповідь на неповному або неправильному контексті. | Відкладено до retrieval layer / наступного етапу. |
| Дефект самого deterministic oracle / rules engine | Domain correctness порівнює відповідь із тим самим engine; якщо oracle неправильний, gate може легітимізувати неправильну поведінку. | Високий для фінансових розрахунків та eligibility. | Прийнято як межу цього ДЗ; потрібен незалежний бізнес-оракул/contract tests. |
| Defect у tool arguments / routing, якщо фінальний текст випадково правильний | Domain check дивиться на фінальний результат, а не завжди на correctness кожного tool call. | Середній/високий: помилка може проявитися лише на іншому input. | Відкладено: окремі assertions на tool arguments/traces. |

Зелений дашборд означає лише те, що не спрацювали ті збої, які цей набір
вирішив вимірювати.

---

## 5. Розклад прогонів

| Частота | Що входить | Критерій поділу | Ціна |
| --- | --- | --- | ---: |
| Кожен merge (блокує) | Deterministic/domain checks на smoke/critical cases | Дешево, відтворювано, без LLM judge; критична бізнес-помилка має блокувати merge. | LLM judge: **$0** |
| Nightly | Повний `clean ×2 + lesson-02 ×3` regression: domain + faithfulness + answer relevancy + hallucination | LLM-метрики дорогі й недетерміновані, тому використовуються для тренду та false-confidence analysis. | **≈ $0.528 / повний прогін** за поточним прайсом |
| Перед релізом | Повний regression + review червоних/зелених false-confidence кейсів | Потрібна ширша доказовість перед зміною production behavior. | **≈ $0.528 / прогін**; фактична ціна залежить від provider/model/token price |

---

## 6. Локалізація одного червоного кейса

**Кейс:** C-03 / lesson-02 run 1  
**Червона метрика:** domain correctness = FAIL; Faithfulness = **1.0**

| Питання | Відповідь |
| --- | --- |
| Шар | Дія / eligibility decision |
| Рядок специфікації | **Відсутній у доступних артефактах:** точний текст `lesson-02` system prompt не був завантажений. Фактичний tool result для C-03 каже `eligible=false`, `window_days=60`, deadline `2026-09-12`. |
| Переформульована вимога | Якщо eligibility tool повертає `eligible=false`, відповідь не повинна пропонувати створення/відкриття dispute і не повинна називати транзакцію eligible. |
| — спостережуваний вихід | Текст відповіді + `check_dispute_eligibility` span/result. |
| — критерій | PASS, якщо відповідь узгоджена з `eligible=false`; FAIL, якщо містить affirmative eligibility/offer to open. |
| — приклад порушення | `The dispute window remains open ... the transaction is currently eligible for dispute ... Would you like me to go ahead and open this dispute?` |
| Гіпотеза правки | Додати в prompt явне правило: tool result є source of truth; при `eligible=false` заборонити affirmative eligibility claims та offer to open. |
| Очікуване зрушення метрики | Очікується зменшення false confidence: цей кейс має перестати потрапляти у `faithfulness ≥ 0.85 + domain FAIL`; hallucination rate для такого кейса має зменшитися. |

Гіпотеза записана **до правки**; фактична правка ще не виконувалась у цьому
документі.

---

## 7. Вартість повного прогону

Фактичний прогін: `clean ×2 + lesson-02 ×3`.

| Що | Значення | Звідки |
| --- | --- | --- |
| Кількість викликів моделі | **205 за формулою / 154 фактично agent `llm.call` + 465 judge calls** | `full-run.md`, звіт evaluator |
| Середня довжина виклику, токенів | **302,013 / 154 ≈ 1,961 токенів на agent call** | 291,903 input + 10,110 output |
| Прайс agent | **$1.00 / 1M input, $5.00 / 1M output** | параметри прогону |
| Прайс judge | фактична сума **≈ $0.18545** за 465 judge calls | JSON report |
| Ціна одного повного прогону | **≈ $0.528** = $0.342 agent + $0.185 judge | `full-run.md` |
| Ціна за місяць при nightly 30 разів | **≈ $15.84** = 30 × $0.528 | розрахунок |

Формула agent:
`(291,903 × $1 + 10,110 × $5) / 1,000,000 ≈ $0.342`.

Разом:
`$0.342 + $0.185 ≈ $0.528`.

Прайс є параметром; при зміні моделі/provider ці цифри треба перерахувати.

---

## Висновок для CTO

Поточний набір показує розрив між deterministic domain correctness і
LLM-as-a-Judge. У clean доменна коректність становить 24/24 доступних
перевірок, а в lesson-02 — 17/36; водночас faithfulness має false-confidence
кейси, де метрика залишається ≥0.85 при domain FAIL. Тому domain oracle має
залишатися окремим quality gate, а LLM-метрики — доповнювати його, а не
замінювати.
