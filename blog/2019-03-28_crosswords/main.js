/*
STATE
*/
//load
var puzzle_name = location.hash.substr(1) || "";
var selected = null;
var direction_horizontal = false;

console.log(`loading puzzle "${puzzle_name}"`);
const _default_state = {
    size: 3,
    content: [
        ['a', 'b', '.'],
        ['d', '', 'f'],
        ['.', 'g', 'h']
    ]
}
const save_state = () => {
    localStorage.setItem(`save_state[${puzzle_name}]`, JSON.stringify(STATE));
    const puzzle_list = JSON.parse(localStorage.getItem('puzzle_list')) || [puzzle_name];
    if (puzzle_list.indexOf(puzzle_name) === -1)
        puzzle_list.push(puzzle_name);
    localStorage.setItem('puzzle_list', JSON.stringify(puzzle_list));
    redraw_board(STATE.size);
    redraw_puzzle_list();
}
var STATE = JSON.parse(localStorage.getItem(`save_state[${puzzle_name}]`)) || _default_state;

/*
BOARD DRAWING
*/

const _create_box = (r, c, content) => {
    new_box = document.createElement('div');
    new_box.className = 'box';
    new_box.id = rc2id({row: r, col: c});
    if (content === '.')
        new_box.classList.add("blocked");
    new_box.innerText = (content || "").toUpperCase();
    return new_box;
}

const _create_row = (r, size, content) => {
    new_row = document.createElement('div');
    new_row.className = 'box-row';
    for (var col = 0; col<size; col++){
        new_row.appendChild(_create_box(r, col, content[col]));
    }
    return new_row;
}

const _create_board = (size, content) => {
    new_board = document.createElement('div');
    for (var row = 0; row < size; row++){
        new_board.appendChild(_create_row(row, size, content[row]));
    }
    return new_board;
}

const redraw_board = () => {
    var size = STATE.size;
    var board = _create_board(size, STATE.content);
    var render_target = document.getElementById("puzzle-board");
    render_target.innerHTML = board.innerHTML;
    if (selected){
        document.getElementById(rc2id(selected)).classList.add("selected");
        const next_item = {
            row: selected.row + (direction_horizontal?0:1),
            col: selected.col + (direction_horizontal?1:0)
        }
        const next = document.getElementById(rc2id(next_item))
        if (next) next.classList.add("next");
    }
}

/*
BOARD EDITING
*/

const handle_click = (event) => {
    var target = id2rc(event.path[0].id);
    if (target.row > -1 && target.col > -1){
        selected = target;
    } else {
        selected = null;
    }
    redraw_board();
}

const handle_keydown = (event) => {
    if (selected && event.key === "Tab") event.preventDefault();
}

const handle_keyup = (event) => {
    if (!selected) return;
    if (event.key.length == 1 || event.key === 'Backspace'){
        const rot = {
            row: STATE.size - 1 - selected.row,
            col: STATE.size - 1 - selected.col
        }
        var next_item = {
            row: Math.min(STATE.size-1, selected.row + (direction_horizontal?0:1)),
            col: Math.min(STATE.size-1, selected.col + (direction_horizontal?1:0))
        }
        if (event.key.toUpperCase().match(/[A-Z ]/)){
            STATE.content[selected.row][selected.col] = event.key;
            const rot_val = STATE.content[rot.row][rot.col];
            if (rot_val == '.'){
                STATE.content[rot.row][rot.col] = ' ';
            }
        }
        if (event.key === '.'){
            STATE.content[selected.row][selected.col] = '.';
            STATE.content[rot.row][rot.col] = '.';
        }
        if (event.key === 'Backspace'){
            STATE.content[selected.row][selected.col] = ' ';
            const rot_val = STATE.content[rot.row][rot.col];
            if (rot_val == '.'){
                STATE.content[rot.row][rot.col] = ' ';
            }
            var next_item = {
                row: Math.max(0, selected.row - (direction_horizontal?0:1)),
                col: Math.max(0, selected.col - (direction_horizontal?1:0))
            }
        }
        selected = next_item;
    } else {
        console.log(event.key)
        switch (event.key){
            case 'ArrowLeft':
                if (!direction_horizontal){
                    direction_horizontal = true;
                }
                selected = {
                    row: selected.row,
                    col: Math.max(0, selected.col - 1)
                }
                break;
            case 'ArrowRight':
                if (!direction_horizontal){
                    direction_horizontal = true;
                } else {
                    selected = {
                        row: selected.row,
                        col: Math.min(STATE.size - 1, selected.col + 1)
                    }
                }
                break;
            case 'ArrowUp':
                if (direction_horizontal){
                    direction_horizontal = false;
                }
                selected = {
                    row: Math.max(0, selected.row - 1),
                    col: selected.col
                }
                break;
            case 'ArrowDown':
                if (direction_horizontal){
                    direction_horizontal = false;
                } else {
                    selected = {
                        row: Math.min(STATE.size-1, selected.row + 1),
                        col: selected.col
                    }
                }
                break;
            case "Tab":
                event.preventDefault();
                direction_horizontal = !direction_horizontal;
                break;
        }
    }
    redraw_board();
}

/*
UTILITIES
*/

const id2rc = (id) => {
    var vals = id.split("-").slice(1)
    return {
        row: parseInt(vals[0]),
        col: parseInt(vals[1])
    }
}

const rc2id = (rc) => {
    return `box-${rc.row}-${rc.col}`;
}


const reset_content = () => {
    STATE.content = []
    for (var _r = 0; _r < STATE.size; _r++){
        var new_row = [];
        for (var _c = 0; _c < STATE.size; _c++){
            new_row.push("");
        }
        STATE.content.push(new_row);
    }
    redraw_board();
    document.getElementById("display-size").textContent = STATE.size;
}

const size_up = () => {
    STATE.size += 2;
    reset_content();
}

const size_down = () => {
    STATE.size -= 2;
    reset_content();
}

const update_name = (event) => {
    console.log(event);
    const pn = document.getElementById("puzzle-name").value;
    location.hash = pn;
    puzzle_name = pn;
}

const change_puzzle = (puzzle_name) => {
    location.hash = puzzle_name;
    location.reload()
}

const redraw_puzzle_list = () => {
    const puzzle_list = JSON.parse(localStorage.getItem('puzzle_list')) || [];
    const render_target = document.getElementById('puzzle-list-links');
    render_target.innerHTML = '';
    for (_p = 0; _p < puzzle_list.length; _p++){
        const new_puzzle_link = document.createElement('div');
        new_puzzle_link.className = 'puzzle_link';
        new_puzzle_link.onclick = change_puzzle.bind(this, puzzle_list[_p]);
        new_puzzle_link.innerText = puzzle_list[_p];
        console.log(new_puzzle_link);
        render_target.appendChild(new_puzzle_link);
    }
}

//initialize puzzle!
function initialize() {
    //hookup listeners
    document.body.onkeyup = handle_keyup;
    document.body.onkeydown = handle_keydown;
    document.body.onclick = handle_click;
    document.getElementById("puzzle-name").onchange = update_name;

    // initialize
    document.getElementById("puzzle-name").value = puzzle_name;
    document.getElementById("display-size").textContent = STATE.size;
    redraw_board(STATE.size);
    redraw_puzzle_list();

    console.log("board initialized");
}