if __name__ == "__main__":

    file_name = ""

    with open(file_name, "r") as file:

        total = 0
        succes = 0

        reader = csv.DictReader(file)
            for row in reader:
                total += 1
                solved= row["solved"]
                if solved:
                    succes += 1

        percentage = succes/total