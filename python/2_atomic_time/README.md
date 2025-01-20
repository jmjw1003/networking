# Project 2: Atomic time
A web client to reach out to the atomic clock at NIST (National Institute of Standards and Technology) and get the number of seconds since January 1, 1900 from their clocks.

This will then be compared to the system clock, which should be very close. (During testing it was always within 1 second.)

The NIST server will only accept requests every 4 seconds, so ensure rate limiting is used to not be blocked by the service.

`TimeClient().print_times()` has a built in 4 second sleep and is used by the `main()` function in `timeclient.py`, so I would recommend just using that.

Note that for some reason the NIST websocket will sometimes return nothing, in which case an error will be logged asking you to try again.

They’re on a rotating IP for `time.nist.gov` and it seems like one or two of the servers might not be working right.

If it keeps coming up zero, something else might be wrong.

### Usage
Call the time client in the terminal by using: `$ python3 timeclient.py`

### Example output:
```
INFO:__main__:NIST time  : 3946217628
INFO:__main__:System time: 3946217628
```