import json
import os
import shutil

def super_aspiradora_hibrida():
    ruta_base = './img/'
    ruta_todo = './img/todo/'
    archivo_json = 'productos.json'
    
    # 1. Asegurar que la carpeta 'todo' exista
    if not os.path.exists(ruta_todo):
        os.makedirs(ruta_todo)

    # 2. Intentar cargar los productos.json actual
    try:
        with open(archivo_json, 'r', encoding='utf-8') as f:
            productos = json.load(f)
        print(f"📖 Catálogo cargado: {len(productos)} productos encontrados.")
    except Exception as e:
        print(f"⚠️ Error al leer JSON o está vacío. Iniciando nuevo. ({e})")
        productos = []

    # 3. SUCCIÓN Y MOVIMIENTO: Escanear todas las carpetas en /img/
    print("🔍 Buscando fotos nuevas en subcarpetas...")
    for raiz, carpetas, archivos in os.walk(ruta_base):
        # No procesar fotos que ya están en la carpeta 'todo'
        if 'todo' in raiz:
            continue
            
        for archivo in archivos:
            if archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                ruta_origen = os.path.join(raiz, archivo)
                ruta_destino = os.path.join(ruta_todo, archivo)
                
                # Si la foto no está en 'todo', la movemos para centralizar
                if not os.path.exists(ruta_destino):
                    shutil.move(ruta_origen, ruta_destino)
                    print(f"🚚 Movido a /todo/: {archivo}")
                else:
                    # Si ya existe en todo pero está duplicada afuera, borramos la de afuera
                    os.remove(ruta_origen)

    # 4. ACTUALIZACIÓN DE RUTAS INTELIGENTE
    # Obtenemos lista real de lo que hay en /todo/
    fotos_fisicas = os.listdir(ruta_todo)
    fotos_en_json = [os.path.basename(p['img']) for p in productos]

    for p in productos:
        nombre_archivo = os.path.basename(p['img'])
        # Si la foto existe en 'todo', actualizamos su ruta en el JSON automáticamente
        if nombre_archivo in fotos_fisicas:
            p['img'] = f"./img/todo/{nombre_archivo}"

    # 5. REGISTRO DE NUEVOS PRODUCTOS
    nuevos_cont = 0
    for foto in fotos_fisicas:
        if foto not in fotos_en_json:
            # Crear ID nuevo basado en el total
            nuevo_id = f"AUTO_{len(productos) + 1:03d}"
            nombre_limpio = foto.split('.')[0].replace('_', ' ').upper()
            
            nuevo_p = {
                "id": nuevo_id,
                "nombre": nombre_limpio,
                "precio": 0,
                "categoria": "general",
                "img": f"./img/todo/{foto}"
            }
            productos.append(nuevo_p)
            fotos_en_json.append(foto)
            nuevos_cont += 1
            print(f"✨ Nuevo hallazgo registrado: {nombre_limpio}")

    # 6. GUARDADO FINAL (Sin eliminar registros huérfanos)
    try:
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(productos, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*40)
        print(f"✅ ¡PROCESO COMPLETADO!")
        print(f"📦 Total en Catálogo: {len(productos)}")
        print(f"🆕 Nuevos agregados: {nuevos_cont}")
        print(f"📁 Todas las imágenes centralizadas en: {ruta_todo}")
        print("="*40)
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")

if __name__ == "__main__":
    super_aspiradora_hibrida()