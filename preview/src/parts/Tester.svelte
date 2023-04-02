<script lang="ts">
  import RangeSlider from '../components/RangeSlider.svelte'
  import SchemeSelect from '../components/SchemeSelect.svelte'
  import Toolbar from '../components/Toolbar.svelte'

  const minWeight = 100
  const maxWeight = 700
  const weightDiff = maxWeight - minWeight

  let value = 'Try it yourself\n>>-!-<<'
  let weight = 400
  let scheme: 'light' | 'dark' = 'light'
  let fontSize = 70

  function handleMouse (e: MouseEvent) {
    const position = e.clientX
    const percent = position / window.innerWidth
    weight = (percent * weightDiff) + minWeight
  }
</script>

<div class="container {scheme}">
    <Toolbar>
      <RangeSlider bind:value={fontSize} min={12} max={200} />
      <SchemeSelect bind:active={scheme} />
    </Toolbar>
    <textarea
      on:mousemove={handleMouse}
      bind:value={value}
      style:--font-size="{fontSize}px"
      style:--font-weight="{weight}"
      spellcheck="false"
    />
</div>

<style>
    .container {
      --color-text: var(--color-text-light);
      --color-background: var(--color-background-light);
      min-height: 100vh;

      padding: var(--padding-layout);
      background-color: var(--color-background);
      transition: background-color .3s ease-out;
    }

    .container.dark {
      --color-background: var(--color-background-dark);
      --color-text: var(--color-text-dark);
    }

    textarea {
        color: var(--color-text);
        transition: color .3s ease-out;
        background-color: transparent;
        font-size: var(--font-size);
        line-height: 1.2;
        font-family: var(--font-family);
        height: 100vh;
        width: 100%;
        margin: 0 auto;
        resize: none;
        border: none;
        font-weight: var(--font-weight, 100);
    }
    textarea:focus {
        outline: none;
    }
</style>
