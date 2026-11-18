# Root causes: asap / test_a / agent-cases-check

406 wrong label decisions on 165 items; the two independent passes agree on 257 of 406. 194 of the decisions were also wrong in every other arm. Cost $0.0970.

| Cause | All | False positives | Misses |
|---|---|---|---|
| prompt_defect | 61 | 10 | 51 |
| model_capability | 20 | 15 | 5 |
| rule_conflict | 18 | 3 | 15 |
| sample_distribution | 0 | 0 | 0 |
| label_ambiguity | 158 | 72 | 86 |
| split | 149 | 62 | 87 |

## Split decisions: the two causes given

| First | Second | Decisions |
|---|---|---|
| label_ambiguity | rule_conflict | 42 |
| label_ambiguity | prompt_defect | 38 |
| label_ambiguity | model_capability | 21 |
| prompt_defect | rule_conflict | 19 |
| model_capability | prompt_defect | 13 |
| model_capability | rule_conflict | 9 |
| label_ambiguity | sample_distribution | 3 |
| None | label_ambiguity | 2 |
| rule_conflict | sample_distribution | 1 |
| None | prompt_defect | 1 |

## By label

| Label | Decisions | prompt_defect | model_capability | rule_conflict | sample_distribution | label_ambiguity | split |
|---|---|---|---|---|---|---|---|
| Price#Level | 46 | 5 | 0 | 7 | 0 | 12 | 22 |
| Food#Portion | 42 | 1 | 5 | 0 | 0 | 18 | 18 |
| Food#Appearance | 35 | 2 | 2 | 0 | 0 | 16 | 15 |
| Price#Cost_effective | 33 | 0 | 2 | 1 | 0 | 18 | 12 |
| Price#Discount | 31 | 9 | 1 | 3 | 0 | 8 | 10 |
| Location#Downtown | 27 | 9 | 0 | 2 | 0 | 7 | 9 |
| Food#Recommend | 24 | 0 | 1 | 1 | 0 | 8 | 14 |
| Ambience#Space | 23 | 5 | 3 | 1 | 0 | 10 | 4 |
| Service#Hospitality | 22 | 2 | 0 | 0 | 0 | 12 | 8 |
| Ambience#Sanitary | 21 | 5 | 0 | 1 | 0 | 10 | 5 |
| Ambience#Decoration | 21 | 4 | 1 | 0 | 0 | 10 | 6 |
| Ambience#Noise | 19 | 7 | 0 | 0 | 0 | 6 | 6 |
| Location#Transportation | 17 | 3 | 1 | 0 | 0 | 6 | 7 |
| Location#Easy_to_find | 16 | 7 | 3 | 1 | 0 | 3 | 2 |
| Service#Queue | 12 | 1 | 0 | 0 | 0 | 5 | 6 |
| Service#Timely | 12 | 0 | 1 | 0 | 0 | 7 | 4 |
| Service#Parking | 3 | 1 | 0 | 0 | 0 | 2 | 0 |
| Food#Taste | 2 | 0 | 0 | 1 | 0 | 0 | 1 |

## Suggested fixes (first pass), grouped by cause

