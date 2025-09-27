// Configuração da API - ALTERE AQUI PARA SUA URL
const API_BASE ="http://185.137.122.137:3010"; // ou sua URL do projeto

let currentUser = null;

// Função para mostrar alertas
function showAlert(containerId, message, type = "error") {
    const container = document.getElementById(containerId);
    container.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    setTimeout(() => {
        container.innerHTML = "";
    }, 5000);

// Função para fazer requisições à API
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
            ...options,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || "Erro na requisição");
        }

        return data;
    } catch (error) {
        console.error("Erro na API:", error);
        throw error;
    }
}

// Navegação entre telas
function showLogin() {
    document.getElementById("loginForm").classList.add("active");
    document.getElementById("registerForm").classList.remove("active");
    document.getElementById("dashboard").classList.remove("active");
}

function showRegister() {
    document.getElementById("loginForm").classList.remove("active");
    document.getElementById("registerForm").classList.add("active");
    document.getElementById("dashboard").classList.remove("active");
}

function showDashboard() {
    document.getElementById("loginForm").classList.remove("active");
    document.getElementById("registerForm").classList.remove("active");
    document.getElementById("dashboard").classList.add("active");
    loadUsers();
}

// Login
document
.getElementById("loginFormElement")
.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const senha = document.getElementById("loginSenha").value;

    try {
        const response = await apiRequest("/api/login',{
            method: 'POST',
            body: JSON.stringify({ email, senha }),
        });

        currentUser = response.usuario;
        showAlert('loginAlert', 'Login realizado com sucesso!', 'success');

        setTimeout(() => {
            showLogin();
            document.getElementById('registerFormElement').reset();
        }, 2000);
                
    } catch (error) {
        showAlert('registerAlert', error.message);
    }
});

// Mostrar informacoes do usuario logado
function displayCurrentUser() {
    if (currentUser) {
        document.getElementById('currentUserInfo').innerHTML = `
            <p><strong>Nome:</strong> ${currentUser.nome}</p>
            <p><strong>Email:</strong> ${currentUser.email}</p>
            <p><strong>Cadastro:</strong> ${new Date(currentUser.dataCadastro).toLocaleDateString('pt-br')}</p>

            `;
    }
}

// Carregar lista de usuários
async function loadUsers() {
    try {
        const users = await apiRequest("/api/usuarios");
        const userList = document.getElementById("userList");
        

    if (response.usuarios && response.usuarios.length > 0) {
        usersList.innerHTML = response.usuarios.map(user => `
            <div class="user-item">
            <strong>${user.nome}</strong><br>
                <small>${user.email}</small><br>
                <small>Cadastro em: ${new Date(user.dataCadastro).toLocaleDateString('pt-br')}</small>
            </div>
        `).join('');
    } else {
        usersList.innerHTML = '<p>Nenhum usuário encontrado.</p>';
    }
    } catch (error) {
        document.getElementById('usersList').innerHTML =
            '<p>Erro ao carregar usuários:' + error.message +'</p>';
    }
}

// Logout
function logout() {
    currentUser = null;
    document.getElementById('loginFormElement').reset();
    document.getElementById('registerFormElement').reset();
    showLogin();
}

// Verificar se API está disponível ao carregar a página
window.addEventListener('load', async () => {
    try {
        await apiRequest('/health');
        console.log('API conectada com sucesso!');
    } catch (error) {
        showAlert('loginAlert',
            'Erro ao conectar com a API (${API_BASE}). Verifique se o servidor está rodando.'
        );
    }
});