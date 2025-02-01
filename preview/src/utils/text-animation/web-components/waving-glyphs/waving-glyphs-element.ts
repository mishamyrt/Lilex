import { WaveAnimator } from "./wave-animator";

export class WavingGlyphsElement extends HTMLElement {
	private animator!: WaveAnimator;
	private weightMin = 0;
	private weightMax = 0;
	private fillRatio = 0;
	private interval = 0;

	static observedAttributes = ["max", "min", "fill-ratio", "interval"];

	public attributeChangedCallback(name: string, _: string, newValue: string) {
		switch (name) {
			case "min":
				this.weightMin = parseInt(newValue, 10);
				break;
			case "max":
				this.weightMax = parseInt(newValue, 10);
				break;
			case "fill-ratio":
				this.fillRatio = parseFloat(newValue);
				break;
			case "interval":
				this.interval = parseInt(newValue, 10);
				break;
		}
	}

	public connectedCallback() {
		this.animator = new WaveAnimator(
			this,
			{
				min: this.weightMin,
				max: this.weightMax,
			},
			this.fillRatio,
			this.interval
		);

		const observer = new IntersectionObserver(([entry]) => {
			if (entry.isIntersecting) {
				this.animator.start();
			} else {
				this.animator.stop();
			}
		});
		observer.observe(this);
	}

	public setThrottling(throttling: boolean) {
		this.animator.setThrottle(throttling)
	}
}
