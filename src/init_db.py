
from database import engine, Session
from models import Base, User

import pandas as pd

# load users data from CSV
def import_users_from_csv(file_path):
    users_df = pd.read_csv(file_path)
    for _, row in users_df.iterrows():
        user = User(
            username=row["username"],
            display_name=row["display_name"],
            hashed_password=row["hashed_password"],
        )
        session.add(user)

    # commit the transaction
    session.commit()

if __name__ == "__main__":
    # Back-UP submissions table to csv
    df = pd.read_sql("SELECT * FROM submissions", engine)
    df.to_csv('backup/data/submissions.csv', index=False)
    
    # DROP TABLE IF EXISTS users;
    User.__table__.drop(engine, checkfirst=True)

    # Create all tables in the engine
    Base.metadata.create_all(engine)

    # create a new session
    session = Session()

    import_users_from_csv('data/user_data/users.csv')
