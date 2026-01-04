from pydantic import BaseModel, Field


class DateTimeData(BaseModel):
    dateTime: str = Field(
        ..., description="Time formatted according to ISO: YYYY-MM-DD HH:MM:SS."
    )
    timeZone: str = Field(default="UTC", description="Timezone code.")


class CalendarEvent(BaseModel):
    summary: str = Field(..., description="The title of the event.")
    start: DateTimeData = Field(..., description="The event start time.")
    end_time: DateTimeData = Field(..., description="The event end time.")
    description: str = Field(default="", description="A description of the event.")
    location: str = Field(default="", description="The location of the event.")


class CalendarEventRequest(CalendarEvent):
    calendar_id: str = Field(..., description="The calendar id for the request.")


class CalendarEventResponse(CalendarEvent):
    status: str = Field(..., description="The response status.")
