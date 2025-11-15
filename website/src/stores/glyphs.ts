import { atom } from "nanostores";

export const $isGlyphsItalicEnabled = atom(false);

export function setGlyphsItalicEnabled(enabled: boolean) {
	$isGlyphsItalicEnabled.set(enabled);
}

export const $isGlyphsDuoEnabled = atom(false);

export function setGlyphsDuoEnabled(enabled: boolean) {
	$isGlyphsDuoEnabled.set(enabled);
}

$isGlyphsDuoEnabled.subscribe((enabled) => {
	if (enabled) {
		$isGlyphsItalicEnabled.set(false);
	}
});

export const $glyphsWeight = atom(300);

export function setGlyphsWeight(weight: number) {
	$glyphsWeight.set(weight);
}

export const $glyphsSize = atom(24);

export function setGlyphsSize(size: number) {
	$glyphsSize.set(size);
}
