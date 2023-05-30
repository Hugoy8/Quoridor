from infrastructure.database.config import Database

run = Database()
# a = run.selectUsername("192_167_1_155", 8000, 2)
# run.addWin(a)

run.dropTableIfExists("192_167_1_155", 8000)
run.createTableGame("192_167_1_155", 8000)

# run.insertUsername("192_167_1_155", 8000, "test1")
# run.insertUsername("192_167_1_155", 8000, "test2")
# run.insertUsername("192_167_1_155", 8000, "test3")
# run.insertUsername("192_167_1_155", 8000, "test4")

# run.deconnexionUser("192_167_1_155", 8000, 2)

# run.insertUsername("192_167_1_155", 8000, "test2")

# run.refreshTabel("192_167_1_155", 8000)