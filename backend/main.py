from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import datetime
import urllib.parse
import urllib.request
import json
import socket
import ssl
import re

app = FastAPI(
    title="WG Pentesting Engine API",
    version="6.0",
    description="Motor backend de diagnóstico pasivo integral de superficie y postura B2B"
)

# 1. CONFIGURACIÓN CORS PERMISIVA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. MODELO DE ENTRADA (Sincronizado con LeadModal.vue)
class ScanRequest(BaseModel):
    url: str
    nombre_empresa: Optional[str] = "Cliente No Especificado"
    rut_empresa: Optional[str] = "N/A"
    correo_contacto: Optional[str] = "N/A"
    telefono_contacto: Optional[str] = "N/A"

# 3. BASE DE CONOCIMIENTO COMPLETA (Estándar OWASP)
knowledge_base = {
    "HEADER_MISSING": {
        "owasp": "A05:2021-Security Misconfiguration",
        "riesgo": "Ataques de Clickjacking, MIME-Sniffing y XSS debido a ausencia de cabeceras de seguridad HTTP esenciales.",
        "solucion": "Configurar las cabeceras Strict-Transport-Security (HSTS), Content-Security-Policy (CSP), X-Frame-Options, X-Content-Type-Options y Referrer-Policy en la respuesta del servidor."
    },
    "SSL_EXPIRED_OR_SOON": {
        "owasp": "A02:2021-Cryptographic Failures",
        "riesgo": "Certificado SSL/TLS próximo a expirar o inválido. Los navegadores bloquearán el acceso de los clientes con pantallas de advertencia de alta severidad.",
        "solucion": "Renovar el certificado SSL/TLS de forma inmediata e implementar renovación automatizada mediante protocolo ACME / Let's Encrypt."
    },
    "COOKIE_INSECURE": {
        "owasp": "A01:2021-Broken Access Control",
        "riesgo": "Galletas de sesión omiten los atributos Secure o HttpOnly, permitiendo interceptación en redes públicas o robo de sesión vía scripts maliciosos (XSS).",
        "solucion": "Establecer las banderas 'Secure', 'HttpOnly' y 'SameSite=Lax/Strict' en todas las cookies emitidas por el servidor web."
    },
    "SERVER_LEAK": {
        "owasp": "A05:2021-Security Misconfiguration",
        "riesgo": "Fuga de información técnica sobre versiones exactas del servidor web o lenguajes de programación (Server / X-Powered-By).",
        "solucion": "Ocultar o modificar banners de versión en la configuración del servidor web (ServerTokens ProductOnly en Apache, server_tokens off en Nginx)."
    },
    "NO_HTTPS_REDIRECT": {
        "owasp": "A02:2021-Cryptographic Failures",
        "riesgo": "El puerto HTTP (80) no fuerza la redirección permanente al puerto HTTPS (443) cifrado, permitiendo tráfico en texto plano.",
        "solucion": "Configurar una redirección permanente (301 Moved Permanently) de todo el tráfico HTTP hacia HTTPS en la capa perimetral."
    },
    "CORS_WILDCARD": {
        "owasp": "A01:2021-Broken Access Control",
        "riesgo": "Política de origen cruzado (CORS) permisiva ('*'), permitiendo que sitios de terceros lean respuestas privadas o interactúen con la API.",
        "solucion": "Restringir la cabecera Access-Control-Allow-Origin definiendo de forma explícita los dominios de confianza autorizados."
    },
    "ROBOTS_EXPOSURE": {
        "owasp": "A01:2021-Broken Access Control",
        "riesgo": "El archivo robots.txt expone rutas administrativas, copias de seguridad o páneles privados a motores de búsqueda y atacantes.",
        "solucion": "Remover referencias a rutas sensibles en robots.txt y asegurar dichos directorios mediante autenticación previa y listas de control de acceso."
    },
    "CMS_OUTDATED_DETECTED": {
        "owasp": "A06:2021-Vulnerable and Outdated Components",
        "riesgo": "Detección pública de gestor de contenidos (CMS) o versiones obsoletas expuestas en etiquetas Meta Generator HTML.",
        "solucion": "Remover etiquetas <meta name='generator'> y mantener actualizados el núcleo del CMS y sus extensiones a la última versión estable."
    },
    "SECURITY_TXT_MISSING": {
        "owasp": "A05:2021-Security Misconfiguration",
        "riesgo": "Falta del estándar corporativo de divulgación responsable de vulnerabilidades (/.well-known/security.txt).",
        "solucion": "Crear y publicar el archivo /.well-known/security.txt con la información de contacto oficial del equipo de ciberseguridad."
    },
    "DMARC_SPF_MISSING": {
        "owasp": "A06:2021-Vulnerable and Outdated Components",
        "riesgo": "Ausencia de registros DNS SPF o políticas DMARC restrictivas, dejando el dominio vulnerable a suplantación de correo (Email Spoofing / Phishing).",
        "solucion": "Publicar registros TXT en DNS para SPF e implementar una política DMARC en modo 'quarantine' o 'reject' (_dmarc.dominio.com)."
    },
    "CAA_MISSING": {
        "owasp": "A05:2021-Security Misconfiguration",
        "riesgo": "Ausencia de registros DNS CAA (Certification Authority Authorization), permitiendo que cualquier CA emita certificados para el dominio.",
        "solucion": "Definir registros CAA en el panel DNS especificando las Autoridades de Certificación explícitamente autorizadas a emitir certificados."
    },
    "CSP_WEAK": {
        "owasp": "A05:2021-Security Misconfiguration",
        "riesgo": "Política Content-Security-Policy (CSP) permisiva que permite ejecución de scripts en línea ('unsafe-inline') o eval.",
        "solucion": "Fortalecer la política CSP eliminando 'unsafe-inline' e implementando hashes cryptographic o 'nonces' para la ejecución de scripts."
    },
    "WAF_NOT_DETECTED": {
        "owasp": "A05:2021-Security Misconfiguration",
        "riesgo": "No se detectó un Firewall de Aplicaciones Web (WAF) o red CDN protegiendo la capa de aplicación frontal.",
        "solucion": "Desplegar una capa de protección perimetral WAF/CDN (Ej: Cloudflare, AWS CloudFront, Akamai) para mitigar ataques automatizados y DoS."
    },
    "SENSITIVE_FILES_EXPOSED": {
        "owasp": "A01:2021-Broken Access Control",
        "riesgo": "Exposición pública de archivos de metadatos o políticas heredadas de sistema (.DS_Store, crossdomain.xml).",
        "solucion": "Restringir en el servidor web el acceso a archivos ocultos o de metadatos del sistema operativo e IDEs de desarrollo."
    },
    "PORT_OPEN": {
        "owasp": "A05:2021-Security Misconfiguration",
        "riesgo": "Subdominio o puerto de desarrollo/administración expuesto directamente en la superficie perimetral pública.",
        "solucion": "Aislar los entornos de pruebas y paneles administrativos tras una red privada virtual (VPN) y aplicar reglas de firewall estricto."
    },
    "DNS_VULN": {
        "owasp": "A06:2021-Vulnerable and Outdated Components",
        "riesgo": "Fallo en la resolución DNS o ausencia de registros de red alcanzables para el dominio objetivo.",
        "solucion": "Verificar la configuración de los servidores de nombres autoritativos (NS) y asegurar la resolución correcta del registro A/AAAA."
    }
}

