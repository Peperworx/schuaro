import sqlalchemy



class Tables:
    """
        Class containing all database table schemas
    """

    users: sqlalchemy.Table
    clients: sqlalchemy.Table

    def __init__(self):
        """
            Class containing all database table schemas
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
            "clientss",
            self.metadata,
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("clientid", sqlalchemy.String),
            sqlalchemy.Column("clientsecret", sqlalchemy.String),
            sqlalchemy.Column("scope", sqlalchemy.String),
        )