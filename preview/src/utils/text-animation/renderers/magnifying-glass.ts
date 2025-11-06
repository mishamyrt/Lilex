import { Coordinate, Rectangle, type CoordinatedEvent } from "../geometry";
import { WeightAnimator, type WeightLimits } from "./weight";

export class MagnifyingGlassAnimator extends WeightAnimator {
	private coordinates!: Coordinate[];
	private reactionRect!: Rectangle;

	constructor(
		container: HTMLElement,
		limits: WeightLimits,
		public reactionSize: number,
	) {
		super(container, limits);
		this.handleResize();
	}

	public handleResize() {
		const rect = this.handleContainerResize();
		this.reactionRect = Rectangle.fromDOMRect(rect);
		const reactionZoneSize = this.reactionSize * 1.5;
		this.reactionRect.expandBy(reactionZoneSize, reactionZoneSize);
		this.coordinates = this.elements.map(Coordinate.fromElement);
	}

	public handlePointerMove(event: CoordinatedEvent): void {
		for (let i = 0; i < this.coordinates.length; i++) {
			const distance = this.coordinates[i].distanceFromEvent(event);
			if (distance > this.reactionSize) {
				this.setGlyphWeight(i, this.limits.min);
			} else {
				this.setGlyphWeight(i, this.calculateWeight(distance));
			}
		}
	}

	public isInReactionZone(event: CoordinatedEvent): boolean {
		return this.reactionRect.contains(event);
	}

	private calculateWeight(distance: number): number {
		const ratio = Math.max(0, 1 - distance / this.reactionSize);
		return this.limits.min + this.weightDelta * ratio;
	}
}
