# Backend Repository of Corona Tracker<br/>
## Android Repository at <a href="https://github.com/ammar-alavi10/Covid19_tracker" target="_blank">Android Repository</a>
## Current Status: 
### Code hasn't been merged to master. Latest code currently at <b>pubnub-sockets</b> branch
### Hosted at: <a href="http://tuhina840.pythonanywhere.com/">Website</a> 
<p>This directory contains the API and administrative panel. We are going to shift hosting service to AWS as pythonanywhere doesn't support background tasks.<br></p>
### APK URL: <a href="https://drive.google.com/open?id=1O_7vBoedff12gYB52rF6SnvbxWApdv0y">Google Drive Apk link</a>
<p>Android Application Google Drive link </p>
Covid Tracking Application<br/>

## How to run this project?
Clone the branch pubnub-sockets
Set up postgres
Edit database configuration at corona->setting.py line 87
```bash
  pip install virtualenv
  virtualenv .
  pip install -r requirements.txt
  cd corona
  python manage.py migrate
  python manage.py createsuper user
  python manage.py runserver
```

</br> On another terminal run the command
```bash
  python manage.py process_tasks
  
```
<p>This command is required to access contact tracing page</p>
# More Links
Android APK Demo: <a href="https://drive.google.com/file/d/1VUhCmWstbAH-Pf2QXOL6mYdCD0-LoY0e/view?usp=sharing">App Demo</a>
Website Demo:<a href="https://drive.google.com/open?id=1J7nq2eeIXKEz7gvgMhqdnNCNtvbmbc8B">Website Demo</a>
