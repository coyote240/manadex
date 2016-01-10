# Manadex
A web application for cataloging, indexing and analyzing our personal
Magic: The Gathering card collections.

* Allow for adding cards to the index
* Collect card records into collections and decks
* Cross-reference cards and decks with friends
* Allow for public and private decks
* Note which cards are in which decks
* Mana curve charts
* Output to CSV
* Lending library?

There are likely plenty of programs out there for this, but this is fun
for me to build and replaces my buddies' spreadsheets.

## Running Manadex
Make sure you have pip and virtualenv.  Also, manadex currently
depends on mongodb, though this is likely to change once I've arrived
at a stable schema.

    virtualenv manadex
    activate manadex
    pip install -r requirements.txt
    honcho start

Then visit http://localhost:8888
