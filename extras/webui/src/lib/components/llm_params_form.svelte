<script lang="ts">
	import type { LLMParams } from '$lib/llm';

	export let params: LLMParams;
	export let isValid: boolean = true;
	const errors: { [key in keyof LLMParams]?: string | undefined } = {};

	$: console.log(params);

	function handleInput(ev: Event, prop: keyof LLMParams) {
		const el = ev.target as HTMLInputElement;

		if (!el.validity.valid) {
			errors[prop] = el.validationMessage;
		} else {
			errors[prop] = undefined;
		}

		isValid = Object.keys(params).every(
			(prop) => !Object.hasOwn(errors, prop) || !errors[prop as keyof LLMParams]
		);
		console.log('isValid', isValid);
	}
</script>

<div class="flex flex-col gap-2">
	<h6>Parameters:</h6>
	<div class="grid grid-cols-1 lg:grid-cols-2 gap-2 max-w-3xl self-center">
		<div class="col-span-1 lg:col-span-2">
			<div class="flex items-baseline flex-row gap-2">
				<label for="max_new_tokens" class="text-right">Max New Tokens:</label>
				<input
					id="max_new_tokens"
					type="number"
					step="1"
					min="1"
					required
					on:input={(e) => handleInput(e, 'max_new_tokens')}
					bind:value={params.max_new_tokens}
				/>
			</div>
			{#if errors.max_new_tokens}
				<div class="text-red-500 dark:text-red-400 text-center">{errors.max_new_tokens}</div>
			{/if}
		</div>
		<div>
			<div class="flex items-baseline flex-row gap-2">
				<label for="temperature" class="text-right">Temperature:</label>
				<input
					id="temperature"
					type="number"
					step="0.1"
					min="0"
					max="3"
					required
					on:input={(e) => handleInput(e, 'temperature')}
					bind:value={params.temperature}
				/>
			</div>
			{#if errors.temperature}
				<div class="text-red-500 dark:text-red-400 text-center">{errors.temperature}</div>
			{/if}
		</div>

		<div>
			<div class="flex items-baseline flex-row gap-2">
				<label for="top_p" class="text-right">Top p:</label>
				<input
					id="top_p"
					type="number"
					step="0.1"
					min="0"
					max="1"
					required
					on:input={(e) => handleInput(e, 'top_p')}
					bind:value={params.top_p}
				/>
			</div>
			{#if errors.top_p}
				<div class="text-red-500 dark:text-red-400 text-center">{errors.top_p}</div>
			{/if}
		</div>

		<div>
			<div class="flex items-baseline flex-row gap-2">
				<label for="frequency_penalty" class=" text-right">Frequency Penalty:</label>
				<input
					id="frequency_penalty"
					type="number"
					step="0.01"
					min="0"
					max="2"
					required
					on:input={(e) => handleInput(e, 'frequency_penalty')}
					bind:value={params.frequency_penalty}
				/>
			</div>
			{#if errors.frequency_penalty}
				<div class="text-red-500 dark:text-red-400 text-center">{errors.frequency_penalty}</div>
			{/if}
		</div>

		<div>
			<div class="flex flex-row gap-2 items-baseline">
				<label for="presence_penalty" class="text-right">Presence Penalty:</label>

				<input
					id="presence_penalty"
					type="number"
					step="0.01"
					min="0"
					max="2"
					required
					on:input={(e) => handleInput(e, 'presence_penalty')}
					bind:value={params.presence_penalty}
				/>
			</div>
			{#if errors.presence_penalty}
				<div class="text-red-500 dark:text-red-400 text-center pt-1">{errors.presence_penalty}</div>
			{/if}
		</div>
	</div>
</div>

<style lang="postcss">
	input[type='number'] {
		@apply px-3 py-2 w-full focus-visible:ring-amber-600 dark:focus-visible:ring-amber-500 focus-visible:ring-[1px];
		@apply placeholder:text-gray-400 dark:placeholder:text-gray-600 bg-zinc-200 dark:bg-zinc-800 rounded-md border-none text-sm box-border;
	}

	label {
		@apply w-full;
	}
</style>
