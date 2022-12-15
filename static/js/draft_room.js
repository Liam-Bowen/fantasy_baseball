const ID_FIELD = 'id'
const BATTER_TABLE = 'batter_table'
const PITCHER_TABLE = 'pitcher_table'

const API_BASE_URL = '/api'
const GET_AVAIL_PITCHER_URL = `${API_BASE_URL}/pitchers`
const GET_AVAIL_BATTER_URL = `${API_BASE_URL}/batters`
const GET_ROSTER_URL = `${API_BASE_URL}/roster`
const ADD_PLAYER_URLS = {}
ADD_PLAYER_URLS[BATTER_TABLE] = `${API_BASE_URL}/roster/batters/add`
ADD_PLAYER_URLS[PITCHER_TABLE] = `${API_BASE_URL}/roster/pitchers/add`

const BATTER_FIELDS = ['name','pos', 'g', 'ab', 'r', 'h', 'db', 'tp', 'hr', 'rbi', 'sb', 'cs', 'bb', 'so', 'hbp', 'ibb']
const PITCHER_FIELDS = ['name','pos', 'w', 'l', 'g', 'cg', 'sho', 'sv', 'ip', 'h', 'er', 'hr', 'bb', 'ibb', 'so', 'hbp']

let which_table;
let batterUL;
let pitcherUL;
let playerTable;
let order_by;
let order_desc;

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
function setHeaderClasses(){
    const playerTable = document.getElementById("player-table");
    const thead = playerTable.getElementsByTagName('thead')[0];
    const headers = thead.getElementsByTagName('th');
    for(let th of headers) {
        if(order_by !== th.dataset.name) {
            th.classList.remove("table-sort-col-asc");
            th.classList.remove("table-sort-col-desc");
        } else {
            if(order_desc) {
                th.classList.remove("table-sort-col-asc");
                th.classList.add("table-sort-col-desc");
            } else {
                th.classList.add("table-sort-col-asc");
                th.classList.remove("table-sort-col-desc");
            }
        }
    }
}
function buildTable(cols) {
    playerTable.innerHTML = '';
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
        th.dataset.name = col;
        th.addEventListener('click', (e)=>{
            console.log('clicked', e.target);
            const sort_col = e.target.dataset.name;
            //if(typeof sort_col === string){
                if(order_by !== sort_col) {
                    order_desc = true;
                } else {
                    order_desc = !order_desc;
                }
            //}
            order_by = sort_col;

            // add css styles to indicate sorting column and dir
            reload_page();
        });
        headerRow.appendChild(th);
    }

    thead.appendChild(headerRow);
    playerTable.appendChild(thead);
    playerTable.appendChild(tbody);
}
const fieldSort = (a,b,desc) => {
    if(!isNaN(a) && !isNaN(b)) {
        return (+b - +a) * desc
    } else {
        return b.localeCompare(a) * desc;
    }
}
const buildTableRows = (which_table, tbody, cols) => (data) => {
    // sort data here
    data.sort((a, b) => fieldSort(a[order_by], b[order_by], (order_desc)?1:-1))

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
            const resp = await fetch(ADD_PLAYER_URLS[which_table], {
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
    setHeaderClasses();
}
async function fetchAvailableBatters() {
    try {
        const resp =  await fetch(GET_AVAIL_BATTER_URL);
        const status = resp.status;
        if(status == 200) {
            const body = await resp.json()
            //console.log('fetchBatters() - resp', body)
            return body;
        } else {
            // some other status code
            throw {status};
        }
    } catch(err) {
        throw {err};
    }
}
async function fetchAvailablePitchers() {
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
async function fetchRoster() {
    try {
        // console.log("fetching roster");
        const resp =  await fetch(GET_ROSTER_URL);
        const status = resp.status;
        if(status == 200) {
            const body = await resp.json();
            console.log("fetch roster success", body);
            return body;
        } else {
            // some other status code
            throw {status};
        }
    } catch(err) {
        throw {err};
    }
}
function showAvailablePitchers(){
    if(which_table != PITCHER_TABLE) {
        order_by = 'name';
        order_desc = true;
        buildTable(PITCHER_FIELDS);
    }
    which_table = PITCHER_TABLE;
    const playerTable = document.getElementById("player-table");
    const tableBody = playerTable.getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';
    fetchAvailablePitchers().then(buildTableRows(which_table, tableBody, PITCHER_FIELDS));
    document.querySelector('#dropButton').innerHTML = 'Pitchers';
}
function showAvailableBatters(){
    if(which_table != BATTER_TABLE) {
        order_by = 'name';
        order_desc = true;
        buildTable(BATTER_FIELDS);
    }
    which_table = BATTER_TABLE;
    const playerTable = document.getElementById("player-table");
    const tableBody = playerTable.getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';
    fetchAvailableBatters().then(buildTableRows(which_table, tableBody, BATTER_FIELDS));
    document.querySelector('#dropButton').innerHTML = 'Batters';
}
function displayRoster(json){
    // console.log('displayRoster', json);
    batterUL.innerHTML = '';
    pitcherUL.innerHTML = '';

    // for loop
    for(let d of json) {
        const li = document.createElement('li');
        li.innerText = d.name;
        switch(d.position) {
            case 'batter':
                // console.log('adding batter', li);
                batterUL.appendChild(li);
                break;
            case 'pitcher':
                // console.log('adding pitcher', li);
                pitcherUL.appendChild(li);
                break;
            default:
                // error has occurred
        }
    }
}
function reload_page(){
    if (which_table === PITCHER_TABLE){
        showAvailablePitchers();
    } else {
        showAvailableBatters();
    }
    fetchRoster().then(displayRoster);
}

window.addEventListener("DOMContentLoaded", ()=>{
    batterUL = document.getElementById('batter-list');
    pitcherUL = document.getElementById('pitcher-list');
    playerTable = document.getElementById('player-table');
    reload_page();
    setInterval(reload_page, 30000);
})




