
export const load = async ({ fetch }) => {

    const resp = await fetch(`${import.meta.env.VITE_API_URL}/training`, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (resp.ok) {
        const data = await resp.json();

        if (data.status == 200) {
            return {
                training: data.training
            }
        }
    }
}