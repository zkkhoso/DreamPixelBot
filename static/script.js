async function fetchScores() {
  try {
    const res = await fetch('/api/scores');
    const json = await res.json();
    renderMatches(json);
  } catch (err) {
    console.error(err);
    document.getElementById('matches').innerHTML = `<li class="list-group-item list-group-item-danger">${err}</li>`;
  }
}

function safe(val) {
  return val === undefined || val === null ? '' : val;
}

function renderMatches(data) {
  const list = document.getElementById('matches');
  list.innerHTML = '';

  if (!data || data.status !== 'success' || !Array.isArray(data.data) || data.data.length === 0) {
    list.innerHTML = '<li class="list-group-item">No live matches at the moment.</li>';
    return;
  }

  data.data.forEach(match => {
    const li = document.createElement('li');
    li.className = 'list-group-item bg-secondary text-white mb-3';

    const scores = (match.score || [])
      .map(s => `${safe(s.inning)}: ${safe(s.r)}/${safe(s.w)} (${safe(s.o)} ov)`) 
      .join('<br>');

    li.innerHTML = `
      <h5>${safe(match.name)}</h5>
      <p>Status: <strong>${safe(match.status)}</strong></p>
      <p>${scores}</p>
    `;
    list.appendChild(li);
  });
}

document.getElementById('refreshBtn').addEventListener('click', fetchScores);

// Initial load and auto-refresh every minute
fetchScores();
setInterval(fetchScores, 60000);