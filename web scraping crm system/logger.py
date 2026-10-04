def log(message):
    with open("log.txt", "a", encoding="utf-8") as file:
        file.write(message + "\n")

