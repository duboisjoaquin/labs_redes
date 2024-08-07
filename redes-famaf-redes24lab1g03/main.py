from flask import Flask, jsonify, request
import random
import proximo_feriado
from unidecode import unidecode

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]


def format_word(palabra):
    # Esta funcion parsea las palabras, eliminando espacios, guiones y mayusculas ciencia ficcion
    palabra_f = palabra.replace('-', ' ') # Reemplazo los guiones por espacios
    palabra_f = palabra_f.strip().lower() # Elimino espacios y paso a minusculas
    palabra_f = unidecode(palabra_f) # Elimino tildes
    return palabra_f

def obtener_peliculas():
    return jsonify(peliculas)


def obtener_pelicula(id):
    pelicula_encontrada = {'mensaje': 'Id no encontrado'}
    for p in peliculas:
        if p['id'] == id:
            pelicula_encontrada = p
    # Lógica para buscar la película por su ID y devolver sus detalles
    return jsonify(pelicula_encontrada)


def agregar_pelicula():

    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id):
    pelicula_actualizada = {
        'id': id,
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    for i in range(0, len(peliculas)):
        if peliculas[i]['id'] == id:
            peliculas[i] = pelicula_actualizada
            return jsonify(pelicula_actualizada)
        
    return jsonify({'mensaje': 'Id no encontrado'})


def eliminar_pelicula(id):
    for p in peliculas:
        if p['id'] == id:
            peliculas.remove(p)
            return jsonify({'mensaje': format_word('Película eliminada correctamente')})
    return jsonify({'mensaje': 'Id no encontrado'})


def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1
    
def peliculas_de_genero(genero):
    peliculas_genero = []
    for p in peliculas:

        palabra_ok = format_word(genero)
        print("Genero: ", palabra_ok)
        if format_word(p['genero']) == palabra_ok:
            peliculas_genero.append(p)

    if len(peliculas_genero) == 0:
        return jsonify({'mensaje': 'Género no encontrado'})
    else:
        return jsonify(peliculas_genero)

def pelicula_con_string(str):
    pelicula_str = {'mensaje': 'Pelicula no encontrado'}
    for p in peliculas:
        if format_word(str) in format_word(p['titulo']):
            pelicula_str = p
    return jsonify(pelicula_str)

def pelicula_random():
    return jsonify(random.choice(peliculas))

def pelicula_random_genero(genero):
    pelicula_genero = titulo_random_genero(genero)
    return jsonify(pelicula_genero)

def titulo_random_genero(genero):
    peliculas_genero = []
    for p in peliculas:
        if format_word(p['genero']) == format_word(genero):
            peliculas_genero.append(p)
    if len(peliculas_genero) == 0:
        err = {'mensaje': 'Género no encontrado'}
        return err
    else:
        return random.choice(peliculas_genero)

def pelicula_en_feriado(gen : str):
    next_holiday = proximo_feriado.NextHoliday()
    next_holiday.fetch_holidays()
    pelicula = titulo_random_genero(gen)

    try:
        pelicula['mensaje']
        return jsonify(pelicula)
    except KeyError:
        titulo = pelicula['titulo']
        mes = proximo_feriado.months[next_holiday.holiday['mes'] - 1]
        res = {"Dia": next_holiday.holiday['dia'],"Mes": mes,"Motivo": next_holiday.holiday['motivo'], "Pelicula": titulo}
        
        return jsonify(res)


app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])
app.add_url_rule('/peliculas/genero/<string:genero>', 'peliculas_de_genero', peliculas_de_genero, methods=['GET'])
app.add_url_rule('/peliculas/string/<string:str>', 'pelicula_con_string', pelicula_con_string, methods=['GET'])
app.add_url_rule('/peliculas/random', 'pelicula_random', pelicula_random, methods=['GET'])
app.add_url_rule('/peliculas/random/<string:genero>', 'pelicula_random_genero', pelicula_random_genero, methods=['GET'])
app.add_url_rule('/peliculas/<string:gen>/feriado', 'pelicula_en_feriado', pelicula_en_feriado, methods=['GET'])

if __name__ == '__main__':
    app.run()
