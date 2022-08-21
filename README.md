# Strava-with-Flask

## Building a tool that will help me practice using APIs and track my Year of Fitness goal

This project is an effort for me to combine my passion for learning new skills and building things, as well as to help push my to stay commited to my Year of Fitness goal - Run a combined 2022 miles with a group of friends during 2022. Instead of moving to a new platform that will track this for us I decided to use this as an opportunity to learn something new: Use Strava's API and build my own tracker. 

This is an ongoing project that I plan to further flesh out. 

As of 08/21/2022, it can:
* Use OAuth2 to sign into Strava
* Pull Athlete data and store it in a database
* Store auth/refresh tokens and save them in a database

Future plans include:
* Accessing runner activities, filtering out anything that isn't a run and then saving it to a database
* Using the activities table to create a leaderboard of that will show different data:
** Total Activities
** Total Distance Ran
** Total Time
** Fastest Average Speed
* A Heatmap of the US/World showing locations of activities
