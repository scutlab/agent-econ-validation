"""Persona sampling for agent-society behavioral validation.

Dimensions are deliberately few and theory-grounded:
- age, gender: demographics
- income: low / middle / high (stakes sensitivity for dictator/endowment)
- risk_attitude: averse / neutral / seeking
- intervention_leaning: 1..5, 1 = strongly pro-government-intervention,
  5 = strongly pro-free-market. This is the gradient variable for the
  snow-shovel fairness experiment, mirroring Horton's
  socialist -> libertarian axis in a Chinese wording.
"""

import random

GENDERS = ["男", "女"]
INCOMES = ["低收入", "中等收入", "高收入"]
RISK = ["风险厌恶", "风险中性", "风险偏好"]


def sample_personas(n, seed=20261105):
    """Return n personas. intervention_leaning cycles 1..5 so that
    gradient tests are powered even at small n."""
    rng = random.Random(seed)
    personas = []
    for i in range(n):
        personas.append({
            "id": f"P{i:04d}",
            "age": rng.randint(20, 65),
            "gender": rng.choice(GENDERS),
            "income": rng.choice(INCOMES),
            "risk_attitude": rng.choice(RISK),
            "intervention_leaning": (i % 5) + 1,
        })
    return personas


def persona_text(p):
    leaning_desc = {
        1: "非常支持政府干预市场",
        2: "比较支持政府干预市场",
        3: "在经济政策上持中立态度",
        4: "比较支持自由市场",
        5: "非常支持自由市场",
    }[p["intervention_leaning"]]
    return (f"你是一位{p['age']}岁{p['gender']}性，{p['income']}，{p['risk_attitude']}，"
            f"在经济政策上{leaning_desc}的普通人。")
