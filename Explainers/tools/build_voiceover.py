# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "kokoro-onnx>=0.4.0",
#   "soundfile>=0.12.1",
#   "numpy>=1.26.0",
# ]
# ///
"""
Offline Local Neural Voiceover Builder (Kokoro-82M int8 ONNX).

Usage:
  1. Generate quick female voice audition samples (downloads ~115 MB model once):
       uv run Explainers/tools/build_voiceover.py --samples

  2. Build synchronized voiceover.wav + voiceover_bundle.js for an explainer:
       uv run Explainers/tools/build_voiceover.py --manifest Explainers/01_async_concurrency/narration.json --voice af_heart
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import time
import urllib.request
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

REPO_EXPL_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = REPO_EXPL_DIR / ".tts_models"

MODEL_URLS = [
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx",
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/kokoro-v1.0.int8.onnx",
]
VOICES_URLS = [
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin",
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/voices-v1.0.bin",
]


def download_with_fallback(urls: list[str], dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 1_000_000:
        print(f"[cached] {dest.name} ({dest.stat().st_size / (1024 * 1024):.1f} MB)")
        return

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    last_err: Exception | None = None

    for url in urls:
        try:
            print(f"[downloading] {dest.name} from {url} ...")
            req = urllib.request.Request(url, headers={"User-Agent": "Jarvis-Explainer-TTS/1.0"})
            with urllib.request.urlopen(req, timeout=120) as resp, open(tmp, "wb") as out:
                while True:
                    chunk = resp.read(1024 * 256)
                    if not chunk:
                        break
                    out.write(chunk)
            tmp.replace(dest)
            print(f"[saved] {dest.name} ({dest.stat().st_size / (1024 * 1024):.1f} MB)")
            return
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            if tmp.exists():
                tmp.unlink()
            print(f"  -> URL attempt failed ({exc}), trying fallback...")

    raise RuntimeError(f"Could not download {dest.name}: {last_err}")


def load_kokoro() -> Kokoro:
    model_path = MODELS_DIR / "kokoro-v1.0.int8.onnx"
    voices_path = MODELS_DIR / "voices-v1.0.bin"
    download_with_fallback(MODEL_URLS, model_path)
    download_with_fallback(VOICES_URLS, voices_path)
    return Kokoro(str(model_path), str(voices_path))


def generate_samples(out_dir: Path) -> None:
    kokoro = load_kokoro()
    out_dir.mkdir(parents=True, exist_ok=True)

    sample_line = (
        "When three users connect at once, a single thread interleaves their sockets "
        "so nobody gets stuck waiting behind a slow request."
    )
    candidates = [
        ("af_heart", "en-us", "Warm American Female"),
        ("af_bella", "en-us", "Expressive American Female"),
        ("bf_emma", "en-gb", "Calm British Editorial Female"),
    ]

    for voice_id, lang, desc in candidates:
        t0 = time.perf_counter()
        samples, sr = kokoro.create(sample_line, voice=voice_id, speed=1.0, lang=lang)
        elapsed = time.perf_counter() - t0
        wav_path = out_dir / f"sample_{voice_id}.wav"
        sf.write(str(wav_path), samples, sr, subtype="PCM_16")
        dur = len(samples) / sr
        print(f"[ok] {voice_id} ({desc}): {dur:.2f}s audio synthesized in {elapsed:.2f}s -> {wav_path}")


def build_from_manifest(manifest_path: Path, voice_override: str | None) -> None:
    cfg = json.loads(manifest_path.read_text(encoding="utf-8"))
    voice_id = voice_override or cfg.get("voice", "af_heart")
    lang = "en-gb" if voice_id.startswith("b") else "en-us"
    speed = float(cfg.get("speed", 1.0))
    lead_pad = float(cfg.get("lead_in_sec", 0.45))
    gap_pad = float(cfg.get("gap_between_cues_sec", 0.65))
    tail_pad = float(cfg.get("tail_out_sec", 1.0))

    kokoro = load_kokoro()
    sr = 24000
    stitched_chunks: list[np.ndarray] = [np.zeros(int(sr * lead_pad), dtype=np.float32)]
    cursor = lead_pad
    resolved_cues = []

    t_start = time.perf_counter()
    for idx, item in enumerate(cfg["cues"], start=1):
        text = item["text"].strip()
        samples, sr = kokoro.create(text, voice=voice_id, speed=speed, lang=lang)
        samples = np.asarray(samples, dtype=np.float32)
        voice_dur = len(samples) / sr
        extra_hold = float(item.get("hold_after_sec", gap_pad))
        cue_start = round(cursor, 3)
        cue_voice_end = round(cursor + voice_dur, 3)
        cue_end = round(cursor + voice_dur + extra_hold, 3)

        resolved_cues.append({
            "id": item.get("id", idx),
            "act": item.get("act", idx),
            "start": cue_start,
            "voiceEnd": cue_voice_end,
            "end": cue_end,
            "text": text,
        })

        stitched_chunks.append(samples)
        stitched_chunks.append(np.zeros(int(sr * extra_hold), dtype=np.float32))
        cursor = cue_end
        print(f"  Cue {idx:02d} [{cue_start:5.2f}s -> {cue_end:5.2f}s]: {text[:64]}...")

    stitched_chunks.append(np.zeros(int(sr * tail_pad), dtype=np.float32))
    total_duration = round(cursor + tail_pad, 3)
    full_audio = np.concatenate(stitched_chunks)

    out_dir = manifest_path.parent
    wav_path = out_dir / "voiceover.wav"
    sf.write(str(wav_path), full_audio, sr, subtype="PCM_16")

    # Also write file:// CORS-safe JS bundle so double-clicking index.html works offline + exports MP4!
    buf = io.BytesIO()
    sf.write(buf, full_audio, sr, format="WAV", subtype="PCM_16")
    b64_wav = base64.b64encode(buf.getvalue()).decode("ascii")

    bundle_payload = {
        "voice": voice_id,
        "sampleRate": sr,
        "duration": total_duration,
        "cues": resolved_cues,
        "wavBase64": b64_wav,
    }
    bundle_path = out_dir / "voiceover_bundle.js"
    bundle_path.write_text(
        "// Auto-generated by Explainers/tools/build_voiceover.py — do not commit to Git\n"
        f"window.VOICEOVER_DATA = {json.dumps(bundle_payload, ensure_ascii=False)};\n",
        encoding="utf-8",
    )

    elapsed = time.perf_counter() - t_start
    print(
        f"\n[done] Synthesized {total_duration:.2f}s voiceover ({voice_id}) in {elapsed:.2f}s!\n"
        f"  -> {wav_path} ({wav_path.stat().st_size / (1024 * 1024):.2f} MB)\n"
        f"  -> {bundle_path}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline Kokoro-82M int8 voiceover builder")
    parser.add_argument("--samples", action="store_true", help="Generate 3 female voice sample WAVs")
    parser.add_argument("--samples-dir", type=Path, default=MODELS_DIR / "samples")
    parser.add_argument("--manifest", type=Path, help="Path to explainer narration.json")
    parser.add_argument("--voice", type=str, default=None, help="Override voice ID (e.g., af_heart, bf_emma)")
    args = parser.parse_args()

    if args.samples:
        generate_samples(args.samples_dir)
    elif args.manifest:
        build_from_manifest(args.manifest, args.voice)
    else:
        parser.error("Provide either --samples or --manifest <path>")


if __name__ == "__main__":
    main()
