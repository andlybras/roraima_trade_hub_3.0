document.addEventListener('DOMContentLoaded', function() {
    const contadorElement = document.getElementById('roteiro-flutuante-contador');
    const botaoFlutuante = document.getElementById('roteiro-flutuante-btn');

    function getRoteiro() {
        const roteiroSalvo = localStorage.getItem('meuRoteiroDestinoRR');
        return roteiroSalvo ? JSON.parse(roteiroSalvo) : [];
    }

    function saveRoteiro(roteiro) {
        localStorage.setItem('meuRoteiroDestinoRR', JSON.stringify(roteiro));
    }

    function atualizarContadorEBotao() {
        if (!contadorElement || !botaoFlutuante) return;

        const roteiro = getRoteiro();
        const totalItens = roteiro.length;

        contadorElement.textContent = totalItens;

        if (totalItens > 0) {
            contadorElement.classList.add('visible');
            botaoFlutuante.classList.add('visible'); 
        } else {
            contadorElement.classList.remove('visible');
            botaoFlutuante.classList.remove('visible'); 
        }
    }

    function atualizarStatusBotoes() {
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

    document.addEventListener('click', function(event) {
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
            atualizarContadorEBotao();
            atualizarStatusBotoes();
        }
    });

    atualizarContadorEBotao();
    atualizarStatusBotoes();
});