from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import datetime
import random

app = FastAPI()

# 1. CONFIGURACIÓN CORS (Permite que el frontend en el puerto 5173/5174 se conecte)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. MODELO DE DATOS (Debe coincidir exactamente con el payload de LeadModal.vue)
class ScanRequest(BaseModel):
    url: str
    nombre_empresa: str
    rut_empresa: Optional[str] = ""
    correo_contacto: str
    telefono_contacto: Optional[str] = ""

# 3. BASE DE DATOS DE VULNERABILIDADES (Estándar OWASP)
knowledge_base = {
    "HEADER_MISSING": {
        "owasp": "A05:2021-Security Misconfiguration",
        "riesgo": "Ataques de Clickjacking y XSS debido a falta de cabeceras de seguridad. Los atacantes pueden inyectar código en la web.",
        "solucion": "Implementar cabeceras Strict-Transport-Security, X-Frame-Options y Content-Security-Policy en el servidor."
    },
    "PORT_OPEN": {
        "owasp": "A05:2021-Security Misconfiguration",
        "riesgo": "Exposición de servicios críticos de administración a ataques de fuerza bruta constantes.",
        "solucion": "Restringir el acceso a puertos mediante reglas de firewall estricto (solo IPs autorizadas) o aislar tras una VPN."
    },
    "DNS_VULN": {
        "owasp": "A06:2021-Vulnerable and Outdated Components",
        "riesgo": "Suplantación de identidad (Phishing). Ciberdelincuentes pueden enviar correos falsos a nombre de su empresa.",
        "solucion": "Configurar registros de validación SPF, DKIM y política restrictiva DMARC en el panel DNS del dominio."
    }
}

@app.get("/api/knowledge")
def get_knowledge():
    return knowledge_base

# 4. MOTOR DE ESCANEO (Simulador de Auditoría)
@app.post("/api/scan")
def run_scan(req: ScanRequest):
    target = req.url
    
    # Simulamos detección de vulnerabilidades
    has_headers_issue = random.choice([True, False])
    has_ports_issue = random.choice([True, False, True]) # Mayor probabilidad de puertos abiertos
    has_dns_issue = random.choice([True, False])
    
    hallazgos = []
    logs = []
    critico = 0
    medio = 0
    
    logs.append({"tipo": "INFO", "mensaje": f"Iniciando auditoría de superficie sobre objetivo: {target}"})
    
    if has_headers_issue:
        hallazgos.append({"id": "HEADER_MISSING", "msg": "Cabeceras HTTP de seguridad ausentes (HSTS, CSP)"})
        logs.append({"tipo": "WARN", "mensaje": "Faltan cabeceras de protección en la respuesta del servidor."})
        medio += 1
    else:
        logs.append({"tipo": "PASS", "mensaje": "Validación de cabeceras HTTP superada con éxito."})

    if has_ports_issue:
        hallazgos.append({"id": "PORT_OPEN", "msg": "Puertos de administración críticos expuestos (Ej: 22, 3306, 3389)"})
        logs.append({"tipo": "FAIL", "mensaje": "ALERTA: Se detectaron puertos de bases de datos/SSH abiertos a Internet."})
        critico += 1
    else:
        logs.append({"tipo": "PASS", "mensaje": "No hay puertos críticos expuestos en la capa perimetral."})

    if has_dns_issue:
        hallazgos.append({"id": "DNS_VULN", "msg": "Falta configuración de seguridad Anti-Phishing (DMARC/SPF)"})
        logs.append({"tipo": "WARN", "mensaje": "Vulnerabilidad de suplantación de dominio de correo detectada."})
        medio += 1
    else:
        logs.append({"tipo": "PASS", "mensaje": "Registros DNS de correo configurados correctamente."})
    
    logs.append({"tipo": "INFO", "mensaje": "Consolidando métricas y generando reporte ejecutivo..."})
    
    # Calcular puntaje final de la auditoría (Score de 0 a 100)
    puntaje = 100 - (critico * 25) - (medio * 10)
    puntaje = max(0, puntaje)
    
    return {
        "dominio": target,
        "nombre_empresa": req.nombre_empresa,
        "rut_empresa": req.rut_empresa,
        "correo_contacto": req.correo_contacto,
        "fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "puntaje": puntaje,
        "nivel_riesgo": {
            "critico": critico,
            "medio": medio
        },
        "hallazgos": hallazgos,
        "logs": logs
    }