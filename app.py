# # from flask import Flask, render_template, request, jsonify, send_file
# # from PIL import Image, ImageDraw, ImageFont
# # import os
# # import random
# # import sqlite3
# # from io import BytesIO
# # import requests

# # app = Flask(__name__)
# # app.config['UPLOAD_FOLDER'] = 'fonts'
# # DATABASE = 'database.db'

# # # Google Fonts handwriting styles with direct TTF links
# # HANDWRITING_FONTS = {
# #     "Dancing Script": "https://fonts.gstatic.com/s/dancingscript/v25/If2cXTr6YS-zF4S-kcSWSVi_sxjsohD9F50Ruu7BMSoHTeB9ptDqpw.ttf",
# #     "Caveat": "https://fonts.gstatic.com/s/caveat/v18/WnznHAc5bAfYB2QRah7pcpNvOx-pjfJ9SIKjYBxPigs.ttf",
# #     "Satisfy": "https://fonts.gstatic.com/s/satisfy/v17/rP2Hp2yn6lkG50LoOZSCHBeHFl0.ttf",
# #     "Pacifico": "https://fonts.gstatic.com/s/pacifico/v22/FwZY7-Qmy14u9lezJ-6H6MmBp0u-.ttf",
# #     "Zeyada": "https://fonts.gstatic.com/s/zeyada/v16/11hAGpPTxVPUbgZDNGatWKaZ3g.ttf",
# #     "Kalam": "https://fonts.gstatic.com/s/kalam/v16/YA9dr0Wd4kDdMuhWMibDszkB.ttf",
# #     "Shadows Into Light": "https://fonts.gstatic.com/s/shadowsintolight/v19/UqyNK9UOIntux_czAvDQx_ZcHqZXBNQzdcD55_E.ttf",
# #     "Patrick Hand": "https://fonts.gstatic.com/s/patrickhand/v20/LDI2apCSOBg7S-QT7q4AOeekWkvZ.ttf",
# #     "Indie Flower": "https://fonts.gstatic.com/s/indieflower/v21/m8JVjfNVeKWVnh3QMuKkFcZVaUuH.ttf",
# #     "Amatic SC": "https://fonts.gstatic.com/s/amaticsc/v26/TUZ3zwprpvBS1izr_vOMscDJeZBpbh8.ttf"
# # }

# # def get_db():
# #     conn = sqlite3.connect(DATABASE)
# #     return conn

# # def init_db():
# #     with app.app_context():
# #         db = get_db()
# #         cursor = db.cursor()
# #         cursor.execute('''
# #             CREATE TABLE IF NOT EXISTS generated_images (
# #                 id INTEGER PRIMARY KEY AUTOINCREMENT,
# #                 filename TEXT,
# #                 font_used TEXT,
# #                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# #             )
# #         ''')
# #         db.commit()

# # def download_font(font_name):
# #     """Download a Google Font TTF file"""
# #     if font_name not in HANDWRITING_FONTS:
# #         return None
        
# #     font_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{font_name.replace(' ', '_')}.ttf")
    
# #     if os.path.exists(font_path):
# #         return font_path
    
# #     try:
# #         response = requests.get(HANDWRITING_FONTS[font_name], timeout=10)
# #         response.raise_for_status()
        
# #         os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# #         with open(font_path, 'wb') as f:
# #             f.write(response.content)
        
# #         return font_path
# #     except Exception as e:
# #         print(f"Error downloading font: {str(e)}")
# #         return None

# # @app.route('/')
# # def index():
# #     return render_template('index.html', fonts=list(HANDWRITING_FONTS.keys()))

# # @app.route('/generate', methods=['POST'])
# # def generate_handwriting():
# #     data = request.json
# #     text = data.get('text', '').strip()
# #     font_name = data.get('font', 'Dancing Script')
# #     font_size = int(data.get('fontSize', 32))
# #     line_spacing = float(data.get('lineSpacing', 1.5))
# #     ink_color = data.get('inkColor', '#1a1a1a')
# #     paper_color = data.get('paperColor', '#ffffff')
# #     randomness = float(data.get('randomness', 0.3))
# #     pressure_var = float(data.get('pressureVar', 0.2))
    
# #     if not text:
# #         return jsonify({'error': 'Please enter some text to convert!'}), 400
    
# #     font_path = download_font(font_name)
# #     if not font_path or not os.path.exists(font_path):
# #         return jsonify({'error': 'Font not available. Please select a different font.'}), 400
    
# #     try:
# #         # Load font
# #         font = ImageFont.truetype(font_path, font_size)
        
# #         # Calculate image dimensions
# #         lines = text.split('\n')
# #         max_width = 0
# #         total_height = 0
# #         line_heights = []
        
# #         for line in lines:
# #             if line.strip():
# #                 bbox = font.getbbox(line)
# #                 line_width = bbox[2] - bbox[0]
# #                 line_height = bbox[3] - bbox[1]
# #             else:
# #                 line_width = 0
# #                 line_height = font_size
            
