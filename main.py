from domain.launcher.launcher import QuoridorLauncher
from infrastructure.database.config import Database

run = QuoridorLauncher(Database())
