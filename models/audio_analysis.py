from .tonality import Tonality


class AudioAnalysis:
    def __init__(
        self,
        duration,
        num_samples,
        sample_md5,
        offset_seconds,
        window_seconds,
        analysis_sample_rate,
        analysis_channels,
        end_of_fade_in,
        start_of_fade_out,
        loudness,
        tempo,
        tempo_confidence,
        time_signature,
        time_signature_confidence,
        key,
        key_confidence,
        mode,
        mode_confidence,
        codestring,
        code_version,
        echoprintstring,
        echoprint_version,
        synchstring,
        synch_version,
        rhythmstring,
        rhythm_version,
    ) -> None:
        self.duration = duration
        self.num_samples = num_samples
        self.sample_md5 = sample_md5
        self.offset_seconds = offset_seconds
        self.window_seconds = window_seconds
        self.analysis_sample_rate = analysis_sample_rate
        self.analysis_channels = analysis_channels
        self.end_of_fade_in = end_of_fade_in
        self.start_of_fade_out = start_of_fade_out
        self.loudness = loudness
        self.tempo = tempo
        self.tempo_confidence = tempo_confidence
        self.time_signature = time_signature
        self.time_signature_confidence = time_signature_confidence
        self.key = key
        self.key_confidence = key_confidence
        self.mode = mode
        self.mode_confidence = mode_confidence
        self.codestring = codestring
        self.code_version = code_version
        self.echoprintstring = echoprintstring
        self.echoprint_version = echoprint_version
        self.synchstring = synchstring
        self.synch_version = synch_version
        self.rhythmstring = rhythmstring
        self.rhythm_version = rhythm_version

    @property
    def tonality(self):
        return Tonality(
            key=self.key,
            key_confidence=self.key_confidence,
            mode=self.mode,
            mode_confidence=self.mode_confidence,
        )
