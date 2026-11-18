// Results viewer: renders window.LAK (viewer/data.js, built by tools/report_data.py from the result files).
// One page per language; the language comes from <html lang>.
const L = document.documentElement.lang.startsWith('zh') ? 'zh' : 'en'
const D = window.LAK
const T = {
  zh: {
    tasks: '标注任务', arms: '对照实验', monitor: '每个标签', confusion: '混淆矩阵', slices: '切片', failures: '失败样本', revision: '改版前后',
    armsLead: (n) => `同一批 ${n} 条样本，每种做法各跑一次。点是微平均 F1，横条是 95% 区间。`,
    arm: '做法', micro: '微平均 F1', macro: '宏平均 F1', exact: '完全对', miss: '漏判', fa: '误判', cost: '每千条费用', calls: '每条调用',
    missFull: '有违规却一个标签都没给', faFull: '合规却给了标签', usd: '美元',
    monitorLead: '精确率低说明这个标签给得太松，召回率低说明漏得多。漏判、误判是条数；低于 60% 的比率和对应的条数标红。',
    pickArm: '看哪种做法', label: '标签', support: '标准里有', precision: '精确率', recall: '召回率', f1: 'F1', fn: '漏判', fp: '误判',
    confLead: '行是标准标签，列是给出的标签。对角线是标对的；最后一行是“标准里没有却给了”，最后一列是“标准里有却没给”。',
    cmDiag: '标对', cmOff: '标错', noGold: '（标准里没有）', noPred: '（没有给）',
    kinds: (k) => `完全对 ${k.exact} 条，少标 ${k['under-labelled']} 条，多标 ${k['over-labelled']} 条，标错 ${k.swapped} 条。`,
    slicesLead: '和其余样本比，区间整个低于 0 才算“更差”。没有标准标签的切片算不了 F1，改比“完全对”的比例。少于 20 条的切片不下结论。',
    slice: '切片', items: '条数', vsRest: '和其余比', verdict: '结论',
    verdicts: { worse: '更差', better: '更好', 'no measured difference': '没有测出差别', 'too few': '样本太少' },
    fields: { 'meta.lang': '语言', 'meta.source': '来源', 'meta.difficulty': '难度', 'meta.stars_band': '星级', 'meta.n_labels_band': '标准标签数', 'meta.has_neutral': '有没有中性提及', 'gold label': '标准标签', 'length of text': '文字长度' },
    values: { zh: '中文', en: '英文', violating: '违规', 'look-alike': '像违规其实合规', plain: '普通合规', written: '写好的广告', 'written-hard': '难题', 'written-lookalike': '相似陷阱', 'video-words': '视频广告的字', synthetic: '合成广告', '(no gold label)': '（没有标准标签）', '1-3 stars': '1–3 星', '4-5 stars': '4–5 星', '1-4 labels': '1–4 个', '5-7 labels': '5–7 个', '8+ labels': '8 个以上', 'has a neutral mention': '有', 'no neutral mention': '没有' },
    failLead: (n, k, a) => `最好的做法在测试集 A 上的 ${n} 个错误判断。每个独立归因两次，${k}/${a} 次两次一致。虚线框是漏判或误判的标签。`,
    all: '全部', gold: '标准', pred: '给出', more: '展开全文', less: '收起', why: '原因', fix: '建议', fpKind: '误判', fnKind: '漏判', stable: '所有做法都错',
    noFail: '这个筛选下没有失败样本。', noRca: '根因分析还没有跑。',
    revLead: '第二版只改根因表指向的地方。测试集 B 在改版前没有用过；测试集 A 看过它的错误，所以只算回归。',
    setB: '测试集 B（留出）', setA: '测试集 A（回归）', onlyA: '只有第一版完全对', onlyB: '只有第二版完全对', noRev: '改版还没有跑。',
    cmp: { 'B better': '第二版更好', 'B worse': '第二版更差', 'no measured difference': '没有测出差别', 'NOT RUN': '没有跑' },
    keys: ['最好做法的微平均 F1', '两个任务', '每千条费用'],
  },
  en: {
    tasks: 'Labelling task', arms: 'Arms', monitor: 'Per label', confusion: 'Confusion', slices: 'Slices', failures: 'Failures', revision: 'Revision',
    armsLead: (n) => `The same ${n} items, one run per arm. The dot is micro F1, the bar its 95% interval.`,
    arm: 'Arm', micro: 'Micro F1', macro: 'Macro F1', exact: 'Exact', miss: 'Missed', fa: 'False alarm', cost: 'USD per 1k', calls: 'Calls/item',
    missFull: 'a violating ad given no label', faFull: 'a compliant ad given a label', usd: 'USD',
    monitorLead: 'Low precision means the label is given too freely; low recall means it is missed. Misses and false alarms are counts; rates under 60% and their counts are in red.',
    pickArm: 'Arm', label: 'Label', support: 'Gold', precision: 'Precision', recall: 'Recall', f1: 'F1', fn: 'Missed', fp: 'False alarm',
    confLead: 'Rows are gold labels, columns the labels given. The diagonal is right; the last row is "given but not in gold", the last column "in gold but not given".',
    cmDiag: 'right', cmOff: 'wrong', noGold: '(no gold label)', noPred: '(not given)',
    kinds: (k) => `${k.exact} exact, ${k['under-labelled']} under-labelled, ${k['over-labelled']} over-labelled, ${k.swapped} swapped.`,
    slicesLead: 'A slice is worse only when its whole interval against the rest is below 0. Slices without gold labels have no F1, so they are compared on exact match. Slices under 20 items get no verdict.',
    slice: 'Slice', items: 'Items', vsRest: 'Against the rest', verdict: 'Verdict',
    verdicts: { worse: 'worse', better: 'better', 'no measured difference': 'no measured difference', 'too few': 'too few' },
    fields: { 'meta.lang': 'Language', 'meta.source': 'Source', 'meta.difficulty': 'Difficulty', 'meta.stars_band': 'Stars', 'meta.n_labels_band': 'Gold labels', 'meta.has_neutral': 'Neutral mention', 'gold label': 'Gold label', 'length of text': 'Text length' },
    values: { zh: 'Chinese', en: 'English', violating: 'violating', 'look-alike': 'look-alike', plain: 'plain compliant', written: 'written ads', 'written-hard': 'hard set', 'written-lookalike': 'look-alike set', 'video-words': 'video ad words', synthetic: 'synthetic ads' },
    failLead: (n, k, a) => `The ${n} wrong label decisions of the best arm on test A. Each was classified twice, independently; the two agree on ${k} of ${a}. Dashed labels were missed or given wrongly.`,
    all: 'All', gold: 'Gold', pred: 'Given', more: 'Show all', less: 'Show less', why: 'Why', fix: 'Fix', fpKind: 'false alarm', fnKind: 'missed', stable: 'every arm wrong',
    noFail: 'No failure under this filter.', noRca: 'The root-cause analysis has not run yet.',
    revLead: 'The second version changes only what the root-cause table points to. Test B was not used before the revision; test A had its failures read, so it counts as regression.',
    setB: 'Test B (held out)', setA: 'Test A (regression)', onlyA: 'only v1 right', onlyB: 'only v2 right', noRev: 'The revision has not run yet.',
    cmp: { 'B better': 'v2 better', 'B worse': 'v2 worse', 'no measured difference': 'no measured difference', 'NOT RUN': 'not run' },
    keys: ['Micro F1 of the best arm', 'Two tasks', 'USD per 1,000 items'],
  },
}[L]

