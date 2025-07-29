import requests # Módulo para realizar solicitudes HTTP (para las APIs SPARQL).
import streamlit as st # Necesario para usar st.cache_data y st.error.

# --- Configuración de Endpoints SPARQL ---
DBPEDIA_ENDPOINT = "http://dbpedia.org/sparql"
WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"

# --- Función Auxiliar para Ejecutar Consultas ---
@st.cache_data(ttl=3600) # Cachea los resultados por 1 hora
def run_sparql_query(endpoint, query):
    """Ejecuta una consulta SPARQL y devuelve los resultados en formato JSON."""
    headers = {'Accept': 'application/sparql-results+json'} # Indica que se espera una respuesta JSON.
    params = {'query': query} # El diccionario de parámetros incluye la consulta SPARQL.
    try:
        # Realiza una solicitud GET al endpoint con la consulta y las cabeceras.
        response = requests.get(endpoint, params=params, headers=headers, timeout=30)
        response.raise_for_status() # Verifica si la solicitud fue exitosa (código 200). Si no, lanza una excepción.
        return response.json() # Retorna la respuesta en formato JSON.
    except requests.exceptions.RequestException as e:
        # Captura cualquier error relacionado con la solicitud (ej. problemas de red, timeouts, errores HTTP).
        st.error(f"Error al conectar con el endpoint SPARQL {endpoint}: {e}") # Muestra un mensaje de error en la interfaz de Streamlit.
        return None # Retorna None para indicar que la consulta falló.

# --- Funciones de Consulta Específicas ---

def get_monuments_or_places_in_ecuador(city=None, limit=10):
    """
    Obtiene  lugares de interés en Ecuador, opcionalmente filtrando por ciudad, desde DBpedia.
    Incluye la URL de la miniatura (thumbnail).
    """
    city_filter = f"dbo:city dbr:{city} ;" if city else ""
    query = f"""
    SELECT DISTINCT ?place ?label ?lat ?long ?abstract ?thumbnail WHERE {{
      ?place rdf:type dbo:Place ;
             rdfs:label ?label ;
             geo:lat ?lat ;
             geo:long ?long ;
             dbo:country dbr:Ecuador ;
             {city_filter}
             dbo:abstract ?abstract .
      OPTIONAL {{ ?place dbo:thumbnail ?thumbnail . }} # Añade la propiedad de la imagen
      FILTER (lang(?label) = "es")
      FILTER (lang(?abstract) = "es")
    }} LIMIT {limit}
    """
    return run_sparql_query(DBPEDIA_ENDPOINT, query)

def get_ecuadorian_personalities(search_term=None, limit=10):
    """
    Obtiene personalidades ecuatorianas destacadas desde Wikidata.
    Incluye la URL de la imagen.
    """
    search_filter = f'FILTER (CONTAINS(LCASE(?personLabel), LCASE("{search_term}")) || CONTAINS(LCASE(?description), LCASE("{search_term}")))' if search_term else ""

    query = f"""
    SELECT DISTINCT ?person ?personLabel ?description ?dateOfBirth ?placeOfBirthLabel ?image WHERE {{
    ?person wdt:P31 wd:Q5 ; # Instance of human
            wdt:P27 wd:Q736 . # Nationality: Ecuador
    OPTIONAL {{ ?person wdt:P569 ?dateOfBirth . }} # Date of birth
    OPTIONAL {{ ?person wdt:P19 ?placeOfBirth . }} # Place of birth
    OPTIONAL {{ ?person wdt:P18 ?image . }} # Añade la propiedad de la imagen (P18)
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es". }}
    OPTIONAL {{ ?person schema:description ?description. FILTER (lang(?description) = "es"). }}
    {search_filter}
    }} LIMIT {limit}
    """
    return run_sparql_query(WIKIDATA_ENDPOINT, query)

# FUNCIÓN MODIFICADA: Eventos Históricos en Ecuador con tipos ampliados
def get_historical_events_in_ecuador(search_term=None, limit=100): # Límite cambiado a 100
    """
    Obtiene eventos históricos en Ecuador desde Wikidata, incluyendo diversos tipos de eventos.
    Incluye la URL de la imagen.
    """
    search_filter = f'FILTER (CONTAINS(LCASE(?eventLabel), LCASE("{search_term}")) || CONTAINS(LCASE(?description), LCASE("{search_term}")))' if search_term else ""

    query = f"""
    SELECT DISTINCT ?event ?eventLabel ?description ?pointInTime ?locationLabel ?image WHERE {{
      ?event wdt:P31 ?instanceOf ;
             wdt:P17 wd:Q736 . # Q736 = Ecuador

      FILTER(?instanceOf IN (
        wd:Q1190554,  # evento histórico
        wd:Q1656682,  # evento
        wd:Q180684,    # conflicto
        wd:Q186362,    # protesta
        wd:Q40231,     # elección
        wd:Q132241     # desastre natural
      ))

      OPTIONAL {{ ?event wdt:P585 ?pointInTime . }}   # Fecha
      OPTIONAL {{ ?event wdt:P276 ?location . }}     # Lugar
      OPTIONAL {{ ?event wdt:P18 ?image . }}         # Imagen

      SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es".
      }}

      OPTIONAL {{
        ?event schema:description ?description.
        FILTER (lang(?description) = "es")
      }}
      {search_filter} # Aplicar el filtro de búsqueda
    }}
    ORDER BY DESC(?pointInTime)
    LIMIT {limit}
    """
    return run_sparql_query(WIKIDATA_ENDPOINT, query)
