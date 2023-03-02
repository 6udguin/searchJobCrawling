"""
These are the URLs that will give you remote jobs for the word 'python'
https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs
Good luck!
"""
from flask import Flask, render_template, request, redirect
from so import get_jobs as so_get_jobs
from wwr import get_jobs as wwr_get_jobs
from remote import get_jobs as re_get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/report")
def report():
    word = request.args.get("word")
    if word:  
        word = word.lower()
        existing_jobs = db.get(word)
        if existing_jobs:
            jobs = existing_jobs
        else:
            jobs = wwr_get_jobs(word) +so_get_jobs(word) + re_get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")  
    return render_template("report.html",
                           searching_by=word,
                           resultsNumber=len(jobs),
                           jobs=jobs)

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs, word)
    return f"Generate CSV for {word}"
  except:
    return redirect("/")

app.run(host="0.0.0.0")