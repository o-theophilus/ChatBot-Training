<script>
	import '../style.css';

	export let data;

	let training = data.training.data;
	let error = '';

	const validate = () => {
		error = '';
		if (!training) {
			error = 'cannot be empty';
		}

		!error && submit('post');
	};

	const submit = async (method) => {
		loading = true;
		const resp = await fetch(`${import.meta.env.VITE_API_URL}/training`, {
			method: method,
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ training })
		});
		loading = false;

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				training = data.training.data;
			} else {
				error = data.message;
			}
		}
	};

	let loading = false;
</script>

<section class="base">
	{#if loading}
		<div class="blocker">Loading . . .</div>
	{/if}
	<textarea placeholder="message" id="message" bind:value={training} />
	{#if error}
		<span class="error">{error}</span>
	{/if}
	<div class="buttons_area">
		<button
			on:click={() => {
				validate();
			}}
		>
			Save
		</button>
		<button
			on:click={() => {
				submit('delete');
			}}
		>
			Reset
		</button>
	</div>
</section>

<style>
	section {
		position: relative;
	}
	.blocker {
		display: flex;
		justify-content: center;
		align-items: center;

		position: absolute;
		inset: 0;

		background-color: rgba(128, 128, 128, 0.9);
		pointer-events: none;

		font-size: large;
	}
	textarea {
		height: 100%;
	}
	.buttons_area {
		display: flex;
		justify-content: center;
		gap: var(--var2);
	}
</style>
