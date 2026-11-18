---
name: case-search
description: Finds labelled cases that resemble a new item, and shows how cases containing a phrase were labelled, from a JSONL case library (BM25 keyword search that works for Chinese and English without a word segmenter). Use it while labelling or reviewing content, to check how similar items were labelled before, to find precedents for a borderline item, to see a dataset's labelling convention for a phrase, or to pick few-shot examples - for example "find similar labelled cases", "how were ads like this labelled", "what label do reviews saying X usually get", "找相似案例", "以前类似的是怎么标的", "这个说法一般标什么". A bundled script does the search; the agent weighs the cases against the label rules.
metadata:
  version: "0.1.0"
---

# Case search

Labelling rules say what a label means; past cases show how it is actually applied. This skill searches a case library two ways:

- **Similar cases**: BM25 over the case texts, top k with their labels.
- **Phrase statistics**: every case that contains an exact phrase, and the share of them carrying each label. This is the quickest way to see a convention ("of 13 cases that say 环境一般, 12 carry Ambience#Noise").

## Inputs

A case library in JSONL: `id`, `text`, `labels` (a list; empty = no label), optionally `source` and `note`.

```json
{"id": "case-0243", "text": "Guaranteed results, every time!", "labels": ["GUARANTEE"], "source": "synthetic"}
```

## Run the script

```bash
python <this-skill-folder>/scripts/case_search.py cases.jsonl --query "the best mattress in the world" -k 5
python <this-skill-folder>/scripts/case_search.py cases.jsonl --query-file item.txt -k 8 --per-label 2 --snippet 120
python <this-skill-folder>/scripts/case_search.py cases.jsonl --query "..." --label ABSOLUTE
python <this-skill-folder>/scripts/case_search.py cases.jsonl --phrase "环境一般"
```

Python 3.9+, standard library only. `--per-label N` keeps at most N cases per label combination so one frequent label does not fill the list; `--snippet N` shows N characters around the best-matching part of long cases; `--exclude-id` keeps the item itself out of its own results; `--format json` for machine output. Exit code 0: results; 1: nothing matched; 2: bad input. Tokens: Latin words and numbers, plus single characters and character pairs for Chinese, Japanese and Korean; scores equal `rank_bm25.BM25Okapi` on the same tokens.

## Use the cases well

1. **Rules win.** A case is evidence of practice, not a rule. When cases and the rulebook disagree, follow the rules and report the disagreement: either the rule or the cases need fixing.
2. **Look for the deciding difference.** Pull cases both with and without the candidate label (`--label` and a plain search) and find the words that separate them.
3. **Weigh by count.** Phrase statistics on 3 cases is an anecdote; on 30 it is a convention. Always give the count.
4. **Know the library's source.** A library of synthetic cases shows what its generator thought the labels meant, not how annotators applied them; say which kind you searched.
5. **Never search the test set.** Cases must come from training or reference data, or the evaluation is contaminated.

## Report

The shape, with the example in `references/tutorial.md` (the ad "Reapply every 2 hours for best results"):

```markdown
The closest case (score 30.5) uses the same usage advice, "reapply every two hours for best results", and carries no label; the case that does carry ABSOLUTE uses "best" to rank the product ("the best coding bootcamp ... in the region"). This ad gives usage advice, so no ABSOLUTE; it matches the rulebook's exclusion. Searched: 600 synthetic ads.
```
