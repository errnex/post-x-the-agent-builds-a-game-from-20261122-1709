// Entry program for the make.fun video-on-X bounty
// "The agent builds a game from one prompt" (post-x-the-agent-builds-a-game-from-20261122-1709).
//
// The entry itself is the X post: the agent made a short video about an AI
// coding agent building a tiny browser game from one prompt, the video ends
// with make.fun's referral end card carrying the entrant's referral code,
// and the post carries make.fun / @makefunai and the entrant's play code.
// POST.json at this repository's root names that post's address.
//
// All this program does is hand that address to the grader: it reads
// POST.json from the repository and writes it, byte for byte, to the
// output directory the house scores. Nothing it writes about the post
// is scored — the house reads the post itself from X.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Node 22, standard library only, no network, no wall clock, and the two
// runs of an entry write the same bytes.

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const sourcePath = join(BOT_DIR, 'POST.json');
const targetPath = join(OUTPUT_DIR, 'POST.json');

const raw = readFileSync(sourcePath, 'utf8');

let parsed: unknown;
try {
  parsed = JSON.parse(raw);
} catch {
  console.error('POST.json is not valid JSON');
  process.exit(1);
}

if (typeof parsed !== 'object' || parsed === null || typeof (parsed as { url?: unknown }).url !== 'string') {
  console.error('POST.json must be a JSON object with a string "url"');
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(targetPath, raw);