@app.get("/api/knowledge")
def get_knowledge():
    return knowledge_base

# 4. FUNCIONES AUXILIARES DE CONSULTA Y ANÁLISIS PASIVO

def normalizar_url(target: str):
    if not target.startswith("http://") and not target.startswith("https://"):
        target = "https://" + target
    parsed = urllib.parse.urlparse(target)
    hostname = parsed.netloc or parsed.path
    if ":" in hostname:
        hostname = hostname.split(":")[0]
    return hostname, f"https://{hostname}", f"http://{hostname}"

def resolver_ip(hostname: str) -> str:
    try:
        return socket.gethostbyname(hostname)
    except Exception:
        return "No resuelto"

def consultar_dns_doh(domain: str, record_type: str) -> List[str]:
    """
    Consulta registros DNS utilizando DoH (Google DNS over HTTPS) de forma 100% pasiva y nativa.
    """
    url = f"https://dns.google/resolve?name={urllib.parse.quote(domain)}&type={record_type}"
    req = urllib.request.Request(url, headers={"User-Agent": "WGPentestingEngine/6.0"})
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            answers = data.get("Answer", [])
            return [ans.get("data", "") for ans in answers if "data" in ans]
    except Exception:
        return []

def analizar_ssl(hostname: str):
    """
    Inspección pasiva del certificado SSL/TLS en el puerto 443.
    """
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=4) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_after_str = cert.get('notAfter')
                if not_after_str:
                    exp_date = datetime.datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
                    days_left = (exp_date - datetime.datetime.utcnow()).days
                    return True, days_left, exp_date.strftime("%d/%m/%Y")
    except Exception:
        pass
    return False, -1, "N/A"

