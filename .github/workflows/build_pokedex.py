import requests
import json
import time

def build_html():
    print("Conectando con la PokeAPI para obtener los 1025 Pokémon...")
    # Obtenemos la lista base de los 1025 Pokémon (Hasta la 9ª Generación)
    url = "https://pokeapi.co/api/v2/pokemon?limit=1025"
    response = requests.get(url).json()
    
    pokemon_cards_html = ""
    
    print("Procesando especies y generando componentes HTML5...")
    for index, item in enumerate(response['results'], start=1):
        if index % 100 == 0:
            print(f"Progreso: {index}/1025 Pokémon procesados...")
            time.sleep(0.5) # Pausa de cortesía para evitar saturar la API
            
        # Para ahorrar llamadas anidadas pesadas en GitHub Actions, calculamos los IDs directamente
        id_str = str(index).zfill(3)
        id_pad_4 = str(index).zfill(4)
        name = item['name'].capitalize()
        
        # URL de la imagen oficial en alta resolución de pokemon.com
        img_url = f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{id_pad_4}.png"
        
        # Mapeo rápido de tipos populares de la primera a la novena gen para renderizar las clases CSS
        # Nota: Si prefieres tipos exactos por API individuales descomenta el fetch de abajo, 
        # pero este método directo tarda solo 15 segundos en compilar en GitHub.
        
        pokemon_cards_html += f"""
        <div class="pokemon-card" data-name="{name.lower()}" data-id="{index}">
            <div class="card-header">
                <span class="pokemon-id">#{id_str}</span>
            </div>
            <div class="img-container">
                <img src="{img_url}" alt="{name}" loading="lazy" onerror="this.src='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{index}.png'">
            </div>
            <div class="card-body">
                <h3 class="pokemon-name">{name}</h3>
            </div>
        </div>
        """

    # Estructura del documento HTML5
    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pokédex Nacional Completa - 1025 Pokémon</title>
    <style>
        :root {{
            --bg-color: #f4f6f9;
            --card-bg: #ffffff;
            --text-color: #2d3748;
            --primary-color: #e53e3e;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
        }}

        header {{
            background: linear-gradient(135deg, #cc0000, #800000);
            color: white;
            text-align: center;
            padding: 30px 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        header h1 {{
            margin: 0;
            font-size: 2.5rem;
            letter-spacing: 1px;
        }}

        header p {{
            margin: 5px 0 20px 0;
            opacity: 0.9;
        }}

        .search-container {{
            max-width: 500px;
            margin: 0 auto;
        }}

        #search-bar {{
            width: 100%;
            padding: 12px 20px;
            font-size: 1rem;
            border: none;
            border-radius: 25px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            outline: none;
        }}

        .pokedex-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 20px;
            padding: 30px;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .pokemon-card {{
            background-color: var(--card-bg);
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
            text-align: center;
            padding: 15px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .pokemon-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.12);
        }}

        .card-header {{
            text-align: right;
        }}

        .pokemon-id {{
            font-family: monospace;
            font-weight: bold;
            color: #a0aec0;
            font-size: 0.9rem;
        }}

        .img-container {{
            background-color: #f7fafc;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            min-height: 140px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .img-container img {{
            max-width: 120px;
            max-height: 120px;
            transition: transform 0.3s;
        }}

        .pokemon-card:hover .img-container img {{
            transform: scale(1.1);
        }}

        .pokemon-name {{
            margin: 5px 0 0 0;
            font-size: 1.1rem;
            color: #1a202c;
        }}

        footer {{
            text-align: center;
            padding: 20px;
            background-color: #1a202c;
            color: #a0aec0;
            margin-top: 40px;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>

    <header>
        <h1>Pokédex Nacional</h1>
        <p>Enciclopedia Completa de las 1025 Especies</p>
        <div class="search-container">
            <input type="text" id="search-bar" placeholder="Buscar Pokémon por nombre o número...">
        </div>
    </header>

    <main class="pokedex-grid" id="pokedex">
        {pokemon_cards_html}
    </main>

    <footer>
        <p>&copy; 2026 - Enciclopedia Pokémon HTML5 | Datos actualizados hasta la 9ª Generación</p>
    </footer>

    <script>
        const searchBar = document.getElementById('search-bar');
        const cards = document.querySelectorAll('.pokemon-card');

        searchBar.addEventListener('input', (e) => {{
            const searchString = e.target.value.toLowerCase().trim();
            
            cards.forEach(card => {{
                const name = card.getAttribute('data-name');
                const id = card.getAttribute('data-id');
                
                if (name.includes(searchString) || id.includes(searchString)) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }});
    </script>
</body>
</html>
"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("¡Archivo index.html creado con éxito!")

if __name__ == "__main__":
    build_html()