### prompt_defect (61)
- Service#Queue (miss, asap-test-10324): Add a flow step requiring the agent to check every label's Applies-when list against the whole review, including negated or hypothetical mentions such as 不用排队 and 去得早没排队, before finalising.
- Ambience#Noise (miss, asap-test-10494): Add a prompt step: whenever a review evaluates 环境 (any positive or negative environment judgement), open the Ambience boundary section and check whether it is general before deciding on Decoration, Noise, Space and Sanitary.
- Ambience#Sanitary (miss, asap-test-10494): Same flow fix: require the agent to consult the Ambience boundary rule for every 环境 evaluation before finalising the four environment labels.
- Price#Discount (miss, asap-test-13823): Make the agent scan every label's Applies-when keywords (券, 团购, 优惠) against the text as a required step before finalising, not only the labels it considers likely.
- Location#Easy_to_find (miss, asap-test-15065): Add a flow step that checks every sentence describing the store's position or landmarks against the Easy_to_find rule, and add a few cases where a landmark-based location description is labelled easy to find.
- Location#Downtown (miss, asap-test-15138): Add a flow step that scans for venue-type keywords (商场, 广场, 百货, 步行街, 购物中心) and reads the matching location rule before deciding, and state in the prompt that a mere mention of such a place counts for Downtown without any evaluative wording.
- Location#Downtown (miss, asap-test-15152): Flow edit: for every place or landmark named in the review, open the location rules and check for mall, plaza or commercial-district wording before concluding the item has no location labels.
- Location#Transportation (miss, asap-test-16675): Prompt edit: make the flow check every Location sub-label (Downtown, Transportation, Easy_to_find) against its rule whenever a location sentence appears, not only the first matching one.
- Location#Downtown (miss, asap-test-16832): Add a flow step that checks each review for named malls, plazas and commercial complexes and applies the Location#Downtown rule whenever one is mentioned as the shop's location.
- Price#Discount (miss, asap-test-16832): Add a flow step that scans for trigger words (券, 团购, 优惠, 打折, 活动, 赠送) and checks the matching rule before deciding that a discount mention is only a fact.
- Price#Level (miss, asap-test-16832): Add a flow step that reads the Price#Level rule whenever a review gives a concrete amount of money, and add a case showing that a specific amount with a positive evaluation such as 划算 counts as price level.
- Service#Hospitality (miss, asap-test-17281): Prompt edit: before finalising, check each person-type word (服务员, 老板, 服务) against Service#Hospitality and label any evaluation of the staff or owner, even when the complaint is about operations.
- Ambience#Noise (miss, asap-test-19183): Add a flow step: when a review praises '环境' in general terms (including 环境考究), check the general-environment boundary rule and tag Decoration, Noise, Space and Sanitary together.
- Ambience#Sanitary (miss, asap-test-19183): Tell the self-check not to remove a label that a general-environment rule requires, and state that a general '环境' praise keeps all four labels even when a cleanliness word appears in a food sentence.
- Ambience#Space (miss, asap-test-19183): Add the general-environment four-label check to the flow before the per-label checks so Space is considered whenever '环境' is praised in general terms.
- Location#Downtown (miss, asap-test-22827): Prompt edit: for every Location item, read the Downtown rule and check for shopping-centre words such as 商厦, 商场, 广场 and 百货. Add a few cases where 商厦 is labelled Downtown.
- Price#Discount (miss, asap-test-24145): Prompt edit: before rejecting a label, check each rule's trigger list (优惠, 活动, 赠送, 券) against the review text. Rule edit: add 积分兑换 and 积分加钱购 as examples under Applies when, with a case like this one.
- Ambience#Noise (false positive, asap-test-25743): Add a prompt step: before labelling Noise from a generic 环境 remark, verify the review mentions noise, quietness or crowd sound; make the self-check unable to add labels without a quoted sound-related cue.
- Location#Easy_to_find (miss, asap-test-28503): Add a prompt edit to the self-check: do not drop a rule-covered label just because the evidence is indirect; add a rule example that landmark-based directions ("离X不远", "在X斜对面", "走错进了隔壁店") count as Easy_to_find.
- Ambience#Decoration (miss, asap-test-29012): Add a prompt step: when a review gives a general verdict on 环境 (环境很好/不好/一般), read the Ambience boundary notes and tag all four environment labels, with polarity from that verdict, even if a specific sub-aspect is also named.
- Ambience#Space (miss, asap-test-29012): Same prompt edit: force the agent to check the general-环境 boundary rule for all four environment labels before finalising, and add a self-check that a general 环境 verdict must not be pruned to a single sub-aspect.
- Ambience#Noise (miss, asap-test-30862): Prompt edit: in the self-check, do not remove labels that the boundary section mandates for generic 环境 ratings; add a worked example of '环境综合X星' tagging all four environment labels.
- Ambience#Space (miss, asap-test-30862): Prompt edit: state in the self-check that generic environment wording triggers the four-label rule and must not be dropped for lack of specific detail; add the same worked example.
- Location#Downtown (false positive, asap-test-30978): Add a prompt edit to the self-check: only add a Location label when the review judges the location itself (where it is, how central or convenient); add a case-library entry where a mall name appears only in a popularity or reputation remark and the gold is no Location label.
- Location#Downtown (miss, asap-test-32060): Add a flow step that checks the Location#Downtown trigger list (商场, 广场, 万象城-style names) whenever a mall or plaza is named, and state explicitly that no evaluation is needed.

