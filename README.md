# BusinessManageProject


Project was created in order to bring customers closer to the service providers of the some business industry.    
I am trying to improve the interaction of the main participants in these processes. 
The client is provided with tools for convenient searching the specialists of a business,
filtering them according position and checking their schedules for concrete date. 
In project is present three main role: an owner, an admin and a manger.
Admin can make an appointments for clients to the specific specialist at the concrete his free working time. 
Manger creates profile for the specialists, adds working locations and schedule for specialists.


[![GitHub license](https://img.shields.io/github/license/ita-social-projects/BeautyProject)](https://github.com/ita-social-projects/BeautyProject/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/ita-social-projects/BeautyProject)](https://github.com/ita-social-projects/BeautyProject/issues)
[![Pending Pull-Requests](https://img.shields.io/github/issues-pr/ita-social-projects/BeautyProject?style=flat-square)](https://github.com/ita-social-projects/BeautyProject/pulls)
[![GitHub top language](https://img.shields.io/github/languages/top/ita-social-projects/BeautyProject)](https://img.shields.io/github/languages/top/ita-social-projects/BeautyProject)

---
Content
- [Installation](#Installation)
  - [Clone](#Clone)
  - [Required to install](#Required-to-install)
  - [Environment](#Environment)
  - [How to run local](#How-to-run-local)
  - [How to run Docker](#How-to-run-Docker)
  - [Setup](#Setup)
- [Tests](#Tests)
- [Project deploy](#project-deploy)
- [Usage](#Usage)
- [Documentation](#Documentation)
- [Contributing](#contributing)
  - [Before entering](#Before-entering)
  - [Git flow](#Git-flow)
  - [Issue flow](#Issue-flow)
  - [Using flake8](#Using-flake8)
- [FAQ](#faq)
- [Teams](#Teams)
- [Support](#support)
- [License](#license)

----

## Installation

### Clone or Download

-  Clone this repo to your local machine using   
```
git clone https://github.com/Misha86/BusinessManageProject.git
```
  or download the project archive: https://github.com/Misha86/BusinessManageProject/archive/refs/heads/main.zip    

<a name="footnote">*</a> - to run the project you need an `.env` file in root folder

### Required to install

- [![Python](https://docs.python.org/3.9/_static/py.svg)](https://www.python.org/downloads/release/python-3912/) 3.9.12
- Project reqirements:
```
pip install -r /requirements.txt
```

### Environment

- Add the environment variables file (.env) to the project folder.
It must contain the following settings:
```
SECRET_KEY = '😊YOUR_SECRET_KEY😊'
DEBUG = False
ALLOWED_HOSTS = *
DB_NAME='😊YOUR_DB_NAME😊'
DB_USER='😊YOUR_DB_USER😊'
DB_PASS='😊YOUR_DB_PASS😊'
DB_HOST='😊YOUR_DB_HOST😊'
DB_PORT='😊YOUR_DB_PORT😊'
```

### How to run local

- Start the terminal.
- Go to the directory "your way to the project" BusinessManageProject / business_manage
- Run the following commands
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### How to run Docker

- Run our project using Docker:
```
docker-compose up
```



### Setup using the terminal

- Create a superuser:    
```
python manage.py createsuperuser
```
- Create a admin:    
```
python manage.py createadmin
```
- Create a manager:    
```
python manage.py createmanager
```

### Setup using the docker

- Create a superuser:    
```
docker src exec python manage.py createsuperuser
```
- Create a admin:    
```
docker src exec python manage.py createadmin
```
- Create a manager:    
```
docker src exec python manage.py createmanager
```

----

## Tests

- Run project tests:
```
python manage.py test
```

## Using flake8

- Install flake8 according to python version:

```
python3.9 -m pip install flake8
```

- Install flake8 extensions:

```
pip instll -r requirements-flake8.txt
```

- Install pre-commit:

``` 
pip install pre-commit
```

- Make sure there are files `.flake8` & `.pre-commit-config.yaml` in the project 
directory

- Create hook:

```
pre-commit install
```

- Settings are ready to use. Before committing, the hook will run 
a flake8 check. If the check does not pass the commit will not take place.

---

## Using coverage

- Install coverage according to python version:

```
python3.9 -m pip install coverage
```

- Run tests coverage from main directory:

```
coverage run business_manage/manage.py test api
```

- Check coverage report:

``` 
 coverage report
```

- Create html coverage report:

``` 
 coverage html
```

- Open html report file in the browser:

``` 
 ./htmlcov/index.html
```

----

## Teams

### Development team 
[![@Misha86/](https://github.com/Misha86.png?size=200)](https://github.com/Misha86)

---

## Support

- This option is currently missing. You can contact a team member directly. You can go to the team member's page in the [teams section](#Teams) by clicking on his or her avatar.

---
