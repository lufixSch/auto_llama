<script lang="ts">
	import { goto } from '$app/navigation';
	import { navigating, page } from '$app/stores';
	import APIInterface from '$lib/api';
	import type { ChatIndex } from '$lib/chats';
	import ChatList from '$lib/components/chat_list.svelte';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	$: if (
		$navigating?.from?.url.pathname === '/chat' &&
		$navigating?.to?.url.searchParams.has('new')
	) {
		APIInterface.getChatIndex().then((chatIndex) => (data.chatIndex = chatIndex));
	}

	/** Delete a chat*/
	async function handleDeleteChat(e: CustomEvent) {
		if ($page.url.pathname.includes(e.detail)) {
			goto('/chat');
		}

		await APIInterface.deleteChat(e.detail);
		data.chatIndex = await APIInterface.getChatIndex();
	}

	/** Update a chat description */
	async function handleEditDescription(e: CustomEvent) {
		await APIInterface.overwriteChatIndex(e.detail);
	}
</script>

<div class="flex h-full">
	<menu class="w-1/4 min-w-64 border-r-[1px] border-zinc-200 dark:border-zinc-800">
		<ChatList chats={data.chatIndex} on:delete={handleDeleteChat} on:edit={handleEditDescription} />
	</menu>
	<slot class="w-full" />
</div>
