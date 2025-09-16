document.addEventListener('DOMContentLoaded', function() {
    const mapaContainer = document.getElementById('mapa');
    if (!mapaContainer) return;

    const pontosDataElement = document.getElementById('pontos-data');
    if (!pontosDataElement) return;

    const pontosData = JSON.parse(pontosDataElement.textContent);
    
    // Inicia o mapa
    const mapa = L.map('mapa').setView([2.8235, -60.6758], 9);
    setTimeout(function() { mapa.invalidateSize(); }, 100);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mapa);

    const markersLayer = new L.FeatureGroup().addTo(mapa);
    const allMarkers = [];

    function createIcon(iconUrl) {
        return L.icon({
            iconUrl: iconUrl,
            iconSize: [38, 38],
            iconAnchor: [19, 38],
            popupAnchor: [0, -42],
            shadowUrl: '{% static "leaflet/images/marker-shadow.png" %}', 
            shadowSize: [41, 41]
        });
    }

    pontosData.features.forEach(feature => {
        const props = feature.properties;
        let markerOptions = {};
        if (props.icone_url) {
            markerOptions.icon = L.icon({
                iconUrl: props.icone_url,
                iconSize: [38, 38],
                iconAnchor: [19, 38],
                popupAnchor: [0, -42],
                shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png', 
                shadowAnchor: [12, 41]
            });
        }
        
        const marker = L.marker([feature.geometry.coordinates[1], feature.geometry.coordinates[0]], markerOptions);

        marker.feature = feature;

        let popupContent = `
            <div class="popup-ponto-interesse">
                ${props.imagem_url ? `<img src="${props.imagem_url}" alt="${props.titulo}">` : ''}
                <div class="popup-ponto-interesse-conteudo">
                    <h3>${props.titulo}</h3>
                    <p>${props.descricao_curta}</p>
                    <a href="${props.detalhe_url}">Ver Detalhes</a>
                    <a href="#" class="btn-add-roteiro" data-slug="${props.slug}">Adicionar ao Roteiro</a>
                </div>
            </div>
        `;
        marker.bindPopup(popupContent);
        allMarkers.push(marker);
    });

    function filtrarMarcadores(categoriaSlug) {
        markersLayer.clearLayers(); 
        
        allMarkers.forEach(marker => {
            if (categoriaSlug === 'todos' || marker.feature.properties.categoria_slug === categoriaSlug) {
                markersLayer.addLayer(marker); 
            }
        });
    }

    filtrarMarcadores('todos');

    if (markersLayer.getLayers().length > 0) {
        mapa.fitBounds(markersLayer.getBounds(), { padding: [50, 50] });
    }

    const filtroBotoes = document.querySelectorAll('.filtro-mapa-btn');
    filtroBotoes.forEach(btn => {
        btn.addEventListener('click', function() {
            filtroBotoes.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const categoriaSlug = this.dataset.categoriaSlug;
            filtrarMarcadores(categoriaSlug);
        });
    });
});