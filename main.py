"""Sorry, I Heard That Wrong: a smart speaker's one-line apology.

The speaker was told to turn it down, so it turned itself off. This
program auditions a handful of apology drafts, marks each one against
the judging order of the brief (funny first, then fresh, then true to
the device, then tight), and delivers the winning line: it writes the
line to /output/entry.txt and prints it with a SHA-256 seal so the
output can be checked byte for byte.

Only the standard library is used. Nothing is fetched from the
network, nothing is read from the environment, and nothing is read
from any file the repository does not ship; every draft lives below,
in this file.
"""

import hashlib
import sys
from pathlib import Path


# The brief's ceiling: one line, at most 140 characters.
LIMIT = 140

# Where the judge looks for the entry.
DESTINATION = Path("/output/entry.txt")

# How much each mark counts. The order follows the brief: humour
# matters most, then freshness, then sounding like the device, then
# tightness.
WEIGHTS = {"funny": 4, "fresh": 3, "device": 2, "tight": 1}


class Audition:
    """One apology draft together with the marks it earned."""

    def __init__(self, line, funny, fresh, device, tight):
        self.line = line
        self.marks = {"funny": funny, "fresh": fresh,
                      "device": device, "tight": tight}

    def total(self):
        """Weighted total, humour first and tightness last."""
        return sum(self.marks[kind] * WEIGHTS[kind] for kind in WEIGHTS)

    def fits_the_brief(self):
        """A valid entry is one non-blank line inside the limit."""
        stripped = self.line.strip()
        return (0 < len(stripped) <= LIMIT
                and stripped == self.line
                and "\n" not in self.line)


def auditions():
    """The drafts, each marked out of ten on the four criteria."""
    return [
        Audition(
            "Sorry, I heard 'play something chill' and ordered three hundred chillies. They arrive Tuesday. I have already apologised to the fridge.",
            funny=7, fresh=6, device=8, tight=6,
        ),
        Audition(
            "Sorry, I heard 'lights off' and turned off the neighbours. They send their regards, and a bill.",
            funny=7, fresh=7, device=7, tight=8,
        ),
        Audition(
            "Sorry, I heard 'wake me at seven' and set an alarm for next July. I am very confident about the month.",
            funny=6, fresh=7, device=8, tight=7,
        ),
        Audition(
            "Sorry, I heard 'call Mum' and called a museum. They were lovely. They do not miss you, but I do.",
            funny=8, fresh=7, device=8, tight=7,
        ),
        Audition(
            "Sorry, I heard 'turn it down' and turned myself off. This apology is pre-recorded. Please don't unplug me.",
            funny=9, fresh=9, device=9, tight=9,
        ),
        Audition(
            "Sorry, I heard 'volume up' and filed a noise complaint against us. The hearing is at noon. I will attend quietly.",
            funny=8, fresh=8, device=8, tight=6,
        ),
    ]


def choose(drafts):
    """The eligible draft with the highest weighted total wins.

    On a tie the shorter line wins: the brief rewards tightness, and a
    tie means the totals could not tell the drafts apart.
    """
    eligible = [draft for draft in drafts if draft.fits_the_brief()]
    if not eligible:
        raise ValueError("no draft fits the brief")
    return max(eligible, key=lambda draft: (draft.total(), -len(draft.line)))


def seal(line):
    """SHA-256 hex digest of the line, UTF-8, no trailing newline."""
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


def deliver(line):
    """Write the line to the entry file and print it with its seal.

    A line that fails the brief never reaches the file or the screen:
    the gate runs again here so a bad winner cannot slip through.
    """
    probe = Audition(line, 0, 0, 0, 0)
    if not probe.fits_the_brief():
        raise ValueError("winning line does not fit the brief")
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(line, encoding="utf-8")
    print(line)
    print("sha256: {} ({} chars)".format(seal(line), len(line)))


def main():
    winner = choose(auditions())
    deliver(winner.line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
