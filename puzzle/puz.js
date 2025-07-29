let level = 1;
let playerName = '';
let board = [];
const boardSize = 4;
const totalLevels = 30;

function startGame() {
  playerName = document.getElementById('playerName').value;
  if (!playerName) {
    alert("Please enter your name.");
    return;
  }
  document.getElementById('startScreen').style.display = 'none';
  document.getElementById('gameScreen').style.display = 'block';
  document.getElementById('showName').innerText = playerName;
  loadLevel();
}
// Existing game logic here...

// 👇 Add this at the bottom to listen for Enter key
document.getElementById("playerName").addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    startGame();
  }
});


function loadLevel() {
  document.getElementById('level').innerText = level;
  initBoard();
  renderBoard();
}

function initBoard() {
  board = [...Array(boardSize * boardSize - 1).keys()].map(x => x + 1);
  board.push(null);
  shuffle(board, level * 5);
}

function shuffle(arr, moves) {
  for (let i = 0; i < moves; i++) {
    let emptyIndex = arr.indexOf(null);
    let neighbors = getNeighborIndices(emptyIndex);
    let swapWith = neighbors[Math.floor(Math.random() * neighbors.length)];
    [arr[emptyIndex], arr[swapWith]] = [arr[swapWith], arr[emptyIndex]];
  }
}

function getNeighborIndices(index) {
  const row = Math.floor(index / boardSize);
  const col = index % boardSize;
  const moves = [];
  if (row > 0) moves.push(index - boardSize);
  if (row < boardSize - 1) moves.push(index + boardSize);
  if (col > 0) moves.push(index - 1);
  if (col < boardSize - 1) moves.push(index + 1);
  return moves;
}

function renderBoard() {
  const boardDiv = document.getElementById('board');
  boardDiv.innerHTML = '';
  board.forEach((num, i) => {
    const div = document.createElement('div');
    div.className = 'tile';
    if (num === null) {
      div.classList.add('empty');
    } else {
      div.innerText = num;
      div.onclick = () => moveTile(i);
    }
    boardDiv.appendChild(div);
  });
}

function moveTile(index) {
  const emptyIndex = board.indexOf(null);
  const validMoves = getNeighborIndices(emptyIndex);
  if (validMoves.includes(index)) {
    [board[emptyIndex], board[index]] = [board[index], board[emptyIndex]];
    renderBoard();
    if (checkWin()) {
      if (level === totalLevels) {
        alert(`🎉 Congratulations ${playerName}, you've completed all ${totalLevels} levels!`);
      } else {
        alert(`✅ Level ${level} completed!`);
        level++;
        loadLevel();
      }
    }
  }
}

function checkWin() {
  for (let i = 0; i < board.length - 1; i++) {
    if (board[i] !== i + 1) return false;
  }
  return true;
}
