<script lang="ts">
	export let value
	export let min
	export let max
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
    color: var(--color-text);
  }

	input[type=range] {
		position: relative;
		appearance: none;
		width: 100%; /* Specific width is required for Firefox. */
		background: transparent; /* Otherwise white in Chrome */
	}

	input[type=range]::after {
		background-color: var(--color-text);
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

	/* Special styling for WebKit/Blink */
	/* input[type=range]::-moz-range-thumb, */
	input[type=range]::-webkit-slider-thumb {
		-webkit-appearance: none;
		z-index: 12;
		position: relative;
		border: 1px solid var(--color-background);
		height: 12px;
		width: 12px;
		border-radius: 50px;
		background: var(--color-text);
		cursor: pointer;
	}

</style>
