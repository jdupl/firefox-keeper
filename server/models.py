from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, Boolean, \
    ForeignKey, DateTime

from sqlalchemy.orm import mapper, relationship

from database import metadata, db_session


class Snapshot():
    query = db_session.query_property()

    def __init__(self, bookmark_id, path, snapshot_date):
        pass


class Bookmark():
    query = db_session.query_property()

    def __init__(self, url, description):
        self.url = url
        self.description = description

bookmarks = Table(
    'bookmarks', metadata,
    Column('id', Integer, primary_key=True),
    Column('url', String(4096), nullable=False),
    Column('description', String(4096), nullable=False),
    Column('online', Boolean),
    Column('created_at', DateTime, default=datetime.now),
    Column('modified_at', DateTime, onupdate=datetime.now)
    )

snapshots = Table(
    'snapshots', metadata,
    Column('id', Integer, primary_key=True),
    Column('bookmark_id', Integer, ForeignKey('bookmarks.id')),
    Column('path', String(4096), nullable=False),
    Column('completed', Boolean),
    Column('snapshotted_at', DateTime, default=datetime.now),
    Column('created_at', DateTime, default=datetime.now),
    Column('modified_at', DateTime, onupdate=datetime.now)
    )

mapper(Bookmark, bookmarks, properties={
    'snapshots': relationship(Snapshot)
})
mapper(Snapshot, snapshots, properties={
    'bookmark': relationship(Bookmark)
})
