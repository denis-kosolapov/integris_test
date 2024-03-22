import json
from flask import Flask, render_template, request, jsonify, send_file
import os, io
from DataProcessing.CalculateBoundary import calculate_boundary



app = Flask(__name__)

# Установка директории для загруженных файлов
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "uploaded_files")


# Главная страница
# Здесь просто прямоугольная область координат
@app.route('/')
def index():
    return render_template('index.html', rectangle_points=calculate_boundary())


# отобразить карту с точками
@app.route('/get_data')
def get_data():
    # Открываем файл JSON и загружаем данные
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)

    # Выводим первые 100 точек
    first_100_points = data[:100]

    # Возвращаем данные в формате JSON
    return jsonify(first_100_points)

# отобразить картинку
@app.route('/new_route')
def get_image():
    plot_path = 'plot.png'  # Путь к изображению
    return send_file(plot_path, mimetype='image/png')



# Страница загрузки файлов
@app.route('/downloads')
def downloads():
    return render_template('downloads.html')


# Загрузка файла
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Файл не был загружен'

    file = request.files['file']
    if file.filename == '':
        return 'Не выбран файл'

    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f'Файл {filename} успешно загружен'


if __name__ == '__main__':
    app.run(debug=True)




