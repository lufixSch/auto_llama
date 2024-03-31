<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let className: string = '';
	export let type: 'submit' | 'reset' | 'button' = 'button';

	let click = createEventDispatcher();
</script>

<button
	{type}
	class={'rounded-lg bg-transparent transition duration-200 hover:bg-amber-600 dark:hover:bg-amber-500 active:bg-amber-600 dark:active:bg-amber-500 ' +
		className}
	on:click={(e) => click('click', e)}
>
	<slot />
</button>
