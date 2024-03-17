<script lang="ts">
	import { Roles } from '$lib/chats';
	import { cn } from '$lib/utils/cn';

	import markdownit from 'markdown-it';
	import markdownitLatex from 'markdown-it-katex';

	export let role: Roles;
	export let content: string;

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
</section>

<style lang="postcss">
	.group:hover .actions {
		visibility: visible;
	}
</style>
