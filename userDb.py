from infrastructure.database.config import Database

run = Database()
a = run.selectUsername("127_0_0_1", 8000, 2)
run.addWin(a)