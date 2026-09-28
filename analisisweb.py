import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import requests
import socket
import ssl
import dns.resolver
import whois
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from datetime import datetime
import urllib3
import json
import os
import re
import math

# Desactivar advertencias de certificados SSL autofirmados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# WAGA KNOWLEDGE BASE (BASE DE CONOCIMIENTO & OWASP)
# ==========================================
KNOWLEDGE_BASE = {
    "PUERTO_CRITICO": {
        "keyword": "PUERTO ABIERTO",
        "owasp": "A05:2021 - Configuración de Seguridad Defectuosa",
        "titulo": "Puertos Críticos Expuestos",
        "riesgo": "EJEMPLO: Un atacante usa el programa Hydra probando 10,000 contraseñas por minuto en tu puerto 3306 hasta entrar a tu base de datos y secuestrar tus clientes (Ransomware).",
        "solucion": "Bloquea el tráfico externo a estos puertos en tu firewall. Solo permite conexiones desde 'localhost' o IPs autorizadas."
    },
    "FALTA_CSP": {
        "keyword": "Falta Política CSP",
        "owasp": "A03:2021 - Inyección",
        "titulo": "Ausencia de Content-Security-Policy",
        "riesgo": "EJEMPLO: Un hacker inyecta JavaScript malicioso en un chat. Sin CSP, el navegador lo ejecuta y roba la cookie de sesión (PHPSESSID) de todos los que entren.",
        "solucion": "Agrega la cabecera CSP en tu servidor. Ejemplo en PHP: header(\"Content-Security-Policy: default-src 'self'\");"
    },
    "FALTA_SPF_DMARC": {
        "keyword": "Faltan registros anti-phishing",
        "owasp": "A08:2021 - Fallos en Software y Datos",
        "titulo": "Vulnerabilidad de Phishing (Correos Falsos)",
        "riesgo": "EJEMPLO: Un ciberdelincuente envía un correo 'Factura Vencida' usando gerencia@tuempresa.cl. Sin DMARC, el correo llega a la bandeja de entrada y estafan al cliente.",
        "solucion": "Configura los registros TXT (SPF y DMARC) en tu proveedor de dominio."
    },
    "FUGA_INFO": {
        "keyword": "Fuga de información",
        "owasp": "A05:2021 - Configuración Defectuosa",
        "titulo": "Fuga de Identidad del Servidor",
        "riesgo": "EJEMPLO: Si tu servidor avisa que usa 'PHP 5.6', el hacker no tiene que adivinar; va directo a Google, busca exploits para PHP 5.6 y te hackea en segundos.",
        "solucion": "Oculta 'Server' y 'X-Powered-By' en tu servidor web (Apache/Nginx o PHP header_remove)."
    },
    "SQL_INJECTION": {
        "keyword": "Inyección SQL",
        "owasp": "A03:2021 - Inyección",
        "titulo": "Posible Inyección SQL",
        "riesgo": "EJEMPLO: El atacante escribe ' OR 1=1 -- en un formulario y la base de datos le da acceso total saltándose la contraseña.",
        "solucion": "Usa siempre Consultas Preparadas (Prepared Statements con PDO o MySQLi)."
    },
    "ARCHIVO_SENSIBLE": {
        "keyword": "Archivo sensible",
        "owasp": "A01:2021 - Control de Acceso Roto",
        "titulo": "Archivos Críticos Expuestos",
        "riesgo": "EJEMPLO: Un atacante descarga tuweb.cl/.env y obtiene todas las contraseñas reales de tu base de datos y llaves maestras.",
        "solucion": "Deniega el acceso web a archivos ocultos mediante reglas en .htaccess o nginx.conf."
    },
    "MISSING_WAF": {
        "keyword": "Sin protección WAF",
        "owasp": "A05:2021 - Configuración Defectuosa",
        "titulo": "Sin Escudo WAF perimetral",
        "riesgo": "EJEMPLO: Una botnet lanza un ataque DDoS de miles de visitas por segundo, tu servidor colapsa y tu intranet cae por días.",
        "solucion": "Implementa un Proxy Inverso o WAF como Cloudflare (su plan gratuito bloquea DDoS)."
    },
    "RATE_LIMIT": {
        "keyword": "Vulnerable a Fuerza Bruta",
        "owasp": "A07:2021 - Fallos de Identificación y Autenticación",
        "titulo": "Sin Bloqueo de Múltiples Intentos",
        "riesgo": "EJEMPLO: Un robot intenta adivinar contraseñas haciendo 100 peticiones por segundo. Como no lo bloqueas, eventualmente adivinará la correcta.",
        "solucion": "Implementa bloqueo de IPs tras 5 intentos fallidos (como ya tienes en effectivaspa.cl)."
    },
    "BLACKLIST_SPAM": {
        "keyword": "IP en Lista Negra",
        "owasp": "A08:2021 - Fallos en Integridad",
        "titulo": "Dominio catalogado como SPAM",
        "riesgo": "EJEMPLO: El servidor fue infectado y mandó SPAM sin que te dieras cuenta. Ahora los correos de tu empresa caen en la carpeta de correo no deseado de tus clientes.",
        "solucion": "Limpia el servidor de malware y solicita la eliminación (delist) en Spamhaus o Barracuda."
    },
    "EMAILS_EXPUESTOS": {
        "keyword": "Correos expuestos",
        "owasp": "A02:2021 - Fallos Criptográficos / Fuga de Datos",
        "titulo": "Correos públicos (Riesgo Data Breach)",
        "riesgo": "EJEMPLO: Se encontraron correos corporativos en la web. Los hackers los toman y los cruzan con bases de datos hackeadas (Dark Web) para ver si la contraseña del empleado se filtró en otro sitio.",
        "solucion": "Obliga a tus empleados a usar 2FA (Doble Factor) y contraseñas distintas para la Intranet y redes sociales."
    }
}