### model_capability (20)
- Location#Transportation (miss, asap-test-15065): Add a rule note that naming a bus stop or metro station as the access point counts as Transportation even when it is also used to locate the store, and clarify that the '附近' exclusion covers only non-transport landmarks such as malls or shops.
- Food#Portion (false positive, asap-test-17261): Add a case-library entry showing that "某菜很大" describing an individual ingredient's size (虾很大, 块很大) is not Food#Portion unless it refers to how much is served, and tighten the rule to require quantity wording such as 分量, 量, 够吃.
- Price#Discount (miss, asap-test-26629): Add an explicit cue to the Price#Discount rule and prompt: winning a lottery, free meal, or 霸王餐 counts as a discount-type aspect even without a stated price; add several lottery/抽中/免费试吃 cases to the library so the agent checks for them.
- Price#Cost_effective (false positive, asap-test-30578): Add a rule edit: phrases pairing a price tier with quality (e.g. '这个价位这个水平') count as Price#Level only unless 性价比/值/划算/不值 is said; add this sentence as a contrast case.
- Food#Portion (false positive, asap-test-30862): Prompt edit: add a note that 饱/撑 describes the diner's state and only counts as Food#Portion when it is tied to dish quantity (e.g. 菜量大, 分量足).
- Food#Appearance (false positive, asap-test-31826): Add a rule note: 摆得不好夹、上菜晃荡等描述实用性或上菜方式的内容不算外观，除非评价摆盘好看或难看；add a few cases where 摆盘 complaints about usability are labelled Service or none.
- Location#Easy_to_find (miss, asap-test-34808): Add a prompt note: when the review praises the shop's location (地理位置优越/位置很好) without mentioning seats, label Location#Easy_to_find, and add a contrast case showing 没位置 (seats) does not count.
- Location#Easy_to_find (false positive, asap-test-35248): Prompt edit: add that descriptions of missing signs or names count for Easy_to_find only when the review says the place is hard or easy to find.
- Service#Timely (false positive, asap-test-3538): Add a boundary example to Service#Timely stating that 添菜/加火 responsiveness counts as 上菜速度 only when the reviewer explicitly comments on speed, and add 2-3 such cases to the library to settle the convention.
- Price#Cost_effective (false positive, asap-test-37219): Add a rule note that conditional ordering advice or 'worth it if you go in a group' without comparing price to quality does not apply, plus a case example.
- Food#Appearance (false positive, asap-test-41254): Add a prompt check: when a look-related phrase is paired with taste or texture comments, label appearance only if the reviewer judges the visual form (shape, colour, presentation), and add a few cases of 看着+形状 versus 看着+口感 to the case library.
- Food#Portion (miss, asap-test-43711): Add 料足、料多、料很足 to the Food#Portion applies-when list with a note that generous ingredient quantity counts as portion.
- Ambience#Space (false positive, asap-test-4376): Add a rule note that counting tables or seats without a size judgment (e.g. '有近二十张桌子' alone) does not apply; add a few such neutral-count cases to the library.
- Location#Easy_to_find (false positive, asap-test-44229): Prompt edit: when a review only gives directions from a stop or landmark, label Location#Transportation only, and add Easy_to_find only if the reviewer comments that the shop is easy or hard to spot.
- Food#Recommend (false positive, asap-test-44665): Add a prompt note that 好评/差评 on a single dish is taste-level evaluation unless the reviewer states recommend or not recommend, and add a few such cases to the library.
- Ambience#Decoration (false positive, asap-test-6972): Add a boundary note under Ambience#Decoration that facade size and inconspicuousness belong to Location#Easy_to_find, and add a few cases of 门面小/不起眼 labelled only as Easy_to_find.
- Food#Portion (false positive, asap-test-7134): Add a rule note that weights or quantities bought from a market or shop-side scale are not Food#Portion unless the dish's serving size is judged.
- Food#Portion (miss, asap-test-7879): Add a prompt example or library cases where praise of how much food was ordered or eaten ("吃到最多", "阔气", "量大") counts as Food#Portion, and clarify that the exclusion applies only when no quantity judgement is made.
- Ambience#Space (false positive, asap-test-8265): Add a case-library example of an incidental size remark ('这个店也不算小') labelled as not applicable when it is a throwaway aside rather than a stated evaluation, and clarify in the rule that the aspect must be judged, not just mentioned in passing.
- Ambience#Space (false positive, asap-test-8837): Add a contrasting example to the Space rule, such as '坐在门口的位置 does not trigger Space', so the model separates seating location from space size.

