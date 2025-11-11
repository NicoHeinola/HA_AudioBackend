import io
from pydub.effects import speedup
from pydub import AudioSegment


class AudioMixer:
    @staticmethod
    def speed_up_audio(
        input_audio_bytes: bytes,
        speed: float,
        output_format: str = "wav",
    ) -> bytes:
        """Speed up audio file using ffmpeg.

        This accepts any format supported by ffmpeg (mp3, mpeg, wav, etc.).
        It decodes the input from bytes using `AudioSegment.from_file` and
        exports the sped-up audio in `output_format` (default: 'wav').
        """
        if not input_audio_bytes:
            raise ValueError("No input audio bytes provided")

        buf = io.BytesIO(input_audio_bytes)

        try:
            # Let ffmpeg/pydub detect the input format from the bytes
            audio = AudioSegment.from_file(buf, format=None)
        except Exception as exc:  # keep broad to wrap pydub/ffmpeg errors
            raise ValueError("Could not decode input audio data") from exc

        sped_up_audio: AudioSegment = speedup(audio, playback_speed=speed)

        out = io.BytesIO()
        try:
            sped_up_audio.export(out, format=output_format)
        except Exception as exc:
            raise ValueError("Failed to export sped up audio") from exc

        data = out.getvalue()
        if not data:
            raise ValueError("Export produced no data")

        return data
