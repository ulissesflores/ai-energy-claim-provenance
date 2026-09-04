# Findings

One section per conjunto: what the article publishes, how this repository
derives it, and what would move the number. Every value below is asserted in
`tests/`; the table of claims is `tests/test_article_numbers.py`.

## 1. The 122-language energy divide

**Published.** The measured spread between the cheapest and the most expensive
of 122 languages is 179x. Portuguese is the second cheapest, at 1.47x English.
Shan spends 175x the energy of English to answer correctly 10.6 percent of the
time, against 94.6 percent for English.

**Derived.** Table 5 of the preprint gives total energy in joules per language.
Ratios are that total divided by the 16,762.1 J of English; ranks are the
position in the list sorted by that total.

**Two published values for one pair, on purpose.** Table 1 prints 179x for
English against Southern Pashto; Table 5 gives 187.8x for the same pair, over
different absolute totals. The paper does not say why the two differ and neither
does this repository: what is recorded is that both are published. The article
uses 179x - the value the authors sign - in the body and 188x in the figure,
which declares that it draws Table 5. `test_the_two_published_english_pashto_ratios_stay_distinct` exists to
stop anyone averaging them.

**What would move it.** A measurement on a production model. These are open
models on an academic GPU, read by hardware counter; only the ratios travel, and
the paper is a preprint without peer review.

## 2. Five PJM capacity auctions

**Published.** The series of RTO clearing prices, in dollars per MW-day: 28.92,
269.92, 329.17, 333.44, 325.00 - a 833.3 percent jump on the first step and
three consecutive auctions clearing at the regulatory cap.

**Derived.** Each Base Residual Auction report states its own delivery year and
restates the year before in the same summary table, so four reports yield five
prices with one overlap each. `fetch_sources.py` refuses to continue if two
reports disagree about a shared year.

**What would move it.** A later auction extends the series; PJM revising a
report changes its digest, which Track 2 reports.

## 3. The US residential electricity price

**Published.** About 32 percent between 2020 and 2025, and about 18 percent
since November 2022.

**Derived.** Simple arithmetic mean of the monthly values inside each calendar
year, in nominal cents per kWh - not adjusted for inflation, not weighted by
sales volume. That rule is pinned in `code/eia.py` because a different rule
gives a different number for the same series.

**What would move it.** The EIA revising a past month. Track 2 checks every
already-frozen month against the live series and goes red on any revision.

## 4. Microsoft datacenter electricity, by location

**Published.** Table 15 lists 29 locations summing to 15,931,489 MWh, 43 percent
of the company's electricity. Only one of the 29 is in Latin America -
Queretaro, at 6,362 MWh - while Table 13 reports 661,556 MWh for the region.
The subtraction leaves 655,194 MWh, 99.04 percent of the region, with no
published location.

**Derived.** The 29 rows are summed; the regional figure comes from Table 13 of
the same document; the share is one division.

**The caveat travels with the number.** Table 15 covers only Microsoft-owned
datacenters under operational control and excludes locations that collectively
represent less than 1 percent of the total. The absence of Brazil is consistent
with leased capacity or with that threshold, and the document does not say
which. This repository records the absence, not a cause.

## 5. Measured power in MLPerf Inference: Datacenter

**Published.** NVIDIA submitted 75, 34 and 61 datacenter results in rounds v5.0,
v5.1 and v6.0 - 170 in total - none carrying measured power. Lenovo did measure
on Blackwell: 12 results on B200 in v5.1. In v6.0 no submitter measured power at
all, 0 of 465. NVIDIA measured in the previous generation: `_MaxQ` systems exist
for H100 in v4.0 and H200 in v4.1 and for no round after.

**Derived.** A row counts as NVIDIA when `submitter == "NVIDIA"` and as
datacenter when `suite == "datacenter"`. Both filters matter: NVIDIA also
submits a handful of edge rows - zero, one and two across the three rounds -
which sit outside the claim and are reported separately, also without power.

**The `_MaxQ` evidence is a directory listing.** Rounds v4.0 and v4.1 predate
the `summary_results.json` ledger, so the evidence there is the list of system
directories under `closed/NVIDIA/results`, plus the `power/` and `ranging/`
directories that MLPerf Power requires, recorded in
`data/mlperf_nvidia_systems.json`.

**What is not claimed.** Nothing about intent. The ledger records what was
submitted, not why. And nothing about benchmarks outside MLPerf Inference:
Datacenter - Green500, SPECpower and the other MLPerf suites were not examined.
