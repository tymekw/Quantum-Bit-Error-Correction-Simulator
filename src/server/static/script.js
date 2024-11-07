console.log('Script loaded');

function toggleOptionalField() {
    const eve_machines_div = document.getElementById('eve_machines_div');
    const isEveChecked = document.getElementById('isEve').checked;
    eve_machines_div.style.display = isEveChecked ? 'block' : 'none';
}

async function submitForm() {
    console.log('Form submission started');
    const form = document.getElementById('simulationForm');
    const formData = new FormData(form);

    const data = {
        range_of_inputs_per_neuron: {
            start: parseInt(formData.get('range_of_inputs_per_neuron_start')),
            stop: parseInt(formData.get('range_of_inputs_per_neuron_stop')),
            step: parseInt(formData.get('range_of_inputs_per_neuron_step'))
        },
        range_of_neurons_in_hidden_layer: {
            start: parseInt(formData.get('range_of_neurons_in_hidden_layer_start')),
            stop: parseInt(formData.get('range_of_neurons_in_hidden_layer_stop')),
            step: parseInt(formData.get('range_of_neurons_in_hidden_layer_step'))
        },
        weights_range: formData.get('weights_range').split(',').map(Number),
        qber_values: formData.get('qber_values').split(',').map(Number),
        eve: formData.get('eve_machines') ? parseInt(formData.get('eve_machines')) || 0 : 0
    };

    try {
        const response = await fetch('/send_params', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        console.log('Response status:', response.status);
        try {
            if (response.redirected) {
                console.log('redirect:', response.url);

                window.location.href = response.url;
            }
        } catch (error){
            console.error('shit')
        }
    } catch (error) {
        console.error('Error submitting form:', error);
        alert('Error submitting form');
    }
}