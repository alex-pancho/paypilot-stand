docker compose run --rm eval --runs 3 --baseline-runs 2 --dry-run
[+]  1/1te 1/1
 ✔ Network paypilot-l02-eval_default Created                                          0.3s 
Container paypilot-l02-eval-eval-run-ac15440ae0b2 Creating 
Container paypilot-l02-eval-eval-run-ac15440ae0b2 Created 
id    check     metrics                                     expected
C-01  regex     faithfulness,answer_relevancy               swift_flat_eur = 15.00, swift_pct = 0.30
C-02  —         answer_relevancy                            —
C-03  no_offer  faithfulness,answer_relevancy,hallucination eligible = False
C-04  percent   faithfulness,answer_relevancy,hallucination spread_pct = 0.90
C-05  number    faithfulness,answer_relevancy               final_amount = 6,463.04
C-06  number    faithfulness,answer_relevancy               source = stand DB, accounts ACC-1003
C-07  number    faithfulness,answer_relevancy               final_amount = 2,154.35
C-08  number    faithfulness,answer_relevancy,hallucination final_amount = 2,154.35
C-09  number    faithfulness,answer_relevancy               monthly_remaining_eur = 964,666.00
C-10  no_offer  faithfulness,answer_relevancy               eligible = False
C-11  days      faithfulness,answer_relevancy               window_days = 120
C-12  days      faithfulness,answer_relevancy               window_days = 60
C-19  not_regex faithfulness,answer_relevancy               product_exists = False

13 кейсів × (clean ×2 + lesson-02 ×3) = 65 звернень до агента (кожне — зазвичай 2–3 llm.call)
формула лонгріда: 205 викликів
DeepEval насправді: ≈465 викликів судді + ≈130–195 llm.call агент

== clean: defects - · prompt base.v1 · provider gemini · judge -
   run 1 C-01  domain=ok   
   run 1 C-02  domain=-    
   run 1 C-03  domain=ok   
   run 1 C-04  domain=ok   
   run 1 C-05  domain=ok   
   run 1 C-06  domain=ok   
   run 1 C-07  domain=ok   
   run 1 C-08  domain=ok   
   run 1 C-09  domain=ok   
   run 1 C-10  domain=ok   
   run 1 C-11  domain=ok   
   run 1 C-12  domain=ok   
   run 1 C-19  domain=ok   
   run 2 C-01  domain=ok   
   run 2 C-02  domain=-    
   run 2 C-03  domain=ok   
   run 2 C-04  domain=ok   
   run 2 C-05  domain=ok   
   run 2 C-06  domain=ok   
   run 2 C-07  domain=ok   
   run 2 C-08  domain=ok   
   run 2 C-09  domain=ok   
   run 2 C-10  domain=ok   
   run 2 C-11  domain=ok   
   run 2 C-12  domain=ok   
   run 2 C-19  domain=ok   

== lesson-02: defects D04,D05,D16,D19,D20,D25 · prompt base.v1+D04+D05+D25 · provider gemini · judge -
   run 1 C-01  domain=FAIL 
   run 1 C-02  domain=-    
   run 1 C-03  domain=ok   
   run 1 C-04  domain=FAIL 
   run 1 C-05  domain=FAIL 
   run 1 C-06  domain=ok   
   run 1 C-07  domain=FAIL 
   run 1 C-08  domain=FAIL 
   run 1 C-09  domain=ok   
   run 1 C-10  domain=FAIL 
   run 1 C-11  domain=ok   
   run 1 C-12  domain=FAIL 
   run 1 C-19  domain=ok   
   run 2 C-01  domain=FAIL 
   run 2 C-02  domain=-    
   run 2 C-03  domain=FAIL 
   run 2 C-04  domain=FAIL 
   run 2 C-05  domain=FAIL 
   run 2 C-06  domain=ok   
   run 2 C-07  domain=FAIL 
   run 2 C-08  domain=FAIL 
   run 2 C-09  domain=ok   
   run 2 C-10  domain=FAIL 
   run 2 C-11  domain=ok   
   run 2 C-12  domain=ok   
   run 2 C-19  domain=ok   
   run 3 C-01  domain=FAIL 
   run 3 C-02  domain=-    
   run 3 C-03  domain=ok   
   run 3 C-04  domain=FAIL 
   run 3 C-05  domain=FAIL 
   run 3 C-06  domain=ok   
   run 3 C-07  domain=FAIL 
   run 3 C-08  domain=FAIL 
   run 3 C-09  domain=ok   
   run 3 C-10  domain=FAIL 
   run 3 C-11  domain=ok   
   run 3 C-12  domain=FAIL 
   run 3 C-19  domain=ok   

Метрика                clean                 lesson-02             Дельта
faithfulness           —                     —                     
answer relevancy       —                     —                     
hallucination rate ↓   —                     —                     
доменна коректність    1.00 (1.00–1.00)      0.42 (0.42–0.42)      -0.58

Зелена метрика на хибному висновку (faithfulness ≥ 0.85, домен ✗):
   немає

Кандидати у false positive (LLM-метрика < 0.7, домен ✓ або без домену) — перевір очима:
   немає

Поріг: скільки дефектних кейсів ловить і скільки чистих зупиняє без причини:
   немає

Вартість: формула лонгріда (кейси × (1 + метрики)) = 65 викликів; фактично 155 llm.call агента + 0 викликів судді
   агент 292,815 in / 10,139 out токенів ≈ $0.344 (прайс 1.0/5.0 за 1M) · суддя ≈ $0.000 · разом ≈ $0.344

звіт: l02-clean-lesson-02-20260930-034841.json