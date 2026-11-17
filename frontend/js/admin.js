document.getElementById('btn-logout').addEventListener('click', async () => {
    await fetchAPI('/logout', 'POST');
    localStorage.removeItem('token');
    window.location.href = 'login.html';
});

async function carregarAdminTutores() {
    const res = await fetchAPI('/tutores');
    const tbody = document.getElementById('tabelaAdminTutores');
    const selectTutor = document.getElementById('petTutorId');
    tbody.innerHTML = ''; selectTutor.innerHTML = '<option value="">Selecione um tutor...</option>';
    if (res.success) {
        const tutores = res.data.tutores;
        tutores.forEach(t => {
            tbody.innerHTML += `<tr><td>${t.id}</td><td>${t.nome}</td><td>${t.email}</td><td>${t.telefone}</td>
                <td><button class="btn-small btn-edit" onclick="editarTutor(${t.id}, '${t.nome}', '${t.email}', '${t.telefone}')">Editar</button>
                <button class="btn-small btn-danger" onclick="excluirTutor(${t.id})">Excluir</button></td></tr>`;
            selectTutor.innerHTML += `<option value="${t.id}">${t.nome}</option>`;
        });
    }
}

document.getElementById('formTutor').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('tutorId').value;
    const body = { nome: document.getElementById('tutorNome').value, email: document.getElementById('tutorEmail').value, telefone: document.getElementById('tutorTelefone').value };
    const res = await fetchAPI(id ? `/tutores/${id}` : '/tutores', id ? 'PUT' : 'POST', body);
    if (res.success) { alert('Tutor salvo!'); resetFormTutor(); carregarAdminTutores(); } else alert('Erro: ' + JSON.stringify(res.data));
});

function editarTutor(id, nome, email, telefone) {
    document.getElementById('tutorId').value = id; document.getElementById('tutorNome').value = nome;
    document.getElementById('tutorEmail').value = email; document.getElementById('tutorTelefone').value = telefone;
    document.getElementById('btnCancelarTutor').style.display = 'inline-block';
}

async function excluirTutor(id) {
    if (confirm('Excluir este tutor?')) {
        const res = await fetchAPI(`/tutores/${id}`, 'DELETE');
        if (res.success) carregarAdminTutores(); else alert('Erro: ' + JSON.stringify(res.data));
    }
}

function resetFormTutor() { document.getElementById('formTutor').reset(); document.getElementById('tutorId').value = ''; document.getElementById('btnCancelarTutor').style.display = 'none'; }
document.getElementById('btnCancelarTutor').addEventListener('click', resetFormTutor);


async function carregarAdminPets() {
    const res = await fetchAPI('/pets');
    const tbody = document.getElementById('tabelaAdminPets');
    tbody.innerHTML = '';
    if (res.success) {
        res.data.pets.forEach(p => {
            tbody.innerHTML += `<tr><td>${p.id}</td><td>${p.nome}</td><td>${p.especie}</td><td>${p.tutor_nome || p.tutor_id}</td>
                <td><button class="btn-small btn-edit" onclick="editarPet(${p.id}, '${p.nome}', '${p.especie}', '${p.raca || ''}', '${p.data_nascimento}', ${p.peso_kg}, ${p.tutor_id})">Editar</button>
                <button class="btn-small btn-danger" onclick="excluirPet(${p.id})">Excluir</button></td></tr>`;
        });
    }
}

document.getElementById('formPet').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('petId').value;
    const body = {
        nome: document.getElementById('petNome').value, especie: document.getElementById('petEspecie').value,
        raca: document.getElementById('petRaca').value || null, data_nascimento: document.getElementById('petData').value,
        peso_kg: parseFloat(document.getElementById('petPeso').value), tutor_id: parseInt(document.getElementById('petTutorId').value)
    };
    const res = await fetchAPI(id ? `/pets/${id}` : '/pets', id ? 'PUT' : 'POST', body);
    if (res.success) { alert('Pet salvo!'); resetFormPet(); carregarAdminPets(); } else alert('Erro: ' + JSON.stringify(res.data));
});

function editarPet(id, nome, especie, raca, data, peso, tutorId) {
    document.getElementById('petId').value = id; document.getElementById('petNome').value = nome;
    document.getElementById('petEspecie').value = especie; document.getElementById('petRaca').value = raca;
    document.getElementById('petData').value = data; document.getElementById('petPeso').value = peso;
    document.getElementById('petTutorId').value = tutorId; document.getElementById('btnCancelarPet').style.display = 'inline-block';
}

async function excluirPet(id) {
    if (confirm('Excluir este pet?')) {
        const res = await fetchAPI(`/pets/${id}`, 'DELETE');
        if (res.success) carregarAdminPets(); else alert('Erro: ' + JSON.stringify(res.data));
    }
}

function resetFormPet() { document.getElementById('formPet').reset(); document.getElementById('petId').value = ''; document.getElementById('btnCancelarPet').style.display = 'none'; }
document.getElementById('btnCancelarPet').addEventListener('click', resetFormPet);

document.addEventListener('DOMContentLoaded', () => { carregarAdminTutores(); carregarAdminPets(); });