### rule_conflict (18)
- Ambience#Space (miss, asap-test-10494): Clarify the boundary text: an evaluation that names only a style or theme (正宗日式, 高大上, 有格调) without naming a specific dimension counts as general and tags all four environment labels; add 3-5 such cases to the library.
- Price#Level (miss, asap-test-11716): Add a rule edit saying that choosing a dish explicitly as the cheapest option ("最便宜的", "选了便宜的") counts as a price-level judgment, and add a few cases of this wording with gold labels.
- Location#Easy_to_find (miss, asap-test-17281): Add a rule note that mentions of choosing a restaurant because it is nearby (就近原则) or sign/location descriptions count as Easy_to_find, and add cases with 就近/招牌 wording.
- Food#Taste (miss, asap-test-19183): Add an explicit rule and cases: when food is praised only for appearance or refinement with no taste word, tag Food#Taste if the dataset convention is to tag it, and give examples.
- Price#Discount (miss, asap-test-21314): Add an explicit example to the Price#Discount rule: 'a free tasting (免费试吃/霸王餐) mentioned as the reviewer's reason for the visit counts as Price#Discount with positive polarity', and add a few similar tasting-event cases to the case library.
- Price#Level (miss, asap-test-23777): Rule edit: state that a concrete spend figure followed by a complaint about the bill or value counts as a negative price-level judgement, and add cases of this implicit pattern to the case library.
- Price#Discount (miss, asap-test-26640): Prompt edit: add an explicit flow step that checks each item for the listed trigger words (霸王餐, 免费试吃, 团购, 优惠, 券, 赠送) before finalising, and state that 免费试吃 counts as Price#Discount even when it is only described.
- Ambience#Sanitary (miss, asap-test-27281): Add a rule edit or case: a hair, insect or foreign object found in a dish counts as Ambience#Sanitary negative when the review frames it as unhygienic, and add several such cases to the library.
- Location#Downtown (miss, asap-test-30578): Add 商业街 and 商业区 to the Location#Downtown applies-when list, with an example such as '在望京商业街' labelled as Downtown.
- Price#Cost_effective (false positive, asap-test-32812): Add a rule example: '价格贵我能接受' with a quality complaint is a price-level judgement only; add 3-5 cases of 'X贵但能接受' labelled Price#Level only to the case library.
- Price#Level (miss, asap-test-3538): Edit the Price#Level rule to state that a price mentioned in a crowded/popular context (e.g. 火爆 with a per-jin price) is labelled neutral, or add cases where a bare price stated alongside a value remark is tagged; add more such cases so the convention is explicit.
- Price#Level (miss, asap-test-40215): Edit Price#Level's Applies list to include 超值 and 划算 as price-level signals when the reviewer judges the price as low relative to the product, and state in the Cost_effective boundary that such words tag both labels.
- Price#Level (miss, asap-test-40239): Rule edit: add 划算 to the Price#Level trigger list alongside 实惠, with two or three worked cases showing when it is tagged alone versus with Cost_effective.
- Price#Discount (miss, asap-test-41893): Add an explicit rule: a bare mention of 团购/优惠券 as the reason for the visit counts as Discount, or state that an evaluation of the offer is required, and add cases of each kind to settle it.
- Price#Level (false positive, asap-test-42257): Add a boundary note: an explicit cheap/expensive judgment about a dish or meal (including comparisons such as 比早点还便宜) counts as Price#Level even when a specific price is quoted; add 3 to 5 such cases
- Price#Level (miss, asap-test-44838): Add an explicit rule example: '才10元''这么便宜' or a sum paired with 'only/才' counts as a price-level evaluation, and add cases of that wording.
- Location#Downtown (miss, asap-test-44979): Add a rule edit clarifying that naming a shopping mall as the restaurant's location counts for Location#Downtown even when a floor number is also given.
- Food#Recommend (false positive, asap-test-7879): Add a rule edit: a recommendation of the restaurant overall (e.g. "这家店推荐", "喜欢鲁菜可以去试试") does not trigger Food#Recommend; add a few such cases to the library as negatives.

