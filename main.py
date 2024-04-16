import argparse
import csv
import os
TEAMS_FILENAME = "teams.csv"
INSTITUTIONS_FILENAME = "institutions.csv"


class Institution:
    """
    Simple class to represent an institution.
    """

    def __init__(self, id, name, city, state, country):
        self.id: int = id
        self.name: str = name
        self.city: str = city
        self.state: str = state
        self.country: str = country

    def __str__(self):
        # Institution representation as csv string
        return f"{self.id},{self.name},{self.city},{self.state},{self.country}"


class Team:
    """
    Simple class to represent a team.
    """

    def __init__(self, team_number, advisor, problem, ranking, institution_id):
        self.team_number: int = team_number
        self.advisor: str = advisor
        self.problem: str = problem
        self.ranking: str = ranking
        self.institution_id: int = institution_id

    def __str__(self):
        # Team representation as csv string
        return f"{self.team_number},{self.advisor},{self.problem},{self.ranking},{self.institution_id}"


def main(filename):
    """
    Load in the institutions and teams from the csv
    file and write them to the csv files.
    """
    institutions = load_institutions(filename)
    teams = load_teams(filename, institutions)
    write_teams(teams)
    write_institutions(institutions)


def load_institutions(filename):
    """
    Produce a dictionary of institutions with the name as the key
    and an Institution object as the value.
    """
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=",")
        # Ignore header
        next(reader)

        # Initialize instution dictionary
        institutions = {}

        for line in reader:
            # Check if the institution already exists
            institution = institutions.get(line[0], None)
            if institution is None:
                # Institution doesn't exist, create a new one
                institution = Institution(
                    # Simple counter for ids
                    id=len(institutions),

                    # Load institution data from team
                    name=line[0],
                    city=line[2],
                    state=line[3],
                    country=line[4]
                )
                institutions[line[0]] = institution
        return institutions


def load_teams(filename, institutions):
    """
    Produce a list of teams from the csv file.
    """
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=",")
        # Ignore header
        next(reader)

        # Initialize team list
        teams = []

        for line in reader:
            # Create team
            teams.append(Team(
                team_number=int(line[1]),
                advisor=line[5],
                problem=line[6],
                ranking=line[7],
                institution_id=institutions.get(line[0]).id
            ))
        return teams


def write_teams(teams):
    """
    Write list of Team objects to csv.
    """
    # Delete teams.csv if it exists
    if os.path.exists(TEAMS_FILENAME):
        os.remove(TEAMS_FILENAME)

    # Create teams.csv file
    with open(TEAMS_FILENAME, 'a') as file:
        # Header
        file.write("Team,Advisor,Problem,Ranking,Institution\n")

        # Team data
        for team in teams:
            file.write(str(team) + "\n")


def write_institutions(institutions):
    """
    Write dict of Institution objects to csv.
    """
    # Delete institutions.csv if it exists
    if os.path.exists(INSTITUTIONS_FILENAME):
        os.remove(INSTITUTIONS_FILENAME)

    # Create institutions.csv file
    with open(INSTITUTIONS_FILENAME, 'a') as file:
        # Header
        file.write("Name,City,State,Country\n")

        # Institution data
        for institution in institutions.values():
            file.write(str(institution) + "\n")


if __name__ == "__main__":
    # Get the filename of the result file
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    filename = parser.parse_args().filename
    main(filename)
