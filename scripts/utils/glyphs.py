from typing import List
from glyphsLib import GSFont
from .feature import FeatureFile, ClassFile

class GlyphsFile:
    _font: GSFont = None
    _path: str

    def __init__(self, path: str):
        self._font = GSFont(path)
        self._path = path

    def glyphs_with_suffix(self, suf: str) -> List[str]:
        """Returns a list of glyph names that end with the specified string"""
        glyphs = []
        for g in self._font.glyphs:
            if g.name.endswith(suf):
                glyphs.append(g.name)
        return glyphs

    def write(self):
        c_classes = len(self._font.classes)
        c_features = len(self._font.features)
        print(f"Writing {c_classes} classes and {c_features} features")
        self._font.save(self._path)

    def set_classes(self, classes: List[ClassFile]):
        classes.sort(key=lambda x: x.name)
        for c in classes:
            if c.name in self._font.classes:
                self._font.classes[c.name] = c.GS()
            else:
                self._font.classes.append(c.GS())

    def set_features(self, features: List[FeatureFile]):
        features.sort(key=lambda x: x.name)
        for c in features:
            if c.name in self._font.features:
                self._font.features[c.name] = c.GS()
            else:
                self._font.features.append(c.GS())