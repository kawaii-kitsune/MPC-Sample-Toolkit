from pathlib import Path

import pytest

import mpctk.cli as cli
from mpctk.music import (
    LAYOUT_CHROMATIC_KEYBOARD,
    LAYOUT_SCALE_PADS,
)


def test_generate_scale_pad_command(monkeypatch, tmp_path):
    captured = {}

    def fake_generate_project_package(**kwargs):
        captured.update(kwargs)

        return (
            tmp_path / "D Minor Kit.xpj",
            tmp_path / "D Minor Kit_[ProjectData]",
        )

    monkeypatch.setattr(
        cli,
        "generate_project_package",
        fake_generate_project_package,
    )

    result = cli.main(
        [
            "generate",
            "Sample.wav",
            "--template",
            "Template.xpj",
            "--source-root",
            "C",
            "--target-root",
            "D",
            "--layout",
            "scale-pads",
            "--scale",
            "natural-minor",
            "--pads",
            "16",
            "--bank",
            "B",
            "--start-octave",
            "-1",
            "--name",
            "D Minor Kit",
            "--output",
            str(tmp_path),
        ]
    )

    assert result == 0

    assert captured["source_wav"] == Path("Sample.wav")
    assert captured["template_path"] == Path("Template.xpj")
    assert captured["destination_dir"] == tmp_path
    assert captured["project_name"] == "D Minor Kit"
    assert captured["start_bank"] == "B"
    assert captured["start_pad"] == 1

    spec = captured["spec"]

    assert spec.source_root == "C"
    assert spec.target_root == "D"
    assert spec.layout == LAYOUT_SCALE_PADS
    assert spec.scale == "natural_minor"
    assert spec.pads == 16
    assert spec.start_octave == -1


def test_generate_chromatic_command(monkeypatch, tmp_path):
    captured = {}

    def fake_generate_project_package(**kwargs):
        captured.update(kwargs)

        return (
            tmp_path / "Chromatic.xpj",
            tmp_path / "Chromatic_[ProjectData]",
        )

    monkeypatch.setattr(
        cli,
        "generate_project_package",
        fake_generate_project_package,
    )

    result = cli.main(
        [
            "generate",
            "Chromatic.wav",
            "--template",
            "Template.xpj",
            "--source-root",
            "C",
            "--target-root",
            "C",
            "--layout",
            "chromatic-keyboard",
            "--pads",
            "16",
            "--output",
            str(tmp_path),
        ]
    )

    assert result == 0

    spec = captured["spec"]

    assert spec.layout == LAYOUT_CHROMATIC_KEYBOARD
    assert spec.scale is None
    assert captured["project_name"] == "Chromatic"


def test_scale_pads_requires_scale(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(
        cli,
        "generate_project_package",
        lambda **kwargs: None,
    )

    with pytest.raises(SystemExit) as exc:
        cli.main(
            [
                "generate",
                "Sample.wav",
                "--template",
                "Template.xpj",
                "--source-root",
                "C",
                "--target-root",
                "C",
                "--layout",
                "scale-pads",
                "--output",
                str(tmp_path),
            ]
        )

    assert exc.value.code == 2


def test_cli_rejects_invalid_bank():
    with pytest.raises(SystemExit) as exc:
        cli.main(
            [
                "generate",
                "Sample.wav",
                "--template",
                "Template.xpj",
                "--source-root",
                "C",
                "--target-root",
                "C",
                "--layout",
                "chromatic-keyboard",
                "--bank",
                "Z",
                "--output",
                "/tmp",
            ]
        )

    assert exc.value.code == 2


@pytest.mark.parametrize("scale, expected", [
    ("dorian", [2, 4, 5, 7, 9, 11, 12, 14]),
    ("minor-pentatonic", [2, 5, 7, 9, 12, 14, 17, 19]),
    ("diminished-half-whole", [2, 3, 5, 6, 8, 9, 11, 12]),
])
def test_cli_expanded_scale_reaches_generation(monkeypatch, tmp_path, scale, expected):
    captured = {}

    def generate(**kwargs):
        captured.update(kwargs)
        return tmp_path / "test.xpj", tmp_path / "test_[ProjectData]"

    monkeypatch.setattr(cli, "generate_project_package", generate)
    assert cli.main([
        "generate", "sample.wav", "--template", "template.xpj",
        "--source-root", "C", "--target-root", "D", "--layout", "scale-pads",
        "--scale", scale, "--pads", "8", "--output", str(tmp_path),
    ]) == 0
    assert captured["spec"].build_offsets() == expected
