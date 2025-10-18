para la compilacion de los ejercicios del examen:
1. 
    existen 3 archivos urdf, el del pulgar, el indice y el robot doble que cuentan con ambos
    dentro del archivo view_robot.launch.py estan las lineas de codigo para compilar depende
    al que se quiera probar

    para el movimiento de los robots se consideran los siguientes comandos:
        pulgar: ros2 run visual_pubsub inverse_k_p
        indice: ros2 run visual_pubsub inverse_k

    para compilar los archivos urdf:
        ros2 launch robot_description view_robot.launch.py

    el robot doble funciona con los comandos para el movimiento de cada articulacion

2. 
    se deben compilar los 5 nodos en terminales diferentes para el ejercicio
        ros2 run sensor_network sensor_1_node
        ros2 run sensor_network sensor_2_node
        ros2 run sensor_network sensor_3_node
        ros2 run sensor_network node_compiler
        ros2 run sensor_network node_display