const socket = io();
const playerId = "{{ session.player_id }}";

socket.on('connect', () => {
    console.log('Подключен к игре');
    socket.emit('join', { player_id: playerId });
});

// Ход противника
socket.on('move', (data) => {
    console.log(data);
    create_cell(data['row'], data['col'], 255, 0, 0, 0.8);
    renderBoard(data['board']);
});

function handleClick(row, col) {
    // Отправляем запрос на сервер для получения доступных ходов
    fetch(`/moves?row=${row}&col=${col}`)
        .then(response => response.json())
        .then(data => {
            handleData(data, row, col);
        })
        .catch(error => console.error('Error fetching moves:', error));
}

function handleData(data, row, col) {
    document.querySelectorAll('.cell').forEach(cell => cell.classList.remove('highlight'));

    if ("moves" in data) {
        data['moves'].forEach(([r, c]) => {
            const cell = document.querySelector(`.cell[data-row="${r}"][data-col="${c}"]`);
            if (cell) {
                cell.classList.add('highlight');
            }
        });
    } else if ("board" in data) {
        renderBoard(data['board']);

        create_cell(row, col, 0, 255, 0, 0.8);
    }
}

function create_cell(row, col, r, g, b, a) {
    const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
    if (!cell) return;

    // Получаем контейнер для индикаторов
    const indicatorsContainer = document.getElementById("indicators-container");

    // Получаем позицию клетки
    const cellRect = cell.getBoundingClientRect();
    const boardRect = document.getElementById("chessboard").getBoundingClientRect();

    // Создаем контейнер для индикатора
    const indicator = document.createElement("div");
    indicator.classList.add("loading-indicator");
    indicator.style.stroke = `rgba(${r}, ${g}, ${b}, ${a})`;

    // Позиционируем индикатор в контейнере, соответствуя клетке
    indicator.style.left = `${cellRect.left - boardRect.left}px`;
    indicator.style.top = `${cellRect.top - boardRect.top}px`;

    // Создаем SVG-кольцо
    indicator.innerHTML = `
        <svg viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45"></circle>
        </svg>
    `;

    // Добавляем индикатор в контейнер (НЕ в саму клетку)
    indicatorsContainer.appendChild(indicator);

    // Удаляем этот индикатор через 5 секунд
    setTimeout(() => {
        indicator.remove();
    }, 5000);
}

const pieceSymbols = {
    "K": "&#9812;", "Q": "&#9813;", "R": "&#9814;", "B": "&#9815;", "N": "&#9816;", "P": "&#9817;",
    "k": "&#9818;", "q": "&#9819;", "r": "&#9820;", "b": "&#9821;", "n": "&#9822;", "p": "&#9823;"
};

function renderBoard(board) {
    const boardElement = document.getElementById("chessboard");
    boardElement.innerHTML = "";
    
    board.forEach((row, rowIndex) => {
        const rowDiv = document.createElement("div");
        rowDiv.classList.add("row");
        
        row.forEach((cell, colIndex) => {
            const cellDiv = document.createElement("div");
            cellDiv.classList.add("cell", (rowIndex + colIndex) % 2 === 0 ? "white" : "black");
            cellDiv.dataset.row = rowIndex;
            cellDiv.dataset.col = colIndex;
            cellDiv.onclick = () => handleClick(rowIndex, colIndex);
            
            if (cell) {
                const pieceSpan = document.createElement("span");
                pieceSpan.classList.add("piece");
                pieceSpan.innerHTML = pieceSymbols[cell] || "";
                cellDiv.appendChild(pieceSpan);
            }
            
            rowDiv.appendChild(cellDiv);
        });
        
        boardElement.appendChild(rowDiv);
    });
}

onload = () => {
    var board = JSON.parse('{{ board | tojson }}');
    renderBoard(board);
}