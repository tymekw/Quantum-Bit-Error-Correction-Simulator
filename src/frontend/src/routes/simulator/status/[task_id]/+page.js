// [task_id]/+page.js
export const load = async ({ params, fetch }) => {
    const { task_id } = params;
    const url = `http://127.0.0.1:8000/simulator/status/${task_id}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch data');
        const data = await response.json();
        console.log(data);
        console.log({data, error: null });
        return {data, error: null };
    } catch (error) {
        return {data: null, error: error.message };
    }
};
