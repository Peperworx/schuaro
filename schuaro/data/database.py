import sqlalchemy
import databases


class DbManager:
    """
        Class for managing the database
    """

    users: sqlalchemy.Table
    clients: sqlalchemy.Table

    def __init__(self, database: databases.Database):
        """
            Class for managing the database
        """

        # Metadata
        self.metadata = sqlalchemy.MetaData()
        
        # Initialize users table
        self.users = sqlalchemy.Table(
            "users",
            self.metadata,
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("username", sqlalchemy.String),
            sqlalchemy.Column("email", sqlalchemy.String),
            sqlalchemy.Column("password", sqlalchemy.String),
            sqlalchemy.Column("scope", sqlalchemy.String),
        )

        # Initialize clients table
        self.clients = sqlalchemy.Table(
            "clients",
            self.metadata,
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("clientid", sqlalchemy.String),
            sqlalchemy.Column("clientsecret", sqlalchemy.String),
            sqlalchemy.Column("scope", sqlalchemy.String),
        )

        self.database = database

        # Create engine and create_all
        self.engine = sqlalchemy.create_engine(
            str(database.url), connect_args={"check_same_thread": False}
        )

        self.metadata.create_all(self.engine)

    

        