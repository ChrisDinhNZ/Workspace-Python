#!/usr/bin/env python3

# This is a simple CoAP client using Aiocoap. More details and examples
# can be found at Aiocoap Github Repo <https://github.com/chrysn/aiocoap>
# 
# Copyright (c) 2021 Chris Dinh <https://aniotodyssey.com/>
#
# This file is published under the MIT license

"""This is a usage example of aiocoap that demonstrates how to implement a
simple client. See the "Usage Examples" section in the aiocoap documentation
for some more information."""

import logging
import asyncio
import random

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    context = await Context.create_client_context()
    alarm_state = random.choice([True, False])
    payload = b"OFF"

    if alarm_state:
        payload = b"ON"

    request = Message(code=PUT, payload=payload, uri="coap://localhost/alarm")

    response = await context.request(request).response
    print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
