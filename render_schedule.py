import argparse
import json
import datetime
import arrow

## This is a record
class UserOverride():
  def __init__(self, user: str, start: arrow, end: arrow):
    self.user = user
    self.start = start
    self.end = end
    
  def __repr__(self) -> str:
    return self.__str__()
  def __str__(self) -> str:
    return f"User: {self.user}, Override start <> end: {self.start} <> {self.end}"

class Scheduler():
  ## later used in TIME_FORMAT property acts as static
  _time_format = 'YYYY-MM-DDTHH:mm:ssZ'
  
  
  ## create the Scheduler object
  def __init__(self, scheduleFile: str, overridesFile: str, fromTime: str, untilTime: str):
    print(f"schedule fp: {scheduleFile}")
    self.schedule = self._parseSchedule(scheduleFile)
    self.overrides = self._parseOverrides(overridesFile)
    
    self.fromTime = arrow.get(fromTime, self.TIME_FORMAT) if fromTime else None
    
    self.untilTime = arrow.get(untilTime, self.TIME_FORMAT) if untilTime else None
    
  ## parse JSON file at given location
  def _parseSchedule(self, jsonFile: str) -> dict:
    schedule = self._loadJSON(jsonFile)
    
    self.users = schedule["users"]
    self.handoverStart = arrow.get(schedule['handover_start_at'], self.TIME_FORMAT)
    self.intervalDays  = int(schedule["handover_interval_days"])
  
  def _parseOverrides(self, jsonFile: str) -> dict:
    parsedOverrides = self._loadJSON(jsonFile)
    overrides = []
    ## multiple overrides
    if isinstance(parsedOverrides, list):
      for override in parsedOverrides:
        if override:
          uo = self._makeUserOverride(override["user"],
                                      override["start_at"],
                                      override["end_at"]
                                    )
          overrides.append(uo)
    ## only one user override
    else:
      uo = self._makeUserOverride(parsedOverrides["user"],
                                    parsedOverrides["start_at"],
                                    parsedOverrides["end_at"]
                                  )
      overrides.append(uo)
    return overrides
    
    
    
  def _makeUserOverride(self, name: str, start: str, end: str) -> UserOverride:
    return UserOverride(
            name, 
            arrow.get(start, self.TIME_FORMAT),
            arrow.get(end, self.TIME_FORMAT)
          )
    
    
  def _loadJSON(self, jsonFile: str) -> dict:
    with open(jsonFile) as f:
      return json.load(f)
  ## create the schedule from the given data
  def render_schedule(self) -> dict:
      pass
      
  def __str__(self) -> str:
    return (f"Scheduler:\n \
              \t users: {self.users} \n \
              \t start <> end: {self.fromTime} <> {self.untilTime}\n  \
              \t==============================\n \
              \t handover start: {self.handoverStart}\n \
              \t intercal days: {self.intervalDays}\n \
              \t overrides: {self.overrides}\n")
    
      
  ## YYYY-MM-DDThh:mmZ -> 'T' is a separator, 'Z'means UTC time zone
  ## im arrow default is UTC
  @property
  def TIME_FORMAT(self):
    return type(self)._time_format
  


  
  
  




def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--schedule", help="pass a JSON file containing a definition of a schedule")
  parser.add_argument("--overrides", help="pass a JSON file containing an array of overrides")
  parser.add_argument("--from", help="the time from which to start listing entries")
  parser.add_argument("--until", help="the time until which to stop listing entries")
  args = vars(parser.parse_args())
  
  # Call render_schedule function with the given arguments
  scheduler = Scheduler(args["schedule"],
                        args["overrides"],
                        args["from"],
                        args["until"]
                      )
  
    # Print all the given parameters
  print("Scheduler:", scheduler)
  
  # Print all the given parameters to init
  
  

if __name__ == "__main__":
  main()