# ==========================================
# WAGA SECURITY APP
# ==========================================
class WagaSecurityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WAGA Security v5.0 Ultimate - Enterprise Edition")
        self.root.geometry("1000x750")
        self.root.configure(bg="#0B0C10")
        
        self.resultados = {}
        self.nivel_riesgo = {"critico": 0, "medio": 0, "bajo": 0}
        
        self.setup_ui()

    def setup_ui(self):
        # Título WAGA
        titulo_frame = tk.Frame(self.root, bg="#0B0C10")
        titulo_frame.pack(pady=10)
        tk.Label(titulo_frame, text="🛡️ WAGA SECURITY", bg="#0B0C10", fg="#45A29E", font=("Verdana", 24, "bold")).pack()
        tk.Label(titulo_frame, text="Enterprise Vulnerability Scanner", bg="#0B0C10", fg="#66FCF1", font=("Consolas", 10)).pack()
        
        # Pestañas (Notebook)
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#0B0C10', borderwidth=0)
        style.configure('TNotebook.Tab', background='#1F2833', foreground='#C5C6C7', font=('Arial', 10, 'bold'), padding=[15, 5])
        style.map('TNotebook.Tab', background=[('selected', '#45A29E')], foreground=[('selected', 'white')])

        self.notebook = ttk.Notebook(self.root)
        self.tab_escaner = tk.Frame(self.notebook, bg="#0B0C10")
        self.tab_dash = tk.Frame(self.notebook, bg="#0B0C10")
        
        self.notebook.add(self.tab_escaner, text="🔍 Modo Auditoría")
        self.notebook.add(self.tab_dash, text="📊 Dashboard (Resultados)")
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # --- CONTENIDO PESTAÑA ESCÁNER ---
        frame_input = tk.Frame(self.tab_escaner, bg="#0B0C10")
        frame_input.pack(pady=15)
        
        tk.Label(frame_input, text="Target URL:", bg="#0B0C10", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.entrada_url = tk.Entry(frame_input, width=50, font=("Arial", 12), bg="#1F2833", fg="white", insertbackground="white")
        self.entrada_url.insert(0, "https://")
        self.entrada_url.pack(side=tk.LEFT, padx=5)

        frame_botones = tk.Frame(self.tab_escaner, bg="#0B0C10")
        frame_botones.pack(pady=10)

        self.btn_escanear = tk.Button(frame_botones, text="⚡ Ejecutar Pentest Automatizado", bg="#c0392b", fg="white", font=("Arial", 11, "bold"), command=self.iniciar_escaneo, borderwidth=0, padx=10, pady=5)
        self.btn_escanear.pack(side=tk.LEFT, padx=10)

        self.btn_reporte = tk.Button(frame_botones, text="📄 Generar Reporte Comercial (PDF/HTML)", bg="#27ae60", fg="white", font=("Arial", 11, "bold"), command=self.generar_reporte_html, state=tk.DISABLED, borderwidth=0, padx=10, pady=5)
        self.btn_reporte.pack(side=tk.LEFT, padx=10)

        self.progreso = ttk.Progressbar(self.tab_escaner, orient="horizontal", length=800, mode="determinate")
        self.progreso.pack(pady=10)

        tk.Label(self.tab_escaner, text="💡 TIP: Haz DOBLE CLIC en cualquier línea de la consola para ver detalles educativos", bg="#0B0C10", fg="#f39c12", font=("Arial", 9, "italic")).pack()

        # Consola con eventos de click
        self.consola = scrolledtext.ScrolledText(self.tab_escaner, width=105, height=22, bg="#000000", fg="#00ff00", font=("Consolas", 10), insertbackground="white")
        self.consola.pack(pady=10)
        self.consola.bind("<Double-Button-1>", self.on_console_doble_click)

        # --- CONTENIDO PESTAÑA DASHBOARD ---
        tk.Label(self.tab_dash, text="Distribución de Riesgos Detectados", bg="#0B0C10", fg="white", font=("Arial", 16, "bold")).pack(pady=20)
        self.canvas_chart = tk.Canvas(self.tab_dash, width=400, height=400, bg="#0B0C10", highlightthickness=0)
        self.canvas_chart.pack()

    def log(self, mensaje, tipo="INFO"):
        colores = {"INFO": "#66FCF1", "WARN": "#F39C12", "FAIL": "#E74C3C", "PASS": "#2ECC71"}
        color = colores.get(tipo, "white")
        
        self.consola.insert(tk.END, f"[{tipo}] ", tipo)
        self.consola.tag_config(tipo, foreground=color, font=("Consolas", 10, "bold"))
        self.consola.insert(tk.END, f"{mensaje}\n")
        self.consola.see(tk.END)

    def on_console_doble_click(self, event):
        # Obtener la línea donde el usuario hizo clic
        try:
            line_start = self.consola.index(f"@{event.x},{event.y} linestart")
            line_end = self.consola.index(f"@{event.x},{event.y} lineend")
            line_text = self.consola.get(line_start, line_end)
            
            for key, data in KNOWLEDGE_BASE.items():
                if data["keyword"].lower() in line_text.lower():
                    # Mostrar Pop-up educativo WAGA
                    popup = tk.Toplevel(self.root)
                    popup.title("WAGA Info Sec")
                    popup.geometry("600x400")
                    popup.configure(bg="#1F2833")
                    
                    tk.Label(popup, text=f"🔍 {data['titulo']}", bg="#1F2833", fg="#66FCF1", font=("Arial", 14, "bold")).pack(pady=10)
                    tk.Label(popup, text=f"Categoría OWASP: {data['owasp']}", bg="#1F2833", fg="#C5C6C7", font=("Arial", 10, "italic")).pack(pady=5)
                    
                    text_box = scrolledtext.ScrolledText(popup, bg="#0B0C10", fg="white", font=("Arial", 11), wrap=tk.WORD)
                    text_box.pack(expand=True, fill="both", padx=20, pady=10)
                    
                    text_box.insert(tk.END, f"⚠️ EL RIESGO REAL:\n{data['riesgo']}\n\n", "riesgo")
                    text_box.insert(tk.END, f"✅ CÓMO SOLUCIONARLO:\n{data['solucion']}", "solucion")
                    
                    text_box.tag_config("riesgo", foreground="#ff6b6b", font=("Arial", 11, "bold"))
                    text_box.tag_config("solucion", foreground="#1dd1a1", font=("Arial", 11, "bold"))
                    text_box.config(state=tk.DISABLED)
                    break
        except:
            pass

    def iniciar_escaneo(self):
        url = self.entrada_url.get().strip()
        if not url.startswith("http"):
            messagebox.showerror("Error", "La URL debe empezar con http:// o https://")
            return
        
        self.btn_escanear.config(state=tk.DISABLED)
        self.btn_reporte.config(state=tk.DISABLED)
        self.consola.delete(1.0, tk.END)
        self.nivel_riesgo = {"critico": 0, "medio": 0, "bajo": 0}
        
        threading.Thread(target=self.proceso_auditoria, args=(url,), daemon=True).start()

    def proceso_auditoria(self, url):
        dominio = urlparse(url).netloc
        puntaje = 100
        hallazgos = []

        self.log(f"Iniciando WAGA Pentest Automation para: {dominio}", "INFO")

        # 1. GEOIP & SPAMHAUS BLACKLIST (OSINT)
        self.progreso['value'] = 10
        self.log("Geolocalizando servidor y comprobando listas negras...", "INFO")
        try:
            ip_server = socket.gethostbyname(dominio)
            geo = requests.get(f"http://ip-api.com/json/{ip_server}", timeout=5).json()
            if geo['status'] == 'success':
                self.log(f"Servidor alojado en: {geo.get('country', '')} - {geo.get('isp', '')}", "PASS")
            
            # Spamhaus Check
            rev_ip = '.'.join(reversed(ip_server.split('.')))
            try:
                dns.resolver.resolve(f"{rev_ip}.zen.spamhaus.org", "A")
                self.log(f"IP en Lista Negra de Spamhaus ({ip_server})", "FAIL")
                hallazgos.append({"id": "BLACKLIST_SPAM", "msg": "Servidor catalogado como generador de SPAM."})
                puntaje -= 15
                self.nivel_riesgo["critico"] += 1
            except:
                self.log("IP limpia, no detectada en listas de SPAM.", "PASS")
        except: pass

        # 2. SUBDOMINIOS CRT.SH (Certificate Transparency)
        self.progreso['value'] = 25
        self.log("Rastreando subdominios reales en bases OSINT (crt.sh)...", "INFO")
        try:
            crt_req = requests.get(f"https://crt.sh/?q=%.{dominio}&output=json", timeout=10)
            if crt_req.status_code == 200:
                data = crt_req.json()
                subs = list(set([item['name_value'] for item in data if '*' not in item['name_value']]))
                if len(subs) > 1:
                    self.log(f"Se encontraron {len(subs)} subdominios reales (Ej: {subs[0]}, {subs[1]}).", "WARN")
                else:
                    self.log("No se expusieron subdominios externos.", "PASS")
        except:
            self.log("Timeout al consultar base de certificados públicos.", "WARN")

        # 3. WAF & CABECERAS (Con BUG corregido)
        self.progreso['value'] = 45
        self.log("Verificando WAF perimetral y defensas HTTP...", "INFO")
        try:
            res = requests.get(url, timeout=10, verify=False)
            
            # Convertimos headers a dict minúscula manual para evitar el error anterior
            headers = {k.lower(): v.lower() for k, v in res.headers.items()}
            
            # Analizar Server
            server_name = headers.get('server', '')
            powered_by = headers.get('x-powered-by', '')
            
            if 'cloudflare' in server_name or 'sucuri' in server_name:
                self.log("Protección WAF perimetral confirmada.", "PASS")
            else:
                self.log("Sin protección WAF detectada.", "WARN")
                hallazgos.append({"id": "MISSING_WAF", "msg": "Infraestructura vulnerable a ataques DDoS de capa 7."})
                puntaje -= 5
                self.nivel_riesgo["medio"] += 1

            if server_name != '' or powered_by != '':
                self.log(f"Fuga de información detectada: {server_name} {powered_by}", "FAIL")
                hallazgos.append({"id": "FUGA_INFO", "msg": f"El servidor expone tecnologías: {server_name} {powered_by}"})
                puntaje -= 5
                self.nivel_riesgo["medio"] += 1

            if 'content-security-policy' not in headers:
                self.log("Falta Política CSP defensiva", "FAIL")
                hallazgos.append({"id": "FALTA_CSP", "msg": "Cabecera CSP ausente, vulnerable a Cross-Site Scripting (XSS)."})
                puntaje -= 15
                self.nivel_riesgo["critico"] += 1

            # Scrapear emails para advertencia de Data Breach
            soup = BeautifulSoup(res.text, 'html.parser')
            emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", res.text.lower()))
            if emails:
                self.log(f"Correos expuestos públicamente: {list(emails)[0]}...", "WARN")
                hallazgos.append({"id": "EMAILS_EXPUESTOS", "msg": f"Posible brecha de empleados. Encontrados {len(emails)} correos."})
                self.nivel_riesgo["bajo"] += 1

        except Exception as e:
            self.log(f"Fallo conexión principal: {e}", "FAIL")

        # 4. PUERTOS CRÍTICOS Y DIRBUSTER MASIVO
        self.progreso['value'] = 65
        self.log("Escaneando Puertos y Directorios Ocultos (Fuerza Bruta)...", "INFO")
        for port in [21, 22, 3306, 3389]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                if s.connect_ex((dominio, port)) == 0:
                    self.log(f"PUERTO ABIERTO detectado: {port}", "FAIL")
                    hallazgos.append({"id": "PUERTO_CRITICO", "msg": f"El puerto {port} acepta conexiones externas."})
                    puntaje -= 10
                    self.nivel_riesgo["critico"] += 1
                s.close()
            except: pass

        rutas_ocultas = ["/.env", "/phpinfo.php", "/.git/config", "/db.sql", "/backup.zip", "/wp-config.php.bak"]
        for ruta in rutas_ocultas:
            try:
                r = requests.get(urljoin(url, ruta), timeout=2, verify=False)
                if r.status_code == 200 and len(r.text) > 0 and 'html' not in r.text[:20].lower():
                    self.log(f"Archivo sensible expuesto: {ruta}", "FAIL")
                    hallazgos.append({"id": "ARCHIVO_SENSIBLE", "msg": f"Ruta crítica encontrada: {ruta}"})
                    puntaje -= 20
                    self.nivel_riesgo["critico"] += 1
            except: pass

        # 5. DNS SPF/DMARC
        self.progreso['value'] = 85
        self.log("Verificando suplantación de identidad (DNS Phishing)...", "INFO")
        try:
            spf = False
            for r in dns.resolver.resolve(dominio, 'TXT'):
                if "v=spf1" in r.to_text(): spf = True
            if not spf:
                self.log("Faltan registros anti-phishing SPF.", "FAIL")
                hallazgos.append({"id": "FALTA_SPF_DMARC", "msg": "Dominio desprotegido contra envío de correos falsos."})
                puntaje -= 10
                self.nivel_riesgo["medio"] += 1
        except: pass

        # 6. SIMULACIÓN DE RATE LIMIT (Anti Fuerza Bruta)
        self.progreso['value'] = 95
        self.log("Simulando ataque DoS para probar Rate Limiting...", "INFO")
        try:
            bloqueado = False
            for _ in range(6):
                r_sim = requests.get(url, timeout=2, verify=False)
                if r_sim.status_code in [429, 403]: bloqueado = True
            
            if not bloqueado:
                self.log("Vulnerable a Fuerza Bruta (Sin Rate Limit).", "WARN")
                hallazgos.append({"id": "RATE_LIMIT", "msg": "El servidor permite peticiones infinitas sin bloquear."})
                puntaje -= 5
                self.nivel_riesgo["medio"] += 1
            else:
                self.log("Escudo Anti-Fuerza bruta activo.", "PASS")
        except: pass

        # --- FINALIZACIÓN ---
        self.progreso['value'] = 100
        puntaje = max(0, puntaje)
        
        # Generar Gráfico en Dashboard
        self.dibujar_grafico_riesgos()

        self.resultados = {
            "dominio": dominio, "puntaje": puntaje,
            "hallazgos": hallazgos, "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        self.log(f"\n{'='*50}\n✅ WAGA AUDIT COMPLETADA. SCORE: {puntaje}/100", "PASS")
        self.btn_escanear.config(state=tk.NORMAL)
        self.btn_reporte.config(state=tk.NORMAL)

    def dibujar_grafico_riesgos(self):
        self.canvas_chart.delete("all")
        total = sum(self.nivel_riesgo.values())
        if total == 0:
            self.canvas_chart.create_text(200, 200, text="SISTEMA SEGURO\nCero riesgos altos/medios", fill="#2ECC71", font=("Arial", 14, "bold"))
            return

        angulos = [
            (self.nivel_riesgo["critico"] / total) * 360,
            (self.nivel_riesgo["medio"] / total) * 360,
            (self.nivel_riesgo["bajo"] / total) * 360
        ]
        
        colores = ["#E74C3C", "#F39C12", "#3498DB"]
        etiquetas = [f"Crítico ({self.nivel_riesgo['critico']})", f"Medio ({self.nivel_riesgo['medio']})", f"Bajo ({self.nivel_riesgo['bajo']})"]
        
        start = 0
        for i in range(3):
            if angulos[i] > 0:
                self.canvas_chart.create_arc(50, 50, 350, 350, start=start, extent=angulos[i], fill=colores[i], outline="#0B0C10", width=3)
                start += angulos[i]
        
        # Leyenda
        self.canvas_chart.create_rectangle(10, 370, 25, 385, fill="#E74C3C")
        self.canvas_chart.create_text(35, 377, text=etiquetas[0], fill="white", anchor="w")
        self.canvas_chart.create_rectangle(150, 370, 165, 385, fill="#F39C12")
        self.canvas_chart.create_text(175, 377, text=etiquetas[1], fill="white", anchor="w")
        self.canvas_chart.create_rectangle(290, 370, 305, 385, fill="#3498DB")
        self.canvas_chart.create_text(315, 377, text=etiquetas[2], fill="white", anchor="w")

    def generar_reporte_html(self):
        if not self.resultados: return
        
        archivo = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML / Exportable a PDF", "*.html")])
        if not archivo: return

        r = self.resultados
        color_score = "#27ae60" if r['puntaje'] >= 80 else "#f39c12" if r['puntaje'] >= 50 else "#c0392b"

        # HTML Premium diseñado para exportar impecable a PDF
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>WAGA Security Audit - {r['dominio']}</title>
            <style>
                body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f8f9fa; color: #2c3e50; margin: 0; padding: 20px; }}
                .page {{ max-width: 900px; margin: auto; background: white; padding: 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
                .header {{ border-bottom: 4px solid #c0392b; padding-bottom: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; }}
                h1 {{ color: #2c3e50; font-size: 32px; margin: 0; }}
                .logo-text {{ font-size: 14px; color: #7f8c8d; text-transform: uppercase; letter-spacing: 2px; }}
                .score-box {{ background-color: {color_score}; color: white; text-align: center; padding: 30px; font-size: 38px; font-weight: 900; border-radius: 8px; margin-bottom: 40px; }}
                .vuln-item {{ border-left: 5px solid #c0392b; background: #fdfefe; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
                .vuln-title {{ font-size: 20px; font-weight: bold; color: #c0392b; margin: 0 0 10px 0; }}
                .owasp-tag {{ display: inline-block; background: #34495e; color: white; padding: 4px 10px; font-size: 12px; border-radius: 4px; margin-bottom: 15px; }}
                .vuln-content p {{ margin: 5px 0; line-height: 1.6; }}
                .print-btn {{ display: block; width: 100%; padding: 15px; background: #2980b9; color: white; text-align: center; text-decoration: none; font-size: 18px; font-weight: bold; margin-bottom: 20px; cursor: pointer; border: none; border-radius: 5px; }}
                @media print {{ .print-btn {{ display: none; }} body {{ background: white; }} .page {{ box-shadow: none; }} }}
            </style>
        </head>
        <body>
            <div class="page">
                <button class="print-btn" onclick="window.print()">🖨️ Guardar como PDF / Imprimir Documento</button>
                <div class="header">
                    <div>
                        <div class="logo-text">WAGA Security Enterprise</div>
                        <h1>Auditoría de Ciberseguridad</h1>
                        <p><strong>Objetivo Analizado:</strong> {r['dominio']}<br><strong>Fecha del Escaneo:</strong> {r['fecha']}</p>
                    </div>
                </div>

                <div class="score-box">
                    CALIFICACIÓN DE RIESGO: {r['puntaje']} / 100
                </div>

                <h2>Desglose de Vulnerabilidades (Plan de Remediación)</h2>
        """

        if not r['hallazgos']:
            html += "<p><strong>✅ Excelente. La infraestructura perimetral no presenta vulnerabilidades críticas obvias.</strong></p>"
        else:
            for h in r['hallazgos']:
                info = KNOWLEDGE_BASE.get(h['id'], {})
                owasp = info.get("owasp", "General Security")
                titulo = info.get("titulo", "Alerta Detectada")
                riesgo = info.get("riesgo", "Riesgo no catalogado.")
                solucion = info.get("solucion", "Revisar configuración.")
                
                html += f"""
                <div class="vuln-item">
                    <h3 class="vuln-title">{titulo}</h3>
                    <span class="owasp-tag">{owasp}</span>
                    <div class="vuln-content">
                        <p><strong>Fallo Técnico:</strong> {h['msg']}</p>
                        <p style="color: #c0392b;"><strong>Impacto Comercial:</strong> {riesgo}</p>
                        <p style="color: #27ae60;"><strong>Solución para TI:</strong> {solucion}</p>
                    </div>
                </div>
                """

        html += """
            </div>
        </body>
        </html>
        """

        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(html)
            messagebox.showinfo("Listo", "El reporte HTML ha sido generado.\n\nContiene un botón azul en la parte superior que te permitirá Guardarlo Directo como PDF al abrirlo en Chrome o Edge.")
        except Exception as e:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = WagaSecurityApp(root)
    root.mainloop()