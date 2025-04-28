import { WeightAnimator, type WeightLimits } from "../../renderers/weight";

/**
 * Calculated shortest distance between two numbers between 0 and 1.
 */
function loopedDistance(a: number, b: number) {
	const forwardFront = Math.abs(a - b)
	return Math.min(forwardFront, 1 - forwardFront)
}

export class WaveAnimator extends WeightAnimator {
	private coordinates: number[];
	private isRunning = false;

	public throttling = false

	constructor(
		container: HTMLElement,
		limits: WeightLimits,
		private fillRatio: number,
		private interval: number
	) {
		super(container, limits);
		const coordinateStep = 1 / (this.elements.length + 1);
		this.coordinates = this.elements.map((_, i) => coordinateStep * (i + 1));
		this.onResize();
	}

	public onResize() {
		this.handleContainerResize();
	}

	public start() {
		requestAnimationFrame(this.drawFrame.bind(this))
		this.isRunning = true
	}

	public stop() {
		this.isRunning = false
	}

	public setThrottle(throttling: boolean) {
		this.throttling = throttling
	}

	private drawFrame(time: number = 0) {
		const progressCoordinate = (time % this.interval) / this.interval
		for (let i = 0; i < this.elements.length; i++) {
			const distance = loopedDistance(this.coordinates[i], progressCoordinate)
			this.setGlyphWeight(i, this.calculateWeight(distance));
		}
		if (!this.isRunning) {
			return
		}
		requestAnimationFrame(this.drawFrame.bind(this))
  }
	
	private calculateWeight(distance: number): number {
		if (distance > this.fillRatio) {
			return this.limits.min
		}
		const ratio = 1 - (distance / this.fillRatio);
		const weight = this.limits.min + (this.weightDelta * ratio)
		if (this.throttling) {
			return Math.round(weight / 100) * 100
		}
		return weight
	}
}
