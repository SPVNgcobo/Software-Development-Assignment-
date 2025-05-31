function showScreen(screen) {
  document.getElementById('surveyScreen').style.display = screen === 'survey' ? 'block' : 'none';
  document.getElementById('resultsScreen').style.display = screen === 'results' ? 'block' : 'none';
  if (screen === 'results') showResults();
}

function calculateAge(dob) {
  const birthDate = new Date(dob);
  const today = new Date();
  let age = today.getFullYear() - birthDate.getFullYear();
  const m = today.getMonth() - birthDate.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  return age;
}

function submitSurvey() {
  const fullname = document.getElementById('fullname').value.trim();
  const email = document.getElementById('email').value.trim();
  const contact = document.getElementById('contact').value.trim();
  const dob = document.getElementById('birthDate').value;

  if (!fullname || !email || !contact || !dob) {
    alert('Please complete all personal details.');
    return;
  }

  const age = calculateAge(dob);
  if (age < 5 || age > 120) {
    alert('Age must be between 5 and 120 based on your date of birth.');
    return;
  }

  const food = Array.from(document.querySelectorAll('input[type=checkbox]:checked')).map(cb => cb.value);
  if (food.length === 0) {
    alert('Please select at least one favourite food.');
    return;
  }

  const ratings = {};
  for (let category of ['eatout', 'movies', 'tv', 'radio']) {
    const selected = document.querySelector(`input[name=${category}]:checked`);
    if (!selected) {
      alert(`Please rate: ${category}`);
      return;
    }
    ratings[category] = parseInt(selected.value);
  }

  const payload = {
    fullname,
    email,
    contact,
    date: dob,
    age,
    food,
    ...ratings
  };

  fetch('http://127.0.0.1:5000/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(response => {
    if (!response.ok) return response.json().then(err => Promise.reject(err.message));
    return response.json();
  })
  .then(data => {
    alert(data.message || 'Submitted!');
    location.reload();
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Failed to submit: ' + error);
  });
}

function showResults() {
  fetch('http://127.0.0.1:5000/results')
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById('resultsScreen');
      if (!data || data.total === 0 || data.message === 'No Surveys Available') {
        container.querySelector('tbody').innerHTML = '<tr><td colspan="2">No Surveys Available</td></tr>';
        return;
      }

      document.getElementById('totalSurveys').textContent = data.total;
      document.getElementById('averageAge').textContent = data.avg_age;
      document.getElementById('oldestAge').textContent = data.oldest;
      document.getElementById('youngestAge').textContent = data.youngest;
      document.getElementById('pizzaPercentage').textContent = data.pizza_percent + '%';
      document.getElementById('eatOutAvg').textContent = data.eatout_avg;
    })
    .catch(error => {
      console.error('Error fetching results:', error);
      const tbody = document.querySelector('#resultsScreen tbody');
      tbody.innerHTML = '<tr><td colspan="2">Error fetching results.</td></tr>';
    });
}

showScreen('survey');