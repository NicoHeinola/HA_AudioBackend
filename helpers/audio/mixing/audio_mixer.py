from pydub.effects import speedup
from pydub import AudioSegment


class AudioMixer:
    @staticmethod
    def speed_up_audio(
        input_audio_bytes: bytes,
        speed: float,
    ) -> bytes:
        """Speed up audio file using ffmpeg."""
        audio = AudioSegment(data=input_audio_bytes)
        sped_up_audio: AudioSegment = speedup(audio, playback_speed=speed)

        raw_data: bytes | None = sped_up_audio.raw_data

        if not raw_data:
            raise ValueError("Failed to speed up audio.")

        return raw_data
