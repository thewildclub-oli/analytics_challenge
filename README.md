# Backend Developer Challenge

Task: Create an analytics component, to analyse provided data in csv file.

## Installation

1. Install [pyenv](https://github.com/yyuu/pyenv#installation)
2. Install [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv#installation)
3. Create new virtual env called e.g. `pyenv virtualenv 3.8.2 challenge_venv`
4. Activate new virtual environment `pyenv activate challenge_venv`
5. Ensuring you are working in the repo root, install project dependencies using `pip install -r requirements.txt`
6. Run migrations to create sqlite db `python manage.py migrate`
7. Import data:
..- Start django shell `python manage.py shell`
..- Import import logic `from analytics_component.import_logic import import_csvs`
..- Run import_csvs, supplying the unzipped data folder path as an argument e.g. `import_csvs('/Users/Oli/Documents/backend_developer_challenge/data/')`
..- Exit from django shell `exit()`

## Running Project
1. `python manage.py runserver`
2. Navigate to [http://127.0.0.1:8000/analytics-challenge/](http://127.0.0.1:8000/analytics-challenge/) in your browser
3. Select date to analyse (click on the calendar icon), and hit the submit button.

## Running the Test Suite
1. `python manage.py test`