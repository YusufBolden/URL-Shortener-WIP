from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from server.database import db_session

engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# users = Table('users', metadata, autoload=True)
# con = engine.connect()
# con.execute(users.insert(), name='admin', email='admin@localhost')

# users.select(users.c.id == 1).execute().first()

def init_db():
    metadata.create_all(bind=engine)

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import yourapplication.models
    Base.metadata.create_all(bind=engine)

@app.teardown_appcontext
def shutdown_session(exeception=None)
    db_session.remove()