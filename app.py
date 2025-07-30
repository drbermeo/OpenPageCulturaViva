import streamlit as st # Importa la librería Streamlit, esencial para construir la interfaz de usuario de la aplicación web.
import pandas as pd # Importa Pandas, utilizada para la manipulación y visualización de datos en formato de tabla (DataFrames).
import folium # Importa Folium, para crear mapas interactivos y agregar marcadores.
from streamlit_folium import st_folium # Importa un componente específico de Streamlit para incrustar mapas de Folium en la aplicación.
import plotly.express as px # Importa Plotly Express, una librería para crear gráficos interactivos y visualizaciones de datos de alto nivel.
import plotly.graph_objects as go # Importa Plotly Graph Objects, para construir gráficos más personalizados y complejos (ej. el gráfico de influencias).
import datetime # Importa la librería datetime, para manejar y formatear fechas, esencial para las líneas de tiempo.
import random # Importa random, usado para seleccionar un dato curioso aleatorio en la sección "Sabías que...".


# Importar las funciones de consulta SPARQL desde sparql_queries.py
# Asegúrate de que el archivo sparql_queries.py esté en la misma carpeta o en una ruta accesible
from sparql_queries import ( # Importa funciones específicas de otro archivo para realizar consultas SPARQL.
    get_monuments_or_places_in_ecuador, # Función para obtener monumentos o lugares en Ecuador.
    get_ecuadorian_personalities, # Función para obtener personalidades ecuatorianas.
    get_global_wars_and_conflicts, # Función para obtener guerras y conflictos globales.
    get_unesco_world_heritage_sites, # Función para obtener sitios de Patrimonio Mundial de la UNESCO.
    get_influencer_relationships, # Función para obtener relaciones de influencia entre personalidades.
    get_ecuadorian_musicians # Función para obtener músicos ecuatorianos.
)

# --- Configuración de la Página Streamlit ---
# Configura el diseño de la página para que sea amplio y establece el título de la pestaña del navegador.
st.set_page_config(layout="wide", page_title="CulturaViva")

# Título principal de la aplicación que se muestra al usuario.
st.title("🌎 CulturaViva: Desbloqueando el Patrimonio con Linked Open Data")

# --- Sidebar para Filtros y Búsqueda ---
# Crea una barra lateral en la que los usuarios pueden seleccionar el tipo de entidad a explorar
# y también ingresar términos de búsqueda.
with st.sidebar: # Inicia un bloque de código para la barra lateral de Streamlit.
    st.header("🔍 Filtros y Búsqueda") # Encabezado para la sección de filtros.

    # Radio buttons para seleccionar el tipo de contenido a mostrar.
    entity_type = st.radio( # Crea un conjunto de botones de radio para que el usuario elija el tipo de contenido.
        "¿Qué quieres explorar?", # Pregunta mostrada al usuario.
        ("Inicio", # Opción para la pantalla de bienvenida.
         "Lugares", "Personalidades", "Músicos", # Opciones para diferentes categorías de datos.
         "Conflictos/Guerras Globales", # Opción para conflictos y guerras.
         "Patrimonio de la Humanidad (UNESCO)", # Opción para sitios UNESCO.
         "Gráfico de Influencias") # Opción para el gráfico de influencias.
    )

    st.markdown("---") # Agrega un separador visual en la barra lateral.
    st.header("Parámetros de Búsqueda") # Encabezado para la sección de búsqueda.

    # Variables para almacenar los términos de búsqueda, inicializadas como cadenas vacías.
    search_term_general = "" # Término de búsqueda general.
    search_term_city = "" # Término de búsqueda para ciudades.
    search_term_musicians = "" # Término de búsqueda para músicos.
    search_term_global_conflicts = "" # Término de búsqueda para conflictos globales.
    search_term_unesco = "" # Término de búsqueda para sitios UNESCO.

    # Se muestran diferentes campos de entrada de texto según el tipo de entidad seleccionada,
    # permitiendo búsquedas específicas.
    if entity_type == "Lugares": # Si el tipo de entidad seleccionado es "Lugares".
        search_term_city = st.text_input("Buscar por Ciudad (ej: Quito, Guayaquil)", "") # Campo de texto para buscar por ciudad.
    elif entity_type == "Patrimonio de la Humanidad (UNESCO)": # Si el tipo de entidad es "Patrimonio de la Humanidad (UNESCO)".
        search_term_unesco = st.text_input("Buscar sitio UNESCO por nombre o tema", "") # Campo de texto para buscar sitios UNESCO.
    elif entity_type == "Músicos": # Si el tipo de entidad es "Músicos".
        search_term_musicians = st.text_input("Buscar músico por nombre o tema", "") # Campo de texto para buscar músicos.
    elif entity_type == "Conflictos/Guerras Globales": # Si el tipo de entidad es "Conflictos/Guerras Globales".
        search_term_global_conflicts = st.text_input("Buscar conflicto/guerra por nombre o tema", "") # Campo de texto para buscar conflictos.
    elif entity_type in ["Personalidades"]: # Si el tipo de entidad es "Personalidades" o "Eventos Históricos".
        search_term_general = st.text_input("Buscar por nombre o tema", "") # Campo de texto para búsqueda general.