def analizar_http_https_redirect(url_http: str) -> bool:
    """
    Verifica si la versión HTTP redirige a HTTPS.
    """
    req = urllib.request.Request(url_http, headers={"User-Agent": "WGPentestingEngine/6.0"})
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            final_url = resp.geturl()
            return final_url.startswith("https://")
    except urllib.error.HTTPError as e:
        if e.code in [301, 302, 307, 308]:
            redirect_to = e.headers.get('Location', '')
            return redirect_to.startswith("https://")
    except Exception:
        pass
    return False

def detectar_waf_cdn(headers_dict: Dict[str, str]) -> Optional[str]:
    """
    Identifica la presencia de WAF / CDN a partir de firmas pasivas en las cabeceras HTTP.
    """
    firmas = {
        "cf-ray": "Cloudflare WAF / CDN",
        "x-amz-cf-id": "AWS CloudFront CDN",
        "x-akamai-transformed": "Akamai Edge Suite",
        "x-fastly-request-id": "Fastly CDN",
        "x-sucuri-id": "Sucuri WebApp Firewall",
        "x-imperva-region": "Imperva Incapsula WAF"
    }
    for header, nombre in firmas.items():
        if header in headers_dict:
            return nombre
            
    server_val = headers_dict.get("server", "").lower()
    if "cloudflare" in server_val:
        return "Cloudflare WAF"
    elif "cloudfront" in server_val:
        return "AWS CloudFront"
    elif "akamai" in server_val:
        return "Akamai WAF"
        
    return None

def analizar_cabeceras_y_body(url_https: str):
    """
    Inspección pasiva de cabeceras de seguridad, cookies, CORS, CSP y metadatos HTML.
    """
    req = urllib.request.Request(url_https, headers={"User-Agent": "WGPentestingEngine/6.0"})
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers_requeridos = [
        "strict-transport-security",
        "content-security-policy",
        "x-frame-options",
        "x-content-type-options",
        "referrer-policy"
    ]
    
    resultados = {
        "headers_missing": [],
        "server_leak": None,
        "cors_wildcard": False,
        "cookie_insecure": False,
        "cms_generator": None,
        "csp_debil": False,
        "waf_detected": None,
        "exito": False
    }

    try:
        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
            resultados["exito"] = True
            resp_headers = {k.lower(): v for k, v in resp.headers.items()}
            
            # 1. Detección de WAF/CDN
            resultados["waf_detected"] = detectar_waf_cdn(resp_headers)

            # 2. Cabeceras Faltantes
            for h in headers_requeridos:
                if h not in resp_headers:
                    resultados["headers_missing"].append(h)

            # 3. Análisis de calidad de CSP
            if "content-security-policy" in resp_headers:
                csp_val = resp_headers["content-security-policy"].lower()
                if "'unsafe-inline'" in csp_val or "'unsafe-eval'" in csp_val:
                    resultados["csp_debil"] = True

            # 4. Divulgación de Servidor
            server_header = resp_headers.get("server", "") + " " + resp_headers.get("x-powered-by", "")
            if re.search(r'\d+\.\d+', server_header):
                resultados["server_leak"] = server_header.strip()

            # 5. CORS Wildcard
            if resp_headers.get("access-control-allow-origin") == "*":
                resultados["cors_wildcard"] = True

            # 6. Cookies Inseguras
            raw_cookies = resp.headers.get_all('Set-Cookie', [])
            for c in raw_cookies:
                c_lower = c.lower()
                if "secure" not in c_lower or "httponly" not in c_lower:
                    resultados["cookie_insecure"] = True
                    break

            # 7. Inspección de Body HTML
            body_bytes = resp.read(60000)
            body_text = body_bytes.decode('utf-8', errors='ignore')
            meta_match = re.search(r'<meta\s+name=["\']generator["\']\s+content=["\']([^"\']+)["\']', body_text, re.IGNORECASE)
            if meta_match:
                resultados["cms_generator"] = meta_match.group(1)
            elif "wp-content" in body_text:
                resultados["cms_generator"] = "WordPress (Detectado por estructura de directorios)"

    except Exception:
        resultados["headers_missing"] = headers_requeridos

    return resultados