# Función para obtener guerras y conflictos globales
def get_global_wars_and_conflicts(search_term=None, limit=50):
    """
    Obtiene conflictos y guerras globales desde Wikidata.
    Asegura que los eventos tengan una fecha de inicio para la línea de tiempo.
    """
    search_filter = f'FILTER (CONTAINS(LCASE(?eventLabel), LCASE("{search_term}")) || CONTAINS(LCASE(?description), LCASE("{search_term}")))' if search_term else ""

    query = f"""
    SELECT DISTINCT ?event ?eventLabel ?description ?startTime ?endTime ?locationLabel ?image WHERE {{
    ?event wdt:P31 wd:Q198 . # Instance of: war (Q198)
    ?event wdt:P580 ?startTime . # Mandatory start time for timeline
    OPTIONAL {{ ?event wdt:P582 ?endTime . }} # Optional end time
    OPTIONAL {{ ?event wdt:P276 ?location . }} # Location (lugar donde ocurrió)
    OPTIONAL {{ ?event wdt:P18 ?image . }} # Image (P18)
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es". }}
    OPTIONAL {{ ?event schema:description ?description. FILTER (lang(?description) = "es"). }}
    {search_filter}
    }} ORDER BY DESC(?startTime) LIMIT {limit}
    """
    return run_sparql_query(WIKIDATA_ENDPOINT, query)

# NUEVA FUNCIÓN: Obtener Sitios del Patrimonio de la Humanidad (UNESCO)
def get_unesco_world_heritage_sites(search_term=None, limit=50):
    """
    Obtiene sitios del Patrimonio de la Humanidad de la UNESCO desde Wikidata.
    """
    search_filter = f'FILTER (CONTAINS(LCASE(?siteLabel), LCASE("{search_term}")) || CONTAINS(LCASE(?description), LCASE("{search_term}")))' if search_term else ""

    query = f"""
    SELECT DISTINCT ?site ?siteLabel ?description ?image ?coords WHERE {{
      ?site wdt:P31 wd:Q9259 . # Instance of: World Heritage Site (Q9259)
      OPTIONAL {{ ?site wdt:P18 ?image . }} # Image
      OPTIONAL {{ ?site wdt:P625 ?coords . }} # Coordinates
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es". }}
      OPTIONAL {{ ?site schema:description ?description. FILTER (lang(?description) = "es"). }}
      {search_filter}
    }} LIMIT {limit}
    """
    return run_sparql_query(WIKIDATA_ENDPOINT, query)

def get_influencer_relationships(limit=10):
    """
    Obtiene relaciones de influencia donde el influencer es de Ecuador, desde DBpedia.
    """
    query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbr: <http://dbpedia.org/resource/>

    SELECT ?influencer ?influencerLabel ?influenced ?influencedLabel
    WHERE {{
    ?influencer dbo:influenced ?influenced ;
    rdfs:label ?influencerLabel ;
    dbo:birthPlace ?lugarNacimiento .

    ?influenced rdfs:label ?influencedLabel .

    FILTER (lang(?influencerLabel) = "es" && lang(?influencedLabel) = "es")
    FILTER (?lugarNacimiento = dbr:Ecuador)
    }}
    LIMIT {limit}
    """
    return run_sparql_query(DBPEDIA_ENDPOINT, query)

def get_ecuadorian_musicians(search_term=None, limit=10):
    """
    Obtiene músicos ecuatorianos desde Wikidata.
    Incluye la URL de la imagen.
    """
    search_filter = f'FILTER (CONTAINS(LCASE(?musicianLabel), LCASE("{search_term}")) || CONTAINS(LCASE(?description), LCASE("{search_term}")))' if search_term else ""

    query = f"""
    SELECT DISTINCT ?musician ?musicianLabel ?description ?dateOfBirth ?placeOfBirthLabel ?image WHERE {{
    ?musician wdt:P31 wd:Q5 ; # Instance of human
              wdt:P106 wd:Q639669 ; # Occupation: musician
              wdt:P27 wd:Q736 . # Nationality: Ecuador
    OPTIONAL {{ ?musician wdt:P569 ?dateOfBirth . }} # Date of birth
    OPTIONAL {{ ?musician wdt:P19 ?placeOfBirth . }} # Place of birth
    OPTIONAL {{ ?musician wdt:P18 ?image . }} # Image (P18)
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es". }}
    OPTIONAL {{ ?musician schema:description ?description. FILTER (lang(?description) = "es"). }}
    {search_filter}
    }} LIMIT {limit}
    """
    return run_sparql_query(WIKIDATA_ENDPOINT, query)