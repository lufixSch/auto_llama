<script lang="ts">
	import { createChat } from '$lib/chats';
	import ChatInput from '$lib/components/chat_input.svelte';

	function handleNewMessage(event: CustomEvent) {
		const { id, chat } = createChat('none');
	}
</script>

<section class="flex flex-col p-4 h-full">
	<div class="h-full"></div>
	<ChatInput on:inputEvent={handleNewMessage}></ChatInput>
</section>
