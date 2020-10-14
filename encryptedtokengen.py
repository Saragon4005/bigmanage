from SKCY11X import fileio
import getpass
token = input("Paste discord token: ")
password = getpass.getpass("Enter password: ")
fileobj = fileio(".bot_token", password)
fileobj.write(token.encode("utf8"))
fileobj.close()
