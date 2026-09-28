import socket
import dns.resolver
import requests
import re
from urllib.parse import urlparse, urljoin
from datetime import datetime
import urllib3
from schemas import ScanRequest
from knowledge_base import KNOWLEDGE_BASE

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WGScannerEngine:
    def __init__(self, request: ScanRequest):
        self.request = request
        self.url = request.url if request.url.startswith("http") else f"https://{request.url}"
        self.dominio = urlparse(self.url).netloc
        self.puntaje = 100
        self.hallazgos = []
        self.logs = []
        self.nivel_riesgo = {"critico": 0, "medio": 0, "bajo": 0}

    def add_log(self, mensaje: str, tipo: str = "INFO"):
        self.logs.append({"tipo": tipo, "mensaje": mensaje})

    def ejecutar(self) -> dict:
        self.add_log(f"Iniciando WG Pentesting Engine v5.0 para {self.dominio}", "INFO")
        
        # 1. Comprobación de WAF y Cabeceras
        try:
            res = requests.get(self.url, timeout=8, verify=False)
            headers = {k.lower(): v.lower() for k, v in res.headers.items()}
            
            server_name = headers.get('server', '')
            if 'cloudflare' in server_name or 'sucuri' in server_name:
                self.add_log("Protección WAF perimetral activa", "PASS")
            else:
                self.add_log("Sin escudo WAF perimetral detectado", "WARN")
                self.hallazgos.append({"id": "MISSING_WAF", "msg": "Infraestructura sin WAF. Vulnerable a DDoS."})
                self.puntaje -= 10
                self.nivel_riesgo["medio"] += 1

            if server_name != '':
                self.add_log(f"Fuga de información del servidor: {server_name}", "FAIL")
                self.hallazgos.append({"id": "FUGA_INFO", "msg": f"El servidor expone su software: {server_name}"})
                self.puntaje -= 5
                self.nivel_riesgo["medio"] += 1

            if 'content-security-policy' not in headers:
                self.add_log("Falta cabecera Content-Security-Policy (CSP)", "FAIL")
                self.hallazgos.append({"id": "FALTA_CSP", "msg": "Ausencia de CSP. Riesgo de inyección XSS."})
                self.puntaje -= 15
                self.nivel_riesgo["critico"] += 1

        except Exception as e:
            self.add_log(f"Error al conectar con la URL objetivo: {str(e)}", "FAIL")

        # 2. Escaneo de Puertos Críticos
        for port in [21, 22, 3306, 3389]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                if s.connect_ex((self.dominio, port)) == 0:
                    self.add_log(f"PUERTO CRÍTICO ABIERTO: {port}", "FAIL")
                    self.hallazgos.append({"id": "PUERTO_CRITICO", "msg": f"El puerto {port} acepta conexiones públicas."})
                    self.puntaje -= 15
                    self.nivel_riesgo["critico"] += 1
                s.close()
            except: pass

        # 3. Verificación de Registros DNS Anti-Phishing
        try:
            spf = any("v=spf1" in r.to_text() for r in dns.resolver.resolve(self.dominio, 'TXT'))
            if not spf:
                self.add_log("Faltan registros DNS SPF contra suplantación", "FAIL")
                self.hallazgos.append({"id": "FALTA_SPF_DMARC", "msg": "Dominio desprotegido contra envío de correos falsos."})
                self.puntaje -= 10
                self.nivel_riesgo["medio"] += 1
            else:
                self.add_log("Protección Anti-Phishing (SPF) confirmada", "PASS")
        except: pass

        # 4. Prueba de Rate Limiting
        try:
            bloqueado = False
            for _ in range(5):
                r_sim = requests.get(self.url, timeout=2, verify=False)
                if r_sim.status_code in [429, 403]:
                    bloqueado = True
            if not bloqueado:
                self.add_log("Vulnerable a Fuerza Bruta (Sin Rate Limit activo)", "WARN")
                self.hallazgos.append({"id": "RATE_LIMIT", "msg": "El servidor no frena ráfagas de peticiones rápidas."})
                self.puntaje -= 5
                self.nivel_riesgo["medio"] += 1
            else:
                self.add_log("Mecanismo de Rate Limit detectado correctamente", "PASS")
        except: pass

        self.puntaje = max(0, self.puntaje)
        
        return {
            "url": self.url,
            "dominio": self.dominio,
            "nombre_empresa": self.request.nombre_empresa,
            "rut_empresa": self.request.rut_empresa,
            "correo_contacto": self.request.correo_contacto,
            "telefono_contacto": self.request.telefono_contacto,
            "puntaje": self.puntaje,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "nivel_riesgo": self.nivel_riesgo,
            "hallazgos": self.hallazgos,
            "logs": self.logs
        }