<script lang="ts">
	import { page } from '$app/stores';
	import type { ChatIndex } from '$lib/chats';
	import { cn } from '$lib/utils/cn';
	import { createEventDispatcher } from 'svelte';

	export let chats: ChatIndex = {};
	let edit: string = '';
	let newName: string = '';
	let inputItem: HTMLElement;

	const onDelete = createEventDispatcher();
	const onEdit = createEventDispatcher();

	/** Enter edit mode for a chat*/
	function handleEdit(id: string) {
		newName = chats[id];
		edit = id;
		requestAnimationFrame(() => inputItem.focus());
	}

	/** Delete a chat */
	function handleDelete(id: string) {
		onDelete('delete', id);
	}

	/** Save new name of a chat */
	function handleAccept() {
		chats[edit] = newName;
		newName = '';
		edit = '';
		onEdit('edit', chats);
	}

	/** Cancel changes to a chat name*/
	function handleCancle() {
		edit = '';
		newName = '';
	}
</script>

<ul class="list-none space-y-2 p-4 m-0">
	{#each Object.keys(chats) as id}
		{#if edit === id}
			<form on:submit|preventDefault={handleAccept}>
				<li
					class="flex rounded-md hover:bg-amber-600 dark:hover:bg-amber-500 border-[1px] border-amber-500 dark:border-amber-600"
				>
					<input
						type="text"
						class="bg-transparent rounded-md focus:border-zinc-800 w-full block text-inherit hover:text-inherit hover:no-underline font-normal truncate h-9 leading-5 p-2 pr-0 box-border"
						bind:value={newName}
						bind:this={inputItem}
					/>
					<button type="submit" class="group/button">
						<svg
							class="icon group-hover/button:fill-zinc-700 group-hover/button:dark:fill-zinc-300"
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 448 512"
							><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
								d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"
							/></svg
						>
					</button>
					<button type="button" class="group/button" on:click={handleCancle}>
						<svg
							class="icon group-hover/button:fill-zinc-700 group-hover/button:dark:fill-zinc-300"
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 384 512"
							><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
								d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"
							/></svg
						>
					</button>
				</li>
			</form>
		{:else}
			<li
				class={cn(
					'flex rounded-md hover:bg-amber-600 dark:hover:bg-amber-500 border-[1px] border-transparent',
					{
						'bg-amber-500 dark:bg-amber-600': $page.url.pathname.includes(id)
					}
				)}
			>
				<a
					href={`/chat/${id}/`}
					class="w-full block text-inherit hover:text-inherit hover:no-underline font-normal truncate h-9 leading-5 p-2 pr-0"
					title={chats[id]}>{chats[id]}</a
				>
				<button class="group/button" on:click={() => handleEdit(id)}>
					<svg
						class="icon group-hover/button:fill-zinc-700 group-hover/button:dark:fill-zinc-300"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 512 512"
						><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
							d="M362.7 19.3L314.3 67.7 444.3 197.7l48.4-48.4c25-25 25-65.5 0-90.5L453.3 19.3c-25-25-65.5-25-90.5 0zm-71 71L58.6 323.5c-10.4 10.4-18 23.3-22.2 37.4L1 481.2C-1.5 489.7 .8 498.8 7 505s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L421.7 220.3 291.7 90.3z"
						/></svg
					>
				</button>
				<button class="group/button" on:click={() => handleDelete(id)}>
					<svg
						class="icon group-hover/button:fill-zinc-700 group-hover/button:dark:fill-zinc-300"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 448 512"
						><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
							d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"
						/></svg
					>
				</button>
			</li>
		{/if}
	{/each}
</ul>
