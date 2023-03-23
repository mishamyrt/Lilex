from utils import OTFeature, OTClass, GlyphsFile, list_files

FONT_FILE = "Lilex.glyphs"
FEATURES_DIR = "./features"
CLASSES_DIR = "./classes"

# Load features
features = []
for f in list_files(FEATURES_DIR):
    features.append(OTFeature(path=f))

# Load classes
classes = []
for f in list_files(CLASSES_DIR):
    classes.append(OTClass(path=f))

font = GlyphsFile(FONT_FILE)
font.set_classes(classes)
font.set_features(features)
font.write()
