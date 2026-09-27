from dataclasses import dataclass, field


@dataclass
class Theatre:
    name: str
    location: str
    showtimes: list[str] = field(default_factory=list)
    rows: list[str] = field(default_factory=lambda: ["A", "B", "C", "D", "E", "F", "G", "H"])
    seats_per_row: int = 10
    premium_rows: list[str] = field(default_factory=lambda: ["A", "B"])