# #             max_width = max(max_width, line_width)
# #             line_heights.append(line_height)
# #             total_height += int(line_height * line_spacing)
        
# #         # Add margins
# #         margin = 50
# #         img_width = max_width + (margin * 2) + 100
# #         img_height = total_height + (margin * 2) + 100
        
# #         # Convert hex colors to RGB
# #         def hex_to_rgb(hex_color):
# #             hex_color = hex_color.lstrip('#')
# #             return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
# #         paper_rgb = hex_to_rgb(paper_color)
# #         ink_rgb = hex_to_rgb(ink_color)
        
# #         # Create image with paper color
# #         img = Image.new('RGBA', (img_width, img_height), (*paper_rgb, 255))
# #         draw = ImageDraw.Draw(img)
        
# #         # Add subtle paper texture
# #         for _ in range(img_width * img_height // 5000):
# #             x = random.randint(0, img_width - 1)
# #             y = random.randint(0, img_height - 1)
# #             gray = random.randint(240, 250)
# #             draw.point((x, y), (gray, gray, gray, 30))
        
# #         # Draw text with natural variations
# #         start_x = margin + random.randint(-10, 10)
# #         start_y = margin + random.randint(-10, 10)
        
# #         if randomness > 0:
# #             # Use advanced rendering with variations
# #             avg_line_height = sum(line_heights) / len(line_heights) if line_heights else font_size
# #             add_natural_variations(draw, text, font, start_x, start_y, 
# #                                  int(avg_line_height * line_spacing), 
# #                                  ink_rgb, randomness, pressure_var)
# #         else:
# #             # Simple rendering
# #             current_y = start_y
# #             for line in lines:
# #                 draw.text((start_x, current_y), line, font=font, fill=ink_rgb)
# #                 if line.strip():
# #                     bbox = font.getbbox(line)
# #                     line_height = bbox[3] - bbox[1]
# #                 else:
# #                     line_height = font_size
# #                 current_y += int(line_height * line_spacing)
        
# #         # Save image to bytes
# #         img_io = BytesIO()
# #         img.save(img_io, 'PNG')
# #         img_io.seek(0)
        
# #         return send_file(img_io, mimetype='image/png')
        
# #     except Exception as e:
# #         return jsonify({'error': f'Failed to generate handwriting: {str(e)}'}), 500

# # def add_natural_variations(draw, text, font, base_x, base_y, line_height, ink_rgb, randomness, pressure_var):
# #     """Add natural handwriting variations"""
# #     y_offset = 0
# #     lines = text.split('\n')
    
# #     for line_idx, line in enumerate(lines):
# #         if not line.strip():
# #             y_offset += line_height
# #             continue
        
# #         x_offset = 0
# #         current_y = base_y + y_offset
        
# #         # Add slight line slant
# #         line_slant = random.uniform(-0.02, 0.02) * randomness
        
# #         for char_idx, char in enumerate(line):
# #             if char == ' ':
# #                 x_offset += font.getbbox(' ')[2] + random.randint(-2, 3)
# #                 continue
            
# #             # Calculate character position with variations
# #             char_x = base_x + x_offset + random.uniform(-randomness * 3, randomness * 3)
# #             char_y = current_y + (char_idx * line_slant) + random.uniform(-randomness * 2, randomness * 2)
            
# #             # Simulate pen pressure by varying opacity
# #             opacity = max(180, min(255, int(255 - (pressure_var * random.uniform(0, 75)))))
# #             char_color = (*ink_rgb, opacity)
            
# #             # Draw character with variations
# #             draw.text((char_x, char_y), char, font=font, fill=char_color)
            
# #             # Update x offset
# #             char_width = font.getbbox(char)[2]
# #             x_offset += char_width + random.uniform(-1, 2)
        
# #         y_offset += line_height

# # if __name__ == '__main__':
# #     init_db()
# #     os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# #     app.run(debug=True)



# from flask import Flask, render_template, request, jsonify, send_file
# from PIL import Image, ImageDraw, ImageFont, ImageOps
# import os
# import random
# import sqlite3
# from io import BytesIO
# import requests
# import textwrap

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'fonts'
# app.config['TEMPLATE_FOLDER'] = 'templates'
# DATABASE = 'database.db'

