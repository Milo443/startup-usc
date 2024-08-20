# Startup USC

Startup USC es una aplicación web desarrollada con Django que permite a los usuarios crear y evaluar ideas de startups utilizando la API de OpenAI.

## Características

- Creación de formularios relacionados para recopilar información sobre una idea de startup.
- Generación de un análisis de viabilidad y puntos a mejorar para la startup utilizando la API de OpenAI.
- Visualización de los resultados del análisis de la startup.

## Tecnologías Utilizadas

- Python
- Django
- HTML/CSS
- Bootstrap
- OpenAI API

## Instalación y Configuración

1. Clona el repositorio:
git clone https://github.com/Milo443/startup-usc.git
 
2. Crea y activa un entorno virtual:
python -m venv venv
source venv/bin/activate
 
3. Instala las dependencias:
pip install -r requirements.txt

4. Configura las variables de entorno necesarias, como la clave de la API de OpenAI.

5. Realiza las migraciones de la base de datos:
python manage.py migrate
 
6. Inicia el servidor de desarrollo:
python manage.py runserver
 
7. Accede a la aplicación en tu navegador: `http://localhost:8000`

## Uso

1. Completa el formulario de creación de la startup con la información relevante.
2. Haz clic en el botón "Generar Análisis" para obtener los resultados del análisis de viabilidad y los puntos a mejorar.
3. Revisa los resultados y utiliza la información para mejorar tu idea de startup.

## Contribución

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama para tu funcionalidad: `git checkout -b feature/nueva-funcionalidad`.
3. Realiza los cambios y commits necesarios.
4. Envía un pull request describiendo tus cambios.
