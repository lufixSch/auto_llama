<script lang="ts">
	import type OpenAI from 'openai';
	import type { Stream } from 'openai/streaming.mjs';
	import ChatBubble from '$lib/components/chat_bubble/base.svelte';
	import { Roles } from '$lib/chats';
	import { createEventDispatcher } from 'svelte';

	export let stream: Stream<OpenAI.Chat.Completions.ChatCompletionChunk>;
	let streamContent = '';

	const streamComplete = createEventDispatcher();

	$: if (stream) {
		updateStream();
	}

	async function updateStream() {
		for await (const chunk of stream!) {
			streamContent += chunk.choices[0].delta.content;
		}

		streamComplete('inputEvent', streamContent);
	}
</script>

{#if streamContent}
	<ChatBubble role={Roles.assistant} content={streamContent} />
{/if}
