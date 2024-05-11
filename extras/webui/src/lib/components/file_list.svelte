<script lang="ts">
	import type { Article } from '$lib/auto_llama_sdk';
	import { cn } from '$lib/utils/cn';
	import { createEventDispatcher } from 'svelte';

	const dispatchEvent = createEventDispatcher();

	export let files: Article[] = [];
</script>

<ul class={cn('flex flex-wrap gap-1 list-none my-1', { hidden: !files.length })}>
	{#each files as file, index}
		<li>
			<button
				class="flex items-center rounded-full px-4 hover:bg-amber-600 dark:hover:bg-amber-500 transition duration-200"
				on:click={() => dispatchEvent('remove', index)}
			>
				<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"
					><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
						d="M320 464c8.8 0 16-7.2 16-16V160H256c-17.7 0-32-14.3-32-32V48H64c-8.8 0-16 7.2-16 16V448c0 8.8 7.2 16 16 16H320zM0 64C0 28.7 28.7 0 64 0H229.5c17 0 33.3 6.7 45.3 18.7l90.5 90.5c12 12 18.7 28.3 18.7 45.3V448c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V64z"
					/></svg
				>
				<p class="m-0 h-fit">{file.source}</p>
			</button>
		</li>
	{/each}
</ul>
