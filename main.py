from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Ваш JSON файл с данными
data = [
    {"latitude": 55.9671, "longitude": 37.44795, "description": "Здесь что-то произошло."},
    # Добавьте другие данные по аналогии
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
