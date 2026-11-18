# Definitions used by label_metrics.py

For one label: TP = items where gold and prediction both have it, FP = prediction has it and gold does not, FN = gold has it and prediction does not.

| Measure | Formula | Interval |
|---|---|---|
| Precision | TP / (TP + FP) | Wilson score interval, 95% |
| Recall | TP / (TP + FN) | Wilson score interval, 95% |
| F1 | 2·TP / (2·TP + FP + FN) | percentile bootstrap over items, 2,000 resamples, fixed seed |
| Micro F1 | the F1 formula on TP, FP, FN summed over labels | bootstrap |
| Macro F1 | mean of the per-label F1 over the labels present in the gold set | bootstrap |
| Exact match | items whose predicted set equals the gold set / items | Wilson |
| Hamming loss | (FP + FN summed over labels) / (items × labels) | – |
| Miss rate | items with gold labels but an empty prediction / items with gold labels | Wilson |
| False-alarm rate | items without gold labels but a non-empty prediction / items without gold labels | Wilson |

- Macro F1 averages over the labels present in the gold set, so two runs on the same items are averaged over the same labels. A label that is predicted but absent from the gold set has F1 0, appears in the table and counts in micro F1, but not in macro F1. Precision is undefined (shown as –) when a label is never predicted.
- The bootstrap resamples whole items, so labels of one item stay together. An interval is not reported when the measure is undefined in more than 10% of resamples.
- **Paired comparison** (`--compare`): both runs are scored on the same resampled items in each of 2,000 resamples; the interval is that of B − A. The exact McNemar p-value is a two-sided binomial test on the items exactly right in only one of the two runs.
- Numbers are checked against scikit-learn (`precision_recall_fscore_support`, `multilabel_confusion_matrix`, `accuracy_score`, `hamming_loss`), statsmodels (`proportion_confint(method="wilson")`, `mcnemar(exact=True)`) and `numpy.percentile` in the repository's tests.

Why intervals: with 200 items, a recall of 80% on a label with 20 gold items has a 95% interval of about 58–92%. A difference of a few points between two prompts is usually inside the noise; the paired bootstrap says whether it is.
