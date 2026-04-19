fetch('http://nv-service-9f8921efeca6d41f4cda2558a6b29bed:8500/test', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ test: 'hello backend' })
})
  .then(res => res.json())
  .then(data => {
    console.log('Response:', data);
  })
  .catch(err => {
    console.error('Error:', err);
  });