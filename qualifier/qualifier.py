import random
import typing
from dataclasses import dataclass

@dataclass(frozen=True)
class Request:
    """Request Object"""
    scope: typing.Mapping[str, typing.Any]
    receive: typing.Callable[[], typing.Awaitable[object]]
    send: typing.Callable[[object], typing.Awaitable[None]]

class RestaurantManager:
    """RestaurantManager Object"""
    def __init__(self):
        """Instantiate the restaurant manager.

        This is called at the start of each day before any staff get on
        duty or any orders come in. You should do any setup necessary
        to get the system working before the day starts here; we have
        already defined a staff dictionary.
        """
        self.staff = {}

    async def __call__(self, request: Request):
        """Handle a request received.

        This is called for each request received by your application.
        In here is where most of the code for your system should go.

        :param request: request object
            Request object containing information about the sent
            request to your application.
        """
        if request.scope["type"] == "staff.onduty": # type -> <class 'mappingproxy'>
            self.staff.update({request.scope["id"]: request})
        
        elif request.scope["type"] == "staff.offduty":
            self.staff.pop(request.scope["id"])
        
        elif request.scope["type"] == "order":
            requested_speciality = request.scope['speciality']
            full_order = await request.receive()
            random_staff_pool = []
        
            for staff_id in self.staff.keys():
                if requested_speciality in self.staff[staff_id].scope['speciality']:
                    random_staff_pool.append(staff_id)            
        
            random_staff_pick = random.sample(random_staff_pool, k=1)
            found = self.staff[random_staff_pick[0]]
            await found.send(full_order)
            result = await found.receive()
            await request.send(result)