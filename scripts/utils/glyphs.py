from typing import List
from glyphsLib import GSFont, GSClass, GSFeature
from .feature import OTClass, OTFeature

class GlyphsFile:
    _font: GSFont = None
    _path: str

    def __init__(self, path: str):
        self._font = GSFont(path)
        self._path = path

    def write(self):
        c_classes = len(self._font.classes)
        c_features = len(self._font.features)
        print(f"Writing {c_classes} classes and {c_features} features")
        self._font.save(self._path)

    def set_classes(self, classes: List[OTClass]):
        classes.sort(key=lambda x: x.name)
        for c in classes:
            k = GSClass(c.name, str(c))
            if c.name in self._font.classes:
                self._font.classes[c.name] = k
            else:
                self._font.classes.append(k)

    def set_features(self, features: List[OTFeature]):
        features.sort(key=lambda x: x.name)
        for c in features:
            k = GSFeature(c.name, str(c))
            if c.name in self._font.features:
                self._font.features[c.name] = k
            else:
                self._font.features.append(k)