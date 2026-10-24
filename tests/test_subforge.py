from subforge import SubtitleSegment, format_vtt, format_srt, wrap_line_42chars

def test_wrap_line():
    long_text = "Esta é uma frase deliberadamente longa desenvolvida para ultrapassar o limite normal de quarenta e dois caracteres em legendas."
    res = wrap_line_42chars(long_text, max_chars=42)
    lines = res.split("\n")
    assert len(lines) <= 2
    for l in lines:
        assert len(l) <= 42

def test_format_vtt():
    segs = [SubtitleSegment(1.5, 4.25, "Olá, bem-vindo ao curso.")]
    vtt = format_vtt(segs)
    assert "WEBVTT" in vtt
    assert "00:00:01.500 --> 00:00:04.250" in vtt
    assert "Olá, bem-vindo ao curso." in vtt
