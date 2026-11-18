# The multi-label confusion matrix (MLCM)

Source: M. Heydarian, T. E. Doyle and R. Samavi, "MLCM: Multi-Label Confusion Matrix", IEEE Access 10 (2022) 19083–19095, doi:10.1109/ACCESS.2022.3151048. The script is a fresh implementation of the published rules; the `mlcm` package on PyPI is not used (its repository licence is CC BY-NC-ND).

Matrix size (L + 1) × (L + 1) for L labels. Rows: gold labels plus NTL (no true label). Columns: predicted labels plus NPL (no predicted label).

| Case (T = gold set, P = predicted set) | Counts added |
|---|---|
| label in T ∩ P | 1 on its diagonal cell |
| T empty, P empty | 1 at (NTL, NPL) |
| T empty, P not empty | 1 at (NTL, p) for each p in P |
| T − P not empty, P − T empty (only misses) | 1 at (t, NPL) for each missed t |
| T − P empty, P − T not empty (only additions) | 1 at (t, p) for every t in T and every added p |
| both not empty (a swap) | 1 at (t, p) for every missed t and every added p |

Worked example, labels A, B, C:

| Item | Gold | Predicted | Counts |
|---|---|---|---|
| 1 | A, B | A, B | (A,A), (B,B) |
| 2 | – | C | (NTL,C) |
| 3 | A, B | A | (A,A), (B,NPL) |
| 4 | A | A, C | (A,A), (A,C) |
| 5 | A, B | A, C | (A,A), (B,C) |

Properties checked in the tests: with one label per item the matrix equals scikit-learn's `confusion_matrix`; each diagonal cell equals the label's true positives from `label-metrics`; the item kinds (exact, under-labelled, over-labelled, swapped) add up to the number of items.

Rows do not sum to a label's gold count when items have several labels, because one item can add several counts. Use `label-metrics` for rates and this matrix for the direction of errors.
