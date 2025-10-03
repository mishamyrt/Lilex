import { atom } from "nanostores";

export const $isGlyphsItalicEnabled = atom(false);

export function setGlyphsItalicEnabled(enabled: boolean) {
	$isGlyphsItalicEnabled.set(enabled);
}

export const $glyphsWeight = atom(400);

export function setGlyphsWeight(weight: number) {
	$glyphsWeight.set(weight);
}
