from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ForeignKey, Boolean)

from databases import Database

DATABASE_URL = 'postgresql://solvabilite_user:solvabilite_password@solvabilite_db/solvabilite_db'

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


credits = Table(
    'credits',
    metadata,
    Column('id_credit', Integer, primary_key=True),
    Column('id_client', String(50), ForeignKey('clients')),
    Column('dette_en_cours', Integer),
    Column('payement_en_retard', Integer),
    Column('antecedent_faillite', Boolean)
)

metadata.create_all(engine)
database = Database(DATABASE_URL)
