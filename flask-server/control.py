from database import Database
from csv_reader import CSVReader


class Control():

    def __init__(self):
        self.database = Database()
        self.csv_reader = CSVReader()

    def load_rawfile(self, json):
        #data, time_string,  timestamp_column, number_chars_timestamp, inseconds
        data = self.csv_reader.read_data(
            json["content"]["data"], json["timestampformat"], json["timestampcolumn"], 8, False)
        print(data)
        self.database.update_latest_log(data)
