import random
import datetime

def weekly_job():
    today = datetime.date.today()
    year, week, weekday = today.isocalendar()
    # weekday: 월=1 ... 일=7

    random.seed(f"{year}-{week}")
    weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    chosen_index = random.randrange(5)
    chosen_day = weekdays[chosen_index]

    # 오늘이 선택된 요일인지 체크
    if weekday == chosen_index + 1:
        print("✅ 이번 주 실행하는 날입니다:", chosen_day)
        return True
    else:
        print("⏭ 아직 실행 안 함")
        print("이번 주 선택된 요일:", chosen_day)
        return False


if __name__ == "__main__":
    weekly_job()
