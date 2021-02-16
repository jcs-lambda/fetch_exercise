# fetch_exercise
 Python app to determine the similarity of two texts.

You can [run the notebook in Google Colab](https://colab.research.google.com/github/jcs-lambda/fetch_exercise/blob/main/similarity.ipynb) or clone this repository to run from the command line.

```python similarity.py [filename] [filename]```

If filenames are not provided on the command line, the program will prompt
the user to type in each document.

To run the web app locally (in repo root):
```
pipenv install
pipenv shell

# bash
export FLASK_APP=similarity_app.py
flask run

# Windows CMD
set FLASK_APP=similarity_app.py
flask run

# Windows Powershell
$env:FLASK_APP = "similarity_app.py"
flask run
```
