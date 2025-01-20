# Project: The word server
https://beej.us/guide/bgnet0/html/split/project-the-word-server.html

This is a project that is all about reading packets.

You’ll receive a stream of encoded data from a server (provided) and you’ll have to write code to determine when you’ve received a complete packet and the print out that data.

### Overview
<b>First:</b> download these files:
- `wordserver.py`: ready-to-run server that hands out lists of random words.
- `wordclient.py`: skeleton code for the client.

<b>RESTRICTION! Do not modify any of the existing code!</b> Just search for TODO and fill in that code. You may add additional functions and variables if you wish.

<b>REQUIREMENT! The code should work with any positive value passed to recv() between 1 and 4096!</b> You might want to test values like 1, 5, and 4096 to make sure they all work.

<b>REQUIREMENT! The code must work with words from length 1 to length 65535.</b> The server won’t send very long words, but you can modify it to test. To build a string in Python of a specific number of characters, you can:

`long_str = "a" * 256   # Make a string of 256 "a"s`

<b>PROTIP! Read and understand all the existing client code before you start.</b> This will save you all kinds of trouble. And note how the structure of the main code doesn’t even care about bytes and streams–it’s only concerned with entire packets. Cleaner, right?

You are going to complete two functions:

- `get_next_word_packet()`: gets the next complete word packet from the stream. This should return the complete packet, the header and the data.
- `extract_word()`: extract and return the word from a complete word packet.
