# Restaurant Staffing Exercise


### Getting Started
To start, you should be able to run `sh startup.sh` from the root directory 

This will install required packages, initialize the database, and open a new console with a dummy smtp server
running it in (for the approve/reject email).  If this doesn't work, you may need to run the commands in `startup.sh`
individually and start the email server manually  by running `python -m smtpd -n -c DebuggingServer localhost:1025`

The app should run at http://127.0.0.1:8000/

The admin page http://127.0.0.1:8000/admin username: `admin` password: `pass` (I registered the models, but didn't really
do anything else with it)

#### Steps 1-3
The app should be fairly self-explanatory.  It was a little difficult to set up since I didn't implement the
User auth model, but hopefully it is clear what parts would be restricted based on navigation (i.e. right now,
anyone can read, approve, or reject and application for a job, but with a user-auth model implemented, only the
hiring manager for that store would be able to get to the page / perform actions)

#### Step 4
For step 4, the email won't actually send, but will print in the separate console window running the dummy smtp server.
This could be easily swapped out for a real server--just made more sense to develop like this.
#### Step 5
For step 5, I implemented a simple api to allow GET, POST, and DELETE, operations on all of the models.  There is no authentication
on the api.  Some examples using the httpie client are below

```
http GET http://127.0.0.1:8000/api/restaurant/
http DELETE http://127.0.0.1:8000/api/restaurant/1
http POST http://127.0.0.1:8000/api/restaurant/ name="Ricky's Radish Soup" restaurant_admin=Rick

http GET http://127.0.0.1:8000/api/applicant/
```
#### Additional 
In addition to the required actions, I implemented an action where a job posting becomes 'closed' when approved,
but can later be re-opened by either a hiring manager or a restaurant admin (can also be closed without any applications
by hiring manager and restaurant admin)


#### Future Work

I would've liked to have written some tests but just ran out of time.

I would like to implement a user-auth model.  I think it may have actually made things easier from the start and would
require a large refactor now.  A lot of the navigation I designed was to show how to separate out/ limit functionality
without having a user auth model.  We wouldn't need to select a restaurant, then location, and instead would just show the
correct one for the logged in user, etc.  I also think we could re-use a number of the views/ templates that are very similar
to one another by being able to capture who the logged in user is and determine what they get to select

