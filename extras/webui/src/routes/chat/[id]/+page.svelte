<script lang="ts">
	import { Roles } from '$lib/chats';
	import ChatBubble from '$lib/components/chat_bubble/actions.svelte';
	import ChatInput from '$lib/components/chat_input.svelte';
	import APIInterface from '$lib/api';
	import type { PageData } from './$types';
	import llm from '$lib/llm';
	import type { Stream } from 'openai/streaming.mjs';
	import type OpenAI from 'openai';
	import StreamChatBubble from '$lib/components/chat_bubble/stream.svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { generateId } from '$lib/utils/id';

	export let data: PageData;
	let chat = data.chat;
	let branch: number = 0;
	let messages = chat.getBranch(branch);
	let stream: Stream<OpenAI.Chat.Completions.ChatCompletionChunk> | undefined;
	let branchPath: number[] = [];
	let shouldRegenerate: boolean = false;

	/** Trigger llm completion on load if redirected from /chat */
	$: if ($page.url.searchParams.has('new')) {
		llm.chatStream(chat, branch).then((s) => (stream = s));
		$page.url.searchParams.delete('new');
		goto('?' + $page.url.searchParams.toString());
	}

	$: branch = Number($page.url.searchParams.get('branch') || 0);
	$: messages = chat.getBranch(branch);
	$: branchPath = chat.getBranchPath(branch);

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
			if (messages.length > 1 && messages[messages.length - 1].message.role === Roles.assistant) {
				// Create new branch if assistant response already exists
				handleBranching(messages[messages.length - 2].id, true);
				return;
			}
		}

		// Otherwise, just add a new message
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
	async function handleBranching(id: string, generate = false) {
		const branchId = chat.createBranch(branch, id);
		APIInterface.overwriteChat(data.id, chat);

		$page.url.searchParams.set('branch', branchId.toString());

		if (chat.messages[id].role === Roles.user || generate) {
			// Automatically generate new assistant response if branch message is from user
			$page.url.searchParams.set('new', 'true');
		}

		await goto($page.url.href);
		messages = messages;
	}

	/** Switch to a different branch */
	async function switchBranch(branchId: number) {
		$page.url.searchParams.set('branch', branchId.toString());
		await goto($page.url.href);
		messages = messages;
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
					message={m.message}
					{branchPath}
					on:branch={() => handleBranching(m.id)}
					on:delete={() => handleDelete(m.id)}
					on:switch={(e) => {
						switchBranch(e.detail);
					}}
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
