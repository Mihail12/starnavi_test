# Starnavi Test

I have chosen django framework for the task. I think it more convenient to start some app fast

## Start
you only need [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) to start  
then: `docker-compose up -d` to start project

and you could visit https://localhost:8000/

all models can be viewed in https://localhost:8000/admin/  (with su credentials login: `admin` pass: `admin`)

####The task was made in the following steps:  
1. user signup - it is just creating user on https://localhost:8000/api/users/
2. user login  - JWT on https://localhost:8000/api/auth/login/ (POST) and logout on https://localhost:8000/api/auth/logout (GET)
3. post creation - https://localhost:8000/api/posts/
4. post like - https://localhost:8000/api/likes/ (POST with data = {'post': `post_guid`, 'is_active': true})
5. post unlike - https://localhost:8000/api/likes/ (POST with data = {'post': `post_guid`, 'is_active': false})
6 analytics - https://localhost:8000/api/analytics/ (GET with optional parameters [date_from(format:%Y-%m-%d), date_to(format:%Y-%m-%d), post(guid), user(guid)])
7. user activity - https://localhost:8000/api/user-activity/ (for current logged-in user)  https://localhost:8000/api/user-activity/<guid>/ (for user with the guid)


####Automated Bot

Could be started with command(after project is started):  

`docker exec -it starnavi_spasenko_test python automated_bot.py`  

if you want to change bot configuration please use `.config.automated_bot` file


# Test description

Test task: python developer

Object of this task is to create a simple REST API. You can use one framework from this list (Django
Rest Framework, Flask or FastAPI) and all libraries which you are prefer to use with this frameworks.

##1. Social Network

Basic models:  
● User  
● Post (always made by a user)

Basic Features:  
● user signup  
● user login  
● post creation  
● post like  
● post unlike  
● analytics about how many likes was made. Example url  
/api/analytics/?date_from=2020-02-02&date_to=2020-02-15 . API should return analytics aggregated by day.  
● user activity an endpoint which will show when user was login last time and when he mades a last
request to the service.

###Requirements:  
● Implement token authentication (JWT is prefered)

Object of this bot demonstrate functionalities of the system according to defined rules. This bot
should read rules from a config file (in any format chosen by the candidate), but should have
following fields (all integers, candidate can rename as they see fit).  

##2. Automated bot

STARNAVI

● number_of_users  
● max_posts_per_user  
● max_likes_per_user  
Bot should read the configuration and create this activity:  
● signup users (number provided in config)  
● each user creates random number of posts with any content (up to
max_posts_per_user)  
● After creating the signup and posting activity, posts should be liked randomly, posts
can be liked multiple times

###Notes:
● ​Clean and usable REST API is important  
● Bot this is just separate python script, not a django management command or etc.   
● the project is not defined in detail, the candidate should use their best judgment for every
non-specified requirements (including chosen tech, third party apps, etc), however every decision must be explained and backed by arguments in the interview  
● Result should be sent by providing a Git url. This is a mandatory requirement.