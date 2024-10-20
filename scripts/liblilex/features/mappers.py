"""OpenType feature mappers"""
import sys

from glyphsLib import GSFeature

FeatureDict = dict[str, GSFeature]

def to_feature_dict(features: list[GSFeature]) -> FeatureDict:
    return {fea.name: fea for fea in features}

def from_feature_dict(feature_dict: FeatureDict) -> list[GSFeature]:
    return list(feature_dict.values())

def force_features(features: list[GSFeature], forced: list[str]):
    fea_dict = to_feature_dict(features)
    for fea in forced:
        if fea not in fea_dict:
            print(f"Unknown feature: '{fea}'")
            sys.exit(1)
        # Move the code of the feature to the calt,
        # which is executed in most cases
        fea_dict[fea].disabled = True
        fea_dict["calt"].code += "\n" + fea_dict[fea].code
        # Remove feature from aalt
        aalt = fea_dict["aalt"]
        aalt.code = aalt.code.replace(f"feature {fea};\n", "")
    return from_feature_dict(fea_dict)
