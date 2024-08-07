import requests
import pytest
import requests_mock

@pytest.fixture
def mock_response():
    with requests_mock.Mocker() as m:
        # Simulamos la respuesta para obtener todas las películas
        m.get('http://localhost:5000/peliculas', json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulamos la respuesta para agregar una nueva película
        m.post('http://localhost:5000/peliculas', status_code=201, json={'id': 3, 'titulo': 'Pelicula de prueba', 'genero': 'Acción'})

        # Simulamos la respuesta para obtener detalles de una película específica
        m.get('http://localhost:5000/peliculas/1', json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})
        m.get('http://localhost:5000/peliculas/50', status_code=200, json={'mensaje': 'Id no encontrado'})

        # Simulamos la respuesta para actualizar los detalles de una película
        m.put('http://localhost:5000/peliculas/1', status_code=200, json={'id': 1, 'titulo': 'Nuevo título', 'genero': 'Comedia'})
        m.put('http://localhost:5000/peliculas/50', status_code=200, json={'mensaje': 'Id no encontrado'})

        # Simulamos la respuesta para eliminar una película
        m.delete('http://localhost:5000/peliculas/1', status_code=200, json={'mensaje': 'Película eliminada correctamente'})
        m.delete('http://localhost:5000/peliculas/50', status_code=200, json={'mensaje': 'Id no encontrado'})

        # Simulamos la respuesta para obtener películas por género
        m.get('http://localhost:5000/peliculas/genero/Acción', status_code=200)
        m.get('http://localhost:5000/peliculas/genero/No_existe', status_code=200, json={'mensaje': 'Género no encontrado'})

        # Simulamos la respuesta para obtener una película por su título
        m.get('http://localhost:5000/peliculas/string/Star', status_code=200)
        m.get('http://localhost:5000/peliculas/string/No_existe', status_code=200, json={'mensaje': 'Pelicula no encontrado'})

        # Simulamos la respuesta para obtener una película aleatoria
        m.get('http://localhost:5000/peliculas/random', status_code=200)
        m.get('http://localhost:5000/peliculas/random/No_existe', status_code=200, json={'mensaje': 'Género no encontrado'})

        # Simulamos la respuesta para obtener una película aleatoria por género
        m.get('http://localhost:5000/peliculas/random/Drama', status_code=200)
        m.get('http://localhost:5000/peliculas/random/No_existe', status_code=200, json={'mensaje': 'Género no encontrado'})

        # Simulamos la respuesta para obtener una película por género en un día feriado
        m.get('http://localhost:5000/peliculas/Drama/feriado', status_code=200)
        m.get('http://localhost:5000/peliculas/No_existe/feriado', status_code=200, json={'mensaje': 'Género no encontrado'})

        yield m

def test_obtener_peliculas(mock_response):
    response = requests.get('http://localhost:5000/peliculas')
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_agregar_pelicula(mock_response):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
    assert response.status_code == 201
    assert response.json()['id'] == 3

def test_obtener_detalle_pelicula(mock_response):
    response = requests.get('http://localhost:5000/peliculas/1')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'

def test_obtener_detalle_pelicula_error(mock_response):
    response = requests.get('http://localhost:5000/peliculas/50')
    assert response.status_code == 200

def test_actualizar_detalle_pelicula(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put('http://localhost:5000/peliculas/1', json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Nuevo título'

def test_actualizar_detalle_pelicula_error(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put('http://localhost:5000/peliculas/50', json=datos_actualizados)
    assert response.status_code == 200

def test_eliminar_pelicula(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/1')
    assert response.status_code == 200

def test_eliminar_pelicula_error(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/50')
    assert response.status_code == 200

def test_obtener_peliculas_por_genero(mock_response):
    response = requests.get(f'http://localhost:5000/peliculas/genero/Acción')
    assert response.status_code == 200

def test_obtener_pelicula_por_genero_error(mock_response):
    response = requests.get(f'http://localhost:5000/peliculas/genero/No_existe')
    assert response.status_code == 200

def test_obtener_pelicula_con_string(mock_response):
    response = requests.get(f'http://localhost:5000/peliculas/string/Star')
    assert response.status_code == 200

def test_obtener_pelicula_random(mock_response):
    response = requests.get('http://localhost:5000/peliculas/random')
    assert response.status_code == 200

def test_obtener_pelicula_random_error(mock_response):
    response = requests.get('http://localhost:5000/peliculas/random/No_existe')
    assert response.status_code == 200

def test_obtener_pelicula_random_por_genero(mock_response):
    response = requests.get(f'http://localhost:5000/peliculas/random/Drama')
    assert response.status_code == 200

def test_obtener_pelicula_random_por_genero_error(mock_response):
    response = requests.get(f'http://localhost:5000/peliculas/random/No_existe')
    assert response.status_code == 200

def test_obtener_pelicula_por_genero_en_feriado(mock_response):
    response = requests.get(f'http://localhost:5000/peliculas/Drama/feriado')
    assert response.status_code == 200

def test_obtener_pelicula_por_genero_en_feriado_error(mock_response):
    response = requests.get(f'http://localhost:5000/peliculas/No_existe/feriado')
    assert response.status_code == 200