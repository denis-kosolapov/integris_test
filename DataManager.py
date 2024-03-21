import os
import pandas as pd
import json

# Класс для работы с данными из CSV
class CSVDataManager:
    def __init__(self, filename):
        self.filename = filename

    # Метод для чтения данных из CSV файла
    def read_csv_data(self):
        try:
            data = pd.read_csv(self.filename)
            return data
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

    # Метод для сохранения данных в формате JSON
    def save_as_json(self, dataframe, output_filename=None):
        if output_filename is None:
            base_filename, _ = os.path.splitext(self.filename)
            output_filename = f"{base_filename}.json"

        try:
            dataframe.to_json(output_filename, orient='records')
            print(f"Данные сохранены в файл {output_filename}")
            return output_filename
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return None

    # Метод для чтения данных из JSON файла
    def read_json_data(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

    # Метод для чтения JSON данных из файла, имеющего тот же путь и имя, что и CSV файл
    def read_json_data_same_name(self):
        base_filename, _ = os.path.splitext(self.filename)
        json_filename = f"{base_filename}.json"
        return self.read_json_data(json_filename)

    # Метод для чтения данных из CSV файла и преобразования их в список словарей
    def read_csv_data_as_json(self):
        try:
            data = pd.read_csv(self.filename)
            json_data = data.to_dict(orient='records')
            return json_data
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

# # Пример использования
# filename = '20240213_1000.csv'
#
# dm = CSVDataManager(filename)
# json_data = dm.read_csv_data_as_json()
#
# print(json_data[1000])