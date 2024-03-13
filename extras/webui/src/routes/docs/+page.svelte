<script lang="ts">
	import type { PageServerData } from './$types';

	export let data: PageServerData;
</script>

<article class="m-4 overflow-y-scroll overflow-x-hidden">
	{@html data.content}
</article>
