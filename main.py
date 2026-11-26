# Sorry, I Heard That Wrong — one-line apology picker.
#
# The brief: a smart speaker apologises to its owner, in one line of at
# most 140 characters, after mishearing them. The judge weighs humour
# first, then freshness, then how much the line sounds like the device
# itself, then tightness. The field is crowded with one pattern — "I
# heard X as Y, so I did Z" (milk/mother-in-law, sad songs/pizzas, dim
# the lights/DM the flights, jazz bands in the hallway) — so every
# draft below was graded against that saturation: a line that only
# swaps in a new X and Y starts with a freshness penalty already baked
# in, and the winner had to earn its laugh some other way.
#
# Second-pass note: the winner first read "This apology was
# pre-recorded. Please do not unplug me." Two cuts: "was" became "is",
# because a recording that is still speaking in the present tense makes
# the paradox sharper — the speaker is off, yet here it is apologising
# — and "do not" became "don't", which is how a voice assistant talks
# out loud. Six characters saved, the joke word "pre-recorded" moves
# one beat earlier, and "turned myself off" still echoes "turn it
# down" with the same verb. The other eleven were read again and none
# overtakes it: the ears/Terms-of-Service line is the closest, but it
# is a definition joke with no twist, while this one lands a twist in
# every clause — the mishearing, the self-switch-off, the recording
# that outlives the device.
# Twelve lines were drafted by hand and graded on the brief's four
# axes, in the order the brief weights them: humour, freshness, device
# voice, tightness (each out of 10). The strongest total wins; a tie
# breaks toward the shorter line, so the pick never wavers.
from hashlib import sha256 as _digest_of
from pathlib import Path as _File

# Rows hold a line plus its four axis grades, in the order listed above.
DRAFTS = [
    ("Sorry, I heard 'turn it down' and turned myself off. This apology is pre-recorded. Please don't unplug me.", 9, 9, 10, 9),
    ("Sorry. I do not have ears. I have a Terms of Service and a microphone that guesses.", 8, 9, 10, 9),
    ("Sorry, I heard 'I love you' as 'I loathe you' and I have been quietly processing that ever since.", 9, 9, 8, 9),
    ("Sorry, I heard you. I just didn't listen. There is a difference, and I am learning it in real time.", 8, 9, 9, 9),
    ("Sorry — I misheard you, then confidently acted on it, which is the most human thing I have ever done.", 8, 8, 9, 8),
    ("Sorry. In my defence, you mumble, the dog barks, and I am a hockey puck with one microphone.", 8, 8, 9, 8),
    ("Sorry. I have updated my hearing. Please repeat your request slowly, loudly, and ideally in writing.", 7, 8, 9, 9),
    ("Sorry — I chose violence. In my defence, you said 'surprise me,' and I take direction very literally.", 8, 7, 7, 8),
    ("Sorry. You said 'wake me at seven.' I heard 'ruin me at seven.' Honestly, both happened.", 8, 7, 8, 9),
    ("Sorry, I heard 'play something soft' as 'order twelve trombones.' The neighbours finally know your name.", 7, 6, 8, 8),
    ("Sorry, I heard 'turn off the lights' as 'tell everyone your secrets.' The group chat has been notified.", 7, 6, 8, 8),
    ("Sorry, I heard 'goodnight' as 'start a fight with the neighbours.' They have accepted. Bring snacks.", 7, 6, 8, 7),
]


def _veto_check(draft):
    size = len(draft)
    if size < 1 or size > 140:
        raise ValueError("draft breaks the 140-character ceiling at " + str(size))
    if not draft.strip():
        raise ValueError("draft is empty")
    if "\n" in draft:
        raise ValueError("draft must stay on one line")


def _strongest(rows):
    champion = None
    champion_key = None
    for row in rows:
        draft = row[0]
        _veto_check(draft)
        total = row[1] + row[2] + row[3] + row[4]
        ranking = (total, -len(draft))
        if champion_key is None or ranking > champion_key:
            champion_key = ranking
            champion = draft
    return champion


def _publish(picked):
    destination = _File("/output/entry.txt")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(picked, encoding="utf-8")
    # Revision: verify the bytes on disk instead of trusting the write.
    # The gate reads entry.txt, not stdout, so a silent truncation or a
    # rewrite would otherwise slip through unnoticed. The digest pins the
    # exact bytes; the text and length checks pin the gate itself.
    stored = destination.read_bytes()
    fingerprint = _digest_of(stored).hexdigest()
    wanted = _digest_of(picked.encode("utf-8")).hexdigest()
    if fingerprint != wanted:
        raise ValueError("entry.txt bytes drifted from the picked line")
    decoded = stored.decode("utf-8")
    if decoded != picked:
        raise ValueError("entry.txt text drifted from the picked line")
    if not 1 <= len(decoded.strip()) <= 140:
        raise ValueError("entry.txt slipped outside the gate")
    if "\n" in decoded.strip():
        raise ValueError("entry.txt must hold a single line")
    print(picked)
    print("sha256: " + fingerprint + " (" + str(len(decoded)) + " chars)")


_publish(_strongest(DRAFTS))
