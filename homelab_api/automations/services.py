import asyncio
import random
import shlex
from asyncio import subprocess
from pathlib import Path

AUDIO_EXTENSIONS = {'.mp3', '.mp4', '.wav', '.ogg', '.flac', '.m4a', '.aac'}


def select_random_music(directory: str) -> str:
    music_dir = Path(directory)

    if not music_dir.is_dir():
        raise ValueError(f'{directory} is not a valid directory')

    files = [f for f in music_dir.iterdir() if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS]

    if not files:
        raise FileNotFoundError(f'No audio files found in {directory}')

    selected = random.choice(files)  # noqa
    return shlex.quote(str(selected))


async def get_music_duration(music_path: str) -> int:
    command = [
        'ffprobe',
        '-v',
        'error',
        '-show_entries',
        'format=duration',
        '-of',
        'default=noprint_wrappers=1:nokey=1',
        music_path,
    ]

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )

    stdout, _ = await process.communicate()

    return int(float(stdout.decode().strip()))
