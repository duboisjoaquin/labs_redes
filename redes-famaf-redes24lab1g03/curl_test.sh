#!/bin/bash

#creamos archivo para las salidas
touch salida.txt

#comentario en el archivo de salida
echo "---------------GET---------------" > salida.txt

#test GET
#obetener todas las peliculas
echo "Obtener todas las peliculas: " >> salida.txt
curl  http://127.0.0.1:5000/peliculas | jq >> salida.txt

#obetener pelicula especifica
echo "Obtener pelicula especifica: "
curl http://127.0.0.1:5000/peliculas/3 | jq >> salida.txt

#test POST
echo "---------------POST---------------" >> salida.txt

curl -X POST -H 'Content-Type: application/json' -d '{"titulo": "cars","genero": "infantil"}' http://127.0.0.1:5000/peliculas >> salida.txt

#chequeamos con get
echo "Chequeamos con get: " >> salida.txt
curl  http://127.0.0.1:5000/peliculas | jq >> salida.txt
echo "O especificamente : " >> salida.txt
curl http://127.0.0.1:5000/peliculas/13 | jq >> salida.txt

#test PUT
echo "---------------PUT---------------" >> salida.txt
curl -X PUT -H 'Content-Type: application/json' -d '{"titulo": "tarzan","genero": "infantil"}' http://127.0.0.1:5000/peliculas/13 >> salida.txt

echo "Chequeamos con get : " >> salida.txt
curl http://127.0.0.1:5000/peliculas/13 | jq >> salida.txt

#test DELETE
echo "---------------DELETE---------------" >> salida.txt
curl -X DELETE  http://127.0.0.1:5000/peliculas/13 >> salida.txt
echo "Chequeamos con get : " >> salida.txt
curl http://127.0.0.1:5000/peliculas | jq >> salida.txt

#test FILTRAR POR GENERO
echo "---------------FILTRAR POR GENERO---------------" >> salida.txt
curl http://127.0.0.1:5000/peliculas/genero/accion | jq >> salida.txt

echo "---------------FILTRAR POR GENERO RANDOM---------------" >> salida.txt
curl http://127.0.0.1:5000/peliculas/random/drama | jq >> salida.txt

#test Feriado
echo "---------------FILTRAR POR Feriado---------------" >> salida.txt
curl http://127.0.0.1:5000/peliculas/ciencia-ficcion/feriado | jq >> salida.txt