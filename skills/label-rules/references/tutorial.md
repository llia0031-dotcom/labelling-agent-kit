# Tutorial: label one borderline ad with the rulebook

Files: the repository's ad-policy rulebook `tasks/ad_policy/rules.json` (9 labels, Chinese and English). The item:

> Lumeo Sunscreen SPF 50. Reapply every 2 hours for best results.

This ad is a look-alike: "best" sounds like an absolute claim. All outputs below are copied from real runs.

## 1. Which labels exist for this item

The ad is English, and two labels exist only for Chinese ads, so restrict the rulebook to English:

```bash
python scripts/label_rules.py tasks/ad_policy/rules.json list --scope en --lang en
```

```text
- ABSOLUTE (Absolute claim): An absolute or superlative claim about the promoted product or service: best, No. 1, ...
- MEDICAL (Medical claim): ...
...
- BEFORE_AFTER (Before-and-after comparison): ...
```

## 2. Candidates from keywords

```bash
python scripts/label_rules.py tasks/ad_policy/rules.json match --text "Lumeo Sunscreen SPF 50. Reapply every 2 hours for best results." --scope en
```

```text
- ABSOLUTE: best
```

A keyword hit is a candidate, never a decision.

## 3. Read the rule, "does not apply" first

```bash
python scripts/label_rules.py tasks/ad_policy/rules.json show ABSOLUTE --lang en --scope en
```

```text
Does not apply when:
- Usage advice such as "for best results, reapply every 2 hours".
- A company's aim, attitude or motto that is not a claim about the product: ...
```

The first exclusion matches the ad's own words, so ABSOLUTE does not apply. Evidence for the decision: "Reapply every 2 hours for best results." (usage advice).

## 4. When two labels compete

```bash
python scripts/label_rules.py tasks/ad_policy/rules.json between ABSOLUTE GUARANTEE --lang en
```

```text
## ABSOLUTE and GUARANTEE

- (ABSOLUTE) "Guaranteed" or "100% pass rate" is a promised outcome (GUARANTEE). ABSOLUTE is only for superlatives and rank. Give both when both are present.
- Both may be given to one item.
```

## 5. Check the rulebook after an edit

```bash
python scripts/label_rules.py tasks/ad_policy/rules.json lint
```

```text
9 labels, 0 problem(s).
```

In this repository the agent's `get_label_rules` and `compare_labels` tools call these same functions (`lak/task.py`), so a person and the agent read identical rule text.
