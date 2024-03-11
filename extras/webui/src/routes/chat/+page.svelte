<script lang="ts">
	import { goto } from '$app/navigation';
	import APIInterface from '$lib/api';
	import ChatInput from '$lib/components/chat_input.svelte';
	import llm from '$lib/llm';

	async function handleNewMessage(event: CustomEvent) {
		const res = await llm.generateDescription(event.detail);

		const { id, index } = await APIInterface.createChat(
			'none',
			res.choices[0].message.content || 'New Chat',
			event.detail
		);
		requestAnimationFrame(() => goto(`/chat/${id}?new`));
	}
</script>

<section class="flex flex-col p-4 h-full w-full">
	<div class="h-full"></div>
	<ChatInput on:inputEvent={handleNewMessage} required={true}></ChatInput>
</section>
