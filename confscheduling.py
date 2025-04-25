class Room:
    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity
        self.talks = []


class Talk:
    def __init__(self, title: str, capacity: int, start_time: int, end_time: int):
        self.title = title
        self.capacity = capacity
        self.attendees = []
        self.room = None
        self.start_time = start_time
        self.end_time = end_time


class Attendee:
    def __init__(self, name: str):
        self.name = name
        self.talks = []


class Conference:
    def __init__(self, name: str):
        self.name = name
        self.attendees = []
        self.talks = []
        self.rooms = []

    def add_attendee(self, attendee: Attendee):
        if attendee in self.attendees:
            raise Exception("Attendee is already registered.")
        self.attendees.append(attendee)

    def add_talk(self, talk: Talk):
        if talk in self.talks:
            raise Exception("Talk is already there.")
        self.talks.append(talk)

    def register_for_talk(self, attendee: Attendee, talk: Talk):
        if attendee in talk.attendees:
            raise Exception("Attendee is already going.")
        if len(talk.attendees) >= talk.capacity:
            raise Exception("The talk is full.")
        for t in attendee.talks:
            if not (t.end_time <= talk.start_time or talk.end_time <= t.start_time):
                raise Exception("Colliding time slots.")
            # if t.start_time > talk.start_time:
            #     if t.start_time < talk.end_time:
            #         raise Exception("Colliding time slots.1")
            # elif t.start_time < talk.start_time:
            #     if t.end_time > talk.start_time:
            #         raise Exception("Colliding time slots.2")
        talk.attendees.append(attendee)
        attendee.talks.append(talk)

    def is_registered(self, attendee: Attendee, talk: Talk):
        if attendee in talk.attendees:
            return True
        return False

    def assign_room(self, room: Room, talk: Talk):
        if talk.capacity > room.capacity:
            raise Exception("Talk registrations to much.")
        room.talks.append(talk)
        talk.room = room

    def get_schedule(self, attendee: Attendee):
        return [(talk.start_time, talk.end_time) for talk in attendee.talks]
