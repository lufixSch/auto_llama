<script lang="ts">
	import { Roles } from '$lib/chats';
	import { cn } from '$lib/utils/cn';

	export let role: Roles;
	export let content: string;
</script>

<section class="flex flex-col">
	<div
		class={cn('w-full md:w-5/6 py-2 px-4 rounded-lg', {
			'bg-amber-500 dark:bg-amber-600 self-end': role === Roles.user,
			'bg-zinc-200 dark:bg-zinc-700 self-start': role === Roles.assistant
		})}
	>
		{content}
	</div>
</section>
