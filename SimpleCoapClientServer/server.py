#!/usr/bin/env python3

# This is a simple CoAP server using Aiocoap. More details and examples
# can be found at Aiocoap Github Repo <https://github.com/chrysn/aiocoap>
# 
# Copyright (c) 2021 Chris Dinh <https://aniotodyssey.com/>
#
# This file is published under the MIT license

import aiocoap.resource as resource
import aiocoap
import threading

import logging

import asyncio

class AlarmResource(resource.ObservableResource):
    """This resource supports the GET and PUT methods and is observable.
    GET: Return current state of alarm
    PUT: Update state of alarm and notify registered observers"""

    def __init__(self):
        super().__init__()

        self.status = "OFF"
        self.has_observers = False
        self.notify_observers = False

    # Ensure observers are notify if required
    def notify_observers_check(self):
        while True:
            if self.has_observers and self.notify_observers:
                print('Notifying observers')
                self.updated_state()
                self.notify_observers = False

    # Observers change event callback
    def update_observation_count(self, count):
        if count:
            self.has_observers = True
        else:
            self.has_observers = False

    # Handles GET request or observer notify
    async def render_get(self, request):
        print('Return alarm state: %s' % self.status)
        payload = b'%s' % self.status.encode('ascii')

        return aiocoap.Message(payload=payload)

    # Handles PUT request
    async def render_put(self, request):
        self.status = request.payload.decode('ascii')
        print('Update alarm state: %s' % self.status)
        self.notify_observers = True

        return aiocoap.Message(code=aiocoap.CHANGED, payload=b'%s' % self.status.encode('ascii'))

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()
    alarmResource = AlarmResource()
    root.add_resource(['alarm'], alarmResource)
    asyncio.Task(aiocoap.Context.create_server_context(root, bind=('localhost', 5683)))

    # Spawn a daemon to notify observers when alarm status changes
    observers_notifier = threading.Thread(target=alarmResource.notify_observers_check)
    observers_notifier.daemon = True
    observers_notifier.start()

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
