<script lang="ts">
	import '../app.postcss';
</script>

<body class={`flex flex-col overflow-hidden`}>
	<slot />
</body>

<style>
	body {
		height: 100vh;
	}

	@supports (height: 100dvh) {
		body {
			height: 100dvh;
		}
	}
</style>