### label_ambiguity (158)
- Service#Queue (false positive, asap-test-10181): Add a rule note: waiting with no specified object after walk-in without reservation counts as Queue when it is about getting a seat, and add a few such cases of 'no reservation, had to wait' labelled Queue to show the convention.
- Food#Appearance (miss, asap-test-10181): none: document as ambiguous, or add a rule clarifying that cut shape and presentation of sashimi count as Appearance only when the reviewer explicitly praises the look.
- Food#Portion (miss, asap-test-10181): none: document as ambiguous; clarify in the Portion rule that 'optional / can skip' about a dish is not a portion judgement unless quantity is mentioned, and review the gold for this item.
- Ambience#Space (false positive, asap-test-10294): Check the gold label for this item and add Ambience#Space; if the gold is intentionally left out, add a rule note that a bare remark on seat count is not labelled when it sits inside a list of other aspects.
- Service#Timely (miss, asap-test-10324): Add a rule edit and cases: a stated dish wait time with no evaluative word counts as neutral Service#Timely, or document this case as ambiguous and do not force a label.
- Location#Transportation (miss, asap-test-1119): Add a rule note: a transit stop named as a route landmark ('X路公交车站旁边') counts as Transportation only when accessibility is judged; otherwise treat it as Easy_to_find, and add a few such landmark-only cases to the library with explicit labels.
- Food#Appearance (miss, asap-test-11716): none: document as ambiguous, or remove Food#Appearance from this gold item after checking whether the annotator meant the decor remark.
- Service#Hospitality (miss, asap-test-1239): none: document as ambiguous; add a boundary note that merely relaying a staff member's words about a promotion does not count as Service#Hospitality unless the reviewer evaluates the staff's attitude.
- Food#Recommend (miss, asap-test-1336): none: document as ambiguous; add a boundary case showing that a reviewer's own confirmation that a colleague's recommended dish was right ("没推荐错") is or is not a Food#Recommend, so the rule is explicit.
- Price#Cost_effective (false positive, asap-test-13435): Add a rule note clarifying that a single item praised as 很值 with a price figure counts as Cost_effective, and add several cases like this to the case library; if the gold stays as is, document as ambiguous.
- Price#Discount (false positive, asap-test-14243): none: document as ambiguous, or add a case stating that a complaint about a discount being unavailable is labelled Price#Discount.
- Service#Hospitality (miss, asap-test-14243): Clarify the Service#Hospitality rule: a neutral report of what staff said counts only if it judges their attitude or helpfulness; otherwise document the case as ambiguous.
- Food#Appearance (false positive, asap-test-14419): none: document as ambiguous, or add cases showing whether 摆盘很漂亮 is labelled Food#Appearance and state the convention explicitly in the rule.
- Ambience#Decoration (false positive, asap-test-1513): Correct the gold to add Ambience#Decoration and Ambience#Space for generic 环境 praise, and add a worked example of 就餐环境不错 to the rule so the convention is explicit.
- Ambience#Space (false positive, asap-test-1513): Correct the gold to include Ambience#Space for this review and make the generic-environment rule visible in the flow so agents read it before labelling environment aspects.
- Service#Hospitality (false positive, asap-test-1513): Correct the gold to add Service#Hospitality for this review and audit other gold items where 服务态度 or 服务员 praise was left unlabelled.
- Price#Cost_effective (false positive, asap-test-15598): Add a case-library example of 'cheap plus good taste/portion' without 性价比/划算/物超所值 wording and record the gold convention, or document as ambiguous.
- Service#Parking (false positive, asap-test-16055): Either add to the rule that a bare statement of no parking spaces is labelled as parking, or add cases showing that negative parking-absence remarks are unlabelled; confirm which convention the gold follows.
- Price#Cost_effective (false positive, asap-test-16845): none: document as ambiguous, or correct the gold to include Price#Cost_effective for 实惠 wording.
- Ambience#Noise (miss, asap-test-16845): none: document as ambiguous, and add a note that the four-label 环境 rule needs an explicit 环境 comment, or verify the gold.
- Ambience#Sanitary (miss, asap-test-16845): none: document as ambiguous, or recheck the gold against the 环境 boundary rule.
- Ambience#Space (miss, asap-test-16845): none: document as ambiguous; add a boundary example separating chair/seat quality from 就餐空间.
- Service#Parking (miss, asap-test-16845): none: correct the gold by removing Service#Parking, after checking for a data-entry mistake.
- Service#Timely (miss, asap-test-16845): none: correct the gold by removing Service#Timely, or confirm whether the waiting-for-a-table remark was meant as Service#Queue only.
- Price#Discount (miss, asap-test-17190): Document as ambiguous, or add a rule edit clarifying that any explicit coupon/group-buy mention with a service-experience judgment (e.g., coupon verification) counts as Price#Discount, and add a few such cases to the library.

