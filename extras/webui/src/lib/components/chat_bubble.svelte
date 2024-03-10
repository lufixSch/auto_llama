<script lang="ts">
	import { Roles } from '$lib/chats';
	import { cn } from '$lib/utils/cn';

	import markdownit from 'markdown-it';
	import markdownitLatex from 'markdown-it-katex';
	import { createEventDispatcher } from 'svelte';

	export let role: Roles;
	export let content: string;

	let onDelete = createEventDispatcher();
	let onBranch = createEventDispatcher();

	let openActions = false;

	const md = markdownit();
	md.use(markdownitLatex);
	let formattedContent = md.render(content);

	$: formattedContent = md.render(content);
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<section
	class={cn('group flex flex-row', {
		'justify-end': role === Roles.user,
		'justify-start': role === Roles.assistant
	})}
>
	<div
		class={cn('w-full md:w-5/6 py-2 px-4 rounded-lg', {
			'bg-amber-500 dark:bg-amber-600': role === Roles.user,
			'bg-zinc-200 dark:bg-zinc-700': role === Roles.assistant
		})}
		on:click={(e) => (openActions = !openActions)}
	>
		{@html formattedContent}
	</div>
	<div class={cn('actions collapse flex self-start', { visible: openActions })}>
		<button type="button" class="group/button" on:click={(e) => onDelete('delete')}>
			<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
				><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
					d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"
				/></svg
			>
		</button>
		<button type="button" class="group/button" on:click={() => onBranch('branch')}>
			<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
				><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
					d="M80 104a24 24 0 1 0 0-48 24 24 0 1 0 0 48zm80-24c0 32.8-19.7 61-48 73.3v87.8c18.8-10.9 40.7-17.1 64-17.1h96c35.3 0 64-28.7 64-64v-6.7C307.7 141 288 112.8 288 80c0-44.2 35.8-80 80-80s80 35.8 80 80c0 32.8-19.7 61-48 73.3V160c0 70.7-57.3 128-128 128H176c-35.3 0-64 28.7-64 64v6.7c28.3 12.3 48 40.5 48 73.3c0 44.2-35.8 80-80 80s-80-35.8-80-80c0-32.8 19.7-61 48-73.3V352 153.3C19.7 141 0 112.8 0 80C0 35.8 35.8 0 80 0s80 35.8 80 80zm232 0a24 24 0 1 0 -48 0 24 24 0 1 0 48 0zM80 456a24 24 0 1 0 0-48 24 24 0 1 0 0 48z"
				/></svg
			>
		</button>
	</div>
</section>

<style lang="postcss">
	.group:hover .actions {
		visibility: visible;
	}
</style>
