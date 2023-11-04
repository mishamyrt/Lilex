<script lang="ts">
  import Toolbar from './Toolbar.svelte'
  import { isDark } from './theme-utils'

  export let dark: boolean = isDark()
</script>

<div
  class="block"
  class:dark
  role="presentation"
  on:mousemove
>
  <Toolbar>
    <slot name="toolbar" />
  </Toolbar>
  <slot />
</div>

<style lang="scss">
  .block {
    --color-content: var(--color-content-light);
    --color-content-dimmed: var(--color-content-dimmed-light);
    --color-accent: var(--color-accent-light);
    --color-background: var(--color-background-light);

    color-scheme: light;
    min-height: 100vh;
    padding: var(--padding-layout);
    background-color: var(--color-background);
    transition: background-color var(--transition-default);

    &.dark {
      --color-content: var(--color-content-dark);
      --color-content-dimmed: var(--color-content-dimmed-dark);
      --color-accent: var(--color-accent-dark);
      --color-background: var(--color-background-dark);

      color-scheme: dark;
    }
  }
</style>
