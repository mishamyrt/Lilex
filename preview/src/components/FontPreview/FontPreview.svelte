<script lang="ts">
  import { afterUpdate } from 'svelte'
  import { handleKeys, setCursor } from './keys-utils'
  import { INDENT, INDENT_SIZE, formatIndent, predictIndent } from './indent-utils'

  export let value = ''
  export let size: number
  export let weight: number
  export let features: string[]

  let ref: HTMLTextAreaElement
  let height: number

  function refreshHeight () {
    if (!ref) return
    ref.style.height = '0'
    height = ref.scrollHeight
    ref.style.height = ''
  }

  function handleKeyDown (e: KeyboardEvent & { currentTarget: EventTarget & HTMLTextAreaElement; }) {
    handleKeys(e, {
      Tab: () => {
        const start = ref.selectionStart
        const end = ref.selectionEnd

        value = value.substring(0, start) + INDENT + value.substring(end)
        setCursor(ref, start + INDENT_SIZE)
      },
      Enter: () => {
        const start = ref.selectionStart
        const end = ref.selectionEnd
        const size = predictIndent(ref)
        const indent = formatIndent(size)
        value = value.substring(0, start) + '\n' + indent + value.substring(end)
        setCursor(ref, start + 1 + indent.length)
      }
    })
  }

  afterUpdate(refreshHeight)

  $: size && refreshHeight()
  $: featureString = features
    .map(v => `"${v}"`)
    .join(', ')
</script>

<textarea
  class="preview"
  spellcheck="false"
  style:--preview-size="{size}px"
  style:--preview-height="{height}px"
  style:--preview-weight={weight}
  style:--preview-features={featureString}
  bind:this={ref}
  bind:value
  on:keydown={handleKeyDown}
/>

<style lang="scss">
  .preview {
    font-family: var(--font-family);
    font-size: var(--preview-size);
    font-weight: var(--preview-weight);
    font-feature-settings: var(--preview-features);
    height: var(--preview-height);

    overflow-y: hidden;
    flex: 1;
    color: var(--color-content);
    transition: color var(--transition-default);
    background-color: transparent;
    width: 100%;
    margin: 0 auto;
    resize: none;
    border: none;
    line-height: 1.2;

    &:focus {
      outline: none;
    }
  }
</style>
