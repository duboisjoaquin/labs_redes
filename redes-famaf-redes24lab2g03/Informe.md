## Integrantes 
- Mateo Ricci
- Joaquin Dubois
- Santiago Miranda


## Preguntas
- ¿Qué estrategias existen para poder implementar este mismo servidor pero con
capacidad de atender múltiples clientes simultáneamente?

        Existen dos formas de implementar el paradigma cliente servidor tomando las request de varios clientes a la vez. 

        Threading: Usar threads como alternativa para atender a varios clientes es una buena solucion como un primer acercamiento, aunque esta opcion no es del todo simultanea, ya que los hilos en python se trabajan de manera concurrente 

        Poll: Poll es una nueva forma de utilizar el metodo select, en la cual la diferencia entre los dos radica en la interfaz que proveen al programador para escuchar los distintos sockets que transmiten informacion, a diferencia de select donde el set predefinido para representar un socket es una cadena (algunas veces muy grande) de bits, en poll solamente se maneja un arreglo de estructuras que representan dicho socket
        con esto se puede manejar varios procesos a la vez ya que poll avisa al servidor cuando algo de informacion esta entrando por un socket   

- ¿Qué diferencia hay si se corre el servidor desde la IP “localhost”, “127.0.0.1” o la ip “0.0.0.0”?

        Las ip “localhost” y “127.0.0.1” son la misma direccion de ip, la cual se conecta con el propio equipo, localhost es la constante asignada a la ip “127.0.0.1” asi que no habria cambios corriendo el servidor en ninguna de las dos 

        La ip "0.0.0.0" representa una ruta por defecto cuando se utiliza en tabla de enrutamientos, tambien se utiliza por acuerdo general como una referencia general para todas las IP que no están en la red interna.