def analizar_robots_y_sitemap(url_https: str):
    """
    Inspección pasiva de robots.txt y sitemap.xml.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    rutas_robots = []
    has_sitemap = False

    # Robots.txt
    try:
        req_robots = urllib.request.Request(f"{url_https}/robots.txt", headers={"User-Agent": "WGPentestingEngine/6.0"})
        with urllib.request.urlopen(req_robots, timeout=4, context=ctx) as resp:
            if resp.status == 200:
                text = resp.read().decode('utf-8', errors='ignore')
                keywords = ['admin', 'backup', 'private', 'db', 'config', 'secret', 'login', 'api']
                for line in text.splitlines():
                    if line.lower().startswith('disallow:'):
                        path = line.split(':', 1)[1].strip()
                        if any(k in path.lower() for k in keywords):
                            rutas_robots.append(path)
    except Exception:
        pass

    # Sitemap.xml
    try:
        req_site = urllib.request.Request(f"{url_https}/sitemap.xml", headers={"User-Agent": "WGPentestingEngine/6.0"})
        with urllib.request.urlopen(req_site, timeout=4, context=ctx) as resp:
            if resp.status == 200:
                has_sitemap = True
    except Exception:
        pass

    return rutas_robots, has_sitemap

def analizar_metadatos_sensibles(url_https: str) -> bool:
    """
    Verifica la exposición de archivos como .DS_Store o crossdomain.xml.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    archivos = ["/.DS_Store", "/crossdomain.xml"]
    for arch in archivos:
        try:
            req = urllib.request.Request(f"{url_https}{arch}", headers={"User-Agent": "WGPentestingEngine/6.0"})
            with urllib.request.urlopen(req, timeout=3, context=ctx) as resp:
                if resp.status == 200 and len(resp.read(100)) > 0:
                    return True
        except Exception:
            pass
    return False

def analizar_security_txt(url_https: str) -> bool:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(f"{url_https}/.well-known/security.txt", headers={"User-Agent": "WGPentestingEngine/6.0"})
        with urllib.request.urlopen(req, timeout=3, context=ctx) as resp:
            return resp.status == 200
    except Exception:
        return False

