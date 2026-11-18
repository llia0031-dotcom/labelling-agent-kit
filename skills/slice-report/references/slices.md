# How slices are compared

- **Slice membership**: the value of the field in the gold file. A list value puts the item in one slice per element; a missing field puts it in `(missing)`.
- **Length buckets** (`--length FIELD --buckets K`): cut points at the K-quantiles of the text lengths, so buckets hold about equal numbers of items. Bounds are inclusive and shown in characters.
- **By label** (`--by-label`): one slice per gold label (items without gold labels form `(no gold label)`). Within such a slice every item has the label, so its F1 mostly reflects recall of that label plus errors on the item's other labels.
- **Micro F1 of a slice**: the F1 formula on TP, FP and FN summed over all labels and items of the slice. It equals `label-metrics` run on the slice's items (tested).
- **Against the rest**: slice micro F1 minus the micro F1 of all other items. The interval resamples the slice and the rest separately (1,000 resamples each, fixed seed) and takes the 2.5th and 97.5th percentiles of the difference.
- **Verdict**: `worse` if the whole interval is below 0, `better` if above 0, `no measured difference` otherwise, `too few` when the slice has fewer than `--min-n` items (default 20).
- **Miss / false alarm**: shown only when the slice has both items with and without gold labels.

Slices that are defined by the gold labels (number of labels, a gold label) describe difficulty, not a deployment segment: use them to explain errors, and slices of the input (language, source, length) to decide where a model is safe to use.

Checking many slices finds some "worse" ones by chance. Treat a verdict on one slice among dozens as a lead to examine, not a finding, unless it was named before the run.
