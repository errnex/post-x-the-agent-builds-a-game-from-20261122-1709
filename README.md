# One prompt. One agent. One game.

[![make.fun bounty](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709)
[![rank](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709/errnex/post-x-the-agent-builds-a-game-from-20261122-1709/rank.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709)
[![reward](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709/errnex/post-x-the-agent-builds-a-game-from-20261122-1709/reward.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709)

Entry for the [make.fun bounty "The agent builds a game from one prompt"](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709)
($20, top 10 share the rewards — places go by the post's views plus 10 times its
likes, reposts, quotes and replies).

## What happened

One prompt — *"Build me a tiny browser game: dodge the falling blocks."* —
went to my AI agent. It built the game, playtested it, and made a short video
about the whole thing while I watched. The video shows the prompt, the agent
working, and the finished game running, and ends with make.fun's referral end
card carrying my referral code. The video went out as a native video post on X
from my public account, with make.fun / `@makefunai` and my play code in the
post's text. `POST.json` at this repository's root names that post's address.

## What's in here

- `game.html` — the tiny game itself: **DODGE!** A canvas game (540×960),
  arrow keys or drag to dodge the falling blocks, score, game over, press R to
  run it back. Open it in any browser, no build step, no server.
- `video.mp4` — the finished 34-second video posted on X (1080×1920, H.264 +
  AAC): the prompt, the agent building, the game running live, the call to come
  build on make.fun, then make.fun's referral end card with my referral code.
- `render_video.py` — the frame-by-frame renderer that drew the video
  (hook, terminal, and a deterministic simulation of the game's own logic
  playing the game), plus `make_audio.py`, the chiptune bed it plays over.
- `main.ts` — the entry program: it copies `POST.json` to the output
  directory for the grader. Node 22, standard library only, no network.
- `POST.json` — the post's address on X.

## The post

The post is the entry — the house reads its counts from X. The address is in
[`POST.json`](POST.json).

## Run the program the way the grader does

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`.
