const API_BASE = '/api';

// Estado de la aplicación
let currentTab = 'live';
let teams = [];
let matches = {
    live: [],
    scheduled: [],
    finished: []
};

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadTeams();
    loadMatches();
});

// Configurar event listeners
function setupEventListeners() {
    // Tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });

    // Botones
    document.getElementById('refreshBtn').addEventListener('click', loadMatches);
    document.getElementById('createMatchBtn').addEventListener('click', openMatchModal);

    // Modal
    document.querySelector('.close').addEventListener('click', closeMatchModal);
    document.getElementById('matchForm').addEventListener('submit', createMatch);

    // Cerrar modal al hacer clic fuera
    window.addEventListener('click', (e) => {
        const modal = document.getElementById('matchModal');
        if (e.target === modal) {
            closeMatchModal();
        }
    });
}

// Cambiar de tab
function switchTab(tabName) {
    currentTab = tabName;
    
    // Actualizar tabs activos
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
        if (tab.dataset.tab === tabName) {
            tab.classList.add('active');
        }
    });

    // Actualizar contenido
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');

    // Cargar datos según el tab
    if (tabName === 'teams') {
        renderTeams();
    }
}

// Cargar selecciones
async function loadTeams() {
    try {
        const response = await fetch(`${API_BASE}/selecciones/`);
        teams = await response.json();
        populateTeamSelects();
    } catch (error) {
        console.error('Error loading teams:', error);
        showError('Error al cargar las selecciones');
    }
}

// Llenar selects de equipos
function populateTeamSelects() {
    const localSelect = document.getElementById('localTeam');
    const visitorSelect = document.getElementById('visitorTeam');
    
    const options = teams.map(team => 
        `<option value="${team.id}">${team.pais}</option>`
    ).join('');
    
    localSelect.innerHTML = '<option value="">Seleccionar equipo local</option>' + options;
    visitorSelect.innerHTML = '<option value="">Seleccionar equipo visitante</option>' + options;
}

// Cargar partidos
async function loadMatches() {
    try {
        // Cargar partidos en vivo
        const liveResponse = await fetch(`${API_BASE}/partidos/en-vivo`);
        matches.live = await liveResponse.json();

        // Cargar partidos programados
        const scheduledResponse = await fetch(`${API_BASE}/partidos/?estado=programado`);
        matches.scheduled = await scheduledResponse.json();

        // Cargar partidos finalizados
        const finishedResponse = await fetch(`${API_BASE}/partidos/?estado=finalizado`);
        matches.finished = await finishedResponse.json();

        renderMatches();
    } catch (error) {
        console.error('Error loading matches:', error);
        showError('Error al cargar los partidos');
    }
}

// Renderizar partidos
function renderMatches() {
    renderLiveMatches();
    renderScheduledMatches();
    renderFinishedMatches();
}

function renderLiveMatches() {
    const container = document.getElementById('liveMatches');
    
    if (matches.live.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">EN VIVO</div>
                <p>No hay partidos en vivo</p>
            </div>
        `;
        return;
    }

    container.innerHTML = matches.live.map(match => createMatchCard(match, true)).join('');
}

function renderScheduledMatches() {
    const container = document.getElementById('scheduledMatches');
    
    if (matches.scheduled.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">PROGRAMADO</div>
                <p>No hay partidos programados</p>
            </div>
        `;
        return;
    }

    container.innerHTML = matches.scheduled.map(match => createMatchCard(match, false)).join('');
}

function renderFinishedMatches() {
    const container = document.getElementById('finishedMatches');
    
    if (matches.finished.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">FINALIZADO</div>
                <p>No hay partidos finalizados</p>
            </div>
        `;
        return;
    }

    container.innerHTML = matches.finished.map(match => createMatchCard(match, false)).join('');
}

function createMatchCard(match, isLive) {
    const localTeam = match.seleccion_local || { pais: 'Equipo Local', bandera: 'N/A' };
    const visitorTeam = match.seleccion_visitante || { pais: 'Equipo Visitante', bandera: 'N/A' };
    
    const statusClass = match.estado === 'en_juego' ? 'status-live' : 
                       match.estado === 'programado' ? 'status-scheduled' : 'status-finished';
    
    const statusText = match.estado === 'en_juego' ? 'EN VIVO' : 
                      match.estado === 'programado' ? 'PROGRAMADO' : 'FINALIZADO';

    const scoreInputs = isLive ? `
        <div class="match-score">
            <input type="number" class="score-input" id="local-${match.id}" value="${match.gol_local || 0}" min="0">
            <span>-</span>
            <input type="number" class="score-input" id="visitor-${match.id}" value="${match.gol_visitante || 0}" min="0">
        </div>
    ` : `
        <div class="match-score">
            <span>${match.gol_local || 0}</span>
            <span>-</span>
            <span>${match.gol_visitante || 0}</span>
        </div>
    `;

    const actionButtons = isLive ? `
        <button class="btn btn-success" onclick="updateScore(${match.id})">Actualizar</button>
        <button class="btn btn-warning" onclick="finishMatch(${match.id})">Finalizar</button>
    ` : match.estado === 'programado' ? `
        <button class="btn btn-primary" onclick="startMatch(${match.id})">Iniciar</button>
    ` : '';

    return `
        <div class="match-card">
            <div class="match-header">
                <span class="match-status ${statusClass}">${statusText}</span>
                <small>${formatDate(match.fecha_hora)}</small>
            </div>
            <div class="match-teams">
                <div class="team">
                    <div class="team-flag">${localTeam.bandera || 'N/A'}</div>
                    <div class="team-name">${localTeam.pais}</div>
                </div>
                ${scoreInputs}
                <div class="team">
                    <div class="team-flag">${visitorTeam.bandera || 'N/A'}</div>
                    <div class="team-name">${visitorTeam.pais}</div>
                </div>
            </div>
            <div class="match-actions">
                ${actionButtons}
                <button class="btn btn-danger" onclick="deleteMatch(${match.id})">Eliminar</button>
            </div>
        </div>
    `;
}

// Renderizar selecciones
function renderTeams() {
    const container = document.getElementById('teamsList');
    
    if (teams.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">SIN REGISTROS</div>
                <p>No hay selecciones registradas</p>
            </div>
        `;
        return;
    }

    container.innerHTML = teams.map(team => `
        <div class="team-card">
            <div class="team-flag-large">${team.bandera || 'N/A'}</div>
            <div class="team-card-name">${team.pais}</div>
        </div>
    `).join('');
}

