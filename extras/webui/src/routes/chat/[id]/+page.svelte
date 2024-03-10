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
	let scroller: HTMLElement;
	let stream: Stream<OpenAI.Chat.Completions.ChatCompletionChunk> | undefined;

	/** Update scroll position to bottom on load */
	$: if (scroller && scroller.scrollTop < scroller.scrollHeight) {
		scroller.scrollTop = scroller.scrollHeight;
	}

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

		chat.messages.push({ role: Roles.user, content: event.detail });
		chat = chat;

		// Create timeout to trigger scrolling after new element was rendered
		// I'm sure ther is a better solution to do this. If you know one open a PR
		setTimeout(() => {
			scroller.scrollTop = scroller.scrollHeight;
		}, 0);

		APIInterface.overwriteChat(data.id, chat);
		stream = await llm.chatStream(chat);
	}

	/** Handle when the stream from the model completed*/
	async function handleStreamComplete(event: CustomEvent) {
		chat.messages.push({ role: Roles.assistant, content: event.detail });
		APIInterface.overwriteChat(data.id, chat);

		stream = undefined;
		chat = chat;
	}
</script>

<section class="flex flex-col p-4 h-full">
	<div class="h-full flex flex-col justify-end my-4 overflow-y-hidden">
		<div bind:this={scroller} class="flex flex-col space-y-4 overflow-y-auto">
			{#each chat.messages as message}
				<ChatBubble role={message.role} content={message.content} />
			{/each}
			{#if stream}
				<StreamChatBubble {stream} on:inputEvent={handleStreamComplete} />
			{/if}
		</div>
	</div>
	<ChatInput on:inputEvent={handleNewMessage}></ChatInput>
</section>
