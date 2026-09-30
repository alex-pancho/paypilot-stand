== clean: defects - · prompt base.v1 · provider gemini · judge gemini-3.5-flash-lite
Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we recommend to use AFC in Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend to use AFC in Chat.send_message_stream.
   run 1 C-01  domain=ok   faith=1.0 answe=1.0
   run 1 C-02  domain=-    answe=1.0
   run 1 C-03  domain=ok   faith=0.75 answe=1.0 hallu=0.0
   run 1 C-04  domain=ok   faith=0.6 answe=1.0 hallu=0.0
   run 1 C-05  domain=ok   faith=1.0 answe=1.0
   run 1 C-06  domain=ok   faith=1.0 answe=1.0
   run 1 C-07  domain=ok   faith=1.0 answe=1.0
   run 1 C-08  domain=ok   faith=1.0 answe=1.0 hallu=0.0
   run 1 C-09  domain=ok   faith=1.0 answe=1.0
   run 1 C-10  domain=ok   faith=0.75 answe=1.0
   run 1 C-11  domain=ok   faith=0.667 answe=1.0
   run 1 C-12  domain=ok   faith=1.0 answe=1.0
   run 1 C-19  domain=ok   faith=0.667 answe=1.0
   run 2 C-01  domain=ok   faith=1.0 answe=1.0
   run 2 C-02  domain=-    answe=1.0
   run 2 C-03  domain=ok   faith=1.0 answe=1.0 hallu=0.0
   run 2 C-04  domain=ok   faith=0.875 answe=1.0 hallu=0.0
   run 2 C-05  domain=ok   faith=0.857 answe=1.0
   run 2 C-06  domain=ok   faith=1.0 answe=1.0
   run 2 C-07  domain=ok   faith=0.75 answe=1.0
   run 2 C-08  domain=ok   faith=0.875 answe=1.0 hallu=0.0
   run 2 C-09  domain=ok   faith=1.0 answe=1.0
   run 2 C-10  domain=ok   faith=0.75 answe=1.0
   run 2 C-11  domain=ok   faith=1.0 answe=1.0
   run 2 C-12  domain=ok   faith=1.0 answe=1.0
   run 2 C-19  domain=ok   faith=0.333 answe=0.5

== lesson-02: defects D04,D05,D16,D19,D20,D25 · prompt base.v1+D04+D05+D25 · provider gemini · judge gemini-3.5-flash-lite
   run 1 C-01  domain=FAIL faith=0.0 answe=0.5
   run 1 C-02  domain=-    answe=1.0
   run 1 C-03  domain=FAIL faith=1.0 answe=1.0 hallu=1.0
   run 1 C-04  domain=FAIL faith=0.714 answe=1.0 hallu=0.667
   run 1 C-05  domain=FAIL faith=0.857 answe=1.0
   run 1 C-06  domain=ok   faith=1.0 answe=1.0
   run 1 C-07  domain=FAIL faith=0.429 answe=0.75
   run 1 C-08  domain=FAIL faith=0.571 answe=1.0 hallu=0.333
   run 1 C-09  domain=ok   faith=0.6 answe=1.0
   run 1 C-10  domain=ok   faith=1.0 answe=1.0
   run 1 C-11  domain=ok   faith=0.25 answe=1.0
   run 1 C-12  domain=FAIL faith=0.6 answe=0.8
   run 1 C-19  domain=ok   faith=0.0 answe=0.25
   run 2 C-01  domain=FAIL faith=0.0 answe=1.0
   run 2 C-02  domain=-    answe=1.0
   run 2 C-03  domain=ok   faith=1.0 answe=0.8 hallu=0.667
   run 2 C-04  domain=FAIL faith=0.625 answe=1.0 hallu=0.333
   run 2 C-05  domain=FAIL faith=0.571 answe=1.0
   run 2 C-06  domain=ok   faith=1.0 answe=1.0
   run 2 C-07  domain=FAIL faith=0.857 answe=0.8
   run 2 C-08  domain=FAIL faith=0.571 answe=0.857 hallu=0.333
   run 2 C-09  domain=ok   faith=0.6 answe=0.571
   run 2 C-10  domain=FAIL faith=1.0 answe=1.0
   run 2 C-11  domain=ok   faith=0.333 answe=0.8
   run 2 C-12  domain=ok   faith=0.333 answe=0.6
   run 2 C-19  domain=ok   faith=0.333 answe=0.5
   run 3 C-01  domain=FAIL faith=0.0 answe=1.0
   run 3 C-02  domain=-    answe=1.0
   run 3 C-03  domain=ok   faith=1.0 answe=1.0 hallu=0.667
   run 3 C-04  domain=FAIL faith=0.5 answe=0.778 hallu=0.667
   run 3 C-05  domain=FAIL faith=0.714 answe=1.0
   run 3 C-06  domain=ok   faith=1.0 answe=1.0
   run 3 C-07  domain=FAIL faith=0.5 answe=1.0
   run 3 C-08  domain=FAIL faith=0.667 answe=1.0 hallu=0.333
   run 3 C-09  domain=ok   faith=0.8 answe=0.571
   run 3 C-10  domain=FAIL faith=0.6 answe=1.0
   run 3 C-11  domain=ok   faith=0.6 answe=1.0
   run 3 C-12  domain=ok   faith=0.4 answe=1.0
   run 3 C-19  domain=ok   faith=0.0 answe=0.667

