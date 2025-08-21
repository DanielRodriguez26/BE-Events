from app.api.schemas.event_schemas import Event, EventCreate, EventUpdate

def validate_event_data(event_data: EventCreate, existing_events):
    if event_data.end_date <= event_data.start_date:
        raise ValueError("End date must be after start date")

    if event_data.capacity < 0:
        raise ValueError("Capacity must be a positive number")

    for event in existing_events:
        if event.title == event_data.title:
            raise ValueError("Event with this title already exists")

        if (event.start_date.date() == event_data.start_date.date() and
            event.end_date.date() == event_data.end_date.date()):
            if (event.start_date.time() == event_data.start_date.time() or
                event.end_date.time() == event_data.end_date.time()):
                raise ValueError("Event with the same date and time already exists")

def validate_event_update_data(event_data: EventUpdate, current_event: Event):
    if not current_event:
        raise ValueError("Event not found")

    if event_data.start_date and event_data.end_date:
        if event_data.end_date <= event_data.start_date:
            raise ValueError("End date must be after start date")

    if event_data.capacity is not None and event_data.capacity < 0:
        raise ValueError("Capacity must be a positive number")
    
    if event_data.title and event_data.title != current_event.title:
        raise ValueError("Title cannot be changed")
    
    if event_data.location and event_data.location != current_event.location:
        raise ValueError("Location cannot be changed")
    