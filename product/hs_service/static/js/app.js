document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('classify-form')
  const output = document.getElementById('json-output')

  form.addEventListener('submit', async (ev) => {
    ev.preventDefault()
    output.textContent = 'Classifying...'
    const fd = new FormData(form)
    const payload = Object.fromEntries(fd.entries())
    
    // Convert weight_kg to number if present and not empty
    if (payload.weight_kg && payload.weight_kg.trim()) {
      payload.weight_kg = parseFloat(payload.weight_kg)
    } else {
      delete payload.weight_kg
    }
    
    // Remove empty strings for optional fields
    Object.keys(payload).forEach(key => {
      if (payload[key] === '') delete payload[key]
    })
    
    try {
      const res = await fetch('/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      const data = await res.json()
      output.textContent = JSON.stringify(data, null, 2)
    } catch (err) {
      output.textContent = 'Error: ' + err.message
    }
  })
})

