from imagekit.specs import ImageSpec
from imagekit import processors

class ResizeThumb(processors.Resize):
    width = 70
    height = 70
    crop = True
    
class ResizeDisplay(processors.Resize):
    width = 300

class EnchanceThumb(processors.Adjustment): 
    contrast = 1.2 
    sharpness = 1.1
    
class Thumbnail(ImageSpec):
    access_as = 'thumbnail_image'
    pre_cache = True
    processors = [ResizeThumb, ResizeDisplay]
    
class Display(ImageSpec):
    increment_count = True
    processors = [ResizeDisplay]
