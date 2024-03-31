<script lang="ts">
	import { Character, ChatType } from '$lib/characters';
	import TextButton from './buttons/text_button.svelte';
	import { cn } from '$lib/utils/cn';
	import APIInterface from '$lib/api';
	import { createEventDispatcher } from 'svelte';

	export let id: string | undefined = undefined;
	export let character: Character = new Character('', '', '');
	let onSave = createEventDispatcher();

	$: isValid = character.name.length > 0;

	async function onHandleSubmit() {
		if (id) {
			await APIInterface.new().overwriteCharacter(id, character);
		} else {
			const { id: newId, index } = await APIInterface.new().createCharacter(character);
			id = newId;
		}

		onSave('save', { id, character });
	}

	async function onHandleReset() {
		if (id) {
			character = await APIInterface.new().getCharacter(id);
		}
	}

	function handleTypeChange(event: any) {
		character.chatType = event.target?.value || ChatType.instruct;
	}
</script>

<form
	class="space-y-2 sm:space-y-4 overflow-y-scroll h-fit p-4 lg:p-8 w-full"
	on:submit|preventDefault={onHandleSubmit}
>
	<input
		id="name"
		type="text"
		name="char"
		placeholder="Character Name"
		required
		bind:value={character.name}
		aria-errormessage="name-error"
		aria-invalid={character.name.length === 0}
	/>
	<span
		id="name-error"
		class={cn('p-3 font-normal text-red-800 dark:text-red-600', {
			hidden: character.name.length > 0
		})}
	>
		Name is required!
	</span>
	<textarea
		name="system-prompt"
		placeholder="System prompt"
		rows={Math.max(4, character.systemPrompt.split('\n').length)}
		bind:value={character.systemPrompt}
	></textarea>
	<textarea
		name="greeting"
		placeholder="Greeting"
		rows={Math.max(2, character.greeting.split('\n').length)}
		bind:value={character.greeting}
	></textarea>
	<div
		class="flex items-center sm:justify-evenly flex-col sm:flex-row sm:space-x-2 space-y-2 sm:space-y-0"
	>
		<div class="flex items-center flex-row space-x-2 w-full">
			<label for="system-name" class="w-24 text-right"> System: </label>
			<input id="system-name" type="text" bind:value={character.names.system} />
		</div>
		<div class="flex items-center flex-row space-x-2 w-full">
			<label for="assistant-name" class="w-24 text-right"> Assistant: </label>
			<input id="assistant-name" type="text" bind:value={character.names.assistant} />
		</div>
		<div class="flex items-center flex-row space-x-2 w-full">
			<label for="user-name" class="w-24 text-right"> User: </label>
			<input id="user-name" type="text" bind:value={character.names.user} />
		</div>
	</div>
	<fieldset
		class="flex items-center sm:justify-evenly flex-col sm:flex-row space-y-2 py-2"
		on:change={handleTypeChange}
	>
		<label for="type-instruct" class="flex items-center space-x-2 h-8">
			<input
				id="type-instruct"
				type="radio"
				name="chat-type"
				value={ChatType.instruct}
				checked={character.chatType === 'instruct'}
			/>
			<span>Instruct</span>
		</label>
		<label for="type-chat" class="flex items-center space-x-2 h-8">
			<input
				id="type-chat"
				type="radio"
				name="chat-type"
				value={ChatType.chat}
				checked={character.chatType === 'chat'}
			/>
			<span>Chat</span>
		</label>
	</fieldset>
	<div class="flex items-center sm:justify-evenly flex-col sm:flex-row space-y-2 sm:space-y-0">
		<TextButton
			className="w-full sm:w-1/4 sm:max-w-64"
			type="submit"
			style="lit"
			disabled={!isValid}>Save</TextButton
		>
		{#if id}
			<TextButton className="w-full sm:w-1/4" type="button" on:click={onHandleReset}
				>Reset</TextButton
			>
		{/if}
	</div>
</form>

<style lang="postcss">
	input[type='text'],
	textarea {
		@apply px-3 py-2 focus-visible:ring-amber-600 dark:focus-visible:ring-amber-500 focus-visible:ring-[1px];
		@apply placeholder:text-gray-400 dark:placeholder:text-gray-600 bg-zinc-200 dark:bg-zinc-800 w-full rounded-md border-none text-sm box-border;
	}

	input[type='radio'] {
		@apply focus:ring-[1px]  checked:bg-amber-600 dark:checked:bg-amber-500 focus:ring-amber-600 dark:focus:ring-amber-500 hover:bg-amber-600 dark:hover:bg-amber-500;
		@apply bg-zinc-200 dark:bg-zinc-800 w-4 h-4 border-none rounded-full cursor-pointer;
	}
</style>
