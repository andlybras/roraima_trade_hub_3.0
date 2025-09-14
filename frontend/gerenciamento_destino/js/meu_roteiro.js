document.addEventListener('DOMContentLoaded', function() {
    
    const ROTEIRO_KEY = 'meuRoteiroDestinoRR';
    const slugsSalvos = JSON.parse(localStorage.getItem(ROTEIRO_KEY) || '[]');

    const painelCarregando = document.getElementById('painel-roteiro-carregando');
    const painelConteudo = document.getElementById('painel-roteiro-conteudo');
    const viewRoteiroCheio = document.getElementById('roteiro-cheio-view');
    const viewRoteiroVazio = document.getElementById('roteiro-vazio-view');
    const listaParadasContainer = document.getElementById('lista-paradas-container');
    const btnLimparRoteiro = document.querySelector('.btn-limpar-roteiro');
    const btnImprimirRoteiro = document.querySelector('.btn-imprimir-roteiro'); // Pega o novo botão

    if (slugsSalvos.length === 0) {
        painelCarregando.style.display = 'none';
        painelConteudo.style.display = 'block';
        viewRoteiroCheio.style.display = 'none';
        viewRoteiroVazio.style.display = 'block';
    } else {
        fetch('/destino-roraima/api/dados-roteiro/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ slugs: slugsSalvos })
        })
        .then(response => response.json())
        .then(data => {
            const pontos = data.pontos || [];
            renderRoteiro(pontos);
        })
        .catch(error => {
            console.error("Erro ao buscar dados do roteiro:", error);
            listaParadasContainer.innerHTML = "<p>Ocorreu um erro ao carregar seu roteiro.</p>";
        });
    }

    function renderRoteiro(pontos) {
        painelCarregando.style.display = 'none';
        painelConteudo.style.display = 'block';

        if (pontos.length === 0) {
            viewRoteiroCheio.style.display = 'none';
            viewRoteiroVazio.style.display = 'block';
            return;
        }

        viewRoteiroCheio.style.display = 'block';
        viewRoteiroVazio.style.display = 'none';

        listaParadasContainer.innerHTML = '';
        pontos.forEach((ponto, index) => {
            const paradaHTML = `
                <div class="parada-item">
                    <div class="parada-numero">${index + 1}</div>
                    <div class="parada-conteudo">
                        <h4>${ponto.titulo}</h4>
                        <p>${ponto.descricao_curta}</p>
                        <a href="${ponto.detalhe_url}">Saber Mais &rarr;</a>
                    </div>
                </div>
            `;
            listaParadasContainer.innerHTML += paradaHTML;
        });

        const mapa = L.map('mapa-meu-roteiro');
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(mapa);

        const geoJsonData = {
            type: 'FeatureCollection',
            features: pontos.map(p => ({
                type: 'Feature',
                geometry: { type: 'Point', coordinates: [p.longitude, p.latitude] },
                properties: { titulo: p.titulo, detalhe_url: p.detalhe_url }
            }))
        };

        const pontosLayer = L.geoJSON(geoJsonData, {
            onEachFeature: (feature, layer) => {
                layer.bindPopup(`<b>${feature.properties.titulo}</b>`);
            }
        }).addTo(mapa);

        setTimeout(() => {
            if(pontosLayer.getBounds().isValid()) {
                mapa.fitBounds(pontosLayer.getBounds(), { padding: [50, 50] });
            } else {
                mapa.setView([2.82, -60.67], 9);
            }
        }, 200);
    }

    btnLimparRoteiro.addEventListener('click', function() {
        if (confirm('Você tem certeza que deseja limpar todo o seu roteiro?')) {
            localStorage.removeItem(ROTEIRO_KEY);
            window.location.reload();
        }
    });

    if (btnImprimirRoteiro) {
        btnImprimirRoteiro.classList.add('btn-limpar-roteiro');
        btnImprimirRoteiro.style.backgroundColor = '#2A9D8F'; // Cor Verde

        btnImprimirRoteiro.addEventListener('click', function() {
            window.print();
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});