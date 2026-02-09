# Copy rules (locked in)

These rules are enforced by tests. Do not break them.

---

## Equation vs persistence

**Rule:** The equation is **S = Satisfaction**. Satisfaction is **Value Delivered ÷ Cost Extracted**. Persistence is a *behavioral outcome* of satisfaction — it is **not** the equation itself.

**Correct:**
- "S = Satisfaction"
- "Value Delivered ÷ Cost Extracted = Satisfaction"
- "Satisfaction enables persistence over time, but persistence is not the equation itself."

**Forbidden:**
- "S = Satisfaction (enables persistence)" — do not use "(enables persistence)" as the definition or label of S.
- Any wording that makes persistence part of the equation definition.

**Rationale:** The framework separates (1) the equation S = (M×E×F)/(B×K×C) and its meaning (Satisfaction = value ÷ cost) from (2) the consequence (satisfaction enables persistence). Conflating them in UI or copy is incorrect.

---

*Enforced by: `test_copy_consistency.py` (must pass in CI/local).*
