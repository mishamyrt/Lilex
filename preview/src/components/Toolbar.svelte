<div class="toolbar">
	<slot></slot>
</div>

<style>
  .toolbar {
    position: sticky;
    z-index: 10;
    top: 0;
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
    margin-top: -12px;
    padding: 12px 0;
    background-color: var(--color-background);
    transition: background-color .3s ease-out;
  }
</style>
