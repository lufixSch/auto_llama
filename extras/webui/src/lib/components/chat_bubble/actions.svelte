<script lang="ts">
	import { Chat, Roles, type Message } from '$lib/chats';
	import { cn } from '$lib/utils/cn';
	import { swipe } from 'svelte-gestures';

	import markdownit from 'markdown-it';
	import markdownitLatex from 'markdown-it-katex';
	import { createEventDispatcher } from 'svelte';

	export let message: Message;
	export let branchPath: number[];
	export let chat: Chat;

	let textBlock: HTMLElement;
	let editable: boolean = false;

	let onDelete = createEventDispatcher();
	let onBranch = createEventDispatcher();
	let onSwitchBranch = createEventDispatcher();
	let onEdit = createEventDispatcher();

	let openActions = false;

	const fileElement = `<div class="flex items-center rounded-full px-2 break-normal break-all">
				<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"
					><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
						d="M320 464c8.8 0 16-7.2 16-16V160H256c-17.7 0-32-14.3-32-32V48H64c-8.8 0-16 7.2-16 16V448c0 8.8 7.2 16 16 16H320zM0 64C0 28.7 28.7 0 64 0H229.5c17 0 33.3 6.7 45.3 18.7l90.5 90.5c12 12 18.7 28.3 18.7 45.3V448c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V64z"
					/></svg
				>
				<p class="m-0 h-fit">{FILE_NAME}</p>
			</div>`;

	const md = markdownit({
		html: true,
		linkify: true,
		breaks: true
	});
	md.use(markdownitLatex);
	// let formattedContent = md.render(message.content);

	$: formattedContent = render(message.content);
	$: _index = message.branchStart.findIndex(
		(start) => start === branchPath.find((i) => message.branchStart.includes(i))
	);
	$: pathIndex = _index == -1 ? 1 : _index + 2;

	function handleStartEdit() {
		editable = true;
		requestAnimationFrame(() => textBlock.focus());
	}

	function handleStopEdit() {
		editable = false;
		formattedContent = render(message.content);
		onEdit('edit', message);
	}

	function render(content: string) {
		content = chat.replaceFileReferences(content, (id) => fileElement.replace('{FILE_NAME}', id));
		return md.render(content);
	}
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<section
	class={cn('group flex flex-row', {
		'justify-end': message.role === Roles.user,
		'justify-start': message.role === Roles.assistant
	})}
>
	<div
		on:click={handleStartEdit}
		on:focusout={handleStopEdit}
		on:blur={handleStopEdit}
		class={cn('w-full md:w-5/6 py-2 px-4 rounded-lg', {
			'bg-amber-500 dark:bg-amber-600 ': message.role === Roles.user,
			'bg-zinc-200 dark:bg-zinc-700 ': message.role === Roles.assistant
		})}
		use:swipe={{ touchAction: 'pan-y' }}
		on:swipe={(e) => {
			if (e.detail.direction == 'left') openActions = true;
			else if (e.detail.direction == 'right') openActions = false;
		}}
	>
		{#if editable}
			<p
				bind:this={textBlock}
				class="outline-none"
				bind:innerText={message.content}
				contenteditable
			></p>
		{:else}
			<div>{@html formattedContent}</div>
		{/if}
	</div>
	<div class={cn('actions hidden self-start flex-col', { flex: openActions })}>
		<div class="flex">
			<button type="button" class="group/button" on:click={(e) => onDelete('delete')}>
				<svg
					class="icon group-hover/button:fill-zinc-600 group-hover/button:dark:fill-zinc-400"
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 448 512"
					><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
						d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"
					/></svg
				>
			</button>
			<button type="button" class="group/button" on:click={() => onBranch('branch')}>
				<svg
					class="icon group-hover/button:fill-zinc-600 group-hover/button:dark:fill-zinc-400"
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 448 512"
					><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
						d="M80 104a24 24 0 1 0 0-48 24 24 0 1 0 0 48zm80-24c0 32.8-19.7 61-48 73.3v87.8c18.8-10.9 40.7-17.1 64-17.1h96c35.3 0 64-28.7 64-64v-6.7C307.7 141 288 112.8 288 80c0-44.2 35.8-80 80-80s80 35.8 80 80c0 32.8-19.7 61-48 73.3V160c0 70.7-57.3 128-128 128H176c-35.3 0-64 28.7-64 64v6.7c28.3 12.3 48 40.5 48 73.3c0 44.2-35.8 80-80 80s-80-35.8-80-80c0-32.8 19.7-61 48-73.3V352 153.3C19.7 141 0 112.8 0 80C0 35.8 35.8 0 80 0s80 35.8 80 80zm232 0a24 24 0 1 0 -48 0 24 24 0 1 0 48 0zM80 456a24 24 0 1 0 0-48 24 24 0 1 0 0 48z"
					/></svg
				>
			</button>
		</div>
		<div class="flex justify-center">
			{#if message.branchStart.length > 0}
				<button
					type="button"
					class="group/branch"
					disabled={pathIndex === 1}
					on:click={() =>
						onSwitchBranch('switch', pathIndex <= 2 ? 0 : message.branchStart[pathIndex - 2 - 1])}
					><svg
						class="w-[16px] h-[32px] py-[8px] fill-black dark:fill-white group-hover/branch:fill-zinc-600 group-hover/branch:dark:fill-zinc-400 group-disabled/branch:fill-zinc-300 group-disabled/branch:dark:fill-zinc-600"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 320 512"
						><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
							d="M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l192 192c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L77.3 256 246.6 86.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-192 192z"
						/></svg
					>
				</button>
				<div class="align-middle text-center text-sm font-bold leading-[32px]">
					{pathIndex} / {message.branchStart.length + 1}
				</div>
				<button
					type="button"
					class="group/branch"
					disabled={pathIndex == message.branchStart.length + 1}
					on:click={() => onSwitchBranch('switch', message.branchStart[pathIndex - 2 + 1])}
				>
					<svg
						class="w-[16px] h-[32px] py-[8px] fill-black dark:fill-white group-hover/branch:fill-zinc-600 group-hover/branch:dark:fill-zinc-400 group-disabled/branch:fill-zinc-300 group-disabled/branch:dark:fill-zinc-600"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 320 512"
						><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
							d="M310.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-192 192c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L242.7 256 73.4 86.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l192 192z"
						/>
					</svg>
				</button>
			{/if}
		</div>
	</div>
</section>

<style>
	@media (hover: hover) {
		.group:hover .actions {
			display: flex;
		}
	}
</style>
