from collections.abc import Sequence


CHROMATIC_INTERVALS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
MAJOR_INTERVALS = (0, 2, 4, 5, 7, 9, 11)
NATURAL_MINOR_INTERVALS = (0, 2, 3, 5, 7, 8, 10)


# Stable internal identifiers; CLI and GUI derive their choices from this registry.
# All entries are twelve-tone equal-tempered pitch collections, not models of
# traditional performance practice or microtonal tuning.
SCALES = {
    "major": MAJOR_INTERVALS,
    "natural_minor": NATURAL_MINOR_INTERVALS,
    "dorian": (0, 2, 3, 5, 7, 9, 10),
    "phrygian": (0, 1, 3, 5, 7, 8, 10),
    "lydian": (0, 2, 4, 6, 7, 9, 11),
    "mixolydian": (0, 2, 4, 5, 7, 9, 10),
    "locrian": (0, 1, 3, 5, 6, 8, 10),
    "major_pentatonic": (0, 2, 4, 7, 9),
    "minor_pentatonic": (0, 3, 5, 7, 10),
    "blues": (0, 3, 5, 6, 7, 10),
    "harmonic_minor": (0, 2, 3, 5, 7, 8, 11),
    "melodic_minor": (0, 2, 3, 5, 7, 9, 11),
    "phrygian_dominant": (0, 1, 4, 5, 7, 8, 10),
    "double_harmonic": (0, 1, 4, 5, 7, 8, 11),
    "hungarian_minor": (0, 2, 3, 6, 7, 8, 11),
    "hirajoshi": (0, 2, 3, 7, 8),
    "in_sen": (0, 1, 5, 7, 10),
    "iwato": (0, 1, 5, 6, 10),
    "yo": (0, 2, 5, 7, 9),
    "whole_tone": (0, 2, 4, 6, 8, 10),
    "diminished_whole_half": (0, 2, 3, 5, 6, 8, 9, 11),
    "diminished_half_whole": (0, 1, 3, 4, 6, 7, 9, 10),
}


def build_scale_offsets(
    intervals: Sequence[int],
    count: int,
    *,
    start_octave: int = 0,
) -> list[int]:
    """Expand scale intervals into semitone offsets across octaves."""
    if count <= 0:
        raise ValueError("Count must be greater than zero")

    if not intervals:
        raise ValueError("Intervals must not be empty")

    normalized = tuple(intervals)

    if any(
        isinstance(interval, bool) or not isinstance(interval, int)
        for interval in normalized
    ):
        raise TypeError("Scale intervals must be integers")

    if any(interval < 0 or interval >= 12 for interval in normalized):
        raise ValueError("Scale intervals must be between 0 and 11")

    if tuple(sorted(set(normalized))) != normalized:
        raise ValueError(
            "Scale intervals must be unique and in ascending order"
        )

    offsets: list[int] = []
    base = start_octave * 12

    for index in range(count):
        octave, degree = divmod(index, len(normalized))
        offsets.append(base + octave * 12 + normalized[degree])

    return offsets
