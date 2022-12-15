const ID_FIELD = 'id'
const BATTER_TABLE = 'batter_table'
const PITCHER_TABLE = 'pitcher_table'

const API_BASE_URL = '/api'
const GET_ROSTER_URL = `${API_BASE_URL}/roster`
const REMOVE_PLAYER_URLS = {}
REMOVE_PLAYER_URLS[BATTER_TABLE] = `${API_BASE_URL}/roster/batters/remove`
REMOVE_PLAYER_URLS[PITCHER_TABLE] = `${API_BASE_URL}/roster/pitchers/remove`

const BATTER_FIELDS = ['name','pos','g', 'ab', 'r', 'h', 'db', 'tp', 'hr', 'rbi', 'sb', 'cs', 'bb', 'so', 'hbp', 'sf',
 'ibb']
const PITCHER_FIELDS = ['name', 'pos', 'w', 'l', 'g', 'cg', 'sho', 'sv', 'ip', 'h', 'er', 'hr', 'bb', 'ibb', 'so', 'hbp']

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
const buildTableRow = (batterTable, pitcherTable, which_table, tbody, cols) => (d) => {
    const row = document.createElement('tr');

    // create a button to add this player to roster
    const td = document.createElement('td');
    td.classList.add('add-button-td');
    const addButton = document.createElement('button');
    addButton.innerText = 'Remove Player';
    addButton.dataset.player_id = d[ID_FIELD];
    addButton.addEventListener('click', async (e) => {
        e.preventDefault();
        const resp = await fetch(REMOVE_PLAYER_URLS[which_table], {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'player-id': e.target.dataset.player_id, which_table})
        });
        reload_page(batterTable, pitcherTable);
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

function displayRoster(batterTable, pitcherTable, json){
    const batterTabBody = batterTable.getElementsByTagName('tbody')[0];
    batterTabBody.innerHTML = '';
    const pitcherTabBody = pitcherTable.getElementsByTagName('tbody')[0];
    pitcherTabBody.innerHTML = '';

    // console.log('batterTabBody', batterTabBody)
    // console.log('pitcherTabBody', pitcherTabBody)

    // for loop
    for(let d of json) {
        switch(d.position) {
            case 'batter':
                buildTableRow(batterTable, pitcherTable, BATTER_TABLE, batterTabBody, BATTER_FIELDS)(d)
                break;
            case 'pitcher':
                buildTableRow(batterTable, pitcherTable, PITCHER_TABLE, pitcherTabBody, PITCHER_FIELDS)(d)
                break;
            default:
                // error has occurred
        }
    }
}
async function fetchRoster() {
    try {
        const resp =  await fetch(GET_ROSTER_URL);
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

function reload_page(batterTable, pitcherTable){
    fetchRoster().then(json => {
        console.log('roster', json);
        displayRoster(batterTable, pitcherTable, json);
    });
}

window.addEventListener("DOMContentLoaded", ()=>{
    const batterTable = document.getElementById("batter-table");
    const pitcherTable = document.getElementById("pitcher-table");
    buildTable(batterTable, BATTER_FIELDS);
    buildTable(pitcherTable, PITCHER_FIELDS);
    reload_page(batterTable, pitcherTable);
    setInterval(()=>reload_page(batterTable, pitcherTable), 10000);
})