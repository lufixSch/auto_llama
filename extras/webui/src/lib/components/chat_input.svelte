<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	let message: string = '';
	const submit = createEventDispatcher();
</script>

<form
	class="flex space-y-2 sm:space-y-0 sm:space-x-2 flex-col sm:flex-row sm:items-end"
	on:submit|preventDefault={(e) => {
		submit('inputEvent', message);
		message = '';
	}}
>
	<textarea
		class=""
		rows={Math.min(message.split('\n').length, 10)}
		bind:value={message}
		on:input={(e) => {
			message = e.currentTarget.value;
		}}
	></textarea>
	<button type="submit">
		<div
			class="flex justify-center rounded-[6px] transition duration-200 hover:bg-amber-600 dark:hover:bg-amber-500 active:bg-amber-600 dark:active:bg-amber-500"
		>
			<svg
				class="w-[36px] h-[36px] p-[8px] fill-black dark:fill-white"
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 512 512"
				><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path
					d="M498.1 5.6c10.1 7 15.4 19.1 13.5 31.2l-64 416c-1.5 9.7-7.4 18.2-16 23s-18.9 5.4-28 1.6L284 427.7l-68.5 74.1c-8.9 9.7-22.9 12.9-35.2 8.1S160 493.2 160 480V396.4c0-4 1.5-7.8 4.2-10.7L331.8 202.8c5.8-6.3 5.6-16-.4-22s-15.7-6.4-22-.7L106 360.8 17.7 316.6C7.1 311.3 .3 300.7 0 288.9s5.9-22.8 16.1-28.7l448-256c10.7-6.1 23.9-5.5 34 1.4z"
				/>
			</svg>
		</div>
	</button>
</form>
