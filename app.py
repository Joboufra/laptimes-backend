from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from config import DB_CONFIG
import psycopg2
import logging
from psycopg2 import Error
from datetime import datetime
from typing import List
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM

# Respuestas
from responses import (
    response_200_total_vueltas,
    response_200_total_pilotos,
    response_200_total_circuitos,
    response_200_lista_pilotos,
    response_200_lista_compuestos,
    response_200_lista_circuitos,
    response_200_datos_piloto,
    response_200_datos_compuesto,
    response_200_datos_circuito,
    response_422,
    response_503
)

# Configuración de logging
logger = logging.getLogger("uvicorn.access")
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler("/home/joboufra/laptimes-backend/access.log", maxBytes=100000000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Configuración de Elastic APM
apm_config = {
    'SERVICE_NAME': 'LapAnalysis API',
    'SERVER_URL': 'http://10.20.10.10:8200',
    'ENVIRONMENT': 'dev'
}
apm_client = make_apm_client(apm_config)

app = FastAPI(
    docs_url="/swagger", 
    redoc_url="/redoc", 
    title="Lap Analysis", 
    version="0.1.0", 
    description="Esta API proporciona datos que hacen referencia al análisis de los tiempos por vuelta de todos los pilotos que compiten en el campeonato de F1 TSR Edición XII",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
app.add_middleware(ElasticAPM, client=apm_client)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://10.20.10.10:4889",
        "https://laptimes.joboufra.es",
        "http://localhost:3000",
    ], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# Modelos de pydantic
class PilotoRequest(BaseModel):
    piloto: str = Field(..., description="Nombre del piloto a consultar", example="Jose Boullosa")
    compuesto: str = Field(None, description="Tipo de compuesto de neumático, opcional", example="C1")
    circuito: str = Field(None, description="Nombre del circuito, opcional", example="Silverstone")

class CompuestoRequest(BaseModel):
    compuesto: str = Field(..., description="Tipo de compuesto de neumático obligatorio", example="C1")
    circuito: str = Field(None, description="Nombre del circuito, opcional", example="Silverstone")

class CircuitoRequest(BaseModel):
    circuito: str = Field(..., description="Nombre del circuito obligatorio", example="Silverstone")


class TiempoVuelta(BaseModel):
    Piloto: str
    Fecha: str
    TiempoVuelta: str
    Compuesto: str
    Sector1: str
    Sector2: str
    Sector3: str
    Lastre: int
    Restrictor: int
    Grip: float
    Circuito: str
    Campeonato: str
    Coche: str
    Team: str
    temp_ambiente: float
    temp_pista: float

    @validator('Fecha', pre=True, always=True)
    def format_fecha(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value

#Conexión a la base de datos
def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Error as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="No se puede conectar a la base de datos")

def transformar_tiempos(t):
    parts = t.split(':')
    return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2]) if len(parts) == 3 else int(parts[0]) * 60 + float(parts[1])

def datos_circuito(request: CircuitoRequest):
    piloto_filter = ""
    compuesto_filter = ""
    
    if request.piloto:
        piloto_filter = f"AND lower(Piloto) LIKE %s"
    if request.compuesto:
        compuesto_filter = f"AND Compuesto = %s"

    query = f"""
        SELECT * FROM ac.TiemposVuelta
        WHERE Circuito = %s {piloto_filter} {compuesto_filter}
    """

    params = [request.circuito]
    if request.piloto:
        params.append(f"%{request.piloto.lower()}%")
    if request.compuesto:
        params.append(request.compuesto)
    
    return execute_query(query, tuple(params))

# Ejecución de consultas
def execute_query(query, params):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="No se puede conectar a la base de datos")
    with conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            records = cur.fetchall()
    return [TiempoVuelta(
        Piloto=row[0],
        Fecha=row[1],
        TiempoVuelta=row[2],
        Compuesto=row[3],
        Sector1=row[4],
        Sector2=row[5],
        Sector3=row[6],
        Lastre=row[7],
        Restrictor=row[8],
        Grip=row[9],
        Circuito=row[10],
        Campeonato=row[11],
        Coche=row[12],
        Team=row[13],
        temp_ambiente=row[14],
        temp_pista=row[15]
    ) for row in records] if records else []

# Función para ejecutar consultas de recuento
def execute_count_query(query):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="No se puede conectar a la base de datos")
    with conn:
        with conn.cursor() as cur:
            cur.execute(query)
            count = cur.fetchone()[0]
    return {"total": count}

# Función para ejecutar consultas de listado
def execute_list_query(query):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="No se puede conectar a la base de datos")
    with conn:
        with conn.cursor() as cur:
            cur.execute(query)
            records = cur.fetchall()
    if not records:
        return []
    return [record[0] for record in records]

