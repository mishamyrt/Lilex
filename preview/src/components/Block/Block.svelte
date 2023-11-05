<script lang="ts">
  import { onDestroy, onMount } from 'svelte'
  import Toolbar from './Toolbar.svelte'
  import { isDark } from '$utils'

  export let dark: boolean = isDark()
  export let title = ''

  let observer: IntersectionObserver
  let titleRef: HTMLHeadingElement
  let titleInView = false

  onMount(() => {
    if (!titleRef) return
    observer = new IntersectionObserver(([entry]) => {
      titleInView = entry.intersectionRatio > 0
    }, {
      rootMargin: '-30%',
      threshold: 0,
    })
    observer.observe(titleRef)
  })

  onDestroy(() => {
    if (observer) {
      observer.disconnect()
    }
  })
</script>

<div
  class="block"
  class:dark
  role="presentation"
  on:mousemove
>
  {#if title.length > 0}
    <h2 class:inView={titleInView} bind:this={titleRef} class="title">{title}</h2>
  {/if}
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
    --color-background-overlay: var(--color-background-overlay-light);
    --color-background-overlay-active: var(--color-background-overlay-active-light);
    --color-background-dimmed: var(--color-background-dimmed-light);

    font-family: var(--font-family);
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
      --color-background-overlay: var(--color-background-overlay-dark);
      --color-background-overlay-active: var(--color-background-overlay-active-dark);
      --color-background-dimmed: var(--color-background-dimmed-dark);

      color-scheme: dark;
    }
  }

  .title {
    color: var(--color-content);
    font-size: 7vw;
    font-weight: 100;
    transition: font-weight var(--transition-default);
    margin: 50px 0 30px;

    &.inView {
      font-weight: 500;
    }
  }

  @media screen and (max-width: 992px) {
    .title {
      font-size: 70px;
    }
  }
</style>
