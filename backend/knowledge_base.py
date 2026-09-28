KNOWLEDGE_BASE = {
    "PUERTO_CRITICO": {
        "keyword": "PUERTO ABIERTO",
        "owasp": "A05:2021 - Configuración de Seguridad Defectuosa",
        "titulo": "Puertos Críticos Expuestos a Internet",
        "riesgo": "Un atacante ejecuta ataques de fuerza bruta en puertos como el 3306 (MySQL) o 21 (FTP) para secuestrar la base de datos con Ransomware.",
        "solucion": "Bloquear el tráfico externo hacia estos puertos en el firewall del servidor y permitir solo conexiones locales (127.0.0.1)."
    },
    "FALTA_CSP": {
        "keyword": "Falta Política CSP",
        "owasp": "A03:2021 - Inyección",
        "titulo": "Ausencia de Content-Security-Policy (CSP)",
        "riesgo": "Permite ataques de Cross-Site Scripting (XSS). Un atacante inyecta scripts maliciosos para robar cookies de sesión de los usuarios.",
        "solucion": "Configurar la cabecera HTTP CSP en el servidor. Ejemplo: header(\"Content-Security-Policy: default-src 'self'\");"
    },
    "FALTA_SPF_DMARC": {
        "keyword": "Faltan registros anti-phishing",
        "owasp": "A08:2021 - Fallos en Software y Datos",
        "titulo": "Vulnerabilidad de Suplantación de Correo (Phishing)",
        "riesgo": "Un ciberdelincuente puede enviar correos falsos usando el dominio de la empresa (ej: gerencia@empresa.cl) para estafar a clientes.",
        "solucion": "Publicar registros TXT para SPF y DMARC en la zona DNS del dominio."
    },
    "FUGA_INFO": {
        "keyword": "Fuga de información",
        "owasp": "A05:2021 - Configuración Defectuosa",
        "titulo": "Fuga de Identidad del Servidor (Footprinting)",
        "riesgo": "Exponer versiones exactas del servidor (ej. PHP/LiteSpeed) facilita a los atacantes encontrar exploits públicos.",
        "solucion": "Remover cabeceras 'Server' y 'X-Powered-By' mediante configuración de servidor o código."
    },
    "MISSING_WAF": {
        "keyword": "Sin protección WAF",
        "owasp": "A05:2021 - Configuración Defectuosa",
        "titulo": "Sin Escudo WAF Perimetral",
        "riesgo": "El servidor queda expuesto a ataques de denegación de servicio (DDoS) e inyecciones automatizadas de capa 7.",
        "solucion": "Implementar un Proxy Inverso o WAF perimetral como Cloudflare."
    },
    "RATE_LIMIT": {
        "keyword": "Vulnerable a Fuerza Bruta",
        "owasp": "A07:2021 - Fallos de Identificación y Autenticación",
        "titulo": "Sin Limitación de Peticiones (Rate Limiting)",
        "riesgo": "Un atacante puede probar miles de combinaciones de credenciales por segundo sin ser bloqueado.",
        "solucion": "Implementar módulos de bloqueo automático de IP tras 5 intentos fallidos consecutuivos."
    }
}