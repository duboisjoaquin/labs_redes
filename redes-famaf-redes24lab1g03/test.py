import requests

# Obtener todas las películas
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(f"ID: {pelicula_agregada['id']}, Título: {pelicula_agregada['titulo']}, Género: {pelicula_agregada['genero']}")
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()

# Actualizar los detalles de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(f'http://localhost:5000/peliculas/{id_pelicula}', json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(f"ID: {pelicula_actualizada['id']}, Título: {pelicula_actualizada['titulo']}, Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()

# Eliminar una película
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película eliminada correctamente.\n")
else:
    print("Error al eliminar la película.\n")

#Obtener películas por género
generos = ["Acción", "No_existe"]
for genero in generos:
    print(f"Buscando una pelicula de género: {genero}\n")
    response = requests.get(f'http://localhost:5000/peliculas/genero/{genero}')
    peliculas_genero = response.json()
    if 'mensaje' in peliculas_genero:
        print(peliculas_genero['mensaje'])
    else:
        print(f"Películas del género {genero}:\n")
        for pelicula in peliculas_genero:
            print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}\n")        


#Obtener pelicula con string
strings = ["Star", "No_existe"]
for str in strings:
    print("Buscando una película con el string: " + str + "\n")
    response = requests.get(f'http://localhost:5000/peliculas/string/{str}')
    pelicula_str = response.json()
    if 'mensaje' in pelicula_str:
        print(pelicula_str['mensaje'])
        print("")
    else:
        print(f"Película con el string '{str}':")
        print(pelicula_str)
        print("")

#Obtener pelicula random
response = requests.get('http://localhost:5000/peliculas/random')
pelicula_random = response.json()
print("Película aleatoria:")
print(f"ID: {pelicula_random['id']}, Título: {pelicula_random['titulo']}, Género: {pelicula_random['genero']}\n`")

#Obtener pelicula random por genero
generos = ["Acción", "No_existe"]
for genero in generos:
    print(f"Buscando una pelicula de género: {genero}\n")
    response = requests.get(f'http://localhost:5000/peliculas/random/{genero}')
    pelicula_random_genero = response.json()
    if 'mensaje' in pelicula_random_genero:
        print(pelicula_random_genero['mensaje'])
        print("")
    else:
        print(f"Película aleatoria del género {genero}:")
        print(f"ID: {pelicula_random_genero['id']}, Título: {pelicula_random_genero['titulo']}, Género: {pelicula_random_genero['genero']}\n")

#Obtener pelicula por genero en un feriado
generos = ["Acción", "No_existe"]
for genero in generos:
    print(f"Buscando una pelicula de género: {genero}\n")
    response = requests.get(f'http://localhost:5000/peliculas/{genero}/feriado')
    pelicula_feriado_genero = response.json()
    if 'mensaje' in pelicula_feriado_genero:
        print(pelicula_feriado_genero['mensaje'])
        print("")
    else:
        print(f"Película del género {genero} en un feriado:")
        print(pelicula_feriado_genero)
        print("")