# Manejo de errores de validación
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"msg": "Error en los parámetros requeridos del input", "errors": exc.errors()}
    )

# Endpoint /api/total/vueltas
@app.get('/api/total/vueltas', summary="Obtener el total de vueltas registradas en la base de datos", responses={
    200: response_200_total_vueltas,
    422: response_422,
    503: response_503
}, tags=["Totales"])
async def total_vueltas():
    query = """
        SELECT COUNT(*) FROM ac.TiemposVuelta where campeonato like '%TSR%'
    """
    return execute_count_query(query)

# Endpoint /api/total/pilotos
@app.get('/api/total/pilotos', summary="Obtener el total de pilotos diferentes en la base de datos", responses={
    200: response_200_total_pilotos,
    422: response_422,
    503: response_503
}, tags=["Totales"])
async def total_pilotos():
    query = """
        SELECT COUNT(DISTINCT Piloto) FROM ac.TiemposVuelta where campeonato like '%TSR%'
    """
    return execute_count_query(query)

# Endpoint /api/total/circuitos
@app.get('/api/total/circuitos', summary="Obtener el total de circuitos diferentes en la base de datos", responses={
    200: response_200_total_circuitos,
    422: response_422,
    503: response_503
}, tags=["Totales"])
async def total_circuitos():
    query = """
        SELECT COUNT(DISTINCT Circuito) FROM ac.TiemposVuelta where campeonato like '%TSR%'
    """
    return execute_count_query(query)

# Endpoint /api/lista/pilotos
@app.get('/api/lista/pilotos', summary="Obtener el listado único de pilotos en la base de datos", responses={
    200: response_200_lista_pilotos,
    422: response_422,
    503: response_503
}, tags=["Listas"])
async def lista_pilotos():
    query = """
        SELECT DISTINCT Piloto FROM ac.TiemposVuelta
        where campeonato like '%TSR%'
        ORDER BY Piloto ASC
    """
    return execute_list_query(query)

# Endpoint /api/lista/compuestos
@app.get('/api/lista/compuestos', summary="Obtener el listado único de compuestos en la base de datos", responses={
    200: response_200_lista_compuestos,
    422: response_422,
    503: response_503
}, tags=["Listas"])
async def lista_compuestos():
    query = """
        SELECT DISTINCT Compuesto FROM ac.TiemposVuelta where campeonato like '%TSR%'
        ORDER BY Compuesto ASC
    """
    return execute_list_query(query)

# Endpoint /api/lista/circuitos
@app.get('/api/lista/circuitos', summary="Obtener el listado único de circuitos en la base de datos", responses={
    200: response_200_lista_circuitos,
    422: response_422,
    503: response_503
}, tags=["Listas"])
async def lista_circuitos():
    query = """
        SELECT DISTINCT Circuito FROM ac.TiemposVuelta where campeonato like '%TSR%'
        ORDER BY Circuito ASC
    """
    return execute_list_query(query)

# Endpoint /piloto/
@app.post('/api/datos/piloto/', response_model=List[TiempoVuelta], tags=["Datos"], responses={
    200: response_200_datos_piloto,
    422: response_422,
    503: response_503
}, summary="Obtener datos por piloto")
async def datos_piloto(request: PilotoRequest):
    query = """
        SELECT * FROM ac.TiemposVuelta 
        WHERE lower(Piloto) LIKE %s
    """
    params = [f"%{request.piloto.lower()}%"]

    if request.compuesto:
        query += " AND Compuesto = %s"
        params.append(request.compuesto)
    
    if request.circuito:
        query += " AND Circuito = %s"
        params.append(request.circuito)
    return execute_query(query, tuple(params))

# Endpoint /compuesto/
@app.post('/api/datos/compuesto/', response_model=List[TiempoVuelta], tags=["Datos"], responses={
    200: response_200_datos_compuesto,
    422: response_422,
    503: response_503
}, summary="Obtener datos por tipo de compuesto")
async def datos_compuesto(request: CompuestoRequest):
    query = """
        SELECT * FROM ac.TiemposVuelta 
        WHERE Compuesto = '%s'
    """
    params = [request.compuesto]
    
    if request.circuito:
        query += " AND Circuito = %s"
        params.append(request.circuito)
    
    return execute_query(query, tuple(params))

# Endpoint /datos/
@app.post('/api/datos/', response_model=List[TiempoVuelta], tags=["Datos"], responses={
    200: response_200_datos_circuito,
    422: response_422,
    503: response_503
}, summary="Obtener datos por circuito")
async def datos_circuito(request: CircuitoRequest):
    query = """
        SELECT * FROM ac.TiemposVuelta
        WHERE Circuito = %s
    """
    params = [request.circuito]
    
    return execute_query(query, tuple(params))

