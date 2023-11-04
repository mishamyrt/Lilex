<script lang="ts">
	export let value: number
	export let min: number
	export let max: number
</script>

<div class="container">
	<span>{min}</span>
	<input type="range" bind:value={value} min={min} max={max}>
	<span>{max}</span>
</div>

<style>
	.container {
		max-width: 200px;
		font-size: 15px;
    display: flex;
    line-height: 16px;
    align-items: center;
    gap: 8px;
	}

  span {
    font-size: 15px;
    line-height: 16px;
    color: var(--color-content);
  }

	input[type=range] {
		position: relative;
		appearance: none;
		width: 100%;
		background: transparent;
	}

	input[type=range]::after {
		background-color: var(--color-content);
    opacity: 0.3;
		pointer-events: none;
		width: 100%;
		height: 1px;
		display: block;
		content: ' ';
		position: absolute;
		top: 5px;
		z-index: 11;
	}

	input[type=range]::-webkit-slider-thumb {
		-webkit-appearance: none;
		z-index: 12;
		position: relative;
		border: 1px solid var(--color-background);
		height: 12px;
		width: 12px;
		border-radius: 50px;
		background: var(--color-content);
		cursor: pointer;
	}
</style>
