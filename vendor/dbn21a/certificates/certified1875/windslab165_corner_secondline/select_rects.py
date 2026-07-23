#!/usr/bin/env /usr/bin/python3
"""
select_rects.py -- hash-seeded deterministic rectangle selection for the
winding-rectangle second-line audit (spotgrid protocol, windnum extension).

seed = SHA256(<tloop log bytes>); selection = random.Random(int(seed,16))
choosing K rectangles from {2..R_last} (rectangle 1 is ALWAYS included as the
t=0 exact anchor -- its t field is exactly 0, so the audit there carries no
display-rounding slack at all), plus one hash-chosen corner index per
selected rectangle (0:(X,y0) 1:(X+1,y0) 2:(X,1) 3:(X+1,1); rectangle 1 is
audited at BOTH bottom corners 0 and 1).
Prints: rect_index, t_printed (exact decimal string), min_printed, ddt, ddz,
corner index. The producer cannot anticipate the selection (it depends on
the log's own bytes); anyone can reproduce it.
"""
import sys, re, hashlib, random

path = sys.argv[1]
K = int(sys.argv[2]) if len(sys.argv) > 2 else 2
raw = open(path, "rb").read()
seed = hashlib.sha256(raw).hexdigest()
rng = random.Random(int(seed, 16))

rects = {}
for line in raw.decode().splitlines():
    m = re.match(r"Rectangle\((\d+)\)\s*:\s*(.*)", line)
    if m:
        idx = int(m.group(1))
        f = [x.strip() for x in m.group(2).split(",")]
        # fields: t, ddt-bound, ddz-bound, winding, min-mesh |f|, meshcount
        rects[idx] = f
R = max(rects)
assert sorted(rects) == list(range(1, R + 1)), "non-contiguous rectangles"
picks = sorted(rng.sample(range(2, R + 1), K))
corners = {p: rng.randrange(4) for p in picks}
# s9 extension: the FINAL rectangle R is ALWAYS included too (t-march
# boundary anchor, t closest to the slab top); its corner index is drawn
# NEXT from the same seeded stream, so it is just as unforgeable.
corners[R] = rng.randrange(4)
print(f"seed_sha256 {seed}")
print(f"rect_count {R}")
for p in [1] + picks + ([R] if R not in picks else []):
    f = rects[p]
    cs = "0,1" if p == 1 else str(corners[p])
    print(f"rect {p} t {f[0]} ddt {f[1]} ddz {f[2]} wind {f[3]} min {f[4]} mesh {f[5]} corners {cs}")
