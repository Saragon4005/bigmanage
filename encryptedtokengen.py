from SKCY11X import fileio
import getpass


def gentoken():
	token = input("Paste discord token: ")
	fileobj = fileio(".bot_token", getpass.getpass("Enter password: "))
	fileobj.write(token.encode("utf8"))
	fileobj.close()


if __name__ == "__main__":
	gentoken()
