import random

_booked_seats_store: dict[tuple[str, str], set[str]] = {}


def get_booked_seats(theatre_name: str, time_str: str, all_seat_ids: list[str]) -> set[str]:
    """Return the set of booked seat_ids for a given theatre+showtime.
    On first request for a given key, generates a small random set of
    pre-booked seats (simulating other customers) and stores it — every
    subsequent call for the same key returns the same (growing) set."""
    key = (theatre_name, time_str)

    if key not in _booked_seats_store:
        sample_size = max(1, len(all_seat_ids) // 10)
        _booked_seats_store[key] = set(random.sample(all_seat_ids, sample_size))

    return _booked_seats_store[key]


def book_seats(theatre_name: str, time_str: str, seat_ids: list[str]):
    """Mark the given seat_ids as booked for a theatre+showtime, so they
    stay booked on future visits within this session."""
    key = (theatre_name, time_str)
    _booked_seats_store.setdefault(key, set()).update(seat_ids)