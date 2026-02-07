import json
import os

def fix_sistema_completo():
    ruta_json = 'productos.json'
    
    if not os.path.exists(ruta_json):
        print("❌ No se encontró productos.json")
        return

    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            productos = json.load(f)

        print(f"🔍 Iniciando auditoría de {len(productos)} productos...")

        # --- 1. FILTRAR HUÉRFANOS (Si no hay foto, se va) ---
        productos_validos = []
        for p in productos:
            ruta_foto = p['img'].replace("./", "")
            if os.path.exists(ruta_foto):
                productos_validos.append(p)
            else:
                print(f"🗑️ Eliminando del JSON: {p['nombre']} (Foto no encontrada)")

        # --- 2. ORDENAR POR CATEGORÍA ---
        # Esto agrupa los productos para que los IDs salgan en orden
        productos_validos.sort(key=lambda x: (x['categoria'].upper(), x['nombre'].upper()))

        # --- 3. REASIGNAR IDs PROFESIONALES ---
        conteo_cat = {}
        for p in productos_validos:
            # Limpiamos la categoría para el prefijo (Ej: "SALA" -> "SALA")
            cat_clean = p['categoria'].strip().upper().replace(" ", "_")
            if not cat_clean: cat_clean = "VARIOS"
            
            if cat_clean not in conteo_cat:
                conteo_cat[cat_clean] = 1
            else:
                conteo_cat[cat_clean] += 1
            
            # Generamos ID tipo: SALA-001, ROPA-012
            # Tomamos las primeras 4 letras de la categoría como prefijo
            prefijo = cat_clean[:4]
            p['id'] = f"{prefijo}-{conteo_cat[cat_clean]:03d}"

        # --- 4. GUARDAR CAMBIOS ---
        with open(ruta_json, 'w', encoding='utf-8') as f:
            json.dump(productos_validos, f, indent=4, ensure_ascii=False)
            
        print(f"✅ ¡Auditoría terminada! {len(productos_validos)} productos en orden total.")

    except Exception as e:
        print(f"❌ Error crítico en el fix: {e}")

if __name__ == "__main__":
    fix_sistema_completo()