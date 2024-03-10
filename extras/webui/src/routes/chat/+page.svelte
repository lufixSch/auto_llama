<script lang="ts">
	import { goto } from '$app/navigation';
	import APIInterface from '$lib/api';
	import ChatInput from '$lib/components/chat_input.svelte';

	async function handleNewMessage(event: CustomEvent) {
		const { id, index } = await APIInterface.createChat('none', 'New Chat', event.detail);
		goto(`/chat/${id}`);
	}
</script>

<section class="flex flex-col p-4 h-full">
	<div class="h-full"></div>
	<ChatInput on:inputEvent={handleNewMessage}></ChatInput>
</section>
