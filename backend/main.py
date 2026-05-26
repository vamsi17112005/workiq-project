from fastapi import FastAPI
from backend.database import engine
from backend.models import Base
from backend.github_service import store_raw_files
from backend.database import SessionLocal
from backend.models import GithubFiles
Base.metadata.create_all(
    bind=engine
)

from backend.github_service import (

    get_repo,
    get_readme,
    get_branches,
    get_commits,
    traverse_repo,
    get_raw_file,
    get_all_raw_files

)

app=FastAPI()
@app.get("/count")
def count_files():

    db=SessionLocal()

    count = db.query(
        GithubFiles
    ).count()

    db.close()

    return {

        "total_files":count

    }

@app.get("/store/{owner}/{repo}")
def save_files(owner,repo):

    return store_raw_files(
        owner,
        repo
    )

@app.get("/")
def home():

    return {
        "message":"WorkIQ running"
    }


@app.get("/repo/{owner}/{repo}")
def fetch_repo(owner,repo):

    return get_repo(
        owner,
        repo
    )


@app.get("/readme/{owner}/{repo}")
def fetch_readme(owner,repo):

    return get_readme(
        owner,
        repo
    )


@app.get("/allfiles/{owner}/{repo}")
def fetch_all_files(owner,repo):

    return traverse_repo(
        owner,
        repo
    )


@app.get("/commits/{owner}/{repo}")
def fetch_commits(owner,repo):

    return get_commits(
        owner,
        repo
    )

@app.get("/raw/{owner}/{repo}/{path:path}")
def fetch_raw_file(
    owner,
    repo,
    path
):

    return get_raw_file(
        owner,
        repo,
        path
    )

@app.get("/rawall/{owner}/{repo}")
def fetch_all_raw_files(
    owner,
    repo
):

    return get_all_raw_files(
        owner,
        repo
    )

@app.get("/db")
def get_db():

    db = SessionLocal()

    data = db.query(
        GithubFiles
    ).limit(10).all()


    result=[]

    for file in data:

        result.append({

            "id":file.id,

            "repo":file.repo,

            "path":file.path,

            "content_preview":
            file.content[:200]

        })


    db.close()

    return result