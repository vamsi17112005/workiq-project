from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from backend.database import Base


class GithubFiles(Base):

    __tablename__="github_files"


    id=Column(
        Integer,
        primary_key=True,
        index=True
    )


    repo=Column(
        String
    )


    path=Column(
        String
    )


    content=Column(
        Text
    )