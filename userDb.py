from infrastructure.database.config import Database

run = Database()
# a = run.selectUsername("127_0_0_1", 8000, 2)
# run.addWin(a)

run.dropTableIfExists("127_0_0_1", 8000)
run.createTableGame("127_0_0_1", 8000)

run.insertUsername("127_0_0_1", 8000, "test1")
run.insertUsername("127_0_0_1", 8000, "test2")
run.insertUsername("127_0_0_1", 8000, "test3")
run.insertUsername("127_0_0_1", 8000, "test4")

run.deconnexionUser("127_0_0_1", 8000, 2)

run.insertUsername("127_0_0_1", 8000, "test2")

run.refreshTabel("127.0.0.1", 8000)