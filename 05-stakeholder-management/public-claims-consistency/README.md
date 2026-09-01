# Public claims consistency

Three instruments. Each compares what Midpage says on one public surface against what
Midpage says on another, and reports where they disagree.

None of them says what is true. They cannot — the truth about retention lives in
contracts nobody outside has read, and the truth about visitor counts lives in an
analytics account. What they report is that **the pages do not agree with each other**,
which is a fact about the pages, verifiable by anyone, and the thing an enterprise
reviewer will notice first.

## Run them

```bash
pip install pyyaml

python3 check_retention.py
python3 subprocessor_consistency.py
python3 check_metrics.py
```

No key, no network call, no model in any code path. Same input, same output, every run.

Add `--strict` to exit non-zero on findings (for CI), `--check` to validate the
observation file alone, `--render` to rewrite the markdown report from source.

## The three

| Tool | Finding | Compares | Reports |
|---|---|---|---|
| [`check_retention.py`](check_retention.py) | **F1** | 4 surfaces × 4 data paths | 4 |
| [`subprocessor_consistency.py`](subprocessor_consistency.py) | **F2** | The DPA-named list against the trust center | 3 |
| [`check_metrics.py`](check_metrics.py) | **F3** | Two first-party traction figures | 2 |

Reports: [retention](retention-findings.md) · [subprocessors](subprocessor-findings.md)
· [metrics](metric-findings.md). All three are rendered by the tools and regenerated in
CI; a stale one fails the build.

## Then attack them

```bash
pip install -r ../../requirements-dev.txt
python3 -m pytest -q
```

93 tests. Every checker carries two specific ones:

**A control test** — clean, agreeing input must produce **zero** findings. Without it, a
checker that returned a finding for every input would pass every other assertion in its
suite.

**A mutation guard** — gut the comparator and the suite must go red. Disable
`INCOMPATIBLE` in the retention checker and its contradiction findings must vanish.
Remove alias resolution from the subprocessor checker and `Neon` versus `NeonDB` must
start producing phantom findings. Force the metrics checker to compare its excluded
third-party row and extra findings must appear. A test suite that stays green while the
thing it tests has been switched off is decoration.

## Three deliberate refusals

These are the parts worth reading the code for.

**A disclosed dependency is not a defect.** Midpage's security page says plugin
workflows do not store queries *and*, in the same sentence, that those workflows may
still share queries with model providers. That is the honest construction, and
`check_retention.py` is built to tell it apart from the marketing page's silent version
of the same claim. If it could not, its findings would be pattern-matching rather than
analysis. There is a test that flips exactly that boolean and nothing else.

**Spelling drift is not a missing vendor.** The two subprocessor pages spell four
providers differently — `Neon`/`NeonDB`, `Cohere`/`Cohere API`, `Mistral`/`Mistral AI`,
`prefect`/`Prefect`. Alias resolution collapses them before comparison, because
inflating three real findings to seven would make the report easier to dismiss and
harder to act on.

**An incomparable figure is excluded, and has to say why.** Semrush measures site
visits; Midpage's pages claim unique visitors who read cases. Comparing them would
manufacture a finding. `check_metrics.py` **refuses to load** an excluded surface that
carries no `incomparable_because` — the exclusion is enforced by the validator, not
promised in a comment.

## The observation files are observations

`retention-claims.yaml`, `subprocessors.yaml`, and `metrics.yaml` record what a page
said on a date, with the quote that supports it. They are not posture statements about
Midpage.

When a page changes, the correct move is to **re-observe and update the entry with a new
`checked` date**. It is never to edit a quote so that it still supports the finding. The
validators enforce what they can — https-only URLs, ISO dates, a quote on every
assertion, no YAML boolean sneaking in where an integer belongs — but that last
discipline is a human one, and it is the one the whole repository rests on.
