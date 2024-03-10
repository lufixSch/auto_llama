<script lang="ts">
	import { Roles } from '$lib/chats';
	import ChatBubble from '$lib/components/chat_bubble.svelte';
	import ChatInput from '$lib/components/chat_input.svelte';
	import APIInterface from '$lib/api';
	import type { PageData } from './$types';
	import llm from '$lib/llm';
	import type { Stream } from 'openai/streaming.mjs';
	import type OpenAI from 'openai';
	import StreamChatBubble from '$lib/components/stream_chat_bubble.svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';

	export let data: PageData;
	let chat = data.chat;
	let stream: Stream<OpenAI.Chat.Completions.ChatCompletionChunk> | undefined;
	let shouldRegenerate: boolean = false;

	/** Trigger llm completion on load if redirected from /chat */
	$: if ($page.url.searchParams.has('new')) {
		llm.chatStream(chat).then((s) => (stream = s));
		goto('?');
	}

	/** Handle a new message from the user */
	async function handleNewMessage(event: CustomEvent) {
		if (stream) {
			stream.controller.abort();
			stream = undefined;
		}

		if (event.detail.trim() != '') {
			chat.messages.push({ role: Roles.user, content: event.detail });
			chat = chat;
		}

		APIInterface.overwriteChat(data.id, chat);
		stream = await llm.chatStream(chat);
	}

	/** Handle when the stream from the model completed*/
	async function handleStreamComplete(event: CustomEvent) {
		if (shouldRegenerate) {
			shouldRegenerate = false;
			return;
		}

		chat.messages.push({ role: Roles.assistant, content: event.detail });
		APIInterface.overwriteChat(data.id, chat);

		stream = undefined;
		chat = chat;
	}

	/** Handle regeneration request */
	async function handleRegeneration() {
		if (stream) {
			shouldRegenerate = true;
			stream.controller.abort();
			stream = undefined;
		} else {
			if (
				chat.messages.length > 0 &&
				chat.messages[chat.messages.length - 1].role === Roles.assistant
			) {
				chat.messages.pop();
				chat = chat;
			}
		}

		APIInterface.overwriteChat(data.id, chat);
		stream = await llm.chatStream(chat);
	}

	/** Handle completion stop request*/
	async function handleStop() {
		if (stream) {
			stream.controller.abort();
			stream = undefined;
		}
	}
</script>

<section class="flex flex-col p-4 h-full">
	<div class="h-full flex flex-col justify-end my-4 overflow-y-hidden">
		<div class="flex flex-col-reverse space-y-4 space-y-reverse overflow-y-auto">
			{#if stream}
				<StreamChatBubble {stream} on:inputEvent={handleStreamComplete} />
			{/if}
			{#each chat.messages.slice().reverse() as message}
				<ChatBubble role={message.role} content={message.content} />
			{/each}
		</div>
	</div>
	<ChatInput
		on:inputEvent={handleNewMessage}
		on:regenerate={handleRegeneration}
		on:stop={handleStop}
		isGenerating={stream !== undefined}
	></ChatInput>
</section>
