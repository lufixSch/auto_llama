<script lang="ts">
	import { Roles, type Message } from '$lib/chats';
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
	import { generateId } from '$lib/utils/id';

	export let data: PageData;
	let chat = data.chat;
	let branch: number = 0;
	let messages = chat.getBranch(branch);
	let stream: Stream<OpenAI.Chat.Completions.ChatCompletionChunk> | undefined;
	let shouldRegenerate: boolean = false;

	/** Trigger llm completion on load if redirected from /chat */
	$: if ($page.url.searchParams.has('new')) {
		llm.chatStream(chat, branch).then((s) => (stream = s));
		$page.url.searchParams.delete('new');
		goto('?' + $page.url.searchParams.toString());
	}

	$: branch = Number($page.url.searchParams.get('branch') || 0);
	$: messages = chat.getBranch(branch);

	/** Handle a new message from the user */
	async function handleNewMessage(event: CustomEvent) {
		if (stream) {
			stream.controller.abort();
			stream = undefined;
		}

		if (event.detail.trim() != '') {
			chat.newMessage(Roles.user, event.detail, branch);
			chat = chat;
		}

		APIInterface.overwriteChat(data.id, chat);
		stream = await llm.chatStream(chat, branch);
	}

	/** Handle when the stream from the model completed*/
	async function handleStreamComplete(event: CustomEvent) {
		if (shouldRegenerate) {
			shouldRegenerate = false;
			return;
		}

		chat.newMessage(Roles.assistant, event.detail, branch);
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
			if (messages.length > 0 && messages[messages.length - 1].message.role === Roles.assistant) {
				chat.deleteMessage(messages[messages.length - 1].id);
				chat = chat;
			}
		}

		APIInterface.overwriteChat(data.id, chat);
		stream = await llm.chatStream(chat, branch);
	}

	/** Handle completion stop request*/
	async function handleStop() {
		if (stream) {
			stream.controller.abort();
			stream = undefined;
		}
	}

	/** Handle message deletion*/
	async function handleDelete(id: string) {
		chat.deleteMessage(id);
		APIInterface.overwriteChat(data.id, chat);
		chat = chat;
	}

	/** Handle message branching */
	async function handleBranching(id: string) {
		console.log('Branch');
		const branchId = chat.createBranch(branch, id);
		APIInterface.overwriteChat(data.id, chat);

		$page.url.searchParams.append('branch', branchId.toString());
		goto($page.url.href);
	}
</script>

<section class="flex flex-col p-4 h-full">
	<div class="h-full flex flex-col justify-end my-4 overflow-y-hidden">
		<div class="flex flex-col-reverse space-y-4 space-y-reverse overflow-y-auto overflow-x-hidden">
			{#if stream}
				<StreamChatBubble {stream} on:inputEvent={handleStreamComplete} />
			{/if}
			{#each messages.slice().reverse() as m}
				<ChatBubble
					role={m.message.role}
					content={m.message.content}
					on:branch={() => handleBranching(m.id)}
					on:delete={() => handleDelete(m.id)}
				/>
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
