<script>
	export let role;
</script>

{#if role != 'system'}
	<section class={role}>
		<div class="block">
			<slot />
		</div>
	</section>
{/if}

<style>
	section {
		display: flex;

		--var2: 8px;
		--var3: 50px;
		--var4: 20px;
		--var10: rgb(0, 150, 184);
	}
	.block {
		position: relative;

		border-radius: var(--var2);
		padding: var(--var2);
		margin-top: var(--var2);

		background-color: var(--var10);
		color: white;
	}
	.block::before {
		position: absolute;
		top: var(--var2);
		left: -19px;

		border: 10px solid transparent;
		/* border-width: 10px 20px; */
		border-right-color: var(--var10);

		content: '';
	}

	.user {
		flex-direction: row-reverse;
	}
	.user .block {
		background-color: rgb(255, 255, 255);
		color: black;
	}
	.user .block::before {
		left: unset;
		border-right-color: transparent;
		right: -19px;
		border-left-color: white;
	}
</style>
