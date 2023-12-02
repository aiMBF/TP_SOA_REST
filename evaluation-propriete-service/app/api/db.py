from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine)

from databases import Database

DATABASE_URL = 'postgresql://eval_user:eval_password@eval_prop_db/eval_prop_database'

engine = create_engine(DATABASE_URL)
metadata = MetaData()

evaluations = Table(
    'evaluation',
    metadata,
    Column('ville', String(50), primary_key=True),
    Column('prix_par_metre', Integer)
)

database = Database(DATABASE_URL)
