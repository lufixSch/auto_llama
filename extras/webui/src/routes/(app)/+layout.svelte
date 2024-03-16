<script lang="ts">
	import type { PageData } from './$types';
	import { goto } from '$app/navigation';
	import { navigating, page } from '$app/stores';
	import APIInterface from '$lib/api';
	import ChatList from '$lib/components/chat_list.svelte';
	import { cn } from '$lib/utils/cn';
	import IconButton from '$lib/components/buttons/icon_button.svelte';
	import CharList from '$lib/components/char_list.svelte';

	export let data: PageData;
	let menuVisible: boolean = false;

	$: if ($navigating) {
		switch (data.location) {
			case 'chat':
				APIInterface.new()
					.getChatIndex()
					.then((chatIndex) => (data.chatIndex = chatIndex));
				break;
			case 'character':
				APIInterface.new()
					.getCharacterIndex()
					.then((charIndex) => (data.charIndex = charIndex));
				break;
		}
	}

	/** Delete a chat*/
	async function handleDeleteChat(e: CustomEvent) {
		if ($page.url.pathname.includes(e.detail)) {
			goto('/chat');
		}

		await APIInterface.new().deleteChat(e.detail);
		data.chatIndex = await APIInterface.new().getChatIndex();
	}

	/** Delete a character */
	async function handleDeleteCharacter(e: CustomEvent) {
		if ($page.url.pathname.includes(e.detail)) {
			goto('/character');
		}

		await APIInterface.new().deleteCharacter(e.detail);
		data.charIndex = await APIInterface.new().getCharacterIndex();
	}

	/** Update a chat description */
	async function handleEditDescription(e: CustomEvent) {
		await APIInterface.new().overwriteChatIndex(e.detail);
	}
</script>

<div class="flex flex-auto h-full">
	<menu
		class={cn(
			'h-page md:h-full flex flex-col justify-between mt-11 md:mt-0 z-10 bg-zinc-50 dark:bg-zinc-950 w-full sm:w-1/4 sm:min-w-64 sm:border-r-[1px] border-zinc-200 dark:border-zinc-800 absolute md:static transition-transform',
			{
				'-translate-x-full md:translate-x-0 md:visible': !menuVisible
			}
		)}
	>
		<!-- <div class="flex justify-end md:hidden pt-2 pr-2">
			<IconButton on:click={() => (menuVisible = false)}>
				<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"
					> -->
		<!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.-->
		<!--<path
						d="M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l192 192c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L77.3 256 246.6 86.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-192 192z"
					/></svg
				>
			</IconButton>
		</div> -->
		<div class="overflow-y-auto">
			{#if data.location === 'chat'}
				<ChatList
					chats={data.chatIndex}
					on:delete={handleDeleteChat}
					on:edit={handleEditDescription}
				/>
			{:else if data.location === 'character'}
				<CharList chars={data.charIndex} on:delete={handleDeleteCharacter} />
			{/if}
			<div class="flex justify-center invisible md:visible">
				<a class="" href={`/${data.location}`}>
					<svg
						class="icon rounded-lg bg-amber-500 dark:bg-amber-600 hover:bg-amber-600 dark:hover:bg-amber-500"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 448 512"
						><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
							d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"
						/></svg
					>
				</a>
			</div>
		</div>
		<div class="p-8 text-right">
			{#if data.location === 'chat'}
				<a class="text-zinc-500 dark:text-zinc-300 hover:no-underline" href="/character"
					>Characters</a
				>
			{:else if data.location === 'character'}
				<a class="text-zinc-500 dark:text-zinc-300 hover:no-underline" href="/chat">Chats</a>
			{/if}
		</div>
	</menu>
	<div class="flex flex-col h-full w-full">
		<div
			class="flex pt-2 px-2 h-11 bg-zinc-50 dark:bg-zinc-950 border-zinc-200 dark:border-zinc-800 border-b-[0px] items-center"
		>
			<IconButton className="md:hidden visible" on:click={() => (menuVisible = !menuVisible)}>
				<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
					><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
						d="M0 96C0 78.3 14.3 64 32 64H416c17.7 0 32 14.3 32 32s-14.3 32-32 32H32C14.3 128 0 113.7 0 96zM0 256c0-17.7 14.3-32 32-32H416c17.7 0 32 14.3 32 32s-14.3 32-32 32H32c-17.7 0-32-14.3-32-32zM448 416c0 17.7-14.3 32-32 32H32c-17.7 0-32-14.3-32-32s14.3-32 32-32H416c17.7 0 32 14.3 32 32z"
					/></svg
				>
			</IconButton>
			<div class="w-full"></div>
			{#if data.currentChar}
				<h6 class="m-0">
					<a href="/character/{data.currentChar.id}">{data.currentChar.name}</a>
				</h6>
			{/if}
			<div class="w-full"></div>
			<IconButton className="md:hidden visible" on:click={() => goto('/chat')}>
				<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
					><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
						d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"
					/></svg
				>
			</IconButton>
		</div>
		<slot />
	</div>
</div>
