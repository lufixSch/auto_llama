<script lang="ts">
	import { goto } from '$app/navigation';
	import APIInterface from '$lib/api';
	import AutoLLaMaAPI from '$lib/auto_llama';
	import type { Article } from '$lib/auto_llama_sdk';
	import IconButton from '$lib/components/buttons/icon_button.svelte';
	import CharSelector from '$lib/components/char_selector.svelte';
	import ChatInput from '$lib/components/chat_input.svelte';
	import FileList from '$lib/components/file_list.svelte';
	import llm from '$lib/llm';
	import { trim } from '$lib/utils/str';
	import type { PageData } from './$types';

	export let data: PageData;
	let selectedCharacter: string = 'none';
	let context: Article[] = [];
	let message: string = '';

	const auto_llama = AutoLLaMaAPI.new();

	async function handleNewMessage(event: CustomEvent) {
		const res = await llm.generateDescription(event.detail, data.config);

		const { id, index } = await APIInterface.new().createChat(
			selectedCharacter,
			trim(res.choices[0].message.content || 'New Chat', '"'),
			event.detail
		);
		requestAnimationFrame(() => goto(`/chat/${id}?new`));
	}

	async function handleFileSelected(ev: CustomEvent<File>) {
		const file = ev.detail;
		if (!file) return;

		const article = await auto_llama.parseFile(file, {}, data.config);
		context = [...context, article];
		message += `\n[${article.source}]{}`;
	}
</script>

<section class="flex flex-col p-4 h-page w-full">
	<div class="h-full flex space-x-2 items-end pb-4">
		<CharSelector characters={data.characters} bind:selectedCharacter />
		<IconButton on:click={() => goto('/character')}
			><svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
				><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
					d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"
				/></svg
			></IconButton
		>
	</div>
	<FileList
		files={context}
		on:remove={(ev) => (context = context.filter((_, i) => i !== ev.detail))}
	></FileList>
	<ChatInput
		bind:message
		on:inputEvent={handleNewMessage}
		on:fileSelected={handleFileSelected}
		required={true}
	></ChatInput>
</section>
