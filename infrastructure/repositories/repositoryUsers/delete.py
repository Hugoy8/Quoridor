class Delete:
    def __init__(self, connection):
        self.connection = connection
        self.queries = connection.cursor()

    def execute(self, query, params=None):
        self.queries.execute(query, params)
        self.connection.commit()

    def close(self):
        self.queries.close()