const $ = (s, el = document) => el.querySelector(s)
const h = (tag, attrs = {}, ...kids) => {
  const el = document.createElement(tag)
  for (const [k, v] of Object.entries(attrs)) {
    if (v == null || v === false) continue
    if (k === 'class') el.className = v
    else if (k === 'style') el.setAttribute('style', v)
    else if (k.startsWith('on')) el.addEventListener(k.slice(2), v)
    else el.setAttribute(k, v === true ? '' : v)
  }
  for (const c of kids.flat(Infinity)) if (c != null && c !== false) el.append(c.nodeType ? c : document.createTextNode(String(c)))
  return el
}
const f3 = (x) => (x == null ? '–' : x.toFixed(3))
const scrollBox = (cls, label, ...kids) => h('div', { class: cls, tabindex: '0', role: 'region', 'aria-label': label }, ...kids)
const pct = (x) => (x == null ? '–' : `${(100 * x).toFixed(0)}%`)
const ci = (c) => (c ? `${c[0].toFixed(2)}–${c[1].toFixed(2)}` : '')
const sci = (c) => (c ? `${c[0] >= 0 ? '+' : ''}${c[0].toFixed(3)} ~ ${c[1] >= 0 ? '+' : ''}${c[1].toFixed(3)}` : '')
const kn = (o) => (o ? `${o.k}/${o.n}` : '–')
const armName = (a) => a.name[L] || a.id
const fieldName = (f) => T.fields[f] || T.fields[f.replace(/^length of .*/, 'length of text')] || f
const valueName = (v) => T.values[v] || (L === 'zh' ? String(v).replace(/^(\d+)–(\d+) chars$/, '$1–$2 字') : String(v).replace(/ chars$/, ' characters'))

