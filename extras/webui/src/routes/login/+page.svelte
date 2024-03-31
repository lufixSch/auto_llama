<script lang="ts">
	import { goto } from '$app/navigation';
	import APIInterface from '$lib/api';
	import auth from '$lib/auth';
	import { cn } from '$lib/utils/cn';

	let secret = '';
	let valid = true;

	async function handleSubmit(event: Event) {
		try {
			valid = true;
			APIInterface.new().validateSecret(secret);
			auth.login(secret);
			goto('/');
		} catch (e) {
			valid = false;
		}
	}
</script>

<div class="flex flex-col justify-center h-full p-8">
	<h6 class="text-center pb-4">
		Login with the secret defined in you <span class="font-bold">.env</span> file!
	</h6>
	<form
		class="h-fit flex space-y-2 sm:space-y-0 sm:space-x-2 flex-col sm:flex-row sm:items-end"
		on:submit|preventDefault={(e) => {
			handleSubmit(e);
			secret = '';
		}}
	>
		<div class="w-full">
			<input
				class="focus-visible:ring-[1px] focus-visible:ring-amber-600 dark:focus-visible:ring-amber-500 placeholder:text-gray-400 dark:placeholder:text-gray-600 bg-zinc-200 dark:bg-zinc-800 w-full rounded-md border-none px-3 py-2 text-sm box-border"
				placeholder="Secret"
				bind:value={secret}
				on:input={(e) => {
					secret = e.currentTarget.value;
				}}
				aria-errormessage="secret-error"
				aria-invalid={!valid}
			/>
			<div
				id="secret-error"
				class={cn('p-3 font-normal text-red-800 dark:text-red-600', {
					hidden: valid
				})}
				aria-hidden={valid}
			>
				Invalid Secret!
			</div>
		</div>
		<div class="flex space-x-2 self-start">
			<button class="w-full group" type="submit" disabled={!secret}>
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
		</div>
	</form>
</div>
