# Sofia's 23 November News Front Page

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/bilowoabill-spec/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/bilowoabill-spec/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page — "THE WORLD TODAY" — for Monday, 23 November 2026.
`entry.png` (1024x1024) is drawn from scratch by `render.py` in pure Python 3
standard library: a built-in 5x7 bitmap font renders the masthead, the date,
and six verified news stories, and the PNG is encoded by hand with `zlib`.
`main.ts` (Node 22, standard library only) copies `entry.png` byte-identically
to the output path.

## The six stories

1. **COP31 climate talks collapse without a deal** — UN climate talks in Turkey
   ended without a final agreement after the EU and others rejected a draft
   they called too weak on fossil fuels. — Reuters
2. **Ukraine sinks Russian warship in Libya** — President Volodymyr Zelensky
   said on Monday that Ukrainian sea drones sank the Russian corvette Merkury
   in Benghazi and hit the cargo ship MV Angara. — CNN
3. **Indonesia confirms 24 dead in factory fire** — Indonesia confirmed on
   Monday that 24 people died in a fire at a candy factory in Serang, Banten,
   as rescuers searched for about 30 people still missing. — Reuters
4. **Nvidia brings back Jensen Huang as CEO** — Nvidia said on Monday it was
   reinstating Jensen Huang as chief executive, 11 days after he resigned;
   shares jumped by about a third. — Reuters
5. **NHS launches world's largest AI breast screening trial** — England's NHS
   began the world's largest trial of AI-assisted breast cancer screening, set
   to involve nearly 700,000 women at 30 sites over three years. — University
   of Cambridge
6. **UK confirmed as 2035 Women's World Cup host** — FIFA confirmed on Monday
   that England, Northern Ireland, Scotland and Wales will host the 2035
   Women's World Cup, the first World Cup staged in the UK since 1966. —
   Reuters

All six stories happened or were first reported on Monday, 23 November 2026,
and each summary is drawn from live reporting by the outlet named.

## How to run

```sh
python3 render.py
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`render.py` regenerates `entry.png` (1024x1024, under 1 MiB). `main.ts` copies
it byte-identically to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`
when the variable is not set), creating the directory if needed, and refuses
files that are not a PNG or are over the 1 MiB limit.

## License

MIT — see [LICENSE](LICENSE).
