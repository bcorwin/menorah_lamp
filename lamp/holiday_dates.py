from datetime import datetime, timedelta

chanukah_start_dates = [
    "2022-12-18",
    "2023-12-07",
    "2024-12-25",
    "2025-12-14",
    "2026-12-04",
    "2027-12-24",
]

chanukah_nights = {
    (datetime.strptime(d, "%Y-%m-%d") + timedelta(days=i)).date(): i + 1
    for d in chanukah_start_dates
    for i in range(8)
}

# Christmas eve
christmas_dates = [
    datetime.strptime(f"{y}-12-24", "%Y-%m-%d").date()
    for y in range(2022, 2028)
]
# Christmas date
christmas_dates += [
    datetime.strptime(f"{y}-12-25", "%Y-%m-%d").date()
    for y in range(2022, 2028)
]
# Boxing day
christmas_dates += [
    datetime.strptime(f"{y}-12-26", "%Y-%m-%d").date()
    for y in range(2022, 2028)
]

shabbat_dates = [
    (datetime.strptime("2022-12-02", "%Y-%m-%d") + timedelta(days=i)).date()
    for i in range(0, 365 * 7, 7)
]
