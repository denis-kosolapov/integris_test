import pandas as pd

# Чтение данных из CSV файла с помощью Pandas
def read_csv_data(filename):
    data = pd.read_csv(filename)
    return data

# Сохранение данных в формате JSON
def save_as_json(dataframe, output_filename):
    dataframe.to_json(output_filename, orient='records')

# Пример использования
filename = '20240213_1000.csv'
output_filename = '20240213_1000.json'

data = read_csv_data(filename)
save_as_json(data, output_filename)

