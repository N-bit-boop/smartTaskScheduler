# test_auth.py

from calendarss.google_auth import get_cal_service

service = get_cal_service()
print("Authenticated successfully:", service)