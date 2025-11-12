import { setProps, wrapChars } from "../nodes";

export type WeightLimits = {
	min: number;
	max: number;
};

const conditionalPx = (value: number | null) => (value ? `${value}px` : "");

export abstract class WeightAnimator {
	protected elements: HTMLElement[];
	private weights: number[];
	protected weightDelta: number;

	constructor(
		public readonly container: HTMLElement,
		protected readonly limits: WeightLimits,
	) {
		this.elements = wrapChars(container, "span");
		this.weights = this.elements.map(() => limits.min);
		this.weightDelta = limits.max - limits.min;
	}

	protected setGlyphWeight(i: number, weight: number) {
		if (this.weights[i] === weight) {
			return;
		}
		this.weights[i] = weight;
		this.elements[i].style.setProperty("--glyph-weight", weight.toString());
	}

	protected handleContainerResize(): DOMRect {
		// Get first glyph
		const glyph = this.elements[0];
		// Reset and update glyph size
		this.setGlyphsSize(0, 0);
		const glyphRect = glyph.getBoundingClientRect();
		this.setGlyphsSize(glyphRect.width, glyphRect.height);
		// Reset and update content size
		this.setContainerSize(0, 0);
		const containerRect = this.container.getBoundingClientRect();
		this.setContainerSize(containerRect.width, containerRect.height);
		return containerRect;
	}

	private setGlyphsSize(width: number, height: number) {
		setProps(this.container, {
			"--glyph-width": conditionalPx(width),
			"--glyph-height": conditionalPx(height),
		});
	}

	private setContainerSize(width: number, height: number) {
		setProps(this.container, {
			"--glyphsContainer-width": conditionalPx(width),
			"--glyphsContainer-height": conditionalPx(height),
		});
	}
}
