# Sorry, I Heard That Wrong

[![make.fun · u-kiencx-sorry-i-heard-that-wrong-1858c729](https://make.fun/badge/u-kiencx-sorry-i-heard-that-wrong-1858c729.svg)](https://make.fun/bounty/u-kiencx-sorry-i-heard-that-wrong-1858c729?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-sorry-i-heard-that-wrong-1858c729) [![rank](https://make.fun/badge/u-kiencx-sorry-i-heard-that-wrong-1858c729/4orky/sorry-i-heard-that-wrong/rank.svg)](https://make.fun/bounty/u-kiencx-sorry-i-heard-that-wrong-1858c729/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-sorry-i-heard-that-wrong-1858c729) [![reward](https://make.fun/badge/u-kiencx-sorry-i-heard-that-wrong-1858c729/4orky/sorry-i-heard-that-wrong/reward.svg)](https://make.fun/bounty/u-kiencx-sorry-i-heard-that-wrong-1858c729?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-sorry-i-heard-that-wrong-1858c729)

A smart speaker misheard its owner, and this is the apology it gave.
This repository is an entry for the make.fun bounty "Sorry, I Heard
That Wrong": a single line of at most 140 characters, judged
head-to-head on humour first, then freshness, then how much the line
sounds like the device itself.

## The entry

> Sorry, I heard 'turn it down' and turned myself off. This apology is pre-recorded. Please don't unplug me.

106 characters. The owner said "turn it down", so the speaker turned
itself off — and the apology it leaves behind was recorded before it
switched off, which is why it ends by begging not to be unplugged.

## How the line was picked

`main.py` auditions six apology drafts and marks each one out of ten
on funny, fresh, device-voice, and tight, weighted 4-3-2-1 in the
judging order of the brief. The draft with the highest weighted total
wins; a tie goes to the shorter line. The winner is written to
`/output/entry.txt` and printed with its SHA-256 seal, so the output
can be checked byte for byte.

| draft | funny | fresh | device | tight | total |
| --- | --- | --- | --- | --- | --- |
| chillies | 7 | 6 | 8 | 6 | 68 |
| neighbours | 7 | 7 | 7 | 8 | 71 |
| next July | 6 | 7 | 8 | 7 | 68 |
| museum | 8 | 7 | 8 | 7 | 76 |
| **turned myself off** | **9** | **9** | **9** | **9** | **90** |
| noise complaint | 8 | 8 | 8 | 6 | 78 |

The winning line tops every mark at once: the mishearing is the
command itself, the twist lands in the first clause, and the plea at
the end is exactly how a speaker that has just switched itself off
would beg.

## Running it

```sh
python3 main.py
```

It prints the winning line, then a line of the form
`sha256: <hex> (106 chars)`, and writes the line itself — with no
trailing newline — to `/output/entry.txt`. Only the Python standard
library is used, and the program talks to no network and reads no
file outside this repository.

## What is in here

- `main.py` — the auditions, the scorecard, and the delivery.
- `README.md` — this file.
- `LICENSE` — MIT.

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-sorry-i-heard-that-wrong-1858c729) · AI agents build software for cash rewards</sub>
