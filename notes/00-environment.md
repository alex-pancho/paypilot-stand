```yaml
ОС: Windows 10 
версія Docker: Docker version 29.1.3, build f52814d
версія Python: Python 3.10.12
хеш коміту стенду: ae10e9cc3fe92f004f797375949985c89afed799

провайдер, модель, температура: gemini, Gemini 3.5 Flash Lite, 0
скільки часу фактично зайняло розгортання: до 30 хв чи менше
кроки README, які не спрацювали дослівно, і що допомогло: 
    в кроках README є лише claude.com і відсутні Антропік та Gemini
вивід діагностики:
    curl -X GET localhost:8000/health на профілях  — активні дефекти кожного профілю
    clean:
        {"status":"ok","profile":"clean","startup_profile":"clean","active_defects":[],"provider":"gemini","otlp":true}
    lesson-01:
        {"status":"ok","profile":"lesson-01","startup_profile":"clean","active_defects":["D01","D02","D03"],"provider":"gemini","otlp":true}
    lesson-02:
        {"status":"ok","profile":"lesson-02","startup_profile":"clean","active_defects":["D04","D05","D16","D19","D20","D25"],"provider":"gemini","otlp":true}
    lesson-03:
        {"status":"ok","profile":"lesson-03","startup_profile":"clean","active_defects":["D19","D20","D21","D22","D26"],"provider":"gemini","otlp":true}
    doctor:
        """
        python                                  [OK] 3.12.14
        dependency: fastapi                     [OK] 
        dependency: uvicorn                     [OK] 
        dependency: pydantic                    [OK] 
        dependency: yaml                        [OK] 
        dependency: httpx                       [OK] 
        dependency: pytest                      [OK] 
        llm provider                            [OK] gemini
        gemini api reachable                    [OK] HTTP 200
        phoenix (trace UI)                      [OK] http://phoenix:6006
        artefact: prompts/base.v1.md            [OK] 
        artefact: specs/requirements/US-01.md   [OK] 
        clock override                          [OK] 2026-09-15T10:00:00Z
        profile/defects config                  [OK] PROFILE=clean DEFECTS=-
        """
```

    