function bestArm(task) {
  return [...task.arms].filter((a) => !/synthetic|mixed/.test(a.id)).sort((a, b) => (b.micro.f1 - a.micro.f1) || (a.cost_per_1k - b.cost_per_1k))[0]
}

// ---------- cover numbers ----------
function cover() {
  const ul = $('#keys')
  if (!ul || !D) return
  D.tasks.forEach((t, i) => {
    const b = bestArm(t)
    ul.append(h('li', { 'data-k-rise': true, style: `--i:${i}` },
      h('b', { class: 'k-big k-num', 'data-k-count': true }, f3(b.micro.f1)),
      h('span', { class: 'k-keys-l' }, t.name[L]),
      h('span', { class: 'k-keys-f k-num' }, `${armName(b)} · ${t.items} ${L === 'zh' ? '条' : 'items'} · ${L === 'zh' ? '区间' : 'interval'} ${ci(b.micro.ci)}`)))
  })
  const costs = D.tasks.map((t) => bestArm(t).cost_per_1k)
  ul.append(h('li', { 'data-k-rise': true, style: `--i:${D.tasks.length}` },
    h('b', { class: 'k-big k-num', 'data-k-count': true }, `$${Math.max(...costs).toFixed(2)}`),
    h('span', { class: 'k-keys-l' }, L === 'zh' ? '最好做法每标一千条的费用' : 'per 1,000 items, best arm'),
    h('span', { class: 'k-keys-f' }, L === 'zh' ? 'claude-haiku-5-5，批量接口' : 'claude-haiku-5-5, Message Batches')))
}

// ---------- sections ----------
function axisOf(arms) {
  const low = Math.min(...arms.map((a) => (a.micro.ci ? a.micro.ci[0] : a.micro.f1)))
  return Math.max(0, Math.floor((low - 0.05) * 10) / 10)
}

function armRows(arms, axis, suffix = () => '') {
  const pos = (x) => `${(100 * (x - axis)) / (1 - axis)}%`
  return h('ul', { class: 'k-rows' }, arms.map((a) => {
    const [lo, hi] = a.micro.ci || [a.micro.f1, a.micro.f1]
    return h('li', {},
      h('span', {}, armName(a) + suffix(a)),
      h('span', { class: 'k-v' }, f3(a.micro.f1)),
      h('span', { class: 'k-bar', role: 'img', 'aria-label': `${T.micro} ${f3(a.micro.f1)}, 95% ${ci(a.micro.ci)}`, style: `--from:${pos(lo)};--to:${pos(hi)};--at:${pos(a.micro.f1)}` }, h('i'), h('b')))
  }))
}