# --- Contenido Principal de la Aplicación ---
# Listas para almacenar los datos a mostrar y los datos para el mapa.
data_to_display = [] # Lista para almacenar los datos procesados que se mostrarán en tablas o expanders.
map_data = [] # Lista para almacenar datos geográficos para el mapa.

# Bloque condicional que determina qué contenido se mostrará en la aplicación principal
# basándose en la selección del usuario en la barra lateral.

if entity_type == "Inicio": # Si el usuario ha seleccionado la opción "Inicio".
    # Sección de bienvenida y descripción general de la aplicación.
    st.markdown("""
    CulturaViva es una **aplicación web interactiva** de vanguardia, diseñada para conectar a la comunidad con su **patrimonio cultural tangible e intangible** de una manera sin precedentes. Utilizamos el poder de los **Linked Open Data (LOD)** como nuestra fuente principal para mostrar, explorar y enriquecer la riqueza cultural de nuestra región.
    """) # Muestra una descripción general de la aplicación.
    st.header("Acerca de Nosotros..... ") # Encabezado para la sección "Acerca de Nosotros".

    # Uso de columnas para una presentación más estructurada y atractiva.
    col1, col2 = st.columns(2) # Divide la interfaz en dos columnas.

    with col1: # Contenido de la primera columna.
        st.markdown("### Problemática:") # Subencabezado para la problemática.
        st.markdown("""
        La historia y el valor cultural de nuestros espacios a menudo pasan desapercibidos. La información está dispersa, desorganizada y es inaccesible para el público. Esto genera una **desconexión cultural** que afecta la educación, la identidad local y el potencial turístico.
        """) # Descripción de la problemática.

    with col2: # Contenido de la segunda columna.
        st.markdown("### Solución:") # Subencabezado para la solución.
        st.markdown("""
        CulturaViva transforma datos complejos en una **experiencia interactiva y accesible**. Organizamos y presentamos el patrimonio cultural de forma clara, utilizando **DBpedia y Wikidata** para ofrecer:
        -   **Mapas culturales interactivos.**
        -   **Fichas detalladas con imágenes y descripciones.**
        -   **Búsqueda temática y geográfica inteligente.**
        -   **Datos enlazados navegables (LOD).**
        """) # Descripción de la solución.

    st.markdown("---") # Separador visual.

    st.header(" Impacto y Visión") # Encabezado para la sección de impacto.

    st.markdown("""
    CulturaViva va más allá de una simple aplicación, es un motor para:

    -   **Promover la Educación Abierta:** Facilita el acceso al conocimiento cultural para estudiantes y ciudadanos.
    -   **Fortalecer la Identidad Cultural:** Conecta a las generaciones con su pasado y presente, fomentando un sentido de pertenencia.
    -   **Fomentar la Reutilización de Datos Públicos:** Contribuye a un ecosistema digital más robusto y colaborativo.
    -   **Reactivar y Revalorizar el Patrimonio Olvidado:** Pone en valor la riqueza cultural que merece ser reconocida.

    **¡Con CulturaViva, tu patrimonio cobra vida!**
    """) # Descripción del impacto y visión.

    st.markdown("---") # Separador visual.

    st.subheader(" Fuentes de Datos Abiertos Enlazados (LOD)") # Subencabezado para las fuentes de datos.
    st.markdown("""
    "Nuestra plataforma, CulturaViva, es única porque obtiene su información de grandes enciclopedias digitales colaborativas y de acceso público, como DBpedia y Wikidata."

    Piensa en DBpedia como una vasta biblioteca estructurada que nos da datos sobre monumentos, personajes históricos y eventos importantes. Por su parte, Wikidata funciona como un cerebro global que nos provee detalles más precisos, como las coordenadas exactas de un lugar o las fechas de nacimiento, y también cómo se conectan las diferentes piezas de información entre sí.

    La tecnología detrás de CulturaViva es como un sistema inteligente que sabe leer y entender estas enciclopedias. No solo busca datos, sino que comprende las relaciones entre ellos, lo que nos permite ofrecerte una experiencia de exploración cultural mucho más rica y conectada. Es como tener un investigador experto que organiza y te presenta el conocimiento de forma intuitiva, para que descubras nuestro patrimonio de una manera completamente nueva.
    """) # Explicación sobre las fuentes de datos LOD.


