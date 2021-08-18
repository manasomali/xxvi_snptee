import collections
import contextlib
import sys
import wave
import webrtcvad
import os
import glob
from pydub import AudioSegment
from auditok import split


def read_wave(path):
    """Reads a .wav file.
    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate


def write_wave(path, audio, sample_rate):
    """Writes a .wav file.
    Takes path, PCM audio data, and sample rate.
    """
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)


class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration


def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from PCM audio data.
    Takes the desired frame duration in milliseconds, the PCM data, and
    the sample rate.
    Yields Frames of the requested duration.
    """
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


def vad_collector(sample_rate, frame_duration_ms,
                  padding_duration_ms, vad, frames):
    """Filters out non-voiced audio frames.
    Given a webrtcvad.Vad and a source of audio frames, yields only
    the voiced audio.
    Uses a padded, sliding window algorithm over the audio frames.
    When more than 90% of the frames in the window are voiced (as
    reported by the VAD), the collector triggers and begins yielding
    audio frames. Then the collector waits until 90% of the frames in
    the window are unvoiced to detrigger.
    The window is padded at the front and back to provide a small
    amount of silence or the beginnings/endings of speech around the
    voiced frames.
    Arguments:
    sample_rate - The audio sample rate, in Hz.
    frame_duration_ms - The frame duration in milliseconds.
    padding_duration_ms - The amount to pad the window, in milliseconds.
    vad - An instance of webrtcvad.Vad.
    frames - a source of audio frames (sequence or generator).
    Returns: A generator that yields PCM audio data.
    """
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    # We use a deque for our sliding window/ring buffer.
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    # We have two states: TRIGGERED and NOTTRIGGERED. We start in the
    # NOTTRIGGERED state.
    triggered = False

    voiced_frames = []
    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)

        sys.stdout.write('1' if is_speech else '0')
        if not triggered:
            ring_buffer.append((frame, is_speech))
            num_voiced = len([f for f, speech in ring_buffer if speech])
            # If we're NOTTRIGGERED and more than 90% of the frames in
            # the ring buffer are voiced frames, then enter the
            # TRIGGERED state.
            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                sys.stdout.write('+(%s)' % (ring_buffer[0][0].timestamp,))
                # We want to yield all the audio we see from now until
                # we are NOTTRIGGERED, but we have to start with the
                # audio that's already in the ring buffer.
                for f, s in ring_buffer:
                    voiced_frames.append(f)
                ring_buffer.clear()
        else:
            # We're in the TRIGGERED state, so collect the audio data
            # and add it to the ring buffer.
            voiced_frames.append(frame)
            ring_buffer.append((frame, is_speech))
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])
            # If more than 90% of the frames in the ring buffer are
            # unvoiced, then enter NOTTRIGGERED and yield whatever
            # audio we've collected.
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
                triggered = False
                yield b''.join([f.bytes for f in voiced_frames])
                ring_buffer.clear()
                voiced_frames = []
    if triggered:
        sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
    sys.stdout.write('\n')
    # If we have any leftover voiced audio when we run out of input,
    # yield it.
    if voiced_frames:
        yield b''.join([f.bytes for f in voiced_frames])


def main():
    inputdirectory = os.path.dirname(os.path.realpath(__file__)) + '\input'
    outputdirectory = os.path.dirname(os.path.realpath(__file__)) + '\output'
    
    directory = os.path.dirname(os.path.realpath(__file__)) + '\input\*.wav'
    caminhos = (glob.glob(directory))
    
    decide = input('Remoção de silencio (s/n)? ')
    if decide == 's':
        inputdirectory = os.path.dirname(os.path.realpath(__file__)) + '\semsilencio'
        agressividade = input('Informe a agressividade [0 a 3]: ')
        # remove silencio
        for caminho in caminhos:
            audio, sample_rate = read_wave(caminho)
            vad = webrtcvad.Vad(int(agressividade))
            frames = frame_generator(30, audio, sample_rate)
            frames = list(frames)
            segments = vad_collector(sample_rate, 30, 300, vad, frames)
            concataudio = [segment for segment in segments]
            joinedaudio = b"".join(concataudio)
            write_wave(caminho.replace('input', 'semsilencio'), joinedaudio, sample_rate)

    # divide os audios em regioes e salva cada regiao de cada audio para uma pasta separada
    nomes_audios = []
    for nome in os.listdir(inputdirectory):
        if ".wav" in nome:
            nomes_audios.append(nome)
            
    for nome_audio in nomes_audios:
        cont=0
        audio_regioes = split(os.path.join(inputdirectory, nome_audio),
            min_dur=0.1,     # minimum duration of a valid audio event in seconds
            max_dur=20,      # maximum duration of an event
            max_silence=0.2  # maximum duration of tolerated continuous silence within an event
        )
        os.makedirs(os.path.join(outputdirectory,nome_audio.replace('.wav', '')), exist_ok=True)
        for region in audio_regioes:
            region.save(os.path.join(outputdirectory,nome_audio.replace('.wav', ''))+'/'+nome_audio.replace('.wav', '_')+str(cont)+".wav")
            cont=cont+1

    # adiciona xs de silencio no inicio dos audios para melhor processamento do wit
    silencio_dur = input('Informe o silencio a ser adicionado (seg): ')
    if float(silencio_dur) != 0:
        # pegando caminho e nomes dos audios - saida
        diretorios_audios_saida = []
        for path, subdirs, files in os.walk(outputdirectory):
            for name in files:
                if ".wav" in name:
                    diretorios_audios_saida.append(os.path.join(path, name))
                
        silent_segment = AudioSegment.silent(duration=float(silencio_dur)*1000)
        cont=0
        for audio_saida in diretorios_audios_saida:
            audio = AudioSegment.from_wav(audio_saida)
            final_audio = silent_segment + audio
            final_audio.export(audio_saida, format="wav")


if __name__ == '__main__':
    main()




