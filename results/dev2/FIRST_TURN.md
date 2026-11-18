# First model turn per arm: dev2

| Task | Arm | Items | First turn called a tool | First turn answered |
|---|---|---|---|---|
| ad_policy | agent | 87 | 70 of 87 | 17 of 87 |
| ad_policy | agent-cases | 87 | 17 of 87 | 70 of 87 |
| ad_policy | agent-cases-check | 87 | 16 of 87 | 71 of 87 |
| ad_policy | agent-cases-check-medium | 87 | 64 of 87 | 23 of 87 |
| ad_policy | prompt-rules | 87 | 0 of 87 | 87 of 87 |
| ad_policy | prompt-short | 87 | 0 of 87 | 87 of 87 |
| asap | agent | 60 | 21 of 60 | 39 of 60 |
| asap | agent-cases | 60 | 0 of 60 | 60 of 60 |
| asap | agent-cases-check | 60 | 0 of 60 | 60 of 60 |
| asap | agent-cases-check-medium | 60 | 20 of 60 | 40 of 60 |
| asap | agent-cases-synthetic | 60 | 1 of 60 | 59 of 60 |
| asap | prompt-rules | 60 | 0 of 60 | 60 of 60 |
| asap | prompt-short | 60 | 0 of 60 | 60 of 60 |

| Task | Arm | Tool | Calls (all turns) |
|---|---|---|---|
| ad_policy | agent | get_label_rules | 70 |
| ad_policy | agent-cases | get_label_rules | 19 |
| ad_policy | agent-cases | search_cases | 4 |
| ad_policy | agent-cases-check | get_label_rules | 41 |
| ad_policy | agent-cases-check | phrase_stats | 1 |
| ad_policy | agent-cases-check | search_cases | 4 |
| ad_policy | agent-cases-check-medium | compare_labels | 1 |
| ad_policy | agent-cases-check-medium | get_label_rules | 84 |
| ad_policy | agent-cases-check-medium | phrase_stats | 4 |
| ad_policy | agent-cases-check-medium | search_cases | 10 |
| asap | agent | compare_labels | 1 |
| asap | agent | get_label_rules | 21 |
| asap | agent-cases-check | get_label_rules | 19 |
| asap | agent-cases-check-medium | get_label_rules | 43 |
| asap | agent-cases-synthetic | get_label_rules | 1 |
