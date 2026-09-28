from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict

class ScanRequest(BaseModel):
    url: str
    nombre_empresa: Optional[str] = "Cliente General"
    rut_empresa: Optional[str] = "N/A"
    correo_contacto: Optional[str] = "N/A"
    telefono_contacto: Optional[str] = "N/A"

class Hallazgo(BaseModel):
    id: str
    msg: str

class ScanResult(BaseModel):
    url: str
    dominio: str
    nombre_empresa: str
    rut_empresa: str
    correo_contacto: str
    telefono_contacto: str
    puntaje: int
    fecha: str
    nivel_riesgo: Dict[str, int]
    hallazgos: List[Hallazgo]
    logs: List[Dict[str, str]]