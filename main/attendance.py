import pytz
import main.share as share
import logging as log
from main.bemo import Bemo
from datetime import date, datetime
class Attendance:

  def __init__(self):
      self.bemo = Bemo()

  # Doing attendance
  def attend(self, force_run=False):
    today = date.today() #datetime.strptime('20210729', "%Y%m%d").date()
    attendance_today = {}
    # Load attendance list
    attendances = self.bemo.load_attendance()
    if attendances:
      # Look for each record to find the today's attendance
      records = attendances['result']['records']
      for i in range(0, len(records)):
        record = records[i]
        check_in = self.__convert_tz(record['check_in'])
        check_out = self.__convert_tz(record['check_out'])
        if check_in.date() == today:
          attendance_today = record
          break
      
      # If today's attendance exists then execute checkout
      if attendance_today:
        if force_run or self.__is_out_working_time():
          log.info('Check out')
          attendance = self.bemo.attendance_manual()
          check_in = self.__convert_tz(attendance['check_in'])
          check_out = self.__convert_tz(attendance['check_out'])
          log.info(f'CI: {check_in}; CO: {check_out}')
        else:
          log.info('Please wait until the end of business hours')
      # Otherwise doing checkin
      else:
        log.info('Check in')
        attendance = self.bemo.attendance_manual()
        check_in = self.__convert_tz(attendance['check_in'])
        check_out = self.__convert_tz(attendance['check_out'])
        log.info(f'CI: {check_in}; CO: {check_out}')

  # Convert to timezone
  def __convert_tz(self, time_str):
    return datetime.strptime(time_str + '+0000', '%Y-%m-%d %H:%M:%S%z').astimezone(pytz.timezone(share.get_timezone()))

  # Check out working time
  def __is_out_working_time(self):
    end_date_time = datetime.strptime(share.config['working-time']['afternoon']['end'], "%H:%M").time()
    return datetime.now().time() > end_date_time
