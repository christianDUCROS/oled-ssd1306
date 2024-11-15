'''ouvrir paint, choisir un nouveau fichier, redimensionner l'image en 128 x 64 PIXELS  (Décocher 'conserver les proportions")'
Energister au format bmp (noir et blanc)
Copier l'image dans le réterptoire de ce script
Exécuter le script
puis copier/coller le résultat dans une variable qui sera traitée avec framebuf.FrameBuffer avant l'affichage avec blit  
'''
from PIL import Image

def load_bmp_as_bytearray(file_path):
    # Ouvrir l'image en mode monochrome (noir et blanc)
    image = Image.open(file_path).convert('1')  # Convertir en mode 1-bit
    width, height = image.size
    
    # Convertir les pixels en un bytearray
    pixels = bytearray()
    for y in range(height):
        byte = 0
        for x in range(width):
            # Récupérer la valeur du pixel (0 ou 255)
            pixel_value = image.getpixel((x, y))
            # Chaque pixel en noir (0) sera 1, chaque pixel en blanc (255) sera 0
            bit = 0 if pixel_value == 255 else 1
            # Mettre le bit au bon endroit dans l'octet courant
            byte = (byte << 1) | bit
            
            # Si on a atteint 8 bits, ajouter l'octet au bytearray
            if (x + 1) % 8 == 0:
                pixels.append(byte)
                byte = 0

        # Si la ligne n'est pas un multiple de 8 pixels, compléter avec des bits à 0
        if width % 8 != 0:
            byte = byte << (8 - (width % 8))
            pixels.append(byte)
    
    return pixels

def save_bytearray_to_txt(byte_array, output_file):
    # Écrire chaque octet sous forme \xXX dans le fichier
    with open(output_file, 'w') as file:
        file.write("bytearray(b'")
        for byte in byte_array:
            file.write(f"\\x{byte:02x}")
        file.write("')\n")
    print(f"Bytearray sauvegardé dans {output_file}")

# Exemple d'utilisation
nom_court = input ("saisir le nom de votre fichier image sans l'extension: ")
file_path = nom_court + '.bmp'
output_file = nom_court + '.txt'

# Charger l'image en bytearray
byte_array = load_bmp_as_bytearray(file_path)

# Sauvegarder le bytearray dans un fichier texte
save_bytearray_to_txt(byte_array, output_file)