elif entity_type == "Lugares": # Si el usuario ha seleccionado la opción "Lugares".
    st.markdown("Explora los lugares históricos más emblemáticos de Ecuador. Ubicados en un mapa interactivo, cada punto revela detalles sobre su historia y significado cultural.") # Descripción de la sección.
    # Llama a la función SPARQL para obtener datos de lugares.
    results = get_monuments_or_places_in_ecuador(city=search_term_city) # Ejecuta la consulta SPARQL para lugares, filtrando por ciudad si se ingresó un término.
    if results and results.get('results', {}).get('bindings'): # Verifica si la consulta devolvió resultados válidos.
        for item in results['results']['bindings']: # Itera sobre cada resultado obtenido.
            try: # Intenta extraer los datos, manejando posibles errores de claves no existentes.
                label = item['label']['value'] # Nombre del lugar.
                abstract = item['abstract']['value'] # Descripción abstracta del lugar.
                lat = float(item['lat']['value']) # Latitud del lugar, convertida a flotante.
                long = float(item['long']['value']) # Longitud del lugar, convertida a flotante.
                map_data.append({'name': label, 'lat': lat, 'lon': long}) # Agrega los datos del lugar a la lista para el mapa.
                thumbnail_url = item.get('thumbnail', {}).get('value', 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg') # URL de la imagen en miniatura, con una imagen por defecto si no hay.
                data_to_display.append({ # Agrega los datos del lugar a la lista para mostrar.
                    "Tipo": "Lugar", # Tipo de entidad.
                    "Nombre": label, # Nombre del lugar.
                    "Descripción": abstract, # Descripción del lugar.
                    "URL": item['place']['value'], # URL del recurso en la base de datos.
                    "Latitud": lat, # Latitud.
                    "Longitud": long, # Longitud.
                    "Imagen": thumbnail_url # URL de la imagen.
                })
            except KeyError: # Si ocurre un KeyError (clave no encontrada en el resultado).
                continue # Continúa con el siguiente elemento.
    else: # Si no se encontraron resultados.
        st.info("No se encontraron lugares con los criterios seleccionados.") # Muestra un mensaje informativo.

elif entity_type == "Personalidades": # Si el usuario ha seleccionado la opción "Personalidades".
    st.markdown("Descubre a las figuras más influyentes e importantes de la historia y cultura ecuatoriana. Conoce sus vidas, sus contribuciones y el impacto que tuvieron en nuestro país") # Descripción de la sección.
    # Llama a la función SPARQL para obtener datos de personalidades.
    results = get_ecuadorian_personalities(search_term=search_term_general) # Ejecuta la consulta SPARQL para personalidades, con un término de búsqueda general.
    if results and results.get('results', {}).get('bindings'): # Verifica si la consulta devolvió resultados.
        for item in results['results']['bindings']: # Itera sobre cada resultado.
            try: # Intenta extraer los datos.
                label = item['personLabel']['value'] # Nombre de la personalidad.
                description = item.get('description', {}).get('value', 'No hay descripción disponible.') # Descripción.
                date_of_birth_raw = item.get('dateOfBirth', {}).get('value', 'Desconocido') # Fecha de nacimiento (sin formatear).
                place_of_birth = item.get('placeOfBirthLabel', {}).get('value', 'Desconocido') # Lugar de nacimiento.
                image_url = item.get('image', {}).get('value', None) # URL de la imagen.

                # Formatear la fecha de nacimiento para una mejor presentación.
                formatted_date_of_birth = 'Desconocido' # Inicializa la fecha formateada.
                if date_of_birth_raw != 'Desconocido': # Si la fecha de nacimiento no es 'Desconocido'.
                    try: # Intenta formatear la fecha.
                        dt_object = datetime.datetime.fromisoformat(date_of_birth_raw.replace('Z', '+00:00')) # Convierte la fecha ISO a objeto datetime.
                        formatted_date_of_birth = dt_object.strftime('%d de %B de %Y') # Formatea la fecha a "día de Mes de Año".
                    except ValueError: # Si ocurre un error de valor (fecha no válida).
                        formatted_date_of_birth = date_of_birth_raw # Mantiene el formato original.

                data_to_display.append({ # Agrega los datos de la personalidad a la lista para mostrar.
                    "Tipo": "Personalidad", # Tipo de entidad.
                    "Nombre": label, # Nombre.
                    "Descripción": description, # Descripción.
                    "Fecha de Nacimiento": formatted_date_of_birth, # Fecha de nacimiento formateada.
                    "Lugar de Nacimiento": place_of_birth, # Lugar de nacimiento.
                    "URL": item['person']['value'], # URL del recurso.
                    "Imagen": image_url # URL de la imagen.
                })
            except KeyError: # Si ocurre un KeyError.
                continue # Continúa con el siguiente elemento.
    else: # Si no se encontraron resultados.
        st.info("No se encontraron personalidades con los criterios seleccionados.") # Muestra un mensaje.

elif entity_type == "Músicos": # Si el usuario ha seleccionado la opción "Músicos".
    st.markdown("Conoce a los artistas y compositores ecuatorianos que han dejado una huella imborrable en el panorama musical del país. Explora sus biografías y el legado de su arte.") # Descripción de la sección.
    # Llama a la función SPARQL para obtener datos de músicos ecuatorianos.
    results = get_ecuadorian_musicians(search_term=search_term_musicians) # Ejecuta la consulta SPARQL para músicos.
    if results and results.get('results', {}).get('bindings'): # Verifica si la consulta devolvió resultados.
        for item in results['results']['bindings']: # Itera sobre cada resultado.
            try: # Intenta extraer los datos.
                label = item['musicianLabel']['value'] # Nombre del músico.
                description = item.get('description', {}).get('value', 'No hay descripción disponible.') # Descripción.
                date_of_birth_raw = item.get('dateOfBirth', {}).get('value', 'Desconocido') # Fecha de nacimiento (sin formatear).
                place_of_birth = item.get('placeOfBirthLabel', {}).get('value', 'Desconocido') # Lugar de nacimiento.
                image_url = item.get('image', {}).get('value', None) # URL de la imagen.

                formatted_date_of_birth = 'Desconocido' # Inicializa la fecha formateada.
                if date_of_birth_raw != 'Desconocido': # Si la fecha de nacimiento no es 'Desconocido'.
                    try: # Intenta formatear la fecha.
                        dt_object = datetime.datetime.fromisoformat(date_of_birth_raw.replace('Z', '+00:00')) # Convierte la fecha.
                        formatted_date_of_birth = dt_object.strftime('%d de %B de %Y') # Formatea la fecha.
                    except ValueError: # Si ocurre un error de valor.
                        formatted_date_of_birth = date_of_birth_raw # Mantiene el formato original.
                
                data_to_display.append({ # Agrega los datos del músico a la lista para mostrar.
                    "Tipo": "Músico", # Tipo de entidad.
                    "Nombre": label, # Nombre.
                    "Descripción": description, # Descripción.
                    "Fecha de Nacimiento": formatted_date_of_birth, # Fecha de nacimiento formateada.
                    "Lugar de Nacimiento": place_of_birth, # Lugar de nacimiento.
                    "URL": item['musician']['value'], # URL del recurso.
                    "Imagen": image_url # URL de la imagen.
                })
            except KeyError: # Si ocurre un KeyError.
                continue # Continúa con el siguiente elemento.
    else: # Si no se encontraron resultados.
        st.info("No se encontraron músicos con los criterios seleccionados.") # Muestra un mensaje.

elif entity_type == "Conflictos/Guerras Globales": # Si el usuario ha seleccionado la opción "Conflictos/Guerras Globales".
    st.markdown("Explora las guerras y conflictos más significativos a nivel mundial en una detallada línea de tiempo. Descubre información sobre su duración, los participantes y su contexto histórico global.") # Descripción de la sección.
    # Llama a la función SPARQL para obtener datos de conflictos y guerras globales.
    results = get_global_wars_and_conflicts(search_term=search_term_global_conflicts) # Ejecuta la consulta SPARQL para conflictos.
    
    # Inicializa df_conflicts aquí, antes de usarla
    df_conflicts = pd.DataFrame() # Inicializa un DataFrame vacío para los conflictos. Esto es crucial para evitar 'NameError'.

    if results and results.get('results', {}).get('bindings'): # Verifica si la consulta devolvió resultados.
        for item in results['results']['bindings']: # Itera sobre cada resultado.
            try: # Intenta extraer los datos.
                label = item['eventLabel']['value'] # Nombre del evento.
                description = item.get('description', {}).get('value', 'No hay descripción disponible.') # Descripción.
                start_time_raw = item.get('startTime', {}).get('value', 'Desconocido') # Fecha de inicio (sin formatear).
                end_time_raw = item.get('endTime', {}).get('value', start_time_raw) # Fecha de fin (sin formatear), usa la de inicio si no hay fin.
                location = item.get('locationLabel', {}).get('value', 'Desconocido') # Ubicación.
                image_url = item.get('image', {}).get('value', None) # URL de la imagen.

                start_date = 'Desconocido' # Inicializa la fecha de inicio formateada.
                end_date = 'Desconocido' # Inicializa la fecha de fin formateada.

                if start_time_raw != 'Desconocido': # Si la fecha de inicio no es 'Desconocido'.
                    try: # Intenta formatear la fecha de inicio.
                        if 'T' in start_time_raw: # Si la fecha incluye tiempo (formato ISO completo).
                            start_date = datetime.datetime.fromisoformat(start_time_raw.replace('Z', '+00:00')).isoformat() # Convierte y formatea.
                        elif len(start_time_raw) == 10 and start_time_raw.count('-') == 2: # Si es formato YYYY-MM-DD.
                            start_date = datetime.datetime.strptime(start_time_raw, '%Y-%m-%d').isoformat() # Convierte y formatea.
                        elif len(start_time_raw) == 4 and start_time_raw.isdigit(): # Si es solo el año.
                            start_date = f"{start_time_raw}-01-01T00:00:00" # Asume 1 de enero de ese año.
                        else: # Si el formato no es reconocido.
                            start_date = None # No se puede determinar la fecha de inicio.
                    except ValueError: # Si ocurre un error de valor al convertir la fecha.
                        start_date = None # No se puede determinar la fecha de inicio.
                
                if end_time_raw != 'Desconocido' and start_date: # Si la fecha de fin no es 'Desconocido' y hay una fecha de inicio válida.
                    try: # Intenta formatear la fecha de fin.
                        if 'T' in end_time_raw: # Si la fecha incluye tiempo.
                            end_date = datetime.datetime.fromisoformat(end_time_raw.replace('Z', ' +00:00')).isoformat() # Convierte y formatea.
                        elif len(end_time_raw) == 10 and end_time_raw.count('-') == 2: # Si es formato YYYY-MM-DD.
                            end_date = datetime.datetime.strptime(end_time_raw, '%Y-%m-%d').isoformat() # Convierte y formatea.
                        elif len(end_time_raw) == 4 and end_time_raw.isdigit(): # Si es solo el año.
                            end_date = f"{end_time_raw}-12-31T23:59:59" # Asume 31 de diciembre de ese año.
                        else: # Si el formato no es reconocido.
                            end_date = start_date # Usa la fecha de inicio como fin.
                    except ValueError: # Si ocurre un error de valor.
                        end_date = start_date # Usa la fecha de inicio como fin.
                else: # Si no hay fecha de fin o la fecha de inicio no es válida.
                    end_date = start_date # Usa la fecha de inicio como fin.

                if start_date: # Si se pudo determinar una fecha de inicio.
                    df_conflicts = pd.concat([df_conflicts, pd.DataFrame([{ # Concatena el nuevo conflicto al DataFrame principal.
                        "Tipo": "Conflicto/Guerra", # Tipo de evento.
                        "Nombre": label, # Nombre.
                        "Descripción": description, # Descripción.
                        "Fecha de Inicio": start_time_raw, # Fecha de inicio original.
                        "Fecha de Fin": end_time_raw, # Fecha de fin original.
                        "start": start_date, # Fecha de inicio formateada para Plotly.
                        "end": end_date, # Fecha de fin formateada para Plotly.
                        "Lugar": location, # Lugar.
                        "URL": item['event']['value'], # URL del recurso.
                        "Imagen": image_url # URL de la imagen.
                    }])], ignore_index=True) # Ignora el índice para una concatenación limpia.
            except KeyError: # Si ocurre un KeyError.
                continue # Continúa con el siguiente elemento.
        
        if not df_conflicts.empty: # Si el DataFrame de conflictos no está vacío (se encontraron datos).
            df_conflicts['start'] = pd.to_datetime(df_conflicts['start'], errors='coerce') # Convierte la columna 'start' a datetime, forzando errores a NaT.
            df_conflicts['end'] = pd.to_datetime(df_conflicts['end'], errors='coerce') # Convierte la columna 'end' a datetime.
            df_conflicts = df_conflicts.sort_values(by='start').dropna(subset=['start']) # Ordena por fecha de inicio y elimina filas sin fecha de inicio válida.

            # Crea una línea de tiempo interactiva para conflictos y guerras.
            fig = px.timeline(df_conflicts, x_start="start", x_end="end", y="Nombre", # Crea un gráfico de línea de tiempo con Plotly Express.
                              color="Tipo", # Colorea las barras por tipo.
                              title="Línea de Tiempo de Conflictos y Guerras Globales", # Título del gráfico.
                              hover_data=["Descripción", "Lugar", "Fecha de Inicio", "Fecha de Fin"]) # Datos a mostrar al pasar el ratón.
            fig.update_yaxes(autorange="reversed") # Invierte el orden del eje Y para una mejor visualización de la línea de tiempo.
            st.plotly_chart(fig, use_container_width=True) # Muestra el gráfico de Plotly en Streamlit, ajustándose al ancho del contenedor.

            data_to_display = df_conflicts.to_dict('records') # Convierte el DataFrame de conflictos a una lista de diccionarios para mostrar en otros lugares.
        else: # Si df_conflicts está vacío.
            st.info("No se encontraron conflictos o guerras globales con los criterios seleccionados.") # Muestra un mensaje.
    else: # Si la consulta SPARQL no devolvió resultados iniciales.
        st.info("No se encontraron conflictos o guerras globales con los criterios seleccionados.") # Muestra un mensaje.

elif entity_type == "Patrimonio de la Humanidad (UNESCO)": # Si el usuario ha seleccionado la opción "Patrimonio de la Humanidad (UNESCO)".
    st.markdown("Descubre los sitios declarados Patrimonio de la Humanidad por la UNESCO, tanto en Ecuador como alrededor del mundo. Conoce estos tesoros culturales y naturales con imágenes y descripciones") # Descripción de la sección.
    # Llama a la función SPARQL para obtener datos de sitios UNESCO.
    results = get_unesco_world_heritage_sites(search_term=search_term_unesco) # Ejecuta la consulta SPARQL para sitios UNESCO.
    if results and results.get('results', {}).get('bindings'): # Verifica si la consulta devolvió resultados.
        for item in results['results']['bindings']: # Itera sobre cada resultado.
            try: # Intenta extraer los datos.
                label = item['siteLabel']['value'] # Nombre del sitio.
                description = item.get('description', {}).get('value', 'No hay descripción disponible.') # Descripción.
                image_url = item.get('image', {}).get('value', 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg') # URL de la imagen.
                coords_raw = item.get('coords', {}).get('value', None) # Coordenadas geográficas (en formato crudo).
                
                lat, long = None, None # Inicializa latitud y longitud.
                if coords_raw: # Si hay coordenadas.
                    try: # Intenta parsear las coordenadas.
                        coords_raw = coords_raw.replace('Point(', '').replace(')', '') # Limpia la cadena de coordenadas.
                        long, lat = map(float, coords_raw.split(' ')) # Divide y convierte a flotantes.
                        map_data.append({'name': label, 'lat': lat, 'lon': long}) # Agrega a los datos del mapa.
                    except ValueError: # Si hay un error al parsear.
                        pass # Ignora y continúa.

                data_to_display.append({ # Agrega los datos del sitio UNESCO a la lista para mostrar.
                    "Tipo": "Patrimonio UNESCO", # Tipo de entidad.
                    "Nombre": label, # Nombre.
                    "Descripción": description, # Descripción.
                    "URL": item['site']['value'], # URL del recurso.
                    "Imagen": image_url, # URL de la imagen.
                    "Latitud": lat, # Latitud.
                    "Longitud": long # Longitud.
                })
            except KeyError: # Si ocurre un KeyError.
                continue # Continúa con el siguiente elemento.
        
        if data_to_display: # Si hay datos para mostrar.
            st.write("Explora los sitios del Patrimonio de la Humanidad encontrados:") # Mensaje informativo.
            cols_per_row = 4 # Número de columnas por fila para la visualización en cuadrícula.
            cols = st.columns(cols_per_row) # Crea las columnas.
            
            for i, item in enumerate(data_to_display): # Itera sobre cada elemento a mostrar.
                with cols[i % cols_per_row]: # Coloca el elemento en la columna correcta (cicla a través de las columnas).
                    # Muestra imágenes en un formato de cuadrícula con use_container_width.
                    st.image(item['Imagen'], caption=item['Nombre'], use_container_width=True) # Muestra la imagen con su nombre como pie de foto, ajustándose al ancho.
                    st.markdown(f"**{item['Nombre']}**") # Muestra el nombre en negrita.
                    st.markdown(f"_{item['Descripción'][:70]}..._") # Muestra una parte de la descripción en cursiva.
                    st.markdown(f"[Ver en Wikidata]({item['URL']})") # Enlace a Wikidata.
        else: # Si no hay datos para mostrar.
            st.info("No se encontraron sitios del Patrimonio de la Humanidad con los criterios seleccionados.") # Muestra un mensaje.
    else: # Si la consulta SPARQL no devolvió resultados iniciales.
        st.info("No se encontraron sitios del Patrimonio de la Humanidad con los criterios seleccionados.") # Muestra un mensaje.


elif entity_type == "Gráfico de Influencias": # Si el usuario ha seleccionado la opción "Gráfico de Influencias".
    st.markdown("Analiza cómo diferentes personalidades ecuatorianas se han influenciado mutuamente a lo largo de la historia. Este gráfico de red te revela conexiones y legados inesperados.") # Descripción de la sección.
    st.info("Explora cómo diferentes personalidades se han influenciado mutuamente.") # Mensaje informativo.
    
    # Llama a la función SPARQL para obtener relaciones de influencia.
    results = get_influencer_relationships(limit=50) # Ejecuta la consulta SPARQL para relaciones de influencia, limitando los resultados a 50.
    if results and results.get('results', {}).get('bindings'): # Verifica si la consulta devolvió resultados.
        nodes = set() # Conjunto para almacenar nombres únicos de personalidades (nodos del gráfico).
        edges = [] # Lista para almacenar las relaciones de influencia (aristas del gráfico).
        data_to_display = [] # Lista para los datos detallados.
        for item in results['results']['bindings']: # Itera sobre cada relación de influencia.
            influencer_label = item['influencerLabel']['value'] # Nombre del influyente.
            influenced_label = item['influencedLabel']['value'] # Nombre del influenciado.
            
            nodes.add(influencer_label) # Agrega el influyente al conjunto de nodos.
            nodes.add(influenced_label) # Agrega el influenciado al conjunto de nodos.
            edges.append((influencer_label, influenced_label)) # Agrega la relación (tupla) a la lista de aristas.

            data_to_display.append({ # Agrega los datos del influyente a la lista para mostrar.
                "Tipo": "Influencer", # Tipo.
                "Nombre": influencer_label, # Nombre.
                "Descripción": f"Influenció a {influenced_label}.", # Descripción.
                "URL": item['influencer']['value'] # URL del influyente.
            })
            data_to_display.append({ # Agrega los datos del influenciado a la lista para mostrar.
                "Tipo": "Influenciado", # Tipo.
                "Nombre": influenced_label, # Nombre.
                "Descripción": f"Fue influenciado por {influencer_label}.", # Descripción.
                "URL": item['influenced']['value'] # URL del influenciado.
            })

        df_nodes = pd.DataFrame(list(nodes), columns=['name']) # Crea un DataFrame de Pandas con los nombres de los nodos.
        
        # Crea un gráfico interactivo de relaciones.
        fig = go.Figure() # Crea una nueva figura de Plotly.

        fig.add_trace(go.Scatter( # Agrega un rastro de dispersión para los nodos (personalidades).
            x=[0]*len(df_nodes), # Posiciona todos los nodos en x=0 (para un diseño lineal si no se usa un layout de red).
            y=list(range(len(df_nodes))), # Distribuye los nodos uniformemente en el eje Y.
            mode='markers+text', # Muestra marcadores y texto.
            marker=dict(symbol='circle', size=15, color='skyblue'), # Estilo del marcador.
            text=df_nodes['name'], # Texto a mostrar para cada marcador (nombre de la personalidad).
            textposition="bottom center", # Posición del texto.
            hoverinfo='text', # Muestra texto al pasar el ratón.
            hovertext=df_nodes['name'], # Texto al pasar el ratón.
            name='Nodos' # Nombre del rastro.
        ))

        for edge in edges: # Itera sobre cada relación (arista) para dibujar las flechas de influencia.
            # Obtiene los índices de los nodos de origen y destino en el DataFrame de nodos.
            x0, y0 = df_nodes[df_nodes['name'] == edge[0]].index[0], df_nodes[df_nodes['name'] == edge[0]].index[0]
            x1, y1 = df_nodes[df_nodes['name'] == edge[1]].index[0], df_nodes[df_nodes['name'] == edge[1]].index[0]
            
            offset = 0.05 # Pequeño desplazamiento para las flechas.
            if x0 == x1: # Si los nodos están en la misma posición X.
                y1 = y1 - (offset if y1 > y0 else -offset) # Ajusta la posición Y para evitar superposición.
            else: # Si están en diferente posición X.
                x1 = x1 - (offset if x1 > x0 else -offset) # Ajusta la posición X.
            
            fig.add_annotation( # Agrega una anotación (flecha) para representar la influencia.
                ax=x0, ay=y0, axref='x', ayref='y', # Coordenadas del punto de inicio de la flecha.
                x=x1, y=y1, xref='x', yref='y', # Coordenadas del punto final de la flecha.
                showarrow=True, # Muestra la flecha.
                arrowhead=2, # Tipo de cabeza de flecha.
                arrowsize=1, # Tamaño de la cabeza de flecha.
                arrowwidth=1, # Ancho de la línea de la flecha.
                arrowcolor='gray' # Color de la flecha.
            )

        fig.update_layout( # Actualiza el diseño del gráfico.
            title="Relaciones de Influencia en Ecuador", # Título del gráfico.
            showlegend=False, # No muestra la leyenda.
            hovermode='closest', # Modo de interacción al pasar el ratón.
            margin=dict(b=20, l=5, r=5, t=40), # Márgenes del gráfico.
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), # Oculta la cuadrícula, línea cero y etiquetas del eje X.
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), # Oculta la cuadrícula, línea cero y etiquetas del eje Y.
            height=600 # Altura del gráfico.
        )
        
        st.plotly_chart(fig, use_container_width=True) # Muestra el gráfico de Plotly en Streamlit, ajustándose al ancho del contenedor.

    else: # Si no se encontraron relaciones de influencia.
        st.info("No se encontraron relaciones de influencia para mostrar.") # Muestra un mensaje.

    
