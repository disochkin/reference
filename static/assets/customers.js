const entities = [
    { title: 'Первая сущность', description: 'Описание первой сущности.', imageUrl: 'https://via.placeholder.com/150' },
    { title: 'Вторая сущность', description: 'Описание второй сущности.', imageUrl: 'https://via.placeholder.com/150' },
    { title: 'Третья сущность', description: 'Описание третьей сущности.', imageUrl: 'https://via.placeholder.com/150' },
    { title: 'Четвертая сущность', description: 'Описание четвертой сущности.', imageUrl: 'https://via.placeholder.com/150' },
];

// Функция для вывода плиток
async function renderTiles() {
    const res = await fetch(`/api/customer`);
    const data = await res.json();
    //document.getElementById("name").value = data.name;


    const container = document.querySelector('.tile-grid');

    data.forEach(entity => {
        const tile = `
            <article class="tile-item">
  //              <img src="${entity.imageUrl}" alt="${entity.title}">
                <h2>${entity.name}</h2>
              //  <p>${entity.description}</p>
            </article>
        `;
        container.insertAdjacentHTML('beforeend', tile);
    });
}

renderTiles();