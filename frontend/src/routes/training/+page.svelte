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

		!error && submit();
	};

	const submit = async () => {
		saving = true;
		const resp = await fetch(`${import.meta.env.VITE_API_URL}/training`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ training })
		});
		saving = false;

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				training = data.training.data;
			} else {
				error = data.message;
			}
		}
	};
	let saving = false;
</script>

<section>
	<textarea placeholder="message" id="message" bind:value={training} disabled={saving} />
	{#if error.message}
		<span class="error">{error.message}</span>
	{/if}
	<button
		on:click={() => {
			validate();
		}}
		class:disabled={saving}
	>
		{#if saving}
			Saving . . .
		{:else}
			Save
		{/if}
	</button>
</section>

<style>
	section {
		--var1: 20px;
		--var2: 8px;

		height: 100vh;
		padding: var(--var1);
	}

	section {
		display: flex;
		flex-direction: column;
		gap: var(--var2);
	}

	textarea,
	button {
		border-radius: var(--var2);
		border: 2px solid gray;
		padding: var(--var1);
	}

	textarea {
		resize: none;
		height: 100%;
	}
	textarea:disabled {
		opacity: 0.5;
		pointer-events: none;
	}
	.disabled {
		pointer-events: none;
	}

	button:hover {
		background-color: rgb(193, 193, 193);
		cursor: pointer;
	}
</style>
