<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	export let isGenerating: boolean = false;
	export let required: boolean = false;
	const onRegenerate = createEventDispatcher();
	const onStop = createEventDispatcher();

	let message: string = '';
	const submit = createEventDispatcher();

	function handleSpecialAction() {
		if (isGenerating) {
			onStop('stop');
		} else {
			onRegenerate('regenerate');
		}
	}
</script>

<form
	class="flex space-y-2 sm:space-y-0 sm:space-x-2 flex-col sm:flex-row sm:items-end"
	on:submit|preventDefault={(e) => {
		submit('inputEvent', message);
		message = '';
	}}
>
	<textarea
		class="focus-visible:ring-[1px] focus-visible:ring-amber-600 dark:focus-visible:ring-amber-500 placeholder:text-gray-400 dark:placeholder:text-gray-600 bg-zinc-200 dark:bg-zinc-800 w-full rounded-md border-none px-3 py-2 text-sm box-border"
		rows={Math.min(message.split('\n').length, 10)}
		bind:value={message}
		on:input={(e) => {
			message = e.currentTarget.value;
		}}
	></textarea>
	<div class="flex space-x-2">
		<button class="w-full group" type="submit" disabled={required && !message}>
			<div
				class="flex justify-center rounded-[6px] transition duration-200 hover:bg-amber-600 dark:hover:bg-amber-500 active:bg-amber-600 dark:active:bg-amber-500 group-disabled:cursor-not-allowed group-disabled:bg-zinc-50 dark:group-disabled:bg-zinc-950"
			>
				<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"
					><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
						d="M498.1 5.6c10.1 7 15.4 19.1 13.5 31.2l-64 416c-1.5 9.7-7.4 18.2-16 23s-18.9 5.4-28 1.6L284 427.7l-68.5 74.1c-8.9 9.7-22.9 12.9-35.2 8.1S160 493.2 160 480V396.4c0-4 1.5-7.8 4.2-10.7L331.8 202.8c5.8-6.3 5.6-16-.4-22s-15.7-6.4-22-.7L106 360.8 17.7 316.6C7.1 311.3 .3 300.7 0 288.9s5.9-22.8 16.1-28.7l448-256c10.7-6.1 23.9-5.5 34 1.4z"
					/>
				</svg>
			</div>
		</button>
		<button class="w-full" type="button" on:click={handleSpecialAction}>
			{#if isGenerating}
				<div
					class="w-full flex justify-center rounded-[6px] transition duration-200 hover:bg-amber-600 dark:hover:bg-amber-500 active:bg-amber-600 dark:active:bg-amber-500"
				>
					<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"
						><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
							d="M0 128C0 92.7 28.7 64 64 64H320c35.3 0 64 28.7 64 64V384c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V128z"
						/></svg
					>
				</div>
			{:else}
				<div
					class="flex justify-center rounded-[6px] transition duration-200 hover:bg-amber-600 dark:hover:bg-amber-500 active:bg-amber-600 dark:active:bg-amber-500"
				>
					<svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"
						><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
							d="M463.5 224H472c13.3 0 24-10.7 24-24V72c0-9.7-5.8-18.5-14.8-22.2s-19.3-1.7-26.2 5.2L413.4 96.6c-87.6-86.5-228.7-86.2-315.8 1c-87.5 87.5-87.5 229.3 0 316.8s229.3 87.5 316.8 0c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0c-62.5 62.5-163.8 62.5-226.3 0s-62.5-163.8 0-226.3c62.2-62.2 162.7-62.5 225.3-1L327 183c-6.9 6.9-8.9 17.2-5.2 26.2s12.5 14.8 22.2 14.8H463.5z"
						/></svg
					>
				</div>
			{/if}
		</button>
	</div>
</form>
