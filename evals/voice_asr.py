#!/usr/bin/env python3
"""
Speech round trip for the voice cases.

Each case's **Prompt:** is spoken by a text-to-speech model, background noise
is mixed in, and a speech recognition model transcribes the result. The
transcript is written into the case as a **Heard:** line, right after the
prompt. `run.py --cases voice --input heard` then sends the model what a voice
assistant would actually receive, recognition errors included.

The voice and the noise are fixed per case (seeded by the case title), so a
rerun with the same models gives the same audio. Speech recognition itself may
still vary a little between runs; the transcript in the file is the one used.

    export OPENAI_BASE_URL=https://your-endpoint/v1 OPENAI_API_KEY=...
    python evals/voice_asr.py evals/voice/voice-dev.md \
        --tts-model "..." --asr-model "..." --snr 8

The script prints counts only, never case text, so it can be run on held-out
files without showing them.
"""

from __future__ import annotations

import argparse
import array
import hashlib
import io
import math
import random
import re
import sys
import wave
from pathlib import Path

VOICES = ["Vivian", "Ryan", "Aiden", "Serena"]


def _seed(text: str) -> int:
    return int(hashlib.sha256(text.encode()).hexdigest()[:8], 16)


def add_noise(wav_bytes: bytes, snr_db: float, seed: int) -> bytes:
    """Mix low-passed (brown-ish) noise into 16-bit mono PCM at the given SNR."""
    with wave.open(io.BytesIO(wav_bytes)) as w:
        params = w.getparams()
        if params.sampwidth != 2 or params.nchannels != 1:
            raise ValueError("expected 16-bit mono audio")
        samples = array.array("h", w.readframes(params.nframes))
    rng = random.Random(seed)
    # Room-like noise: white noise through a one-pole low-pass, plus a slow hum.
    noise, prev = [], 0.0
    for i in range(len(samples)):
        prev = 0.97 * prev + 0.03 * rng.gauss(0, 1)
        noise.append(prev + 0.02 * math.sin(2 * math.pi * 120 * i / params.framerate))
    p_sig = sum(x * x for x in samples) / max(1, len(samples))
    p_noise = sum(x * x for x in noise) / max(1, len(noise))
    if p_sig == 0 or p_noise == 0:
        return wav_bytes
    k = math.sqrt(p_sig / (p_noise * 10 ** (snr_db / 10)))
    mixed = array.array("h", (max(-32768, min(32767, int(s + k * n))) for s, n in zip(samples, noise)))
    out = io.BytesIO()
    with wave.open(out, "wb") as w:
        w.setparams(params)
        w.writeframes(mixed.tobytes())
    return out.getvalue()


def round_trip(client, text: str, title: str, tts_model: str, asr_model: str, snr: float) -> str:
    seed = _seed(title)
    voice = VOICES[seed % len(VOICES)]
    audio = client.audio.speech.create(model=tts_model, voice=voice, input=text).content
    if snr > 0:
        audio = add_noise(audio, snr, seed)
    result = client.audio.transcriptions.create(model=asr_model, file=("speech.wav", audio, "audio/wav"))
    return " ".join(result.text.split())


PROMPT_RE = re.compile(r'^(\*\*Prompt:\*\*\s*"?)(.*?)("?\s*)$', re.M)


def process(path: Path, client, tts_model: str, asr_model: str, snr: float, force: bool) -> tuple[int, int]:
    text = path.read_text()
    # Drop earlier transcripts when redoing them.
    if force:
        text = re.sub(r"\n\n\*\*Heard:\*\* [^\n]*", "", text)
    blocks = re.split(r"(?=\n### \d+\.)", text)
    done = changed = 0
    for i, block in enumerate(blocks):
        heading = re.match(r"\s*### \d+\.\s+(.+)", block)
        m = PROMPT_RE.search(block)
        if not heading or not m:
            continue
        done += 1
        if "**Heard:**" in block:
            continue
        heard = round_trip(client, m.group(2).strip().strip('"'), heading.group(1).strip(),
                           tts_model, asr_model, snr)
        heard = heard.replace('"', "'")
        blocks[i] = block[: m.end()] + f'\n\n**Heard:** "{heard}"' + block[m.end():]
        changed += 1
        print(f"  {changed} transcribed", file=sys.stderr, flush=True)
    path.write_text("".join(blocks))
    return done, changed


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("files", nargs="+", type=Path)
    p.add_argument("--tts-model", required=True)
    p.add_argument("--asr-model", required=True)
    p.add_argument("--snr", type=float, default=8.0,
                   help="Signal-to-noise ratio in dB for the added noise; 0 adds none (default: 8)")
    p.add_argument("--force", action="store_true", help="Redo cases that already have a **Heard:** line")
    args = p.parse_args(argv)
    from openai import OpenAI
    client = OpenAI()
    for f in args.files:
        done, changed = process(f, client, args.tts_model, args.asr_model, args.snr, args.force)
        print(f"{f}: {done} cases, {changed} transcribed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
