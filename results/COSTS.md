# Model costs

Summed from the token usage stored with every answer (claude-haiku-5-5 list price; Message Batches answers at half price).

| Run | Purpose | Answers | Via batch | Copied from another run, not charged again | Input tokens | Output tokens | USD |
|---|---|---|---|---|---|---|---|
| dev1 | development on dev, first agent design | 1,126 | 1,126 | 0 | 4,545,338 | 609,912 | 0.2365 |
| dev2 | development on dev, retrieval step and tuning | 1,946 | 1,946 | 0 | 9,996,561 | 1,290,781 | 0.5571 |
| main | preregistered arms on test A | 3,826 | 3,823 | 0 | 20,843,625 | 3,106,059 | 1.2642 |
| main/rca | root-cause classification, two passes | 338 | 330 | 0 | 845,332 | 224,972 | 0.1000 |
| main/rca (translation) | Chinese text of the root-cause reasons, for the Chinese viewer | 34 | 0 | 0 | 86,911 | 72,026 | 0.0447 |
| revision | v1 and v2 on test B, v2 on test A | 3,026 | 3,017 | 1,035 | 19,894,353 | 2,446,122 | 1.1629 |
| smoke | first check of the flow on dev (direct calls) | 50 | 0 | 0 | 197,671 | 30,381 | 0.0302 |
| synth-asap | 700 synthetic reviews for the case-library comparison | 700 | 698 | 0 | 3,255,350 | 857,302 | 0.2369 |
| **total** | | 11,046 | 10,940 | 1,035 | | | **3.6325** |