# # Extended font collection with handwriting styles from Google Fonts and 1001fonts.com
# HANDWRITING_FONTS = {
#     # Google Fonts
#     "Dancing Script": "https://fonts.gstatic.com/s/dancingscript/v25/If2cXTr6YS-zF4S-kcSWSVi_sxjsohD9F50Ruu7BMSoHTeB9ptDqpw.ttf",
#     "Caveat": "https://fonts.gstatic.com/s/caveat/v18/WnznHAc5bAfYB2QRah7pcpNvOx-pjfJ9SIKjYBxPigs.ttf",
#     "Satisfy": "https://fonts.gstatic.com/s/satisfy/v17/rP2Hp2yn6lkG50LoOZSCHBeHFl0.ttf",
#     "Pacifico": "https://fonts.gstatic.com/s/pacifico/v22/FwZY7-Qmy14u9lezJ-6H6MmBp0u-.ttf",
#     "Zeyada": "https://fonts.gstatic.com/s/zeyada/v16/11hAGpPTxVPUbgZDNGatWKaZ3g.ttf",
#     "Kalam": "https://fonts.gstatic.com/s/kalam/v16/YA9dr0Wd4kDdMuhWMibDszkB.ttf",
#     "Shadows Into Light": "https://fonts.gstatic.com/s/shadowsintolight/v19/UqyNK9UOIntux_czAvDQx_ZcHqZXBNQzdcD55_E.ttf",
#     "Patrick Hand": "https://fonts.gstatic.com/s/patrickhand/v20/LDI2apCSOBg7S-QT7q4AOeekWkvZ.ttf",
#     "Indie Flower": "https://fonts.gstatic.com/s/indieflower/v21/m8JVjfNVeKWVnh3QMuKkFcZVaUuH.ttf",
#     "Amatic SC": "https://fonts.gstatic.com/s/amaticsc/v26/TUZ3zwprpvBS1izr_vOMscDJeZBpbh8.ttf",
    
#     # 1001fonts.com handwriting fonts
#     "Hello Honey": "https://www.1001fonts.com/download/font/hello-honey.regular.ttf",
#     "Little Day": "https://www.1001fonts.com/download/font/little-day.regular.ttf",
#     "Sweet Hipster": "https://www.1001fonts.com/download/font/sweet-hipster.regular.ttf",
#     "The Hand": "https://www.1001fonts.com/download/font/the-hand.regular.ttf",
#     "White Angelica": "https://www.1001fonts.com/download/font/white-angelica.regular.ttf",
#     "Signerica": "https://www.1001fonts.com/download/font/signerica.medium.ttf",
#     "Raksana": "https://www.1001fonts.com/download/font/raksana.regular.ttf",
#     "Journal": "https://www.1001fonts.com/download/font/journal.regular.ttf",
#     "Millionaire": "https://www.1001fonts.com/download/font/millionaire.regular.ttf",
#     "The Scientist": "https://www.1001fonts.com/download/font/the-scientist.regular.ttf"
# }

# # Notebook templates from Freepik (placeholder URLs - you should replace with actual template URLs)
# NOTEBOOK_TEMPLATES = {
#     "None": None,
#     "Lined Paper": "https://img.freepik.com/free-vector/blank-white-notepaper-design-vector_53876-161340.jpg",
#     "Yellow Notepad": "https://img.freepik.com/free-vector/yellow-note-paper-background_52683-28386.jpg",
#     "School Notebook": "https://img.freepik.com/free-vector/school-notebook-with-blue-cover_1308-42240.jpg",
#     "Sticky Note": "https://img.freepik.com/free-vector/realistic-sticky-notes_23-2148158381.jpg",
#     "Grid Paper": "https://img.freepik.com/free-vector/grid-paper-background_53876-95018.jpg",
#     "Vintage Paper": "https://img.freepik.com/free-vector/vintage-paper-texture_1194-6503.jpg",
#     "Coffee Stained Paper": "https://img.freepik.com/free-vector/coffee-stained-paper-texture_1194-6289.jpg"
# }

# def get_db():
#     conn = sqlite3.connect(DATABASE)
#     return conn

