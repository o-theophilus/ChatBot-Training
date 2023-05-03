<script>
	import '../style.css';

	export let data;

	let form = {
		training: data.training.data
	};
	let openai_api_key;
	let error = {};
	$: if (openai_api_key) {
		error.openai_api_key = '';
	} else {
		error.openai_api_key = 'get key at: https://platform.openai.com/account/api-keys';
	}

	const submit = async (method) => {
		form.openai_api_key = openai_api_key;
		loading = true;
		show_key = false;
		const resp = await fetch(`${import.meta.env.VITE_API_URL}/training`, {
			method: method,
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(form)
		});
		loading = false;

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				form.training = data.training.data;
			} else {
				show_key = true;
				error = data.message;
			}
		}
	};

	let loading = false;
	let show_key = true;
</script>

<section class="base">
	{#if loading}
		<div class="blocker">Loading . . .</div>
	{/if}
	{#if show_key}
		<label for="openai_api_key"> OpenAI API Key </label>
		{#if error.openai_api_key}
			<span class="error">{error.openai_api_key}</span>
		{/if}
		<input
			id="openai_api_key"
			type="text"
			placeholder="OpenAI API Key"
			bind:value={openai_api_key}
		/>
		<br />
	{/if}
	<label for="training"> Training Information </label>
	{#if error.training}
		<span class="error">{error.training}</span>
	{/if}
	<textarea id="training" placeholder="Training Information" bind:value={form.training} />
	<div class="buttons_area">
		<button
			on:click={() => {
				error = {};
				if (!form.training) {
					error.training = 'cannot be empty';
				}
				if (!openai_api_key) {
					error.openai_api_key =
						'cannot be empty. get key at: https://platform.openai.com/account/api-keys';
				}
				Object.keys(error).length === 0 && submit('post');
			}}
		>
			Train
		</button>
		<button
			on:click={() => {
				error = {};
				if (!openai_api_key) {
					error.openai_api_key =
						'cannot be empty. get key at: https://platform.openai.com/account/api-keys';
				}
				Object.keys(error).length === 0 && submit('delete');
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