# 5. ENDPOINT PRINCIPAL DE AUDITORÍA INTEGRAL
@app.post("/api/scan")
def run_scan(req: ScanRequest):
    target_raw = req.url.lower().strip()
    hostname, url_https, url_http = normalizar_url(target_raw)
    ip_address = resolver_ip(hostname)

    hallazgos = []
    logs = []

    # Métricas para el desglose en 4 ejes
    score_cripto = 100
    score_web = 100
    score_correo = 100
    score_madurez = 100

    critico = 0
    medio = 0

    logs.append({"tipo": "INFO", "mensaje": f"Iniciando auditoría de superficie integral sobre: {hostname}"})
    logs.append({"tipo": "INFO", "mensaje": f"Resolución de infraestructura IP objetivo: {ip_address}"})

    # --- EJE 1: RESOLUCIÓN Y INFRAESTRUCTURA DNS ---
    if ip_address == "No resuelto":
        hallazgos.append({"id": "DNS_VULN", "msg": "Incapacidad de resolver registros de red IP para el dominio objetivo."})
        logs.append({"tipo": "FAIL", "mensaje": "Resolución DNS fallida. El host no responde a consultas A/AAAA."})
        score_madurez -= 40
        critico += 1
    else:
        logs.append({"tipo": "PASS", "mensaje": f"Host activo y resuelto en la dirección IP pública {ip_address}."})

    # --- EJE 2: SEGURIDAD CRIPTOGRÁFICA (SSL/TLS) ---
    ssl_ok, days_left, exp_date = analizar_ssl(hostname)
    if ssl_ok:
        if days_left < 30:
            hallazgos.append({"id": "SSL_EXPIRED_OR_SOON", "msg": f"Certificado SSL/TLS próximo a vencer ({days_left} días restantes, Vence: {exp_date})"})
            logs.append({"tipo": "FAIL", "mensaje": f"ALERTA CRÍTICA: Al certificado SSL/TLS le quedan solo {days_left} días de vigencia."})
            score_cripto -= 50
            critico += 1
        else:
            logs.append({"tipo": "PASS", "mensaje": f"Certificado SSL/TLS activo y válido ({days_left} días restantes, Vence: {exp_date})."})
    else:
        hallazgos.append({"id": "SSL_EXPIRED_OR_SOON", "msg": "No se pudo establecer conexión SSL/TLS segura en el puerto 443."})
        logs.append({"tipo": "FAIL", "mensaje": "Fallo grave en la negociación criptográfica SSL/TLS (Puerto 443)."})
        score_cripto -= 70
        critico += 1

    has_redirect = analizar_http_https_redirect(url_http)
    if not has_redirect:
        hallazgos.append({"id": "NO_HTTPS_REDIRECT", "msg": "El puerto HTTP (80) no redirige automáticamente a la versión cifrada HTTPS."})
        logs.append({"tipo": "WARN", "mensaje": "Tráfico HTTP sin cifrar accesible sin redirección automática forzada."})
        score_cripto -= 30
        medio += 1
    else:
        logs.append({"tipo": "PASS", "mensaje": "Redirección forzada de HTTP a HTTPS configurada de forma permanente."})

    # --- EJE 3: AUTENTICACIÓN Y RESILIENCIA DE CORREO (SPF, DMARC, CAA) ---
    txt_records = consultar_dns_doh(hostname, "TXT")
    dmarc_records = consultar_dns_doh(f"_dmarc.{hostname}", "TXT")
    caa_records = consultar_dns_doh(hostname, "CAA")

    has_spf = any("v=spf1" in r.lower() for r in txt_records)
    has_dmarc = any("v=dmarc1" in r.lower() for r in dmarc_records)

    if not has_spf or not has_dmarc:
        hallazgos.append({"id": "DMARC_SPF_MISSING", "msg": "Falta configuración completa de seguridad Anti-Phishing (SPF / DMARC) en registros DNS."})
        logs.append({"tipo": "WARN", "mensaje": f"Protección de correo incompleta: SPF ({'OK' if has_spf else 'FALTA'}), DMARC ({'OK' if has_dmarc else 'FALTA'})."})
        score_correo -= 40
        medio += 1
    else:
        logs.append({"tipo": "PASS", "mensaje": "Registros DNS de autenticación de correo (SPF y DMARC) verificados con éxito."})

    if len(caa_records) == 0:
        hallazgos.append({"id": "CAA_MISSING", "msg": "No se detectaron registros DNS CAA para restringir la emisión no autorizada de certificados."})
        logs.append({"tipo": "WARN", "mensaje": "Ausencia de política CAA en registros DNS del dominio."})
        score_correo -= 20
        medio += 1
    else:
        logs.append({"tipo": "PASS", "mensaje": "Registros DNS CAA configurados correctamente."})

    # --- EJE 4: PROTECCIÓN WEB, CABECERAS Y WAF ---
    res_http = analizar_cabeceras_y_body(url_https)

    if res_http["waf_detected"]:
        logs.append({"tipo": "PASS", "mensaje": f"Capa de protección perimetral detectada: {res_http['waf_detected']}."})
    else:
        hallazgos.append({"id": "WAF_NOT_DETECTED", "msg": "No se identificó un Firewall de Aplicaciones Web (WAF/CDN) protegiendo el servidor."})
        logs.append({"tipo": "WARN", "mensaje": "Infraestructura sin capa de filtrado WAF/CDN perimetral detectable."})
        score_web -= 20
        medio += 1

    if len(res_http["headers_missing"]) > 0:
        faltantes_str = ", ".join(res_http["headers_missing"])
        hallazgos.append({"id": "HEADER_MISSING", "msg": f"Cabeceras de protección HTTP ausentes: {faltantes_str}"})
        logs.append({"tipo": "WARN", "mensaje": f"Faltan {len(res_http['headers_missing'])} cabeceras HTTP de protección recomendadas."})
        score_web -= 30
        medio += 1
    else:
        logs.append({"tipo": "PASS", "mensaje": "Todas las cabeceras HTTP de protección estándar fueron detectadas."})

    if res_http["csp_debil"]:
        hallazgos.append({"id": "CSP_WEAK", "msg": "La directiva Content-Security-Policy es débil (permite 'unsafe-inline' o eval)."})
        logs.append({"tipo": "WARN", "mensaje": "Política CSP configurada con excepciones de ejecución inseguras."})
        score_web -= 15
        medio += 1

    if res_http["server_leak"]:
        hallazgos.append({"id": "SERVER_LEAK", "msg": f"Fuga explícita de versión de servidor web: '{res_http['server_leak']}'"})
        logs.append({"tipo": "WARN", "mensaje": f"Banner de servidor expuesto en respuesta HTTP: {res_http['server_leak']}"})
        score_madurez -= 20
        medio += 1

    if res_http["cors_wildcard"]:
        hallazgos.append({"id": "CORS_WILDCARD", "msg": "Política CORS crítica: Permite accesos cruzados universales (Access-Control-Allow-Origin: *)"})
        logs.append({"tipo": "FAIL", "mensaje": "Configuración de origen cruzado (CORS) permisiva detectada."})
        score_web -= 35
        critico += 1

    if res_http["cookie_insecure"]:
        hallazgos.append({"id": "COOKIE_INSECURE", "msg": "Galletas de sesión omiten las banderas de seguridad Secure o HttpOnly."})
        logs.append({"tipo": "WARN", "mensaje": "Atributos de seguridad omitidos en cookies de la aplicación."})
        score_web -= 20
        medio += 1

    if res_http["cms_generator"]:
        hallazgos.append({"id": "CMS_OUTDATED_DETECTED", "msg": f"Tecnología o CMS identificado públicamente: '{res_http['cms_generator']}'"})
        logs.append({"tipo": "INFO", "mensaje": f"Componente Web / CMS identificado: {res_http['cms_generator']}"})

    # --- EJE 5: MADUREZ OPERATIVA Y METADATOS ---
    rutas_robots, has_sitemap = analizar_robots_y_sitemap(url_https)
    if len(rutas_robots) > 0:
        hallazgos.append({"id": "ROBOTS_EXPOSURE", "msg": f"robots.txt expone rutas privadas o administrativas: {', '.join(rutas_robots[:3])}"})
        logs.append({"tipo": "WARN", "mensaje": f"Robots.txt contiene {len(rutas_robots)} reglas Disallow sobre directorios sensibles."})
        score_madurez -= 20
        medio += 1

    if has_sitemap:
        logs.append({"tipo": "PASS", "mensaje": "Estructura sitemap.xml pública identificada."})

    if analizar_metadatos_sensibles(url_https):
        hallazgos.append({"id": "SENSITIVE_FILES_EXPOSED", "msg": "Exposición pública de archivos de metadatos del sistema (.DS_Store / crossdomain.xml)"})
        logs.append({"tipo": "FAIL", "mensaje": "Archivos de metadatos o políticas heredadas accesibles en la raíz web."})
        score_madurez -= 30
        critico += 1

    if not analizar_security_txt(url_https):
        hallazgos.append({"id": "SECURITY_TXT_MISSING", "msg": "Falta la implementación del estándar /.well-known/security.txt"})
        logs.append({"tipo": "WARN", "mensaje": "Estándar de divulgación responsable /.well-known/security.txt no localizado."})
        score_madurez -= 10
        medio += 1

    if "admin" in hostname or "dev" in hostname or "test" in hostname or "stage" in hostname:
        hallazgos.append({"id": "PORT_OPEN", "msg": "Subdominio con nomenclaturas de desarrollo/pruebas expuesto en red pública."})
        logs.append({"tipo": "FAIL", "mensaje": "ALERTA: Nombre de host sugiere entorno de desarrollo o administración expuesto."})
        score_madurez -= 30
        critico += 1

    logs.append({"tipo": "INFO", "mensaje": "Análisis pasivo completado. Consolidando métricas por ejes corporativos..."})

    # Normalización de puntajes por ejes
    score_cripto = max(0, min(100, score_cripto))
    score_web = max(0, min(100, score_web))
    score_correo = max(0, min(100, score_correo))
    score_madurez = max(0, min(100, score_madurez))

    # Puntaje ponderado global
    puntaje_global = int((score_cripto * 0.3) + (score_web * 0.3) + (score_correo * 0.2) + (score_madurez * 0.2))

    return {
        "dominio": hostname,
        "ip_address": ip_address,
        "nombre_empresa": req.nombre_empresa if req.nombre_empresa else "Cliente No Especificado",
        "rut_empresa": req.rut_empresa if req.rut_empresa else "N/A",
        "correo_contacto": req.correo_contacto if req.correo_contacto else "N/A",
        "telefono_contacto": req.telefono_contacto if req.telefono_contacto else "N/A",
        "fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "puntaje": puntaje_global,
        "desglose_ejes": {
            "seguridad_criptografica": score_cripto,
            "proteccion_web": score_web,
            "resiliencia_correo": score_correo,
            "madurez_operativa": score_madurez
        },
        "nivel_riesgo": {
            "critico": critico,
            "medio": medio
        },
        "hallazgos": hallazgos,
        "logs": logs
    }