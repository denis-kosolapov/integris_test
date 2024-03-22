from DataProcessing.DataProcessor import CoordinatesProcessor
from DataProcessing.CreateImage import create_graphic
from DataProcessing.CalculateBoundary import calculate_boundary


processor = CoordinatesProcessor()
processor.create_json_file()

calculate_boundary()

create_graphic()
