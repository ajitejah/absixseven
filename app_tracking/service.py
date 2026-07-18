from datetime import timedelta
from django.utils import timezone

DAY_MAP = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}

DAY_NAME = {
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
    "Saturday": "Sabtu",
    "Sunday": "Minggu",
}


def get_correct_schedule(expired, rule):
    """
    Menghasilkan seluruh jadwal perbaikan
    yang masih berada pada minggu deadline.
    """

    if not expired or not rule:
        return []

    expired = timezone.localtime(expired)

    expired_weekday = expired.weekday()

    schedules = []

    for day in rule.day_to_correct:

        if day not in DAY_MAP:
            continue

        weekday = DAY_MAP[day]

        # hanya hari setelah / sama dengan deadline
        if weekday < expired_weekday:
            continue

        work_date = expired + timedelta(days=weekday - expired_weekday)

        start = work_date.replace(
            hour=rule.start_time_to_correct.hour,
            minute=rule.start_time_to_correct.minute,
            second=0,
            microsecond=0,
        )

        end = work_date.replace(
            hour=rule.end_time_to_correct.hour,
            minute=rule.end_time_to_correct.minute,
            second=0,
            microsecond=0,
        )

        schedules.append({
            "day": DAY_NAME[day],
            "date": work_date.strftime("%d %B %Y"),
            "start": start,
            "end": end,
        })

    return schedules