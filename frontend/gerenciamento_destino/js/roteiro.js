// frontend/gerenciamento_destino/js/roteiro.js

document.addEventListener('DOMContentLoaded', function() {
    const ROTEIRO_KEY = 'meuRoteiroDestinoRR';
    const contadorElement = document.getElementById('roteiro-contador');

    // --- Funções Auxiliares (sem alterações) ---
    function getRoteiro() {
        const roteiroSalvo = localStorage.getItem(ROTEIRO_KEY);
        return roteiroSalvo ? JSON.parse(roteiroSalvo) : [];
    }
    function saveRoteiro(roteiro) {
        localStorage.setItem(ROTEIRO_KEY, JSON.stringify(roteiro));
    }

    // --- Funções Principais (sem alterações) ---
    function atualizarContador() {
        if (!contadorElement) return;
        const roteiro = getRoteiro();
        const totalItens = roteiro.length;
        contadorElement.textContent = totalItens;
        if (totalItens > 0) {
            contadorElement.classList.add('visible');
        } else {
            contadorElement.classList.remove('visible');
        }
    }

    // Função para atualizar a aparência de TODOS os botões visíveis na página
    function atualizarTodosOsBotoesVisiveis() {
        const roteiro = getRoteiro();
        const botoesAdicionar = document.querySelectorAll('.btn-add-roteiro');
        botoesAdicionar.forEach(botao => {
            const slugDoPonto = botao.dataset.slug;
            if (roteiro.includes(slugDoPonto)) {
                botao.classList.add('active');
                botao.textContent = 'Remover do Roteiro';
            } else {
                botao.classList.remove('active');
                botao.textContent = 'Adicionar ao Roteiro';
            }
        });
    }

    // --- LÓGICA DE EVENTOS COM DELEGAÇÃO ---
    // O "Gerente" (document) ouve todos os cliques
    document.addEventListener('click', function(event) {
        
        // Verifica se o alvo do clique é um botão de roteiro
        if (event.target.matches('.btn-add-roteiro')) {
            event.preventDefault(); 
            
            const botaoClicado = event.target;
            const slugDoPonto = botaoClicado.dataset.slug;
            let roteiro = getRoteiro();

            if (roteiro.includes(slugDoPonto)) {
                roteiro = roteiro.filter(slug => slug !== slugDoPonto);
            } else {
                roteiro.push(slugDoPonto);
            }

            saveRoteiro(roteiro);
            atualizarContador();
            
            // Atualiza a aparência de todos os botões, incluindo o que foi clicado
            // e outros botões para o mesmo ponto que possam estar na página.
            atualizarTodosOsBotoesVisiveis();
        }
    });

    // --- Inicialização ---
    atualizarContador();
    atualizarTodosOsBotoesVisiveis();
});