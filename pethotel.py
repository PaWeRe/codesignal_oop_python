class Room:
    def __init__(self, id: str, name: str, capacity: int):
        self.id = id
        self.name = name
        self.species = None
        self.capacity = capacity
        self.pets = []


class Customer:
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id


class Pet:
    def __init__(self, name: str, species: str, belongs_to: Customer):
        self.name = name
        self.species = species
        self.checked_in = False
        self.belongs_to = belongs_to
        self.assigned = None


class PetHotel:
    def __init__(self):
        self.rooms = []
        self.customers = []
        self.pets = []

    def register_customer(self, customer: Customer):
        self.customers.append(customer)

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def add_room(self, room: Room):
        self.rooms.append(room)

    def assign_pet_to_room(self, pet: Pet, room: Room):
        if not pet.checked_in:
            raise Exception("Pet is not checked in.")
        if pet.assigned is not None:
            raise Exception(f"{pet} is already assigned to a room {pet.assigned}")
        if len(room.pets) >= room.capacity:
            raise Exception(f"{room} is full")
        if room.species is None:
            room.species = pet.species
        elif pet.species != room.species:
            raise Exception(
                f"Pet species {pet.species} does not match room species {room.species}"
            )
        room.pets.append(pet)
        pet.assigned = room

    def check_in(self, pet: Pet):
        if pet.checked_in:
            raise Exception("Pet is already checked in")
        pet.checked_in = True

    def check_out(self, pet: Pet):
        if not pet.checked_in:
            raise Exception("Pet is not checked in")
        if pet.assigned:
            pet.assigned.pets.remove(pet)
            pet.assigned = None
        pet.checked_in = False

    def list_pets(self):
        return [(pet.name, pet.species, pet.belongs_to.name) for pet in self.pets]