function axisNote(axis) {
  return h('p', { class: 'k-label v-axis' }, L === 'zh' ? `横轴从 ${axis.toFixed(1)} 到 1.0` : `Axis from ${axis.toFixed(1)} to 1.0`)
}

function secArms(t) {
  const best = bestArm(t)
  const axis = axisOf(t.arms)
  const rows = armRows(t.arms, axis)
  const hasDecision = t.arms.some((a) => a.miss)
  const head = [T.arm, T.micro, T.macro, T.exact, ...(hasDecision ? [T.miss, T.fa] : []), T.calls, T.cost]
  const table = scrollBox('v-table-wrap', T.arms, h('table', { class: 'v-table' },
    h('thead', {}, h('tr', {}, head.map((x) => h('th', { scope: 'col' }, x)))),
    h('tbody', {}, t.arms.map((a) => h('tr', { class: a.id === best.id ? 'v-best' : null },
      h('th', { scope: 'row' }, armName(a)),
      h('td', { class: 'v-strong' }, f3(a.micro.f1), h('span', { class: 'v-ci' }, ci(a.micro.ci))),
      h('td', {}, f3(a.macro.f1)),
      h('td', {}, kn(a.exact)),
      ...(hasDecision ? [h('td', { title: T.missFull }, kn(a.miss)), h('td', { title: T.faFull }, kn(a.fa))] : []),
      h('td', {}, a.calls.toFixed(2)),
      h('td', {}, `$${a.cost_per_1k.toFixed(2)}`))))))
  const cmps = t.comparisons.length ? h('div', { style: 'margin-top:16px' }, scrollBox('v-table-wrap', L === 'zh' ? '比较' : 'Comparisons', h('table', { class: 'v-table' },
    h('thead', {}, h('tr', {}, [L === 'zh' ? '比较' : 'Comparison', 'Δ ' + T.micro, '95%', T.verdict].map((x) => h('th', { scope: 'col' }, x)))),
    h('tbody', {}, t.comparisons.map((c) => {
      const an = t.arms.find((a) => a.id === c.a), bn = t.arms.find((a) => a.id === c.b)
      return h('tr', {}, h('th', { scope: 'row' }, `${c.id}: ${bn ? armName(bn) : c.b} ${L === 'zh' ? '对' : 'vs'} ${an ? armName(an) : c.a}`),
        h('td', {}, c.diff == null ? '–' : `${c.diff >= 0 ? '+' : ''}${c.diff.toFixed(3)}`), h('td', {}, sci(c.ci)),
        h('td', {}, h('span', { class: `k-mark ${c.verdict === 'B better' ? 'k-mark--yes' : c.verdict === 'B worse' ? 'k-mark--stop' : 'k-mark--no'}` },
          { 'B better': L === 'zh' ? '后者更好' : 'second better', 'B worse': L === 'zh' ? '后者更差' : 'second worse', 'no measured difference': T.verdicts['no measured difference'], 'NOT RUN': T.cmp['NOT RUN'] }[c.verdict] || c.verdict)))
    }))))) : null
  return [h('div', { class: 'k-card' }, rows, axisNote(axis)), table, cmps]
}

