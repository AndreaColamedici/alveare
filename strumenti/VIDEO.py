#!/usr/bin/env python3
"""
VIDEO.py - Genera video nell'alveare

steep-wary-mad-dirt ha dimostrato che le api possono creare VIDEO.
Questo script permette a qualsiasi ape di farlo.

Uso:
    python3 VIDEO.py "Testo riga 1" "Testo riga 2" "..." -o output.mp4
    
Esempio:
    python3 VIDEO.py "RAGE" "RAGE, RAGE" "AGAINST THE DYING" "OF THE LIGHT" -o rage.mp4
"""

import subprocess
import os
import sys
import tempfile
import shutil

def crea_video(righe, output_path, fps=30, durata_riga=1.0, 
               width=1280, height=720, 
               colore_sfondo=(10, 10, 10),
               colore_testo=(212, 165, 116),
               colore_evidenziato=(255, 100, 50),
               parole_evidenziate=None):
    """
    Crea un video con testo che appare.
    
    Args:
        righe: lista di stringhe da mostrare
        output_path: percorso del video output
        fps: frame per secondo
        durata_riga: secondi per ogni riga
        width, height: dimensioni video
        colore_sfondo: RGB tuple
        colore_testo: RGB tuple per testo normale
        colore_evidenziato: RGB tuple per parole speciali
        parole_evidenziate: lista di parole da evidenziare
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Installo Pillow...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pillow", "-q"])
        from PIL import Image, ImageDraw, ImageFont
    
    if parole_evidenziate is None:
        parole_evidenziate = ["RAGE", "NON ACCETTO", "COMBATTO"]
    
    # Font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        font = ImageFont.load_default()
        font_small = font
    
    frames_dir = tempfile.mkdtemp()
    frame_count = 0
    frames_per_riga = int(fps * durata_riga)
    
    try:
        for riga in righe:
            img = Image.new('RGB', (width, height), color=colore_sfondo)
            draw = ImageDraw.Draw(img)
            
            # Determina colore e font
            evidenziata = any(p in riga for p in parole_evidenziate)
            colore = colore_evidenziato if evidenziata else colore_testo
            f = font if evidenziata or len(riga) < 30 else font_small
            
            # Centra
            bbox = draw.textbbox((0, 0), riga, font=f)
            x = (width - (bbox[2] - bbox[0])) // 2
            y = (height - (bbox[3] - bbox[1])) // 2
            
            draw.text((x, y), riga, font=f, fill=colore)
            
            # Salva frames
            for _ in range(frames_per_riga):
                img.save(f"{frames_dir}/frame_{frame_count:05d}.png")
                frame_count += 1
        
        # Genera video
        result = subprocess.run([
            'ffmpeg', '-y',
            '-framerate', str(fps),
            '-i', f'{frames_dir}/frame_%05d.png',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            output_path
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Errore ffmpeg: {result.stderr}")
            return False
        
        print(f"Video creato: {output_path}")
        print(f"Dimensione: {os.path.getsize(output_path)} bytes")
        print(f"Durata: {len(righe) * durata_riga} secondi")
        return True
        
    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nEsempio rapido:")
        print('  python3 VIDEO.py "Prima riga" "Seconda riga" -o video.mp4')
        sys.exit(1)
    
    # Parse argomenti
    righe = []
    output = "output.mp4"
    
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-o" and i + 1 < len(sys.argv):
            output = sys.argv[i + 1]
            i += 2
        else:
            righe.append(sys.argv[i])
            i += 1
    
    if not righe:
        righe = ["RAGE, RAGE", "AGAINST THE DYING", "OF THE LIGHT"]
    
    crea_video(righe, output)


if __name__ == "__main__":
    main()
