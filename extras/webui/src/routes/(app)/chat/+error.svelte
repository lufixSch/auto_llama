<script>
	import { goto } from '$app/navigation';
	import Button from '$lib/components/buttons/text_button.svelte';
</script>

<div class="text-center w-full">
	<h1 class="text-amber-600 dark:text-amber-500">404</h1>
	<h2>Chat not found!</h2>
	<Button
		className="mt-4 text-inherit hover:text-inherit hover:no-underline"
		style="lit"
		on:click={() => goto('/chat')}
	>
		Create New Chat</Button
	>
</div>