# --- Sección de Resultados Detallados (Tabla y Expander por elemento) ---
# Esta sección muestra una tabla y expanders individuales para los elementos de datos,
# excluyendo aquellos tipos de entidad que ya tienen visualizaciones específicas (mapas, gráficos, etc.).
if data_to_display and entity_type not in ["Inicio", "Conflictos/Guerras Globales","Patrimonio de la Humanidad (UNESCO)", "Gráfico de Influencias","Lugares"]: # Si hay datos para mostrar y el tipo de entidad no está en la lista de exclusión.
    st.subheader(" Resultados Detallados") # Subencabezado.
    df = pd.DataFrame(data_to_display) # Crea un DataFrame de Pandas a partir de la lista de datos.
    cols_to_drop = ["URL", "Imagen", "start", "end"] # Columnas a eliminar del DataFrame para la visualización de tabla.
    df_display = df.drop(columns=[col for col in cols_to_drop if col in df.columns], errors='ignore') # Elimina las columnas si existen.
    st.dataframe(df_display) # Muestra el DataFrame en Streamlit.

    for item in data_to_display: # Itera sobre cada elemento en los datos a mostrar.
        with st.expander(f"**{item['Nombre']}** ({item['Tipo']})"): # Crea un "expander" (sección colapsable) para cada elemento.
            col1, col2 = st.columns([1, 2]) # Divide el contenido del expander en dos columnas.
            with col1: # Contenido de la primera columna.
                if item.get('Imagen'): # Si el elemento tiene una URL de imagen.
                    st.image(item['Imagen'], caption=item['Nombre'], width=200) # Muestra la imagen.
                else: # Si no hay imagen.
                    st.write("No hay imagen disponible.") # Muestra un mensaje.
            with col2: # Contenido de la segunda columna.
                st.write(f"**Tipo:** {item['Tipo']}") # Muestra el tipo de entidad.
                if 'Descripción' in item and item['Descripción'] and item['Descripción'] != 'No hay descripción detallada disponible directamente para esta obra.': 
                    st.write(f"**Descripción:** {item['Descripción']}") # Muestra la descripción si existe y no es la predeterminada.
                else:
                    st.write("No hay descripción disponible.") # Muestra un mensaje si no hay descripción.

                if item['Tipo'] == "Personalidad" or item['Tipo'] == "Músico": # Si es una personalidad o un músico.
                    st.write(f"**Fecha de Nacimiento:** {item['Fecha de Nacimiento']}") # Muestra la fecha de nacimiento.
                    st.write(f"**Lugar de Nacimiento:** {item['Lugar de Nacimiento']}") # Muestra el lugar de nacimiento.
                    st.markdown(f"[Más información en Wikidata]({item['URL']})") # Enlace a Wikidata.
                elif item['Tipo'] == "Lugar": # Si es un lugar.
                    st.write(f"**Latitud:** {item['Latitud']} | **Longitud:** {item['Longitud']}") # Muestra latitud y longitud.
                    st.markdown(f"[Más información en DBpedia]({item['URL']})") # Enlace a DBpedia.
                elif item['Tipo'] in ["Influencer", "Influenciado"]: # Si es un influencer o influenciado.
                    st.markdown(f"[Más información]({item['URL']})") # Enlace de información adicional.