# def init_db():
#     with app.app_context():
#         db = get_db()
#         cursor = db.cursor()
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS generated_images (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 filename TEXT,
#                 font_used TEXT,
#                 template_used TEXT,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         ''')
#         db.commit()

# def download_font(font_name):
#     """Download a font TTF file"""
#     if font_name not in HANDWRITING_FONTS:
#         return None
        
#     font_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{font_name.replace(' ', '_')}.ttf")
    
#     if os.path.exists(font_path):
#         return font_path
    
#     try:
#         response = requests.get(HANDWRITING_FONTS[font_name], timeout=30)
#         response.raise_for_status()
        
#         os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#         with open(font_path, 'wb') as f:
#             f.write(response.content)
        
#         return font_path
#     except Exception as e:
#         print(f"Error downloading font {font_name}: {str(e)}")
#         return None

# def download_template(template_name):
#     """Download a notebook template"""
#     if template_name not in NOTEBOOK_TEMPLATES or NOTEBOOK_TEMPLATES[template_name] is None:
#         return None
        
#     template_path = os.path.join(app.config['TEMPLATE_FOLDER'], f"{template_name.replace(' ', '_')}.jpg")
    
#     if os.path.exists(template_path):
#         return template_path
    
#     try:
#         response = requests.get(NOTEBOOK_TEMPLATES[template_name], timeout=30)
#         response.raise_for_status()
        
#         os.makedirs(app.config['TEMPLATE_FOLDER'], exist_ok=True)
#         with open(template_path, 'wb') as f:
#             f.write(response.content)
        
#         return template_path
#     except Exception as e:
#         print(f"Error downloading template {template_name}: {str(e)}")
#         return None

# @app.route('/')
# def index():
#     return render_template('index.html', 
#                          fonts=list(HANDWRITING_FONTS.keys()),
#                          templates=list(NOTEBOOK_TEMPLATES.keys()))

# @app.route('/generate', methods=['POST'])
# def generate_handwriting():
#     data = request.json
#     text = data.get('text', '').strip()
#     font_name = data.get('font', 'Dancing Script')
#     font_size = int(data.get('fontSize', 32))
#     line_spacing = float(data.get('lineSpacing', 1.5))
#     ink_color = data.get('inkColor', '#1a1a1a')
#     paper_color = data.get('paperColor', '#ffffff')
#     randomness = float(data.get('randomness', 0.3))
#     pressure_var = float(data.get('pressureVar', 0.2))
#     template_name = data.get('template', 'None')
#     margin_left = int(data.get('marginLeft', 50))
#     margin_top = int(data.get('marginTop', 50))
#     word_spacing = float(data.get('wordSpacing', 1.0))
    
#     if not text:
#         return jsonify({'error': 'Please enter some text to convert!'}), 400
    
#     font_path = download_font(font_name)
#     if not font_path or not os.path.exists(font_path):
#         return jsonify({'error': 'Font not available. Please select a different font.'}), 400
    
#     try:
#         # Load font
#         font = ImageFont.truetype(font_path, font_size)
        
#         # Calculate image dimensions
#         lines = text.split('\n')
#         max_width = 0
#         total_height = 0
#         line_heights = []
        
#         for line in lines:
#             if line.strip():
#                 bbox = font.getbbox(line)
#                 line_width = bbox[2] - bbox[0]
#                 line_height = bbox[3] - bbox[1]
#             else:
#                 line_width = 0
#                 line_height = font_size
            
#             max_width = max(max_width, line_width)
#             line_heights.append(line_height)
#             total_height += int(line_height * line_spacing)
        
#         # Add margins
#         img_width = max_width + (margin_left * 2) + 100
#         img_height = total_height + (margin_top * 2) + 100
        
#         # Convert hex colors to RGB
#         def hex_to_rgb(hex_color):
#             hex_color = hex_color.lstrip('#')
#             return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
#         paper_rgb = hex_to_rgb(paper_color)
#         ink_rgb = hex_to_rgb(ink_color)
        
#         # Create image with paper color
#         img = Image.new('RGBA', (img_width, img_height), (*paper_rgb, 255))
#         draw = ImageDraw.Draw(img)
        
#         # Add subtle paper texture if no template
#         if template_name == 'None':
#             for _ in range(img_width * img_height // 5000):
#                 x = random.randint(0, img_width - 1)
#                 y = random.randint(0, img_height - 1)
#                 gray = random.randint(240, 250)
#                 draw.point((x, y), (gray, gray, gray, 30))
#         else:
#             # Apply notebook template
#             template_path = download_template(template_name)
#             if template_path and os.path.exists(template_path):
#                 try:
#                     template = Image.open(template_path).convert('RGBA')
#                     # Resize template to match our image size
#                     template = template.resize((img_width, img_height))
#                     # Composite the template with our image
#                     img = Image.alpha_composite(img, template)
#                     draw = ImageDraw.Draw(img)
#                 except Exception as e:
#                     print(f"Error applying template: {str(e)}")
        
#         # Draw text with natural variations
#         start_x = margin_left + random.randint(-10, 10)
#         start_y = margin_top + random.randint(-10, 10)
        
#         if randomness > 0:
#             # Use advanced rendering with variations
#             avg_line_height = sum(line_heights) / len(line_heights) if line_heights else font_size
#             add_natural_variations(draw, text, font, start_x, start_y, 
#                                  int(avg_line_height * line_spacing), 
#                                  ink_rgb, randomness, pressure_var, word_spacing)
#         else:
#             # Simple rendering
#             current_y = start_y
#             for line in lines:
#                 draw.text((start_x, current_y), line, font=font, fill=ink_rgb)
#                 if line.strip():
#                     bbox = font.getbbox(line)
#                     line_height = bbox[3] - bbox[1]
#                 else:
#                     line_height = font_size
#                 current_y += int(line_height * line_spacing)
        
#         # Save image to bytes
#         img_io = BytesIO()
#         img.save(img_io, 'PNG')
#         img_io.seek(0)
        
#         return send_file(img_io, mimetype='image/png')
        
#     except Exception as e:
#         return jsonify({'error': f'Failed to generate handwriting: {str(e)}'}), 500

# def add_natural_variations(draw, text, font, base_x, base_y, line_height, ink_rgb, randomness, pressure_var, word_spacing):
#     """Add natural handwriting variations with improved word spacing"""
#     y_offset = 0
#     lines = text.split('\n')
    
#     for line_idx, line in enumerate(lines):
#         if not line.strip():
#             y_offset += line_height
#             continue
        
#         x_offset = 0
#         current_y = base_y + y_offset
        
#         # Add slight line slant
#         line_slant = random.uniform(-0.02, 0.02) * randomness
        
#         # Split line into words for better word spacing
#         words = line.split(' ')
        
#         for word_idx, word in enumerate(words):
#             if not word:
#                 continue
                
#             # Add space between words (except first word)
#             if word_idx > 0:
#                 space_width = font.getbbox(' ')[2] * word_spacing
#                 x_offset += space_width + random.uniform(-2, 3)
            
#             for char_idx, char in enumerate(word):
#                 # Calculate character position with variations
#                 char_x = base_x + x_offset + random.uniform(-randomness * 3, randomness * 3)
#                 char_y = current_y + (char_idx * line_slant) + random.uniform(-randomness * 2, randomness * 2)
                
#                 # Simulate pen pressure by varying opacity
#                 opacity = max(180, min(255, int(255 - (pressure_var * random.uniform(0, 75)))))
#                 char_color = (*ink_rgb, opacity)
                
#                 # Draw character with variations
#                 draw.text((char_x, char_y), char, font=font, fill=char_color)
                
#                 # Update x offset
#                 char_width = font.getbbox(char)[2]
#                 x_offset += char_width + random.uniform(-1, 2)
        
#         y_offset += line_height

# if __name__ == '__main__':
#     init_db()
#     os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#     os.makedirs(app.config['TEMPLATE_FOLDER'], exist_ok=True)
#     app.run(debug=True)















from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import random
import sqlite3
from io import BytesIO
import requests
import math

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'fonts'
DATABASE = 'database.db'

# Expanded Google Fonts handwriting styles with direct TTF links
HANDWRITING_FONTS = {
    # Casual & Handwritten
    "Dancing Script": "https://fonts.gstatic.com/s/dancingscript/v25/If2cXTr6YS-zF4S-kcSWSVi_sxjsohD9F50Ruu7BMSoHTeB9ptDqpw.ttf",
    "Caveat": "https://fonts.gstatic.com/s/caveat/v18/WnznHAc5bAfYB2QRah7pcpNvOx-pjfJ9SIKjYBxPigs.ttf",
    "Kalam": "https://fonts.gstatic.com/s/kalam/v16/YA9dr0Wd4kDdMuhWMibDszkB.ttf",
    "Patrick Hand": "https://fonts.gstatic.com/s/patrickhand/v20/LDI2apCSOBg7S-QT7q4AOeekWkvZ.ttf",
    "Indie Flower": "https://fonts.gstatic.com/s/indieflower/v21/m8JVjfNVeKWVnh3QMuKkFcZVaUuH.ttf",
    "Shadows Into Light": "https://fonts.gstatic.com/s/shadowsintolight/v19/UqyNK9UOIntux_czAvDQx_ZcHqZXBNQzdcD55_E.ttf",
    "Homemade Apple": "https://fonts.gstatic.com/s/homemadeapple/v18/Qw3EZQFVECDrI2q789IhWQZmFWL6yhvS.ttf",
    "Covered By Your Grace": "https://fonts.gstatic.com/s/coveredbyyourgrace/v15/QGYwz-AZahWOJJI9kykWW9mD6opopoqXSOS0FgItq6bFIg.ttf",
    "Architects Daughter": "https://fonts.gstatic.com/s/architectsdaughter/v18/KtkxAKiDZI_td1Lkx62xHZHDtgO_Y-bvTYlg5g.ttf",
    "Coming Soon": "https://fonts.gstatic.com/s/comingsoon/v19/qWcuB6mzpYL7AJ2VfdQR1u-SUjjzsykh.ttf",
    "Schoolbell": "https://fonts.gstatic.com/s/schoolbell/v18/92zQtBhWNqBhGp0s2PXaFRRiQf7T.ttf",
    "Reenie Beanie": "https://fonts.gstatic.com/s/reeniebeanie/v16/z7NSdR76eDkaJKZJFkkjuvWxbP2_qoOgVao.ttf",
    "Just Another Hand": "https://fonts.gstatic.com/s/justanotherhand/v15/845CNN4-AJyIGvIou60a9w4elH6S7qX2.ttf",
    "Waiting for the Sunrise": "https://fonts.gstatic.com/s/waitingforthesunrise/v16/WBL1rFvOYl9CEv2i1mO6KUW8RKWJ2zoXoz5JsYZQ9h_ZYk5J.ttf",
    "Markerfield": "https://fonts.gstatic.com/s/markerfield/v15/Cn-6JtuGWZJKmThFCuOYONbFwI4MpJCvDZUXDGZ0.ttf",
    "Mountains of Christmas": "https://fonts.gstatic.com/s/mountainsofchristmas/v22/3y9w6a4zcCnn5X0FDyrKi2ZiuswkWJKiH_jwLwbAGTSw.ttf",
    "Kimberly": "https://fonts.gstatic.com/s/kimberly/v17/YeZaa-IoBz8cNIzWkrZUVr5.ttf",
    "Cedarville Cursive": "https://fonts.gstatic.com/s/cedarvillecursive/v17/yYL00g_a2veiudhUmxjo5VKkoqA-B_neJbBx.ttf",
    "Delius": "https://fonts.gstatic.com/s/delius/v15/PN_xRfK0pW_9e1rtYcI-jT3L_w.ttf",
    "Delius Swash Caps": "https://fonts.gstatic.com/s/deliusswashcaps/v19/oY1E8fPLr7v1EX3T3OsrOyNLvAMcY1jBHdFrXXBh.ttf",
    "Grand Hotel": "https://fonts.gstatic.com/s/grandhotel/v14/7Au7p_IgjDKdCRWuR1azpmQNEl0O.ttf",
    "Great Vibes": "https://fonts.gstatic.com/s/greatvibes/v14/RWmMoKWR9v4ksMfaWd_JN-XCg6UKBw.ttf",
    "Handlee": "https://fonts.gstatic.com/s/handlee/v16/-F6xfjBsISg9aMakDmr2yz3L_g.ttf",
    "Kristi": "https://fonts.gstatic.com/s/kristi/v20/uK_y4ricdeU6zwdRCh0TMv6EXQ.ttf",
    "La Belle Aurore": "https://fonts.gstatic.com/s/labelleaurore/v16/RrQIbot8-mNYKnGNDkWlocovHeIIG-eFNVmULg.ttf",
    "League Script": "https://fonts.gstatic.com/s/leaguescript/v16/CSR54zpSlumSWj9CGVsoBZdeaNfUcMwk.ttf",
    "Love Ya Like A Sister": "https://fonts.gstatic.com/s/loveyalikeasister/v16/R70EjzUBlOqPeouhFDfR80-0FhOqJubN-Be78nYMcg.ttf",
    "Loved by the King": "https://fonts.gstatic.com/s/lovedbytheking/v17/Gw6gwdP16VKoTm2boSdE0oFOVpnM8aEEE-vgcVNkTME.ttf",
    "Nanum Pen Script": "https://fonts.gstatic.com/s/nanumpenscript/v19/daaDSSYiLGqEal3MvdA_FOL_3FkN2z7-aMFCcTU.ttf",
    "Nothing You Could Do": "https://fonts.gstatic.com/s/nothingyoucoulddo/v15/oY1B8fbBpaP5OX3DtrRYf_Q2BPB1SnfZb0OJl1ol2Ymo.ttf",
    "Over the Rainbow": "https://fonts.gstatic.com/s/overtherainbow/v13/11haGoXG1k_HKhMLUWz7Mc7vvW5ulhSgqY0Y.ttf",
    "Pacifico": "https://fonts.gstatic.com/s/pacifico/v22/FwZY7-Qmy14u9lezJ-6H6MmBp0u-.ttf",
    "Permanent Marker": "https://fonts.gstatic.com/s/permanentmarker/v16/Fh4uPib9Iyv2ucM6pGQMWimMp004HaqIfrT5nlk.ttf",
    "Rock Salt": "https://fonts.gstatic.com/s/rocksalt/v18/MwQ0bhv11fWD6QsAVOZbsEk7hbBWrA.ttf",
    "Sacramento": "https://fonts.gstatic.com/s/sacramento/v13/buEzpo6gcdjy0EiZMBUG0CoV_NxLeiw.ttf",
    "Satisfy": "https://fonts.gstatic.com/s/satisfy/v17/rP2Hp2yn6lkG50LoOZSCHBeHFl0.ttf",
    "Sue Ellen Francisco": "https://fonts.gstatic.com/s/sueellenfrancisco/v16/wXK3E20CsoJ9j1DDkjHcQ5ZL8xRaxru9ropF2lqk.ttf",
    "Sunshiney": "https://fonts.gstatic.com/s/sunshiney/v24/LDIpapSCOBt_binc2NqYabkOJUCY.ttf",
    "Zeyada": "https://fonts.gstatic.com/s/zeyada/v16/11hAGpPTxVPUbgZDNGatWKaZ3g.ttf",
    "Amatic SC": "https://fonts.gstatic.com/s/amaticsc/v26/TUZ3zwprpvBS1izr_vOMscDJeZBpbh8.ttf"
}

# Paper templates
PAPER_TEMPLATES = {
    "blank": {
        "name": "Blank Paper",
        "lines": False,
        "color": "#ffffff",
        "texture": True
    },
    "lined": {
        "name": "Lined Paper",
        "lines": True,
        "line_color": "#b3d9ff",
        "line_height": 40,
        "color": "#ffffff",
        "texture": True
    },
    "notebook": {
        "name": "Notebook Paper",
        "lines": True,
        "line_color": "#d1e7dd",
        "line_height": 35,
        "color": "#fefefe",
        "texture": True,
        "margin": True,
        "margin_color": "#ff6b6b"
    },
    "college": {
        "name": "College Ruled",
        "lines": True,
        "line_color": "#e6f3ff",
        "line_height": 28,
        "color": "#ffffff",
        "texture": True,
        "margin": True,
        "margin_color": "#ff9999"
    },
    "wide": {
        "name": "Wide Ruled",
        "lines": True,
        "line_color": "#e6f3ff",
        "line_height": 45,
        "color": "#ffffff",
        "texture": True,
        "margin": True,
        "margin_color": "#ff9999"
    },
    "graph": {
        "name": "Graph Paper",
        "lines": False,
        "grid": True,
        "grid_size": 20,
        "grid_color": "#e6f3ff",
        "color": "#ffffff",
        "texture": True
    },
    "vintage": {
        "name": "Vintage Paper",
        "lines": True,
        "line_color": "#d4c5b9",
        "line_height": 38,
        "color": "#f5f1e8",
        "texture": True,
        "aged": True
    }
}

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generated_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                font_used TEXT,
                template_used TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

def download_font(font_name):
    """Download a Google Font TTF file"""
    if font_name not in HANDWRITING_FONTS:
        return None
        
    font_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{font_name.replace(' ', '_').replace('/', '_')}.ttf")
    
    if os.path.exists(font_path):
        return font_path
    
    try:
        response = requests.get(HANDWRITING_FONTS[font_name], timeout=10)
        response.raise_for_status()
        
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        with open(font_path, 'wb') as f:
            f.write(response.content)
        
        return font_path
    except Exception as e:
        print(f"Error downloading font: {str(e)}")
        return None

def create_paper_background(width, height, template_name):
    """Create paper background with lines/grid based on template"""
    template = PAPER_TEMPLATES.get(template_name, PAPER_TEMPLATES['blank'])
    
    # Convert hex colors to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    paper_rgb = hex_to_rgb(template['color'])
    img = Image.new('RGBA', (width, height), (*paper_rgb, 255))
    draw = ImageDraw.Draw(img)
    
    # Add paper texture
    if template.get('texture', False):
        for _ in range(width * height // 8000):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            if template.get('aged', False):
                # Vintage paper texture
                gray = random.randint(230, 245)
                draw.point((x, y), (gray - 20, gray - 10, gray - 15, 20))
            else:
                gray = random.randint(240, 250)
                draw.point((x, y), (gray, gray, gray, 15))
    
    # Add lines
    if template.get('lines', False):
        line_color = hex_to_rgb(template['line_color'])
        line_height = template['line_height']
        
        for y in range(80, height - 50, line_height):
            draw.line([(50, y), (width - 50, y)], fill=(*line_color, 180), width=1)
    
    # Add margin line
    if template.get('margin', False):
        margin_color = hex_to_rgb(template['margin_color'])
        margin_x = 120
        draw.line([(margin_x, 50), (margin_x, height - 50)], fill=(*margin_color, 150), width=2)
    
    # Add grid
    if template.get('grid', False):
        grid_color = hex_to_rgb(template['grid_color'])
        grid_size = template['grid_size']
        
        # Vertical lines
        for x in range(50, width - 50, grid_size):
            draw.line([(x, 50), (x, height - 50)], fill=(*grid_color, 120), width=1)
        
        # Horizontal lines
        for y in range(50, height - 50, grid_size):
            draw.line([(50, y), (width - 50, y)], fill=(*grid_color, 120), width=1)
    
    return img

def get_line_positions(template_name, start_y, height):
    """Get y positions for text lines based on template"""
    template = PAPER_TEMPLATES.get(template_name, PAPER_TEMPLATES['blank'])
    
    if not template.get('lines', False):
        return None
    
    line_height = template['line_height']
    positions = []
    
    for y in range(80, height - 50, line_height):
        if y >= start_y:
            positions.append(y - 8)  # Adjust to sit on line properly
    
    return positions

@app.route('/')
def index():
    return render_template('index.html', 
                         fonts=list(HANDWRITING_FONTS.keys()),
                         templates=PAPER_TEMPLATES)

@app.route('/generate', methods=['POST'])
def generate_handwriting():
    data = request.json
    text = data.get('text', '').strip()
    font_name = data.get('font', 'Dancing Script')
    font_size = int(data.get('fontSize', 32))
    line_spacing = float(data.get('lineSpacing', 1.5))
    ink_color = data.get('inkColor', '#1a1a1a')
    template_name = data.get('template', 'lined')
    randomness = float(data.get('randomness', 0.3))
    pressure_var = float(data.get('pressureVar', 0.2))
    
    if not text:
        return jsonify({'error': 'Please enter some text to convert!'}), 400
    
    font_path = download_font(font_name)
    if not font_path or not os.path.exists(font_path):
        return jsonify({'error': 'Font not available. Please select a different font.'}), 400
    
    try:
        # Load font
        font = ImageFont.truetype(font_path, font_size)
        
        # Calculate image dimensions
        lines = text.split('\n')
        max_width = 0
        
        for line in lines:
            if line.strip():
                bbox = font.getbbox(line)
                line_width = bbox[2] - bbox[0]
                max_width = max(max_width, line_width)
        
        # Set image dimensions
        margin = 100
        img_width = max(800, max_width + (margin * 2))
        
        # Calculate height based on template
        template = PAPER_TEMPLATES.get(template_name, PAPER_TEMPLATES['blank'])
        if template.get('lines', False):
            line_height = template['line_height']
            img_height = max(600, len(lines) * line_height + 200)
        else:
            img_height = max(600, len(lines) * int(font_size * line_spacing) + 200)
        
        # Create paper background
        img = create_paper_background(img_width, img_height, template_name)
        draw = ImageDraw.Draw(img)
        
        # Convert ink color to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        ink_rgb = hex_to_rgb(ink_color)
        
        # Get line positions for lined paper
        line_positions = get_line_positions(template_name, 80, img_height)
        
        # Draw text systematically on lines
        start_x = 150 if template.get('margin', False) else 80
        
        if template.get('lines', False) and line_positions:
            # Write on paper lines systematically
            write_on_lines(draw, text, font, start_x, line_positions, 
                          ink_rgb, randomness, pressure_var)
        else:
            # Free form writing
            start_y = 80
            write_free_form(draw, text, font, start_x, start_y, 
                          int(font_size * line_spacing), ink_rgb, randomness, pressure_var)
        
        # Save image to bytes
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        # Save to database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO generated_images (filename, font_used, template_used)
            VALUES (?, ?, ?)
        ''', (f"{font_name}_{template_name}.png", font_name, template_name))
        db.commit()
        
        return send_file(img_io, mimetype='image/png')
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate handwriting: {str(e)}'}), 500

def write_on_lines(draw, text, font, start_x, line_positions, ink_rgb, randomness, pressure_var):
    """Write text systematically on paper lines"""
    lines = text.split('\n')
    line_index = 0
    
    for text_line in lines:
        if line_index >= len(line_positions):
            break
            
        if not text_line.strip():
            line_index += 1
            continue
        
        y_pos = line_positions[line_index]
        x_offset = 0
        
        # Add slight line slant for realism
        line_slant = random.uniform(-0.01, 0.01) * randomness if randomness > 0 else 0
        
        for char_idx, char in enumerate(text_line):
            if char == ' ':
                x_offset += font.getbbox(' ')[2] + random.randint(-1, 2) if randomness > 0 else font.getbbox(' ')[2]
                continue
            
            # Calculate character position
            char_x = start_x + x_offset
            if randomness > 0:
                char_x += random.uniform(-randomness * 2, randomness * 2)
            
            char_y = y_pos + (char_idx * line_slant)
            if randomness > 0:
                char_y += random.uniform(-randomness * 1.5, randomness * 1.5)
            
            # Apply pressure variation
            if pressure_var > 0:
                opacity = max(180, min(255, int(255 - (pressure_var * random.uniform(0, 75)))))
                char_color = (*ink_rgb, opacity)
            else:
                char_color = ink_rgb
            
            # Draw character
            draw.text((char_x, char_y), char, font=font, fill=char_color)
            
            # Update x offset
            char_width = font.getbbox(char)[2]
            x_offset += char_width
            if randomness > 0:
                x_offset += random.uniform(-1, 2)
        
        line_index += 1

def write_free_form(draw, text, font, start_x, start_y, line_height, ink_rgb, randomness, pressure_var):
    """Write text in free form without lines"""
    lines = text.split('\n')
    current_y = start_y
    
    for line in lines:
        if not line.strip():
            current_y += line_height
            continue
        
        x_offset = 0
        
        # Add slight line slant
        line_slant = random.uniform(-0.01, 0.01) * randomness if randomness > 0 else 0
        
        for char_idx, char in enumerate(line):
            if char == ' ':
                x_offset += font.getbbox(' ')[2] + random.randint(-1, 2) if randomness > 0 else font.getbbox(' ')[2]
                continue
            
            # Calculate character position
            char_x = start_x + x_offset
            if randomness > 0:
                char_x += random.uniform(-randomness * 2, randomness * 2)
            
            char_y = current_y + (char_idx * line_slant)
            if randomness > 0:
                char_y += random.uniform(-randomness * 1.5, randomness * 1.5)
            
            # Apply pressure variation
            if pressure_var > 0:
                opacity = max(180, min(255, int(255 - (pressure_var * random.uniform(0, 75)))))
                char_color = (*ink_rgb, opacity)
            else:
                char_color = ink_rgb
            
            # Draw character
            draw.text((char_x, char_y), char, font=font, fill=char_color)
            
            # Update x offset
            char_width = font.getbbox(char)[2]
            x_offset += char_width
            if randomness > 0:
                x_offset += random.uniform(-1, 2)
        
        current_y += line_height

if __name__ == '__main__':
    init_db()
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)