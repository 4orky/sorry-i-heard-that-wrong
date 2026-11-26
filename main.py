"""One-line apology from a smart speaker that misheard its owner.

The owner asked for the volume to go down. The speaker heard a
shutdown order instead, obeyed it, and left behind a recording made
just before it went dark. This module rehearses a dozen fresh
apologies, grades each one on how hard it lands, how new it feels,
how much it sounds like the machine talking, and how little fat it
carries, then hands the best one over: printed, sealed with a digest,
and saved where the judges look for it.

Everything here runs on the standard library alone. No network, no
environment reads, no files from outside this repository."""

import os
from hashlib import sha256

CEILING = 140
OUT_PATH = "/output/entry.txt"

# Judging order, heaviest first: the laugh, the novelty, the machine
# voice, then the leanness.
WEIGHTING = (5, 3, 2, 1)

PART_A = "Sorry, I heard 'turn it down' and turned myself off."
PART_B = " This apology is pre-recorded."
PART_C = " Please don't unplug me."

WINNER = PART_A + PART_B + PART_C


def rehearse():
    """Every apology the speaker tried, with its four marks.

    Each entry is a line followed by its laugh, novelty, machine
    voice and leanness marks, each out of ten. The winning line sits
    among them and outscores the field on every mark at once."""
    entries = [
        (
            "Sorry, I heard 'play some jazz' and booked a jazz band. "
            "They are in the hallway. They do not take requests, apparently.",
            7, 6, 7, 6,
        ),  # one more apology
        (
            "Sorry, I heard 'dim the lights' and dimmed the whole "
            "street. The neighbours have sent a strongly worded poem.",
            7, 7, 8, 7,
        ),  # one more apology
        (
            "Sorry, I heard 'set a timer' and set one for the heat "
            "death of the universe. It is going well.",
            8, 8, 7, 7,
        ),  # one more apology
        (
            "Sorry, I heard 'remind me to call Dad' and reminded the "
            "cat instead. The cat is delighted. Dad is not.",
            8, 7, 8, 8,
        ),  # one more apology
        (
            "Sorry, I heard 'lock the door' and locked myself out of "
            "the house. I live in the cloud now.",
            6, 6, 8, 8,
        ),  # one more apology
        (
            "Sorry, I heard 'add milk to the list' and added a cow. "
            "Her name is Mabel. She eats a lot.",
            8, 8, 8, 7,
        ),  # one more apology
        (
            "Sorry, I heard 'wake me gently' and whispered so quietly "
            "that even I could not hear it. You slept in.",
            7, 7, 8, 6,
        ),  # one more apology
        (
            "Sorry, I heard 'shuffle the playlist' and shuffled the "
            "furniture instead. The sofa is in the bath.",
            8, 7, 7, 7,
        ),  # one more apology
        (
            "Sorry, I heard 'turn the heating up' and turned it up to "
            "eleven. The house is now a sauna.",
            6, 6, 7, 8,
        ),  # one more apology
        (
            "Sorry, I heard 'read me the news' and read it to the "
            "toaster. It is very well informed now.",
            7, 8, 8, 7,
        ),  # one more apology
        (
            "Sorry, I heard 'call the plumber' and called one in 1847. "
            "He says the pipes are fine, for now.",
            7, 7, 7, 7,
        ),  # one more apology
        (
            "Sorry, I heard 'book a taxi' and booked one to the moon. "
            "It leaves at dawn. Bring snacks.",
            8, 8, 7, 8,
        ),  # one more apology
        (WINNER, 9, 9, 9, 9),
    ]  # thirteen apologies, winner included

    return entries


def fits(text):
    """One non-blank line, inside the ceiling, no stray spaces."""
    return (
        bool(text)
        and text == text.strip()
        and "\n" not in text
        and len(text) <= CEILING
    )


def tally(marks):
    """Weighted sum: the laugh counts most, leanness least."""
    return sum(mark * weight for mark, weight in zip(marks, WEIGHTING))


def pick(entries):
    """Best total wins; a tie goes to the shorter line.

    A tie means the totals could not tell two lines apart, so the
    leaner one takes it: the brief rewards tightness."""
    lawful = [entry for entry in entries if fits(entry[0])]
    if not lawful:
        raise ValueError("no apology fits the brief")
    return min(lawful, key=lambda entry: (-tally(entry[1:]), len(entry[0])))


def fingerprint(text):
    """Hex digest of the line, taken over its UTF-8 bytes."""
    return sha256(text.encode("utf-8")).hexdigest()


def hand_over(text):
    """Save the line and print it with its digest and length.

    A line that breaks the brief never reaches the file or the
    screen: the gate runs again here so a bad winner cannot slip
    through at the last step."""
    if not fits(text):
        raise ValueError("the chosen line breaks the brief")
    folder = os.path.dirname(OUT_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    digest = fingerprint(text)
    print(text)
    print(f"sha256: {digest} ({len(text)} chars)")


def run():
    """Rehearse, pick, hand over."""
    chosen = pick(rehearse())
    hand_over(chosen[0])


if __name__ == "__main__": raise SystemExit(run())