function secMonitor(t, armId) {
  const box = h('div')
  const sel = h('select', { class: 'v-select', id: `arm-${t.id}`, onchange: (e) => draw(e.target.value) },
    t.arms.map((a) => h('option', { value: a.id, selected: a.id === armId ? true : null }, armName(a))))
  const draw = (id) => {
    const a = t.arms.find((x) => x.id === id)
    box.replaceChildren(scrollBox('v-table-wrap', T.monitor, h('table', { class: 'v-table' },
      h('thead', {}, h('tr', {}, [T.label, T.support, T.precision, T.recall, T.f1, T.fn, T.fp].map((x) => h('th', { scope: 'col' }, x)))),
      h('tbody', {}, a.labels.map((r) => h('tr', {},
        h('th', { scope: 'row' }, r.label),
        h('td', {}, r.support),
        h('td', {}, bar(r.p, r.p_ci)),
        h('td', {}, bar(r.r, r.r_ci)),
        h('td', { class: 'v-strong' }, f3(r.f1)),
        h('td', { class: r.fn && r.r != null && r.r < 0.6 ? 'v-flag' : null }, r.fn),
        h('td', { class: r.fp && r.p != null && r.p < 0.6 ? 'v-flag' : null }, r.fp)))))))
    drawConfusion(t, id)
  }
  queueMicrotask(() => draw(armId))
  return [h('div', { class: 'v-controls' }, h('label', { for: `arm-${t.id}` }, T.pickArm), sel), box]
}

function bar(v, c) {
  const low = v != null && v < 0.6
  return h('span', { class: 'v-pr', title: c ? `95% ${pct(c[0])}–${pct(c[1])}` : null },
    h('span', {}, pct(v)), h('span', { class: `v-mini${low ? ' v-low' : ''}`, 'aria-hidden': 'true' }, h('i', { style: `--w:${v == null ? 0 : 100 * v}%` })))
}

function drawConfusion(t, armId) {
  const host = $(`#cm-${t.id}`)
  if (!host) return
  const a = t.arms.find((x) => x.id === armId)
  const cm = a.confusion
  const max = Math.max(1, ...cm.m.flat())
  const short = (s) => s.replace('(no gold label)', T.noGold).replace('(no predicted label)', T.noPred)
  const table = h('table', { class: 'v-cm' },
    h('caption', { class: 'k-label', style: 'text-align:left;padding-bottom:8px' }, `${armName(a)}. ${T.kinds(cm.kinds)}`),
    h('thead', {}, h('tr', {}, h('td', { class: 'v-corner' }), cm.cols.map((c) => h('th', { scope: 'col' }, short(c))))),
    h('tbody', {}, cm.m.map((row, i) => h('tr', {}, h('th', { scope: 'row' }, short(cm.rows[i])),
      row.map((v, j) => {
        const diag = i === j && i < cm.rows.length - 1
        const share = v / max
        const cls = v === 0 ? 'v-zero' : diag ? 'v-diag' : 'v-off'
        return h('td', { class: `${cls}${share > 0.55 ? ' v-dark' : ''}`, style: `--a:${Math.round(12 + 78 * share)}%`,
          title: `${short(cm.rows[i])} → ${short(cm.cols[j])}: ${v}` }, v === 0 ? '' : v)
      })))))
  host.replaceChildren(scrollBox('v-cm-wrap', T.confusion, table),
    h('p', { class: 'k-label v-legend' }, h('span', { class: 'v-l-diag' }, T.cmDiag), h('span', { class: 'v-l-off' }, T.cmOff)))
}

function secSlices(t, armId) {
  const a = t.arms.find((x) => x.id === armId)
  return a.slices.filter((g) => g.field !== 'gold label').map((g) => [
    h('h3', { class: 'v-sub' }, fieldName(g.field)),
    scrollBox('v-table-wrap', `${T.slices}: ${fieldName(g.field)}`, h('table', { class: 'v-table' },
      h('thead', {}, h('tr', {}, [T.slice, T.items, T.micro, T.exact, T.vsRest, T.verdict].map((x) => h('th', { scope: 'col' }, x)))),
      h('tbody', {}, g.slices.map((s) => h('tr', {},
        h('th', { scope: 'row' }, valueName(s.value)),
        h('td', {}, s.n),
        h('td', {}, f3(s.f1), h('span', { class: 'v-ci' }, ci(s.ci))),
        h('td', {}, `${s.exact}/${s.n}`),
        h('td', {}, s.diff == null ? '–' : `${s.diff >= 0 ? '+' : ''}${s.diff.toFixed(3)}`,
          s.diff != null && s.measure === 'exact match' ? h('span', { class: 'v-ci' }, L === 'zh' ? '完全对' : 'exact') : null),
        h('td', {}, h('span', { class: `k-mark ${s.verdict === 'worse' ? 'k-mark--stop' : s.verdict === 'better' ? 'k-mark--yes' : 'k-mark--no'}` }, T.verdicts[s.verdict] || s.verdict)))))))])
}

