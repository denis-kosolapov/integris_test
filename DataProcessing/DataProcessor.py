import pandas as pd
from settings import UPLOADED_FILES, ROOT
from collections import OrderedDict
import os
import asyncio
import json


class UniqueCoordinatesProcessor:

    """
    Этот класс проверяет папку UPLOADED_FILES на наличие файла csv.
    Если файл существует, то он преобразует его во множество кортежей
    """

    def __init__(self, chunk_size=1000):
        self.folder_path = UPLOADED_FILES
        self.chunk_size = chunk_size
        self.timestamps_set = OrderedDict()
        self.csv_file = self.find_csv_file()

    def find_csv_file(self):
        for file in os.listdir(self.folder_path):
            if file.endswith('.csv'):
                return f"{self.folder_path}/{file}"
        return None

    # Функция для обработки чанка данных
    async def process_chunk(self, chunk):
        # Множество для хранения уникальных координат и высот
        unique_coordinates = set()
        # Множество для хранения уникальных координат и высот текущего чанка
        processed_coordinates = set()
        for index, row in chunk.iterrows():
            coordinates = (row['lat'], row['lon'], row['altHAE'])
            timestamp = row['time']
            if coordinates in self.timestamps_set:
                existing_timestamp = self.timestamps_set[coordinates]
                if existing_timestamp != timestamp:
                    # print(f"Изменение координат/высоты: {coordinates}")
                    self.timestamps_set[coordinates] = timestamp
            else:
                self.timestamps_set[coordinates] = timestamp
                coordinates = (self.timestamps_set[coordinates],) + coordinates
                # Добавляем уникальные координаты и высоту во временное множество
                processed_coordinates.add(coordinates)
        # Добавляем уникальные координаты и высоты текущего чанка в основное множество
        unique_coordinates.update(processed_coordinates)
        if unique_coordinates:
            return unique_coordinates

    # Чтение данных по чанкам и обработка их асинхронно
    async def read_and_process_chunks(self):
        # Множество для хранения всех уникальных координат и высот
        all_unique_coordinates = set()
        for chunk in pd.read_csv(self.csv_file, chunksize=self.chunk_size):
            unique_coordinates = await self.process_chunk(chunk)
            if unique_coordinates:
                # Объединяем уникальные координаты из текущего чанка
                all_unique_coordinates.update(unique_coordinates)
        return all_unique_coordinates

    # Запуск асинхронного чтения и обработки чанков данных
    async def main(self):
        all_unique_coordinates = await self.read_and_process_chunks()
        # Преобразовать множество уникальных координат в список
        unique_coordinates_list = list(all_unique_coordinates)
        # Отсортировать список по дате и времени (первый элемент кортежа)
        # sorted_unique_coordinates = sorted(unique_coordinates_list, key=lambda x: x[0])
        return unique_coordinates_list


class CoordinatesProcessor(UniqueCoordinatesProcessor):

    """
    Этот класс преобразует множество кортежей во множество словарей
    """
    def __init__(self, chunk_size=100):
        super().__init__()
        self.chunk_size = chunk_size

    async def split_into_chunks_async(self, sorted_unique_coordinates):
        # разбиение множества кортежей на части
        chunks = []
        for i in range(0, len(sorted_unique_coordinates), self.chunk_size):
            chunk = sorted_unique_coordinates[i:i + self.chunk_size]
            chunks.append(chunk)
        return chunks

    def tuple_to_dict(self, coordinate):
        keys = ['time', 'lat', 'lon', 'altHAE']
        # преобразование одного кортежа в словарь
        return {key: value for key, value in zip(keys, coordinate)}

    async def chunks_to_dicts(self, chunks):
        # преобразование части множества кортежей в словари
        dicts_list = []
        for chunk in chunks:
            dicts = [self.tuple_to_dict(coordinate) for coordinate in chunk]
            dicts_list.extend(dicts)
        return dicts_list

    async def sort_dicts_by_time(self, dicts_list):
        # сортировка всех словарей в списке по дате и времени (хронологический порядок)
        return sorted(dicts_list, key=lambda x: x['time'])

    async def main(self):
        # сначала выполняется преобразование csv в множество кортежей
        sorted_unique_coordinates = await super().main()
        # затем множество кортежей преобразуется во множество словарей
        chunks = await self.split_into_chunks_async(sorted_unique_coordinates)
        dicts_list = await self.chunks_to_dicts(chunks)
        sorted_dicts = await self.sort_dicts_by_time(dicts_list)
        return sorted_dicts

# if __name__ == "__main__":
#     processor = CoordinatesProcessor()
#     dicts_list = asyncio.run(processor.main())
#     print(len(dicts_list))
#     for dictionary in dicts_list:
#         print(dictionary)

# if __name__ == "__main__":
#     processor = UniqueCoordinatesProcessor()
#     sorted_unique_coordinates = asyncio.run(processor.main())
#     print(len(sorted_unique_coordinates))
#     for i in sorted_unique_coordinates:
#         print(i)

if __name__ == "__main__":
    processor = CoordinatesProcessor()
    dicts_list = asyncio.run(processor.main())

    # Путь к выходному JSON файлу
    output_json_file_path = f'{ROOT}/data.json'

    # Запись первых 10 точек в новый JSON файл
    with open(output_json_file_path, 'w') as output_json_file:
        json.dump(dicts_list, output_json_file, indent=4)
