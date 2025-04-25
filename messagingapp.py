# project structure
#
# codesignal_prescreen_sim/
# ├── app_logic/
# │   ├── base_app.py
# │   └── app_impl.py
# ├── test_level_1.py
# ├── test_level_2.py
# ├── test_level_3.py
# ├── test_level_4.py
# └── README.md

# =============================
# File: app_logic/base_app.py
# =============================
from abc import ABC, abstractmethod


class AppBase(ABC):
    @abstractmethod
    def create_user(self, username: str) -> bool:
        pass

    @abstractmethod
    def delete_user(self, username: str) -> bool:
        pass

    @abstractmethod
    def send_message(self, sender: str, receiver: str, message: str) -> bool:
        pass

    @abstractmethod
    def get_messages(self, username: str) -> list[str]:
        pass

    @abstractmethod
    def block_user(self, blocker: str, blockee: str) -> bool:
        pass


# =============================
# File: app_logic/app_impl.py
# =============================
from app_logic.base_app import AppBase


class User:
    def __init__(self, username: str):
        self.username = username
        self.received = dict()  # key timestamp, value msg
        self.sent = dict()  # key timestamp, value msg
        self.wantstoblock = []
        self.wasblocked = []


class AppImpl(AppBase):
    def __init__(self):
        # TODO: implement initialization of users, messages, and block list
        self.users = []

    def create_user(self, username: str) -> bool:
        # TODO: implement
        existantusername = next(
            (u.username for u in self.users if u.username == username), None
        )
        if not existantusername:
            self.users.append(User(username))
            return True
        return False

    def delete_user(self, username: str) -> bool:
        # TODO: implement
        target = next((u for u in self.users if u.username == username), None)
        if not target:
            return False
        self.users.remove(target)
        for user in self.users:
            user.wasblocked = [b for b in user.wasblocked if b.username != username]
            user.wantstoblock = [b for b in user.wantstoblock if b.username != username]
        # NOT GOOD TO DELETE WHILE ITERATING OF ITEM!
        # for user in self.users:
        #   if user.username == username:
        #     self.users.remove(user)
        #   for blockee in user.wasblocked:
        #     if blockee.username == username:
        #       user.wasblocked.remove(blockee)
        #   for blocked in user.wantstoblock:
        #     if blocked.username == username:
        #       user.wantstoblock.remove(blocked)
        return True

    import datetime

    def get_time_helper(self):
        return datetime.datetime.now()

    def send_message(self, sender: str, receiver: str, message: str) -> bool:
        # TODO: implement
        senderuser = next((u for u in self.users if u.username == sender), None)
        receiveruser = next((u for u in self.users if u.username == receiver), None)
        if not senderuser or not receiveruser:
            return False
        if (
            senderuser in receiveruser.wantstoblock
            or receiveruser in senderuser.wantstoblock
        ):
            return False
        time = self.get_time_helper()
        senderuser.sent[time] = message
        receiveruser.received[time] = message
        return True

    def get_messages(self, username: str) -> list[str]:
        # TODO: implement
        receiver = next((u for u in self.users if u.username == username), None)
        if not receiver:
            return []
        # sorted_timestamps = sorted(receiver.received, key=lambda t: list(receiver.received.keys()), reverse=False)
        # sorted_msgs = []
        # for t in sorted_timestamps:
        #   sorted_msgs.append(receiver.received[t])
        # return sorted_msgs
        return [receiver.received[t] for t in sorted(receiver.received, reverse=False)]

    def block_user(self, blocker: str, blockee: str) -> bool:
        # TODO: implement
        blocker_obj = next((u for u in self.users if u.username == blocker), None)
        blockee_obj = next((u for u in self.users if u.username == blockee), None)
        if not blocker_obj or not blockee_obj:
            return False
        if blocker_obj not in blockee_obj.wasblocked:
            blockee_obj.wasblocked.append(blocker_obj)
        if blockee_obj not in blocker_obj.wantstoblock:
            blocker_obj.wantstoblock.append(blockee_obj)
        return True


# # =============================
# # File: README.md
# # =============================
# # CodeSignal Industry Coding Assessment Simulation

# This is a mock 90-minute coding screen modeled after Anthropic/MATS assessments.

# ## Description
# You're tasked with implementing a messaging app simulator. Each level adds a new capability.

# ### Level 1: User Management
# Implement user creation and deletion.
# - `create_user(username)` -> True if created, False if already exists
# - `delete_user(username)` -> True if deleted, False if nonexistent

# ### Level 2: Messaging
# Implement sending and retrieving messages.
# - `send_message(sender, receiver, message)` -> True if sent, False if either user doesn't exist
# - `get_messages(username)` -> List of messages received (strings), ordered by time received

# ### Level 3: Blocking
# Implement user blocking.
# - `block_user(blocker, blockee)` -> True if block registered, False on failure
# - Blocked users cannot send messages to blockers

# ### Level 4: Bonus Behavior
# Block relationships should be symmetric. If A blocks B, B cannot message A either.

# To progress to the next level, all tests in the current level must pass.

# Run tests like:
# ```bash
# python -m unittest test_level_1.py
# ```


# =============================
# File: test_level_1.py
# =============================
import unittest
from app_logic.app_impl import AppImpl


class TestLevel1(unittest.TestCase):
    def setUp(self):
        self.app = AppImpl()

    def test_create_user(self):
        self.assertTrue(self.app.create_user("alice"))
        self.assertFalse(self.app.create_user("alice"))

    def test_delete_user(self):
        self.app.create_user("bob")
        self.assertTrue(self.app.delete_user("bob"))
        self.assertFalse(self.app.delete_user("bob"))


# =============================
# File: test_level_2.py
# =============================
import unittest
from app_logic.app_impl import AppImpl


class TestLevel2(unittest.TestCase):
    def setUp(self):
        self.app = AppImpl()
        self.app.create_user("alice")
        self.app.create_user("bob")

    def test_send_and_receive(self):
        self.assertTrue(self.app.send_message("alice", "bob", "Hello Bob!"))
        self.assertEqual(self.app.get_messages("bob"), ["Hello Bob!"])

    def test_send_fails_if_user_missing(self):
        self.assertFalse(self.app.send_message("charlie", "bob", "Hi!"))
        self.assertFalse(self.app.send_message("alice", "charlie", "Hi!"))


# =============================
# File: test_level_3.py
# =============================
import unittest
from app_logic.app_impl import AppImpl


class TestLevel3(unittest.TestCase):
    def setUp(self):
        self.app = AppImpl()
        self.app.create_user("alice")
        self.app.create_user("bob")

    def test_blocking(self):
        self.assertTrue(self.app.block_user("bob", "alice"))
        self.assertFalse(self.app.send_message("alice", "bob", "Hello?"))

    def test_message_goes_through_if_not_blocked(self):
        self.assertTrue(self.app.send_message("alice", "bob", "Hello!"))


# =============================
# File: test_level_4.py
# =============================
import unittest
from app_logic.app_impl import AppImpl


class TestLevel4(unittest.TestCase):
    def setUp(self):
        self.app = AppImpl()
        self.app.create_user("alice")
        self.app.create_user("bob")

    def test_symmetric_blocking(self):
        self.assertTrue(self.app.block_user("alice", "bob"))
        self.assertFalse(self.app.send_message("bob", "alice", "Yo!"))
        self.assertFalse(self.app.send_message("alice", "bob", "Hey!"))