function secFailures(t) {
  if (!t.rca) return [h('p', { class: 'v-empty' }, T.noRca)]
  const counts = {}
  t.failures.forEach((f) => f.decisions.forEach((d) => { counts[d.cause] = (counts[d.cause] || 0) + 1 }))
  const causes = Object.keys(counts).sort((x, y) => counts[y] - counts[x])
  let cur = 'all'
  const list = h('div', { class: 'v-cases' })
  const chips = h('div', { class: 'v-chips', role: 'group', 'aria-label': L === 'zh' ? '按根因筛选' : 'Filter by root cause' },
    ['all', ...causes].map((c) => h('button', { type: 'button', 'aria-pressed': String(c === cur), 'data-c': c, onclick: () => { cur = c; chips.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.c === c))); draw() } },
      c === 'all' ? T.all : (D.causes[c] || {})[L] || c, h('b', {}, c === 'all' ? t.rca.decisions : counts[c]))))
  const draw = () => {
    const shown = t.failures.filter((f) => cur === 'all' || f.decisions.some((d) => d.cause === cur)).slice(0, 40)
    list.replaceChildren(...(shown.length ? shown.map((f) => card(f, cur)) : [h('p', { class: 'v-empty' }, T.noFail)]))
  }
  draw()
  return [h('p', { class: 'k-label', style: 'margin-bottom:16px' }, T.failLead(t.rca.decisions, t.rca.agreement.k, t.rca.agreement.n)), chips, list]
}

function card(f, cur) {
  const long = f.text.length > 180
  const text = h('p', { class: `v-text${long ? ' v-clip' : ''}`, lang: /[一-鿿]/.test(f.text) ? 'zh-CN' : 'en' }, f.text)
  const more = long ? h('button', { type: 'button', class: 'v-more', 'aria-expanded': 'false', onclick: (e) => {
    const open = text.classList.toggle('v-clip'); e.target.textContent = open ? T.more : T.less; e.target.setAttribute('aria-expanded', String(!open)) } }, T.more) : null
  const tags = (arr, other, kind) => (arr.length ? arr.map((x) => (other.includes(x)
    ? h('span', { class: 'k-tag' }, x)
    : h('span', { class: 'k-tag v-tag-off', title: kind === 'miss' ? T.fnKind : T.fpKind }, x, h('span', { class: 'v-sr' }, ` (${kind === 'miss' ? T.fnKind : T.fpKind})`))))
    : [h('span', { class: 'k-label' }, '–')])
  return h('article', { class: 'k-card v-case' },
    h('header', {}, h('span', { class: 'k-label' }, f.id)),
    text, more,
    h('dl', { class: 'v-labels' }, h('dt', {}, T.gold), h('dd', {}, tags(f.gold, f.pred, 'miss')), h('dt', {}, T.pred), h('dd', {}, tags(f.pred, f.gold, 'extra'))),
    f.decisions.filter((d) => cur === 'all' || d.cause === cur).map((d) => h('div', { class: 'v-dec' },
      h('div', { class: 'v-dec-h' }, h('b', {}, d.label), h('span', { class: 'k-mark k-mark--no' }, d.kind === 'miss' ? T.fnKind : T.fpKind),
        h('span', { class: `k-mark ${d.cause === 'split' ? 'k-mark--no' : 'k-mark--yes'}` }, (D.causes[d.cause] || {})[L] || d.cause),
        d.stable ? h('span', { class: 'k-label' }, T.stable) : null),
      reason(T.why, L === 'zh' ? d.why_zh : d.why, ''),
      reason(T.fix, L === 'zh' ? d.fix_zh : d.fix, 'v-fix'))))
}