// Actualizar marcador
async function updateScore(matchId) {
    const localScore = document.getElementById(`local-${matchId}`).value;
    const visitorScore = document.getElementById(`visitor-${matchId}`).value;

    try {
        const response = await fetch(`${API_BASE}/partidos/${matchId}/marcador`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                gol_local: parseInt(localScore),
                gol_visitante: parseInt(visitorScore),
                estado: 'en_juego'
            })
        });

        if (response.ok) {
            loadMatches();
            showSuccess('Marcador actualizado correctamente');
        } else {
            showError('Error al actualizar el marcador');
        }
    } catch (error) {
        console.error('Error updating score:', error);
        showError('Error al actualizar el marcador');
    }
}

// Iniciar partido
async function startMatch(matchId) {
    try {
        const response = await fetch(`${API_BASE}/partidos/${matchId}/marcador`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                gol_local: 0,
                gol_visitante: 0,
                estado: 'en_juego'
            })
        });

        if (response.ok) {
            loadMatches();
            showSuccess('Partido iniciado correctamente');
        } else {
            showError('Error al iniciar el partido');
        }
    } catch (error) {
        console.error('Error starting match:', error);
        showError('Error al iniciar el partido');
    }
}

// Finalizar partido
async function finishMatch(matchId) {
    const localScore = document.getElementById(`local-${matchId}`).value;
    const visitorScore = document.getElementById(`visitor-${matchId}`).value;

    try {
        const response = await fetch(`${API_BASE}/partidos/${matchId}/marcador`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                gol_local: parseInt(localScore),
                gol_visitante: parseInt(visitorScore),
                estado: 'finalizado'
            })
        });

        if (response.ok) {
            loadMatches();
            showSuccess('Partido finalizado correctamente');
        } else {
            showError('Error al finalizar el partido');
        }
    } catch (error) {
        console.error('Error finishing match:', error);
        showError('Error al finalizar el partido');
    }
}

// Eliminar partido
async function deleteMatch(matchId) {
    if (!confirm('¿Estás seguro de eliminar este partido?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/partidos/${matchId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadMatches();
            showSuccess('Partido eliminado correctamente');
        } else {
            showError('Error al eliminar el partido');
        }
    } catch (error) {
        console.error('Error deleting match:', error);
        showError('Error al eliminar el partido');
    }
}

// Crear partido
async function createMatch(e) {
    e.preventDefault();

    const localTeam = document.getElementById('localTeam').value;
    const visitorTeam = document.getElementById('visitorTeam').value;
    const matchDate = document.getElementById('matchDate').value;

    if (!localTeam || !visitorTeam || !matchDate) {
        showError('Por favor completa todos los campos');
        return;
    }

    if (localTeam === visitorTeam) {
        showError('Los equipos deben ser diferentes');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/partidos/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                fk_id_seleccion_local: parseInt(localTeam),
                fk_id_seleccion_visitante: parseInt(visitorTeam),
                fecha_hora: matchDate,
                estado: 'programado',
                gol_local: 0,
                gol_visitante: 0
            })
        });

        if (response.ok) {
            closeMatchModal();
            loadMatches();
            showSuccess('Partido creado correctamente');
            document.getElementById('matchForm').reset();
        } else {
            showError('Error al crear el partido');
        }
    } catch (error) {
        console.error('Error creating match:', error);
        showError('Error al crear el partido');
    }
}

// Modal functions
function openMatchModal() {
    document.getElementById('matchModal').style.display = 'block';
}

function closeMatchModal() {
    document.getElementById('matchModal').style.display = 'none';
}

// Utilidades
function formatDate(dateString) {
    if (!dateString) return 'Fecha no definida';
    const date = new Date(dateString);
    return date.toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.textContent = message;
    document.querySelector('.content').prepend(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'error';
    successDiv.style.background = '#d4edda';
    successDiv.style.color = '#155724';
    successDiv.style.borderColor = '#c3e6cb';
    successDiv.textContent = message;
    document.querySelector('.content').prepend(successDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}
