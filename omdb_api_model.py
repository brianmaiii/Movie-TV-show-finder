# Armin Abaye - aabaye.
# Yanely Hernandez - yanelyh.
# Brian Mai - bamai.


import json
import urllib.parse
import urllib.request
import csv
from pathlib import Path
import os


class Model:

    def __init__(self):
        """Constructor that initializes api attributes."""
        self.API_KEY = '51d24da8'
        self.BASE_URL = 'http://www.omdbapi.com/?t='

    def build_url(self, query):
        """Builds the initial URL."""
        query = query.replace(" ", "+")
        return self.BASE_URL + query + '&' + 'apikey=' + self.API_KEY

    def get_result(self, url):
        """Gets the results from API and returns it back to python."""
        response = None
        try:
            response = urllib.request.urlopen(url)
            json_text = response.read().decode(encoding='utf-8')
            return json.loads(json_text)

        finally:
            if response != None:
                response.close()

    def get_total_seasons(self, overview):
        """Gets the total number of seasons."""
        total_seasons = overview['totalSeasons']
        return int(total_seasons)

    def get_total_seasons_url(self, seasonNum, query):
        """Gets the url for all the seasons of the show."""
        listSeasonsUrl = []
        query = query.replace(" ", "+")
        for x in range(seasonNum):
            listSeasonsUrl.append(self.BASE_URL + query + '&' +
                                  '&r=json&type=series&Season=' + str(x+1) + '&' + 'apikey=' + self.API_KEY)
        return listSeasonsUrl

    def get_list_episodes(self, list_seasons_url):
        """Returns a list of the episodes."""
        list_episodes = []
        for x in list_seasons_url:
            list_episodes.append(self.get_result(x))
        return list_episodes

    def print_all_episodes(self, list_episodes):
        """Prints all the episodes."""
        for y in range(len(list_episodes)):
            for x in list_episodes[y]['Episodes']:
                print("Season: %s, Episode: %s, Title: %s" % (str(y+1), x["Episode"], x['Title']))

    def user_input_five(self):
        """Picks five episodes from the list."""
        seasons_and_episodes = []
        counter = 0
        while True:
            user_input = input('Enter Season# first, space and then Episode# (ex.1 2): ')
            split = user_input.split()
            try:
                list_episodes_nums = []
                dummy = list_episodes[int(split[0])-1]
                for x in list_episodes[int(split[0])-1]['Episodes']:
                    list_episodes_nums.append(x['Episode'])
                if split[1] not in list_episodes_nums:
                    raise Exception
                seasons_and_episodes.append(user_input)
                counter += 1
            except:
                print("season dne or episode dne")
            if counter == 5:
                break
        lines = '\n'.join(seasons_and_episodes)
        season_episode_list = lines.split('\n')
        season_episode_list.sort()
        season_episode_list = sort_epi(season_episode_list)
        return season_episode_list

    def input_episode(self, episode, list_episodes):
        """Inputs episode to the list."""
        seasons_and_episodes = []
        user_input = episode
        list_episodes = list_episodes
        split = user_input.split()
        try:
            list_episodes_nums = []
            dummy = list_episodes[int(split[0])-1]
            for x in list_episodes[int(split[0])-1]['Episodes']:
                list_episodes_nums.append(x['Episode'])
            if split[1] not in list_episodes_nums:
                raise Exception
            seasons_and_episodes.append(user_input)
            lines = '\n'.join(seasons_and_episodes)
            season_episode_list = lines.split('\n')
            return season_episode_list
        except:
            print("season dne or episode dne")

    def sort_epi(self, listo):
        """Sorts the episodes."""
        for x in range(len(listo)):
            listo[x] = listo[x].split()
        for y in range(len(listo)):
            for x in range(len(listo)):
                try:
                    if int(listo[x][1]) > int(listo[x + 1][1]) and int(listo[x][0]) >= int(listo[x+1][0]):
                        temp = listo[x+1]
                        listo[x+1] = listo[x]
                        listo[x] = temp
                except:
                    pass
        for x in range(len(listo)):
            listo[x] = " ".join(listo[x])
        return listo

    def user_picks_five(self, season_episode_list, query):
        """Takes the user input and creates the URL's."""
        listSeasonsUrl = []
        query = query.replace(" ", "+")
        for x in season_episode_list:
            season = x[0]
            episode = x[2:]
            listSeasonsUrl.append(self.BASE_URL + query + '&' + '&r=json&type=series&Season=' + season + '&' + 'Episode=' + episode + '&' +
                                  'apikey=' + self.API_KEY)
        return listSeasonsUrl

    def print_five_episodes(self, list_episodes):
        """Prints out the information for the 5 episodes needed."""
        for y in list_episodes:
            print("Title: %s, Season: %s, Episode: %s, Plot: %s" %
                  (y['Title'], y['Season'], y['Episode'], y['Plot']))

    def user_preferred_path(self):
        """Asks the user where they would like to save the information."""
        user_input = input("Where would you like to save your csv file? ")
        return user_input

    def create_path(self, directory):
        """Creates the Path."""
        pwd = str(Path.home())
        directory = os.path.join(pwd, directory)
        if os.path.isdir(directory):
            csv_file = os.path.join(pwd, directory, 'Omdb_Results.csv')
            return csv_file
        else:
            print('Not a valid entry: ')
            user_preferred_path()

    def create_csv(self, path, list_episodes):
        """Creates the csv."""
        with open(path, 'w', newline='') as f:
            fieldnames = ['Episode Title', 'Season Number', 'Episode Number', 'Plot Summary']
            thewriter = csv.DictWriter(f, fieldnames=fieldnames)

            thewriter.writeheader()

            for y in list_episodes:
                thewriter.writerow({'Episode Title': y['Title'], 'Season Number': y['Season'],
                                    'Episode Number': y['Episode'], 'Plot Summary': y['Plot']})
