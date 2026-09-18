from PIL import Image,ImageOps
from pathlib import Path
for p in Path('site/assets').glob('*.webp'):
 if p.name.startswith('._'): continue
 im=ImageOps.exif_transpose(Image.open(p)).convert('RGB')
 w=1800 if '-large' in p.name else 800
 im.thumbnail((w,w))
 im.save(p,'WEBP',quality=85,method=6)
print('Images optimized')