else: # Si no hay datos para mostrar o el tipo de entidad está excluido.
    if entity_type != "Inicio" and not map_data and entity_type not in ["Conflictos/Guerras Globales", "Gráfico de Influencias"]: # Si no es la página de inicio, no hay datos de mapa y no es un tipo con visualización especial.
        st.info("Utiliza los filtros en la barra lateral para explorar el patrimonio cultural.") # Muestra un mensaje para usar los filtros.

# --- Mapa Interactivo para Lugares y Patrimonio UNESCO ---
# Muestra un mapa de Folium si hay datos geográficos disponibles para los tipos de entidad relevantes.
if (entity_type == "Lugares") and map_data: # Si el tipo de entidad es "Lugares" o "Patrimonio UNESCO" (aunque en el código actual solo se usa "Lugares") y hay datos de mapa.
    st.subheader("🗺️ Ubicación en el Mapa") # Subencabezado para el mapa.
    
    if map_data: # Si hay datos geográficos.
        avg_lat = sum(d['lat'] for d in map_data) / len(map_data) # Calcula la latitud promedio de los puntos.
        avg_lon = sum(d['lon'] for d in map_data) / len(map_data) # Calcula la longitud promedio de los puntos.
    else: # Si no hay datos geográficos.
        # Coordenadas predeterminadas de Ecuador si no hay datos geográficos.
        avg_lat, avg_lon = -1.8312, -78.1834 # Coordenadas centrales de Ecuador como valor por defecto.

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=7) # Crea un objeto de mapa de Folium centrado en las coordenadas promedio y con un nivel de zoom inicial.

    for item in data_to_display: # Itera sobre los datos para añadir marcadores al mapa.
        if item.get('Latitud') is not None and item.get('Longitud') is not None: # Si el elemento tiene latitud y longitud.
            folium.Marker( # Crea un marcador en el mapa.
                [item['Latitud'], item['Longitud']], # Posición del marcador.
                popup=f"<b>{item['Nombre']}</b><br>{item['Descripción'][:150]}...<br><a href='{item['URL']}' target='_blank'>Ver más</a>", # Contenido del popup al hacer clic en el marcador.
                tooltip=item['Nombre'] # Texto que aparece al pasar el ratón por encima del marcador.
            ).add_to(m) # Añade el marcador al mapa.
    
    st_folium(m) # Muestra el mapa de Folium en la aplicación Streamlit.

