# Interfaz Multimodal Adaptativa para Accesibilidad Computacional

## Descripción

Este proyecto implementa una interfaz multimodal adaptativa diseñada para mejorar la accesibilidad en la interacción con computadoras. Combina tecnologías de visión por computadora, dispositivos de entrada especializados y procesamiento en tiempo real para proporcionar una experiencia de usuario fluida y personalizable para personas con diversas capacidades motoras.

## Características Principales

### 1. Modos de Operación Múltiples
- **Joystick Dual**: Control preciso utilizando dos joysticks.
- **Webcam y Sip-and-Puff**: Combina seguimiento facial con entrada de soplido/succión.
- **Joystick y Sip-and-Puff**: Integra control de joystick con comandos de soplido/succión.

### 2. Seguimiento Facial Avanzado
- Utiliza MediaPipe para detección facial y puntos de referencia en tiempo real.
- Implementa algoritmos de filtrado adaptativo para estabilizar el movimiento del cursor.

### 3. Interfaz Gráfica Personalizable
- Desarrollada con Tkinter para una experiencia de usuario intuitiva.
- Permite ajustes en tiempo real de sensibilidad y modos de operación.

### 4. Integración de Sip-and-Puff
- Soporta comandos complejos como clic, doble clic y clic sostenido.
- Manejo robusto de conexión y reconexión del dispositivo.

### 5. Procesamiento Multihilo
- Utiliza `multiprocessing` para optimizar el rendimiento en tareas simultáneas.
- Garantiza una respuesta fluida del sistema incluso con múltiples entradas.

### 6. Calibración y Adaptabilidad
- Funciones de auto-calibración para adaptarse a diferentes usuarios y entornos.
- Ajustes de sensibilidad independientes para ejes X e Y en cada modo.

### 7. Compatibilidad con Sistema Operativo
- Diseñado para Windows, con uso extensivo de la API Win32.
- Integración con funciones del sistema para control preciso del cursor y eventos de teclado.

### 8. Procesamiento de Video en Tiempo Real
- Captura y procesa video de webcam con OpenCV.
- Implementa técnicas de visión por computadora para seguimiento facial preciso.

### 9. Manejo Avanzado de Estados
- Sistema robusto de manejo de estados para transiciones suaves entre modos y funciones.
- Prevención de conflictos entre diferentes métodos de entrada.

### 10. Accesibilidad y Usabilidad
- Diseñado con principios de diseño universal.
- Proporciona retroalimentación visual y auditiva para acciones del usuario.

## Tecnologías Utilizadas

- **Python**: Lenguaje principal de desarrollo.
- **OpenCV**: Para procesamiento de video y visión por computadora.
- **MediaPipe**: Framework de Google para detección facial y de puntos de referencia.
- **Tkinter**: Para la interfaz gráfica de usuario.
- **Pyserial**: Para comunicación con dispositivos seriales (Sip-and-Puff).
- **Win32API**: Para interacción de bajo nivel con el sistema operativo Windows.
- **Numpy**: Para cálculos numéricos eficientes.
- **Multiprocessing**: Para manejo de procesos paralelos.

## Instalación y Configuración

1) Instalar las dependencias del archivo requeriments.txt

2) Para ejecutar desde consola (CMD)

Ejecutar Archivo "iniciarPrograma.py" desde consola 

opcional:

PARA COMPILAR: en consola escribir  pyinstaller --debug=all iniciarPrograma.spec --windowed --onefile (debe estar incluido el archivo iniciarPrograma.spec en la carpeta) 

NOTA: Incluir archivo imagen "plantilla_interfaz v2.png" en la carpeta dist una vez compilado el programa

No es necesario que estén todos los periféricos conectados para que el programa funcione, a excepción de la webcam. Sin embargo se recomienda tener al menos el joystick de PS4


## Uso

[EN CONSTRUCCIÓN]

## Licencia

Copyright (c) 2024 Leonardo Riffo A.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

## Contacto

leonardo.riffo@biomedica.udec.cl
