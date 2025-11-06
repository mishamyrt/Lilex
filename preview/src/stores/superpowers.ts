import { atom } from "nanostores";

export const $isSuperpowersEnabled = atom(true);

export function setSuperpowersEnabled(enabled: boolean) {
	console.log("setSuperpowersEnabled", enabled);
	$isSuperpowersEnabled.set(enabled);
}
