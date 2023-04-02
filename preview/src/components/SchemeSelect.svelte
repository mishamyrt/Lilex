<script lang="ts">
  export let active: 'dark' | 'light' = 'dark'
</script>

<ul class="{active}">
  <li>
    <button
      class:active="{active === "light"}"
      class="light"
      on:click={() => { active = 'light' }} />
    <button
      class:active="{active === "dark"}"
      class="dark"
      on:click={() => { active = 'dark' }} />
  </li>
</ul>

<style>
  button {
    appearance: none;
    border: none;
    width: 16px;
    height: 16px;
    border-radius: 16px;
    border: 1px solid var(--color-outline);
  }

  button.light {
    background-color: var(--color-background-light);
  }

  button.dark {
    background-color: var(--color-background-dark);
  }

  ul {
    list-style-type: none;
    display: flex;
    gap: 8px;
    padding: 0;
    margin: 0;
  }

  ul.dark {
    --color-outline: rgba(223, 223, 223, 0.22);
    --color-outline-selected: rgba(223, 223, 223, 0.15);
  }

  ul.light {
    --color-outline: rgba(0, 0, 0, 0.20);
    --color-outline-selected: rgba(0, 0, 0, 0.14);
  }

  @media (prefers-color-scheme: dark) {
  :root {
    --color-text: var(--color-text-dark);
    --color-background: var(--color-background-dark);
  }
}
</style>
