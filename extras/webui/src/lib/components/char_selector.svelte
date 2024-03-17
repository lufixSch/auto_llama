<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let characters: { [key: string]: string };
	export let selectedCharacter = 'none';

	const onCharSelect = createEventDispatcher();
</script>

<label for="character-select" class="flex items-center space-x-2 w-full">
	<span class="color-zinc-200 dark:color-zinc-800">Character:</span>
	<select
		id="character-select"
		class="focus-visible:ring-[1px] focus-visible:ring-amber-600 dark:focus-visible:ring-amber-500 focus:ring-amber-600 dark:focus:ring-amber-500 placeholder:text-gray-400 dark:placeholder:text-gray-600 bg-zinc-200 dark:bg-zinc-800 w-full rounded-md border-none px-3 py-2 text-sm box-border"
		on:change={(e) => onCharSelect('select', selectedCharacter)}
		bind:value={selectedCharacter}
	>
		<option value="none">None</option>
		{#each Object.keys(characters) as id}
			<option value={id}>{characters[id]}</option>
		{/each}
	</select>
</label>
