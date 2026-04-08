import { atom } from "nanostores";

export interface Feature {
	name: string;
	code: string;
}

export const $features = atom<Feature[]>([]);
export const $textareaFeatures = atom<Record<string, string[]>>({});

export async function loadFeatures(): Promise<void> {
	if ($features.get().length > 0) return;
	const resp = await fetch("/opentype_features.json");
	const data: Feature[] = await resp.json();
	$features.set(data);
}

export function toggleFeature(textareaId: string, code: string): void {
	const current = $textareaFeatures.get();
	const enabled = current[textareaId] ?? [];
	const next = enabled.includes(code)
		? enabled.filter((c) => c !== code)
		: [...enabled, code];
	$textareaFeatures.set({ ...current, [textareaId]: next });
}

export function isFeatureEnabled(textareaId: string, code: string): boolean {
	const enabled = $textareaFeatures.get()[textareaId];
	return enabled?.includes(code) ?? false;
}

export function getFeatureSettings(textareaId: string): string {
	const enabled = $textareaFeatures.get()[textareaId];
	if (!enabled || enabled.length === 0) return '"liga"';
	return ['"liga"', ...enabled.map((c) => `"${c}"`)].join(", ");
}
