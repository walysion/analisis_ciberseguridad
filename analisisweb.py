import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import requests
import urllib3
from datetime import datetime

# Desactivar advertencias de certificados SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def auditar_sitio():
    url = entrada_url.get().strip()
    
    if not url.startswith("http"):
        messagebox.showwarning("Error", "La URL debe empezar con http:// o https://")
        return

    area_resultados.delete(1.0, tk.END)
    area_resultados.insert(tk.END, f"[*] AUDITORÍA INICIADA: {url}\n")
    area_resultados.insert(tk.END, f"[*] FECHA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    puntaje = 100 # Empezamos con 100 puntos estilo profesional
    problemas = []
    
    try:
        respuesta = requests.get(url, timeout=10, verify=False)
        cabeceras = respuesta.headers
        
        # 1. EVALUAR HTTPS
        if url.startswith("https"):
            area_resultados.insert(tk.END, "[PASS] Protocolo HTTPS activo.\n")
        else:
            area_resultados.insert(tk.END, "[FAIL] Protocolo HTTPS inactivo. Tráfico en texto plano.\n")
            puntaje -= 20
            problemas.append("CRÍTICO: El sitio no usa HTTPS. Los datos pueden ser interceptados.")

        # 2. FUGA DE INFORMACIÓN (Server / X-Powered-By)
        if 'Server' in cabeceras:
            area_resultados.insert(tk.END, f"[WARN] El servidor expone su identidad: {cabeceras['Server']}\n")
            puntaje -= 5
            problemas.append("MEDIO: Ocultar la cabecera 'Server' para no revelar tecnología al atacante.")
        if 'X-Powered-By' in cabeceras:
            area_resultados.insert(tk.END, f"[FAIL] Fuga de tecnología detectada: {cabeceras['X-Powered-By']}\n")
            puntaje -= 10
            problemas.append("ALTO: La cabecera 'X-Powered-By' revela el lenguaje (ej. PHP). Debe eliminarse.")

        # 3. CABECERAS DE SEGURIDAD DEFENSIVAS
        if 'X-Frame-Options' in cabeceras:
            area_resultados.insert(tk.END, f"[PASS] Protección Clickjacking activa ({cabeceras['X-Frame-Options']}).\n")
        else:
            area_resultados.insert(tk.END, "[FAIL] Vulnerable a Clickjacking (Falta X-Frame-Options).\n")
            puntaje -= 10
            problemas.append("ALTO: Implementar X-Frame-Options para evitar clonación visual.")

        if 'X-Content-Type-Options' in cabeceras:
            area_resultados.insert(tk.END, "[PASS] Protección MIME Sniffing activa.\n")
        else:
            area_resultados.insert(tk.END, "[FAIL] Vulnerable a MIME Sniffing (Falta X-Content-Type-Options).\n")
            puntaje -= 5
            problemas.append("MEDIO: Implementar X-Content-Type-Options: nosniff.")

        if 'Content-Security-Policy' in cabeceras:
            area_resultados.insert(tk.END, "[PASS] Política de Seguridad de Contenido (CSP) detectada.\n")
        else:
            area_resultados.insert(tk.END, "[FAIL] No se encontró Content-Security-Policy (CSP).\n")
            puntaje -= 15
            problemas.append("ALTO: Falta CSP. El sitio es muy vulnerable a inyección de scripts (XSS).")

        # 4. ANÁLISIS DE COOKIES
        if 'Set-Cookie' in cabeceras:
            cookie_data = cabeceras['Set-Cookie'].lower()
            area_resultados.insert(tk.END, "[INFO] Se detectaron cookies emitidas por el servidor.\n")
            
            if 'httponly' not in cookie_data:
                area_resultados.insert(tk.END, "  --> [FAIL] Falta bandera HttpOnly. Riesgo de robo por XSS.\n")
                puntaje -= 10
                problemas.append("CRÍTICO: Las cookies deben tener el atributo HttpOnly.")
            else:
                area_resultados.insert(tk.END, "  --> [PASS] Bandera HttpOnly detectada.\n")
                
            if 'secure' not in cookie_data:
                area_resultados.insert(tk.END, "  --> [FAIL] Falta bandera Secure. Cookies pueden viajar sin cifrar.\n")
                puntaje -= 10
                problemas.append("ALTO: Las cookies deben tener el atributo Secure.")
            else:
                area_resultados.insert(tk.END, "  --> [PASS] Bandera Secure detectada.\n")
        else:
            area_resultados.insert(tk.END, "[INFO] El servidor no emitió cookies en la respuesta inicial.\n")

        # GENERAR VEREDICTO
        puntaje = max(0, puntaje)
        area_resultados.insert(tk.END, "\n" + "="*50 + "\n")
        area_resultados.insert(tk.END, f"SCORE DE SEGURIDAD BÁSICA: {puntaje} / 100\n")
        area_resultados.insert(tk.END, "="*50 + "\n")
        
        if problemas:
            area_resultados.insert(tk.END, "\n[PLAN DE ACCIÓN SUGERIDO PARA EL CLIENTE]\n")
            for prob in problemas:
                area_resultados.insert(tk.END, f"- {prob}\n")
        else:
             area_resultados.insert(tk.END, "\n[+] ¡Excelente! La configuración básica de seguridad es muy sólida.\n")

        # Habilitar botón de guardado
        btn_guardar.config(state=tk.NORMAL)

    except requests.exceptions.RequestException as e:
        area_resultados.insert(tk.END, f"[!] Error de conexión: {e}\n")

def guardar_reporte():
    contenido = area_resultados.get(1.0, tk.END)
    if len(contenido.strip()) == 0:
        messagebox.showwarning("Aviso", "No hay resultados para guardar.")
        return
        
    archivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt")],
        title="Guardar Reporte de Seguridad"
    )
    
    if archivo:
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write("REPORTE DE AUDITORÍA DE SEGURIDAD WEB\n")
                f.write("Generado por Effectiva Security Scanner v2.0\n")
                f.write("-" * 50 + "\n\n")
                f.write(contenido)
            messagebox.showinfo("Éxito", f"Reporte guardado exitosamente en:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

# --- INTERFAZ GRÁFICA (GUI) ---
ventana = tk.Tk()
ventana.title("Scanner Profesional de Ciberseguridad v2.0")
ventana.geometry("700x600")
ventana.configure(bg="#1e1e1e")

tk.Label(ventana, text="URL del objetivo (ej. https://empresa.cl):", bg="#1e1e1e", fg="white", font=("Arial", 11, "bold")).pack(pady=10)

entrada_url = tk.Entry(ventana, width=60, font=("Arial", 12))
entrada_url.pack(pady=5)
entrada_url.insert(0, "https://")

# Frame para los botones
frame_botones = tk.Frame(ventana, bg="#1e1e1e")
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="🕵️ Iniciar Escaneo", bg="#d9534f", fg="white", font=("Arial", 10, "bold"), command=auditar_sitio, width=20).pack(side=tk.LEFT, padx=10)
btn_guardar = tk.Button(frame_botones, text="💾 Exportar Reporte", bg="#5cb85c", fg="white", font=("Arial", 10, "bold"), command=guardar_reporte, state=tk.DISABLED, width=20)
btn_guardar.pack(side=tk.LEFT, padx=10)

area_resultados = scrolledtext.ScrolledText(ventana, width=80, height=22, bg="#2d2d2d", fg="#00ff00", font=("Consolas", 10))
area_resultados.pack(pady=10)

ventana.mainloop()