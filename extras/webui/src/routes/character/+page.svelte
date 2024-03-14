<script lang="ts">
	import { goto } from '$app/navigation';
	import CharacterForm from '$lib/components/character_form.svelte';
</script>

<div class="flex justify-center">
	<CharacterForm on:save={(e) => goto(`/character/${e.detail.id}`)} />
</div>
