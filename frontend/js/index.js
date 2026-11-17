async function carregarTutores() {
    const res = await fetchAPI('/tutores');
    const tbody = document.getElementById('tabelaTutores');
    tbody.innerHTML = '';
    if (res.success && res.data) {
        const tutores = res.data.lista || res.data; 
        if (tutores.length === 0) return tbody.innerHTML = '<tr><td colspan="4">Nenhum tutor registado.</td></tr>';
        tutores.forEach(t => tbody.innerHTML += `<tr><td>${t.id}</td><td>${t.nome}</td><td>${t.email}</td><td>${t.telefone}</td></tr>`);
    } else tbody.innerHTML = '<tr><td colspan="4" style="color:red;">Erro ao carregar tutores.</td></tr>';
}

async function carregarPets(especie = '') {
    const tbody = document.getElementById('tabelaPets');
    tbody.innerHTML = '<tr><td colspan="5">A carregar...</td></tr>';
    const endpoint = especie ? `/pets?especie=${encodeURIComponent(especie)}` : '/pets';
    const res = await fetchAPI(endpoint);
    tbody.innerHTML = '';
    if (res.success && res.data) {
        if (res.data.length === 0) return tbody.innerHTML = '<tr><td colspan="5">Nenhum pet encontrado.</td></tr>';
        res.data.forEach(p => tbody.innerHTML += `<tr><td>${p.id}</td><td>${p.nome}</td><td>${p.especie}</td><td>${p.raca || '-'}</td><td>${p.nome_tutor || p.tutor_id}</td></tr>`);
    } else tbody.innerHTML = '<tr><td colspan="5" style="color:red;">Erro ao carregar pets.</td></tr>';
}

document.getElementById('btnFiltrarPets').addEventListener('click', () => {
    carregarPets(document.getElementById('filtroEspecie').value);
});

document.addEventListener('DOMContentLoaded', () => {
    carregarTutores();
    carregarPets();
});