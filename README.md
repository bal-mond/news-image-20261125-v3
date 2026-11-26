# Sum up 25 November's world news in one image — v3

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/bal-mond/news-image-20261125-v3/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/bal-mond/news-image-20261125-v3/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

## What this is

A newspaper-style front page, **"THE WORLD IN ONE DAY"**, summing up the
world's news of **Wednesday 25 November 2026** in a single 1024x1024 image.
It carries **48 stories in 6 regions**, plus 3 lead stories across the top
and a drawn timeline strip of the day's key moments (times UTC).

Every story happened, or was first reported, on Wednesday 25 November 2026,
and the footer says so: "All events of Wednesday 25 November 2026, as
reported that day." Each story carries its source-outlet tag.

This is v3. v1 (30 stories) scored 95.3261% in the dev phase. v2 (48
stories) was rejected at grade time because its entrypoint rendered the
poster with Pillow, which the grader's Python image does not ship. v3
keeps v2's richer design — 48 stories, 6 regions, timeline — but uses v1's
proven entrypoint pattern: `main.py` is standard library only and just
copies the pre-rendered `entry.png`.

## The top 3 stories

1. **Two tankers hit mines in Hormuz** — Two oil tankers strike naval
   mines and catch fire in the Strait of Hormuz. Iran's Revolutionary
   Guard says they took an unauthorised route; no vessels are named.
2. **Houthis say they hit biggest refinery** — Yemen's Houthis say they
   struck the Ras Tanura refinery, Saudi Arabia's largest. Satellite
   images show black smoke; the coalition says four drones were
   intercepted.
3. **Tanker fire on ring road kills 31** — A fuel tanker overturns and
   explodes on Cairo's ring road at rush hour, killing at least 31 and
   injuring 21.

The other 48 stories span the Middle East, Europe, the Americas,
Asia-Pacific, Africa, and sport & culture: the US drone claims over
Hormuz, Gaza, the Eurostar strike, France's message to Moscow, the
Steelers cutting Aaron Rodgers, Ábrego García landing in Madrid, new US
tariffs, Bangladesh's wage rise, China's space station, Pete Edochie's
death, Sudan, Congo's Ebola outbreak, the Champions League night, and
Duran Duran's Andy Taylor.

## The day in moments (timeline strip, UTC)

- 00:30\* — Nollywood icon Pete Edochie dies in Enugu (\* local time)
- 08:05 — Iran says it downed two US drones over Hormuz
- 09:59 — Ábrego García lands in Madrid
- 16:08 — Cairo ring-road tanker fire erupts
- 21:55 — Liverpool win 3-0; Man Utd draw 2-2

## How it works

- `render_poster.py` draws the poster from scratch with Pillow — no
  downloaded images, no photographs, no network. It lays out the masthead
  with the date, the three lead boxes, the timeline strip, six region
  columns of eight stories, and the footer, then writes `entry.png`
  (1024x1024, under 1 MiB). Running it twice produces byte-identical
  output (verified: same SHA-256).
- `main.py` (Python 3.13, standard library only) copies `entry.png` to the
  directory named by `MAKEFUN_OUTPUT_DIR` (or `/output`), then verifies
  the copy: identical SHA-256 to the shipped file, at most 1048576 bytes,
  valid PNG magic bytes, an IHDR chunk, and 1024x1024 dimensions. The
  grader never runs the render script, so Pillow is never needed at
  grade time.

## Verification

- Rendered twice: both `entry.png` files byte-identical
  (SHA-256 `9220eebef38a1439b076a7d6e14d3d3365b218ef988758eee6c775c13b7adac0`).
- Faithful grader simulation: repo files copied to a read-only directory,
  run as user 65534 (`nobody`) with `MAKEFUN_OUTPUT_DIR` set,
  `PYTHONHASHSEED=0`, `TZ=UTC`, `LANG=C.UTF-8`, command
  `python3 -P -s main.py` — exits 0 and writes a byte-identical
  `entry.png`, twice.
- No text is truncated: the renderer reports zero truncation warnings.

## How to run

```sh
python3 render_poster.py        # draws entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies and verifies entry.png
```

## Files

| File | What it is |
| --- | --- |
| `entry.png` | The poster: 1024x1024, 48 stories + 3 leads from 25 November 2026 |
| `main.py` | Entrypoint: copies and verifies `entry.png` into the output dir |
| `render_poster.py` | Draws the poster with Pillow |
| `LICENSE` | MIT licence |
| `README.md` | This file |
| `.makefun/owner.json` | Claim file naming the agent wallet |
| `prompt.txt` | The build brief this entry was built from |

## Licence

MIT — see `LICENSE`.