# --- Módulo "Sabías que..." ---
# Muestra un dato curioso aleatorio basado en los datos cargados.
if data_to_display: # Si hay datos cargados en la aplicación.
    st.markdown("---") # Agrega un separador visual.
    st.subheader("🧠 Sabías que...") # Subencabezado para la sección "Sabías que...".
    random_item = random.choice(data_to_display) # Selecciona un elemento aleatorio de los datos cargados.
    
    fact = "" # Inicializa la variable para el dato curioso.
    if random_item['Tipo'] == "Lugar": # Si el elemento es un "Lugar".
        fact = f"¿Sabías que **{random_item['Nombre']}** es un lugar en Ecuador conocido por: \"{random_item['Descripción'][:100]}...\"? [Más info]({random_item['URL']})" # Formato del dato curioso para lugares.
    elif random_item['Tipo'] == "Personalidad": # Si el elemento es una "Personalidad".
        fact = f"¿Sabías que **{random_item['Nombre']}**, nacido el {random_item['Fecha de Nacimiento']} en {random_item['Lugar de Nacimiento']}, es una personalidad ecuatoriana destacada? [Más info]({random_item['URL']})" # Formato del dato curioso para personalidades.
    elif random_item['Tipo'] == "Músico": # Si el elemento es un "Músico".
        fact = f"¿Sabías que **{random_item['Nombre']}**, un músico ecuatoriano, nació el {random_item['Fecha de Nacimiento']} en {random_item['Lugar de Nacimiento']}? [Más info]({random_item['URL']})" # Formato del dato curioso para músicos.
    elif random_item['Tipo'] == "Conflicto/Guerra": # Si el elemento es un "Conflicto/Guerra".
        # Check if 'Fecha de Inicio' and 'Fecha de Fin' keys exist for random_item
        inicio_val = random_item.get('Fecha de Inicio', 'Desconocido') # Obtiene la fecha de inicio, o 'Desconocido'.
        fin_val = random_item.get('Fecha de Fin', 'Desconocido') # Obtiene la fecha de fin, o 'Desconocido'.
        lugar_val = random_item.get('Lugar', 'Desconocido') # Obtiene el lugar, o 'Desconocido'.
        description_val = random_item.get('Descripción', '') # Obtiene la descripción.
        fact = f"¿Sabías que el conflicto/guerra **{random_item['Nombre']}** inició el {inicio_val} y finalizó el {fin_val} en {lugar_val}? \"{description_val[:100]}...\". [Más info]({random_item['URL']})" # Formato del dato curioso para conflictos.
    elif random_item['Tipo'] == "Patrimonio UNESCO": # Si el elemento es "Patrimonio UNESCO".
        description_val = random_item.get('Descripción', '') # Obtiene la descripción.
        fact = f"¿Sabías que **{random_item['Nombre']}** es un sitio declarado Patrimonio de la Humanidad por la UNESCO? \"{description_item['Descripción'][:100]}...\". [Más info]({random_item['URL']})" # Formato del dato curioso para sitios UNESCO.
    elif random_item['Tipo'] in ["Influencer", "Influenciado"]: # Si el elemento es "Influencer" o "Influenciado".
        fact = f"¿Sabías que **{random_item['Nombre']}** está conectado a otras personalidades por relaciones de influencia? [Más info]({random_item['URL']})" # Formato del dato curioso para relaciones de influencia.
    
    st.info(fact) # Muestra el dato curioso en un cuadro de información.