import requests
import base64

from backend.config import GITHUB_TOKEN
from backend.database import SessionLocal
from backend.models import GithubFiles

headers={

    "Authorization":f"Bearer {GITHUB_TOKEN}"

}


# -----------------------
# Common API Request
# -----------------------

def github_request(url):

    response=requests.get(

        url,
        headers=headers

    )

    data=response.json()


    if response.status_code!=200:

        return {

            "error":"Github API failed",
            "details":data

        }

    return data



# -----------------------
# Repository info
# -----------------------

def get_repo(owner,repo):

    url=f"https://api.github.com/repos/{owner}/{repo}"

    return github_request(url)



# -----------------------
# README
# -----------------------

def get_readme(owner,repo):

    url=f"https://api.github.com/repos/{owner}/{repo}/readme"

    data=github_request(url)

    if "content" not in data:

        return data


    decoded=base64.b64decode(

        data["content"]

    ).decode(

        "utf-8",
        errors="ignore"

    )

    return{

        "name":data["name"],
        "content":decoded

    }



# -----------------------
# Get branches
# -----------------------

def get_branches(owner,repo):

    url=f"https://api.github.com/repos/{owner}/{repo}/branches"

    data=github_request(url)

    result=[]

    for branch in data:

        result.append(

            branch["name"]

        )

    return result



# -----------------------
# Get commits
# -----------------------

def get_commits(owner,repo):

    url=f"https://api.github.com/repos/{owner}/{repo}/commits"

    data=github_request(url)

    result=[]


    for commit in data:

        result.append({

            "message":

            commit["commit"]["message"],

            "author":

            commit["commit"]["author"]["name"]

        })

    return result



# -----------------------
# Get full repository tree
# -----------------------

def traverse_repo(owner,repo):


    repo_data=get_repo(
        owner,
        repo
    )


    branch=repo_data["default_branch"]


    url=f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"


    data=github_request(url)


    allowed_extensions=[

        ".py",
        ".js",
        ".ts",
        ".java",
        ".cpp",
        ".md"

    ]


    files=[]


    for item in data["tree"]:

        if item["type"]=="blob":

            if any(

                item["path"].endswith(ext)

                for ext in allowed_extensions

            ):

                files.append({

                    "name":

                    item["path"].split("/")[-1],

                    "path":

                    item["path"]

                })


    return files



# -----------------------
# Raw file content
# -----------------------

def get_raw_file(

        owner,
        repo,
        path
):


    repo_data=get_repo(
        owner,
        repo
    )


    branch=repo_data["default_branch"]


    url=f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"


    data=github_request(
        url
    )


    if "content" not in data:

        return{

            "error":"File not found"

        }


    decoded=base64.b64decode(

        data["content"]

    ).decode(

        "utf-8",
        errors="ignore"

    )


    print(
    f"Processing: {data['path']}"
)

def get_all_raw_files(owner,repo):

    files=traverse_repo(
        owner,
        repo
    )

    all_content=[]

    repo_data=get_repo(
        owner,
        repo
    )

    branch=repo_data["default_branch"]

    for file in files:

        path=file["path"]

        try:

            url=f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"

            data=github_request(
                url
            )

            if "content" in data:

                decoded=base64.b64decode(
                    data["content"]
                ).decode(
                    "utf-8",
                    errors="ignore"
                )

                print(
                    f"Processing: {path}"
                )

                all_content.append({

                    "name":data["name"],
                    "path":data["path"],
                    "content":decoded
                })

        except Exception as e:

            print(
                f"Skipped: {path}"
            )

            continue

    return all_content
def store_raw_files(owner,repo):

    db=SessionLocal()

    files=get_all_raw_files(
        owner,
        repo
    )


    for file in files:

        new_file=GithubFiles(

            repo=repo,

            path=file["path"],

            content=file["content"]

        )


        db.add(
            new_file
        )


    db.commit()

    db.close()


    return{

        "message":"Stored successfully"

    }