class Read:
    def __init__(self, connection):
        self.queries = connection.cursor()

    def execute(self, query, params=None):
        self.queries.execute(query, params)

    def fetchone(self):
        return self.queries.fetchone()

    def close(self):
        self.queries.close()