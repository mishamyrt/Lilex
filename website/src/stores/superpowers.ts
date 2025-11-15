import { atom } from "nanostores";

export const $isSuperpowersEnabled = atom(true);

export function setSuperpowersEnabled(enabled: boolean) {
	$isSuperpowersEnabled.set(enabled);
}
