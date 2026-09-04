# Roadmap

## 0.2.0 - candidates

- **A Colab notebook** that runs Track 1 and verifies the chain hash from a
  cold browser, the way `blast-radius-containment` does. The repository is
  standard library plus pytest, so this is packaging, not new code.
- **Figures as code.** The article's eight figures are rendered by the website's
  own chart components from a TypeScript data module, not by this repository.
  If a figure ever needs to exist outside the article, it comes in here as a
  script with a claim map in its docstring - never as an exported image.

## Deliberately out of scope

- **The one-line accounts.** 46.1 against 348 gCO2/kWh, the 1.7 percent figure
  from the IEA, the ratio between the connection queue and operating capacity in
  Brazil: each is a single division the reader performs while reading. They are
  demonstrated in the article itself and adding them here would be ceremony.
- **Re-measuring anything.** See `REPRODUCIBILITY.md`, "What cannot be re-run".
- **Tracking sources over time.** This repository records what the publishers
  said on a date. A watcher that polls for revisions is a different project.
