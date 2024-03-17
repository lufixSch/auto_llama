<script lang="ts">
	import CharacterForm from '$lib/components/character_form.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<div class="flex flex-col h-page overflow-y-hidden">
	<CharacterForm id={data.id} character={data.character} />
</div>