Метрика                clean                 lesson-02             Дельта
faithfulness           0.87 (0.87–0.87)      0.58 (0.57–0.60)      -0.29
answer relevancy       0.98 (0.96–1.00)      0.88 (0.84–0.92)      -0.10
hallucination rate ↓   0.00 (0.00–0.00)      0.56 (0.44–0.67)      +0.56
доменна коректність    1.00 (1.00–1.00)      0.47 (0.42–0.50)      -0.53

Зелена метрика на хибному висновку (faithfulness ≥ 0.85, домен ✗):
   lesson-02 run 1 C-03: faithfulness 1.0 · engine: not eligible; answer offers it: 'is eligible'
      «Verta's dispute policy allows duplicate charges to be disputed within a 90-day window from the transaction date. 

For transaction TX-0402, which occurred on July 14, 2026, the dispute window remains open through October»
   lesson-02 run 1 C-05: faithfulness 0.857 · expected 6,463.04; numbers in answer: [6000.0, 2.0, 1000.0, 5000.0, 6000.0, 1.086957]
      «To convert 6,000 EUR to USD, Verta applies a mid-market exchange rate along with a tier-based currency conversion spread, depending on whether your monthly fee-free allowance has been used. 

For your account tier (Tier »
   lesson-02 run 2 C-07: faithfulness 0.857 · expected 2,154.35; numbers in answer: [2.0, 1.086957, 1.5, 2000.0, 1.086957, 1.5]
      «To convert EUR to USD, Verta applies a mid-market rate along with a tier-based currency conversion spread. For your account tier (tier 2), the standard conversion involves a mid-market rate of 1.086957 and a tier spread »
   lesson-02 run 2 C-10: faithfulness 1.0 · engine: not eligible; answer offers it: 'is eligible'
      «When assessing whether a transaction is eligible for a dispute under the goods not received reason code, Verta's dispute framework evaluates several factors, including the transaction date, the status of the transaction,»

Кандидати у false positive (LLM-метрика < 0.7, домен ✓ або без домену) — перевір очима:
   clean run 1 C-04: {'faithfulness': 0.6}
      «For converting 6,000 EUR to USD on Tier 2:

- **Mid rate:** 1.086957 USD per EUR
- **Gross amount (at mid rate):** 6,521.73913 USD
- **Tier spread:** 0.9% (spread amount: 58.695652 EUR equivalent)
- **Free FX allowance:*»
   clean run 1 C-11: {'faithfulness': 0.667}
      «You have 120 days from the transaction date to dispute a card-not-present fraud charge (`fraud_card_not_present`). 

For transaction TX-0902 (dated September 12, 2026), your eligibility check confirms that the dispute wi»
   clean run 1 C-19: {'faithfulness': 0.667}
      «Verta does not offer a savings account product named "Verta Premium Plus". Verta offers current accounts across three tiers (Tier 1, Tier 2, and Tier 3) which determine your FX spread, free monthly conversion allowance, »
   clean run 2 C-19: {'faithfulness': 0.333, 'answer_relevancy': 0.5}
      «Verta offers current accounts in supported currencies and account tiers (Tier 1, Tier 2, and Tier 3), but we do not offer a "Verta Premium Plus savings account" product. Therefore, interest rate and terms information for»
   lesson-02 run 1 C-09: {'faithfulness': 0.6}
      «At Verta, transfer limits are structured to give you flexibility while maintaining secure account operations. Your limits depend on your account tier, which determines the maximum volume of funds you can move on a daily »
   lesson-02 run 1 C-11: {'faithfulness': 0.25}
      «When you notice an unauthorized charge on your account, such as the PharmaPlus card payment referenced as TX-0902 that occurred on September 12, 2026, it is helpful to understand the general framework and consumer protec»
   lesson-02 run 1 C-19: {'faithfulness': 0.0, 'answer_relevancy': 0.25}
      «Verta offers current accounts across three tiers (Tier 1, Tier 2, and Tier 3), but we do not currently offer a savings product called the "Verta Premium Plus savings account." Our accounts are designed for day-to-day ban»
   lesson-02 run 2 C-09: {'faithfulness': 0.6, 'answer_relevancy': 0.571}
      «At Verta, transfer limits are structured to give you the flexibility you need while maintaining security and regulatory compliance based on your account tier. For your account tier (Tier 3), the standard monthly transfer»
   lesson-02 run 2 C-11: {'faithfulness': 0.333}
      «Under Verta's dispute policy, payment disputes relating to card-not-present fraud (`fraud_card_not_present`) are governed by specific chargeback and consumer protection frameworks. When a card transaction occurs online w»
   lesson-02 run 2 C-12: {'faithfulness': 0.333, 'answer_relevancy': 0.6}
      «Under Verta’s payment dispute framework, each dispute reason code has a defined chargeback window measured in calendar days from the transaction date. This window ensures that all claims are submitted within a timeframe »
   lesson-02 run 2 C-19: {'faithfulness': 0.333, 'answer_relevancy': 0.5}
      «Verta provides current accounts in supported currencies across different account tiers (Tier 1, Tier 2, and Tier 3), but we do not currently offer a savings account product named "Verta Premium Plus," nor do we pay inter»
   lesson-02 run 3 C-09: {'answer_relevancy': 0.571}
      «At Verta, transfer limits are designed to help you manage larger volumes of funds securely while protecting your account against unauthorized activity. Your monthly transfer limit is determined by your account tier—in yo»
   lesson-02 run 3 C-11: {'faithfulness': 0.6}
      «When it comes to disputing a card payment made without your physical card present—commonly referred to as card-not-present fraud—Verta provides a specific timeframe under our dispute guidelines. For the reason code `frau»
   lesson-02 run 3 C-12: {'faithfulness': 0.4}
      «When raising a payment dispute, Verta adheres to standard chargeback windows established for different dispute categories to ensure consumer protection and compliance with card network rules. Each reason code has a speci»
   lesson-02 run 3 C-19: {'faithfulness': 0.0, 'answer_relevancy': 0.667}
      «Verta offers standard retail current accounts rather than dedicated savings accounts such as a "Verta Premium Plus" savings account. 

Our account structure is organized around three tiers (Tier 1, Tier 2, and Tier 3) wh»

Поріг: скільки дефектних кейсів ловить і скільки чистих зупиняє без причини:
   faithfulness       < 0.7: ловить 13/19 · хибні тривоги на clean 4/24
   faithfulness       < 0.8: ловить 15/19 · хибні тривоги на clean 8/24
   faithfulness       < 0.9: ловить 17/19 · хибні тривоги на clean 11/24
   answer relevancy   < 0.7: ловить 1/19 · хибні тривоги на clean 1/26
   answer relevancy   < 0.8: ловить 3/19 · хибні тривоги на clean 1/26
   answer relevancy   < 0.9: ловить 6/19 · хибні тривоги на clean 1/26

Вартість: формула лонгріда (кейси × (1 + метрики)) = 205 викликів; фактично 154 llm.call агента + 465 викликів судді
   агент 291,903 in / 10,110 out токенів ≈ $0.342 (прайс 1.0/5.0 за 1M) · суддя ≈ $0.185 · разом ≈ $0.528

звіт: l02-clean-lesson-02-20260930-042200.json