<script lang="ts">
	import CharacterForm from '$lib/components/character_form.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<div class="flex justify-center">
	<CharacterForm id={data.id} character={data.character} />
</div>
