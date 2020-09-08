import sqlalchemy
import databases

# DATABASE_URL = "sqlite:///./test.db"
DATABASE_URL = "postgresql://praveshchapagain@localhost:5432/globalfantasyleague"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


engine = sqlalchemy.create_engine(DATABASE_URL)

print(engine.table_names())
