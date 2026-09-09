from dataclasses import dataclass, field

@dataclass
class Theatre:
    name: str
    location: str
    showtimes: list[str] = field(default_factory=list)