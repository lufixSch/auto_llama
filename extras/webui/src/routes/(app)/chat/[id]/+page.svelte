<script lang="ts">
	import { Roles, type Message } from '$lib/chats';
	import ChatBubble from '$lib/components/chat_bubble/actions.svelte';
	import BaseBubble from '$lib/components/chat_bubble/base.svelte';
	import ChatInput from '$lib/components/chat_input.svelte';
	import APIInterface from '$lib/api';
	import type { PageData } from './$types';
	import llm, { type LLmResponse } from '$lib/llm';
	import StreamChatBubble from '$lib/components/chat_bubble/stream.svelte';
	import { navigating, page } from '$app/stores';
	import { goto, invalidate } from '$app/navigation';
	import { onMount } from 'svelte';

	export let data: PageData;
	let stream: LLmResponse | undefined;
	let branch: number = 0;
	let shouldWriteNew = false;
	let messages: { id: string; message: Message }[] = [];
	let branchPath: number[] = [];
	let shouldRegenerate: boolean = false;

	$: chat = data.chat;
	$: character = data.character;

	$: {
		$page.url.searchParams.set('branch', branch.toString());
		goto($page.url.href, { keepFocus: true });
		messages = chat.getBranch(branch);
		branchPath = chat.getBranchPath(branch);
	}

	/** Trigger llm completion on load if redirected from /chat */
	$: if (shouldWriteNew) {
		$page.url.searchParams.delete('new');
		goto($page.url.href, { keepFocus: true });
		shouldWriteNew = false;
		stream = llm.response(chat, branch, character);
	}

	onMount(() => {
		branch = Number($page.url.searchParams.get('branch') || 0);
		shouldWriteNew = $page.url.searchParams.has('new');
	});

	/** Handle a new message from the user */
	async function handleNewMessage(event: CustomEvent) {
		if (stream) {
			stream.return();
			stream = undefined;
		}

		if (event.detail.trim() != '') {
			chat.newMessage(Roles.user, event.detail, branch);
			chat = chat;
		}

		APIInterface.new().overwriteChat(data.id, chat);
		stream = llm.response(chat, branch, data.character);
	}

	/** Handle when the stream from the model completed*/
	async function handleStreamComplete(event: CustomEvent) {
		if (shouldRegenerate) {
			shouldRegenerate = false;
			return;
		}

		chat.newMessage(Roles.assistant, event.detail, branch);
		APIInterface.new().overwriteChat(data.id, chat);

		stream = undefined;
		chat = chat;
	}

	/** Handle regeneration request */
	async function handleRegeneration() {
		if (stream) {
			shouldRegenerate = true;
			stream.return();
			stream = undefined;
		} else {
			if (messages.length > 1 && messages[messages.length - 1].message.role === Roles.assistant) {
				// Create new branch if assistant response already exists
				handleBranching(messages[messages.length - 2].id, true);
				return;
			}
		}

		// Otherwise, just add a new message
		stream = llm.response(chat, branch, data.character);
	}

	/** Handle completion stop request*/
	async function handleStop() {
		if (stream) {
			stream.return();
			stream = undefined;
		}
	}

	/** Handle message deletion*/
	async function handleDelete(id: string) {
		chat.deleteMessage(id);
		APIInterface.new().overwriteChat(data.id, chat);
		chat = chat;
	}

	/** Handle message branching */
	async function handleBranching(id: string, generate = false) {
		const branchId = chat.createBranch(branch, id);
		APIInterface.new().overwriteChat(data.id, chat);

		if (chat.messages[id].role === Roles.user || generate) {
			// Automatically generate new assistant response if branch message is from user
			shouldWriteNew = true;
		}

		branch = branchId;
	}

	/** Handle message editing */
	async function handleEdit(id: string, message: Message) {
		chat.messages[id].content = message.content;
		APIInterface.new().overwriteChat(data.id, chat);
	}

	/** Switch to a different branch */
	async function switchBranch(branchId: number) {
		branch = branchId;
	}
</script>

<section class="flex flex-col h-page justify-end p-2 w-full">
	<div
		class="rounded-md flex flex-col-reverse h-fit mb-2 space-y-2 space-y-reverse md:space-y-4 md:space-y-reverse md:mb-4 overflow-y-auto overflow-x-hidden"
	>
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
				on:edit={(e) => handleEdit(m.id, e.detail)}
			/>
		{/each}
		{#if character.greeting}
			<BaseBubble role={Roles.assistant} content={character.greeting} />
		{/if}
	</div>
	<ChatInput
		on:inputEvent={handleNewMessage}
		on:regenerate={handleRegeneration}
		on:stop={handleStop}
		isGenerating={stream !== undefined}
	></ChatInput>
</section>
