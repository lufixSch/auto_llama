<script lang="ts">
	import ChatBubble from '$lib/components/chat_bubble/base.svelte';
	import { Roles } from '$lib/chats';
	import { createEventDispatcher } from 'svelte';
	import type { LLmResponse } from '$lib/llm';

	export let stream: LLmResponse;
	let streamContent = '';

	const streamComplete = createEventDispatcher();

	$: if (stream) {
		updateStream();
	}

	async function updateStream() {
		for await (const chunk of stream!) {
			streamContent += chunk.delta;
		}

		streamComplete('inputEvent', streamContent);
	}
</script>

{#if streamContent}
	<ChatBubble role={Roles.assistant} content={streamContent} />
{/if}
