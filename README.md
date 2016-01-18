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


## Running Manadex in Windows
** It is advisable to run at least Python 2.7.11 (don't forget to update virtualenv)
** Make sure your python install path is all lowercase (i.e. c:\python27).  See http://stackoverflow.com/questions/8688709/virtualenv-on-windows-7-returns-assertionerror for more info.

#####Modify Procfile to this.
    web: python app/app.py --config=app/config.py
    db: mongod --dbpath c:\mongodb\data
    grunt: grunt watch

If you run mongo as a service, take out the mongo line.	

#####Run the following commands:

	npm install
	virtualenv manadex
	mnadex/Scripts/activate
	pip install -r requirements.txt
	honcho start*

*Sometimes less would not run with honcho.  If this happens and your css is not updating, simply manually run a  grunt less.