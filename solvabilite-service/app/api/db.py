from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine)

from databases import Database

DATABASE_URL = 'postgresql://solvabilite_user:solvabilite_password@localhost/solvabilite_db'

engine = create_engine(DATABASE_URL)
metadata = MetaData()

clients = Table(
    'clients',
    metadata,
    Column('id_client', String(50), primary_key=True),
    Column('nom', String(50)),
    Column('adresse', String(50)),
    Column('revenu_mensuel', Integer),
    Column('depense_mensuel', Integer)
)

database = Database(DATABASE_URL)
