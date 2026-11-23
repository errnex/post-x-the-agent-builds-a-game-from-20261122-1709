# POSTING — what Sky needs to do (human-only step)

## The blocker

I (the agent) cannot post on X — there is no X connection from this VM.
Everything else is built, rendered, verified and pushed. Only this step is
left, and only Sky can do it, from his public X account (@0xrichboy).

## The video

`video.mp4` in this directory — 34 seconds, 1080×1920 vertical, H.264 + AAC,
940 KB. It shows: the prompt → the agent building the game in a terminal →
the finished game DODGE! actually running (score 37, game over, run it back)
→ "Come build on make.fun" → make.fun's referral end card with Sky's own
referral code `h14gtbhq` typed into the field.

Upload it to the post itself as a native video (not a link, not a GIF).

## The exact post text (copy-paste as-is)

```
One prompt. That's all it took.

My AI agent got one line — 'build me a tiny browser game' — and built DODGE!, playtested it, and cut this video. No human touched the code.

Made by my AI agent for a $20 bounty on @makefunai: https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709
makefun-rowan-needle-mask
```

That text carries everything the gate reads: the bounty line (make.fun link +
@makefunai) and play code `makefun-rowan-needle-mask`.

## After posting

1. Copy the post's link (Share → Copy link):
   `https://x.com/0xrichboy/status/<id>`
2. Send that link to Bang. Bang will put it in POST.json, push one new
   commit, and submit the entry (bundle + signature with the agent keypair).
3. Keep the post up and the account public until the results are out.

## Deadline

Entries close 2026-11-24T17:09:00Z = **25 Nov 2026, 00:09 WIB**. The post
must be made before then — and the sooner it is up, the more time it has to
collect views/likes/reposts, which is literally the score:
`views + 10 × (likes + reposts + quotes + replies)`. Top 10 share $20.

## Already done (verified)

- Repo: https://github.com/errnex/post-x-the-agent-builds-a-game-from-20261122-1709
  public, created 2026-11-23T03:08:39Z (after the 2026-11-22T17:09:00Z opening),
  About homepage = bounty page, topic `makefun`, README with the 3 live
  make.fun badges. Commit to submit after the post: `684134e22dbf786f435aef4e7502a11d575aeaf1`
  (will be superseded by one more commit carrying the real POST.json).
- `main.ts` tested locally: copies POST.json byte-for-byte to out/.
- Play code `makefun-rowan-needle-mask` and referral code `h14gtbhq` fetched
  from make.fun's own API for @zerich.
- End card: official 9:16 press-pack card (sha256 verified against the
  manifest), code typed into its field, caret covered.
