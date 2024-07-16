# responses.py
from fastapi import status

response_200_total_vueltas = {
    "description": "Datos recuperados correctamente",
    "content": {
        "application/json": {
            "examples": {
                "normal": {
                    "summary": "Respuesta estándar",
                    "value": [
                        {
                            "total": 1808
                        }
                    ]
                }
            }
        }
    }
}

response_200_total_pilotos = {
    "description": "Datos recuperados correctamente",
    "content": {
        "application/json": {
            "examples": {
                "normal": {
                    "summary": "Respuesta estándar",
                    "value": [
                        {
                            "total": 25
                        }
                    ]
                }
            }
        }
    }
}

response_200_total_circuitos = {
    "description": "Datos recuperados correctamente",
    "content": {
        "application/json": {
            "examples": {
                "normal": {
                    "summary": "Respuesta estándar",
                    "value": [
                        {
                            "total": 3
                        }
                    ]
                }
            }
        }
    }
}

response_200_lista_pilotos = {
    "description": "Datos recuperados correctamente",
    "content": {
        "application/json": {
            "examples": {
                "normal": {
                    "summary": "Respuesta estándar",
                    "value": [
                        {
                            "Eduardo Cesar",
                            "Jose Manuel Riancho",
                            "Ismael Rodríguez",
                            "Alberto Fernandez",
                            "Fran Fuentes",
                            "Isidro Villar",
                            "Ignacio Oleaga",
                            "Cesar Dosil",
                            "Carlos Moreno",
                            "Manuel Boga",
                            "Jesus Manzaneque",
                            "Carlos Cabaco",
                            "Alberto vila",
                            "Karol Campo",
                            "Angel Aisa",
                            "Ruben Sanchez",
                            "Pako Sanchez Diaz",
                            "Alberto Mengelle",
                            "César Tizón",
                            "Jose Boullosa",
                            "Alejandro García",
                            "Francisco José Cuadra ",
                            "Pedro Crespo",
                            "Antonio Galdeano",
                            "Israel Contreras"
                        }
                    ]
                }
            }
        }
    }
}

response_200_lista_compuestos = {
    "description": "Datos recuperados correctamente",
    "content": {
        "application/json": {
            "examples": {
                "normal": {
                    "summary": "Respuesta estándar",
                    "value": [
                        {
                            "C3",
                            "C2",
                            "C1"
                        }
                    ]
                }
            }
        }
    }
}

response_200_lista_circuitos = {
    "description": "Datos recuperados correctamente",
    "content": {
        "application/json": {
            "examples": {
                "normal": {
                    "summary": "Respuesta estándar",
                    "value": [
                        {
                            "Silverstone",
                            "Spa",
                            "Spielberg",
                            "Bahrain"
                        }
                    ]
                }
            }
        }
    }
}

response_200_datos_piloto = {
    "description": "Datos recuperados correctamente",
    "content": {
        "application/json": {
            "examples": {
                "normal": {
                    "summary": "Respuesta estándar",
                    "value": [
                        {
                            "Piloto": "Jose Boullosa",
                            "Fecha": "2024-05-06 20:41:29",
                            "TiempoVuelta": "02:04.385",
                            "Compuesto": "C1",
                            "Sector1": "00:54.446",
                            "Sector2": "00:42.363",
                            "Sector3": "00:27.576",
                            "Lastre": 0,
                            "Restrictor": 15,
                            "Grip": "100.00%",
                            "Circuito": "Silverstone"
                        }
                    ]
                }
            }
        }
    }
}

response_200_datos_compuesto = {
    "description": "Datos recuperados correctamente",
    "content": {
        "application/json": {
            "examples": {
                "normal": {
                    "summary": "Respuesta estándar",
                    "value": [
                        {
                            "Piloto": "Jose Boullosa",
                            "Fecha": "2024-05-06 20:41:29",
                            "TiempoVuelta": "02:04.385",
                            "Compuesto": "C1",
                            "Sector1": "00:54.446",
                            "Sector2": "00:42.363",
                            "Sector3": "00:27.576",
                            "Lastre": 0,
                            "Restrictor": 15,
                            "Grip": "100.00%",
                            "Circuito": "Silverstone"
                        }
                    ]
                }
            }
        }
    }
}

response_200_datos_circuito = {
    "description": "Datos recuperados correctamente",
    "content": {
        "application/json": {
            "examples": {
                "normal": {
                    "summary": "Respuesta estándar",
                    "value": [
                        {
                            "Piloto": "Jose Boullosa",
                            "Fecha": "2024-05-06 20:41:29",
                            "TiempoVuelta": "02:04.385",
                            "Compuesto": "C1",
                            "Sector1": "00:54.446",
                            "Sector2": "00:42.363",
                            "Sector3": "00:27.576",
                            "Lastre": 0,
                            "Restrictor": 15,
                            "Grip": "100.00%",
                            "Circuito": "Silverstone"
                        }
                    ]
                }
            }
        }
    }
}

response_422 = {
    "description": "Petición no válida",
    "content": {
        "application/json": {
            "examples": {
                "invalidRequest": {
                    "summary": "Solicitud inválida",
                    "value": {
                        "msg": "Error en los parámetros requeridos del input",
                        "errors": [{"loc": ["query", "compuesto"], "msg": "field required", "type": "value_error.missing"}]
                    }
                }
            }
        }
    }
}

response_503 = {
    "description": "Servicio no disponible",
    "content": {
        "application/json": {
            "examples": {
                "serviceUnavailable": {
                    "summary": "Base de datos no accesible",
                    "value": {"msg": "No se puede conectar a la base de datos"}
                }
            }
        }
    }
}
