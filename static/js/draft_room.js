const BASE_URL = '/api'
const GET_AVAIL_PITCHER_URL = `${BASE_URL}/pitchers`
const GET_AVAIL_BATTER_URL = `${BASE_URL}/batters`

const BATTER_FIELDS = ['name', 'g', 'ab', 'r', 'h', 'db', 'tp', 'hr', 'rbi', 'sb', 'cs', 'bb', 'so', 'hbp', 'sf', 'ibb']
const PITCHER_FIELDS = ['name', 'w', 'l', 'g', 'cg', 'sho', 'sv', 'ip', 'h', 'er', 'hr', 'bb', 'ibb', 'so', 'hbp']
const ID_FIELD = 'id'
const BATTER_TABLE = 'batter_table'
const PITCHER_TABLE = 'pitcher_table'

let which_table = BATTER_TABLE

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}
window.onclick = function(event) {
    if(!event.target.matches('.drop')){
        var dropdowns = document.getElementsByClassName("dropdown-event");
        var i;
        for(i=0; i < dropdowns.length; i++){
            var openDropdown = dropdowns[i];
            if(openDropdown.classList.contains('show')){
            openDropdown.classList.remove('show');
            }
        }
    }
}
function buildTable(table, cols) {
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    const headerRow = document.createElement('tr');

    const th = document.createElement('th');
    th.innerText = "";
    th.classList.add('add-button-header');
    headerRow.appendChild(th);

    for(let col of cols) {
        const th = document.createElement('th');
        th.innerText = col;
        headerRow.appendChild(th);
    }

    thead.appendChild(headerRow);
    table.appendChild(thead);
    table.appendChild(tbody);
}
const buildTableRows = (table, cols) => (data) => {
    const tbody = table.querySelector('tbody');

    for(let d of data) {
        const row = document.createElement('tr');

        // create a button to add this player to roster
        const td = document.createElement('td');
        td.classList.add('add-button-td');
        const addButton = document.createElement('button');
        addButton.innerText = 'Add Player';
        addButton.dataset.player_id = d[ID_FIELD];
        addButton.addEventListener('click', async (e) => {
            e.preventDefault();
            const resp = await fetch('/add_player', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'player-id': e.target.dataset.player_id, which_table})
            });
            reload_page();
        });
        td.appendChild(addButton);
        row.appendChild(td);

        for(let col of cols) {
            const td = document.createElement('td');
            td.innerText = d[col];
            row.appendChild(td);
        }
        tbody.appendChild(row);
    }
    table.appendChild(tbody);
}
async function fetchBatters() {
    try {
        const resp =  await fetch(GET_AVAIL_BATTER_URL);
        const status = resp.status;
        if(status == 200) {
            const body = await resp.json()
            console.log('fetchBatters() - resp', body)
            return body;
        } else {
            // some other status code
            throw {status};
        }
    } catch(err) {
        throw {err};
    }
}
async function fetchPitchers() {
    try {
        const resp =  await fetch(GET_AVAIL_PITCHER_URL);
        const status = resp.status;
        if(status == 200) {
            return resp.json();
        } else {
            // some other status code
            throw {status};
        }
    } catch(err) {
        throw {err};
    }
}
function showAvailablePitchers(){
    which_table = PITCHER_TABLE;
    var playerTable = document.getElementById("player-table");
    playerTable.innerHTML = '';
    buildTable(playerTable, PITCHER_FIELDS);
    fetchPitchers().then(buildTableRows(playerTable, PITCHER_FIELDS));
}
function showAvailableBatters(){
    which_table = BATTER_TABLE;
    var playerTable = document.getElementById("player-table");
    playerTable.innerHTML = '';
    buildTable(playerTable, BATTER_FIELDS);
    fetchBatters().then(buildTableRows(playerTable, BATTER_FIELDS));
}

function reload_page(){
    if (which_table === BATTER_TABLE){
        showAvailableBatters();
    } else if (which_table === PITCHER_TABLE){
        showAvailablePitchers();
    }
}

window.addEventListener("DOMContentLoaded", ()=>{
    reload_page();
})