function reason(label, text, cls) {
  return text ? h('p', { class: cls || null }, `${label}${L === 'zh' ? '：' : ': '}`, text) : null
}

function secRevision(t) {
  if (!t.revision) return [h('p', { class: 'v-empty' }, T.noRev)]
  const out = []
  for (const [set, label] of [['test_b', T.setB], ['test_a', T.setA]]) {
    const arms = t.revision[set]
    if (!arms) continue
    const c = (t.revision_comparisons || []).find((x) => x.set === set)
    out.push(h('h3', { class: 'v-sub' }, label))
    const axis = axisOf(arms)
    out.push(h('div', { class: 'k-card' }, armRows(arms, axis), axisNote(axis)))
    if (c) out.push(h('p', { class: 'k-label', style: 'margin-top:12px' },
      L === 'zh'
        ? `Δ ${T.micro} ${c.diff >= 0 ? '+' : ''}${c.diff.toFixed(3)}（95% 区间 ${sci(c.ci)}），${T.cmp[c.verdict] || c.verdict}；${T.onlyB} ${c.b_only} 条，${T.onlyA} ${c.a_only} 条。`
        : `Δ ${T.micro} ${c.diff >= 0 ? '+' : ''}${c.diff.toFixed(3)} (95% ${sci(c.ci)}), ${T.cmp[c.verdict] || c.verdict}; ${T.onlyB} ${c.b_only}, ${T.onlyA} ${c.a_only}.`))
  }
  return out
}

// ---------- page ----------
function section(id, title, lead, body) {
  return h('section', { class: 'v-sec', id }, h('div', { class: 'k-head' }, h('h2', {}, title), lead ? h('p', {}, lead) : null), body)
}

function render() {
  if (!D) return
  const host = $('#tasks')
  const tabs = h('div', { class: 'k-tabs', role: 'tablist', 'aria-label': T.tasks })
  const panels = []
  D.tasks.forEach((t, i) => {
    tabs.append(h('button', { type: 'button', role: 'tab', id: `tab-${t.id}`, 'aria-controls': `panel-${t.id}` }, t.name[L]))
    const best = bestArm(t).id
    panels.push(h('div', { role: 'tabpanel', id: `panel-${t.id}`, 'aria-labelledby': `tab-${t.id}`, class: 'k-wrap', hidden: i > 0 ? true : null },
      section(`arms-${t.id}`, T.arms, T.armsLead(t.items), secArms(t)),
      section(`monitor-${t.id}`, T.monitor, T.monitorLead, secMonitor(t, best)),
      section(`confusion-${t.id}`, T.confusion, T.confLead, h('div', { id: `cm-${t.id}` })),
      section(`slices-${t.id}`, T.slices, T.slicesLead, secSlices(t, best)),
      section(`failures-${t.id}`, T.failures, null, secFailures(t)),
      section(`revision-${t.id}`, T.revision, T.revLead, secRevision(t))))
  })
  const nav = h('nav', { 'aria-label': L === 'zh' ? '本页' : 'On this page' },
    [['arms', T.arms], ['monitor', T.monitor], ['confusion', T.confusion], ['slices', T.slices], ['failures', T.failures], ['revision', T.revision]]
      .map(([k, label]) => h('a', { href: `#${k}`, 'data-sec': k }, label)))
  nav.addEventListener('click', (e) => {
    const a = e.target.closest('a'); if (!a) return
    e.preventDefault()
    const open = panels.find((p) => !p.hidden)
    const target = open && open.querySelector(`#${a.dataset.sec}-${open.id.replace('panel-', '')}`)
    if (target) target.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' })
  })
  // #tasks carries data-k-tabs, so kit.js switches the panels; the bar with the tabs stays at the top while scrolling
  host.append(h('div', { class: 'v-bar-tabs' }, h('div', { class: 'k-wrap' }, tabs, nav)), ...panels)
}

cover()
render()
