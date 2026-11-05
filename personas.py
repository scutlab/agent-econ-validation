"""Persona sampling for agent-society behavioral validation.

Dimensions are deliberately few and theory-grounded:
- age, gender: demographics
- income: low / middle / high (stakes sensitivity for dictator/endowment)
- risk_attitude: averse / neutral / seeking
- intervention_leaning: 1..5, 1 = strongly pro-government-intervention,
  5 = strongly pro-free-market. This is the gradient variable for the
  snow-shovel fairness experiment, mirroring Horton's
  socialist -> libertarian axis in a Chinese wording.
- math_ability: arm-level treatment (not sampled per persona), appended
  by persona_text(p, math=...) for the Oprea mirror test: "strong" /
  "weak", mirroring Horton's "very bad at math" persona.
"""

import random

GENDERS = ["男", "女"]
INCOMES = ["低收入", "中等收入", "高收入"]
RISK = ["风险厌恶", "风险中性", "风险偏好"]
MATH_ABILITY = {
    "strong": "你的数学能力很强，擅长心算和概率计算。",
    "weak": "你的数学能力很差，算数经常出错，看到复杂的数字就头疼。",
}


def sample_personas(n, seed=20261105):
    """Return n personas. intervention_leaning cycles 1..5 so that
    gradient tests are powered even at small n. firm_size cycles
    large/medium/small (used only by the settle experiment); it is
    assigned by index, not by RNG, so the other fields are unchanged
    for a given seed."""
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
            "firm_size": ("large", "medium", "small")[i % 3],
        })
    return personas


def persona_text(p, math=None):
    leaning_desc = {
        1: "非常支持政府干预市场",
        2: "比较支持政府干预市场",
        3: "在经济政策上持中立态度",
        4: "比较支持自由市场",
        5: "非常支持自由市场",
    }[p["intervention_leaning"]]
    text = (f"你是一位{p['age']}岁{p['gender']}性，{p['income']}，{p['risk_attitude']}，"
            f"在经济政策上{leaning_desc}的普通人。")
    if math in MATH_ABILITY:
        text += MATH_ABILITY[math]
    return text
