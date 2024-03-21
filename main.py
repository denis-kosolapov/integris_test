from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Установка директории для загруженных файлов
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "uploaded_files")

# JSON данные
data = [
    {'time': '2024-02-13T07:18:24.000Z', 'lat': 55.967101667, 'lon': 37.447898333, 'altHAE': 218.2}
    # Добавьте другие данные по аналогии
]


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')


# Получение данных в формате JSON
@app.route('/get_data')
def get_data():
    return jsonify(data)


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
