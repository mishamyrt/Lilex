from os.path import join
from utils import (
    FeatureFile,
    ClassFile,
    GlyphsFile,
    list_files,
    ligature_lookups
)

FONT_FILE = "Lilex.glyphs"
CLASSES_DIR = "./classes"
FEATURES_DIR = "./features"
CALT_DIR = join(FEATURES_DIR, "calt")

font = GlyphsFile(FONT_FILE)

# Find ligatures
ligatures = []
print("Ligatures:")
for ligature in font.glyphs_with_suffix(".liga"):
    name = ligature.split('.')[0]
    print(f" - {name}")
    ligatures.append(name)
ligatures.sort(key=lambda x: len(x.split('_')), reverse=True)

# Build calt feature
calt = FeatureFile(name="calt")
for f in list_files(CALT_DIR):
    calt.append_file(f)
calt.append(ligature_lookups(ligatures))

# Load features
features = [calt]
for f in list_files(FEATURES_DIR):
    features.append(FeatureFile(path=f))

# Load classes
classes = []
for f in list_files(CLASSES_DIR):
    classes.append(ClassFile(path=f))

font.set_classes(classes)
font.set_features(features)
font.write()