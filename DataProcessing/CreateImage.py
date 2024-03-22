import json
import pandas as pd
import matplotlib.pyplot as plt
from settings import *

j_file = f'{DATA}/data.json'

def create_graphic():
    # Чтение данных из файла JSON
    with open(j_file, 'r') as file:
        data = json.load(file)

    # Преобразование данных в DataFrame
    df = pd.DataFrame(data)

    # Преобразование строки времени в формат datetime
    df['time'] = pd.to_datetime(df['time'])

    # Сортировка данных по времени
    df = df.sort_values(by='time')

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(df['time'], df['altHAE'])
    plt.title('Высота от времени')
    plt.xlabel('Время')
    plt.ylabel('Высота, м')
    plt.grid(True)
    plt.savefig(f'{IMAGES}/plot.png')

