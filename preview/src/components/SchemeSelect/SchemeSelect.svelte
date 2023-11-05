<script lang="ts">
  export let dark: boolean

  const handleDark = () => { dark = true }
  const handleLight = () => { dark = false }
</script>

<div class="selector">
  <button
    class:active={!dark}
    class="light"
    on:click={handleLight} />
  <button
    class:active={dark}
    class="dark"
    on:click={handleDark} />
</div>

<style lang="scss">
  button {
    cursor: pointer;
    transition: var(--transition-fast);
    appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 16px;
    border: 1px solid var(--color-content-dimmed);

    &.light {
      background-color: var(--color-background-light);
    }

    &.dark {
      background-color: var(--color-background-dark);
    }

    &.active {
      pointer-events: none;
    }
  }

  .selector {
    display: flex;
    gap: var(--space-s);
    padding: 0;
    margin: 0;
  }
</style>
