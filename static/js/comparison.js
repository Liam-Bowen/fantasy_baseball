const ID_FIELD = 'id'
const BATTER_TABLE = 'batter_table'
const PITCHER_TABLE = 'pitcher_table'
const TEAM_LIST = 'team-select'

const API_BASE_URL = '/api'
const GET_ROSTER_URL = `${API_BASE_URL}/roster`
const GET_TEAM_URL = `${API_BASE_URL}/teams`
const GET_COMPARE_ROSTER_URL = `${API_BASE_URL}/roster/<team>`

const BATTER_FIELDS = ['name','pos', 'g', 'ab', 'r', 'h', 'db', 'tp', 'hr', 'rbi', 'sb', 'cs', 'bb', 'so', 'hbp', 'ibb']
const PITCHER_FIELDS = ['name','pos', 'w', 'l', 'g', 'cg', 'sho', 'sv', 'ip', 'h', 'er', 'hr', 'bb', 'ibb', 'so', 'hbp']

function buildTable(table, cols) {
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    const headerRow = document.createElement('tr');

    const th = document.createElement('th');
    th.innerText = "";
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
async function fetchRoster(teamName) {
    console.log("fetchRoster", teamName)
    try {
        let url;
        if(teamName == null) {

            url = GET_ROSTER_URL;
        } else {
            url = `${GET_ROSTER_URL}/${teamName}`;
        }
        const resp = fetch(url);
        console.log("fetch roster url", url);
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

function displayTeamNames(teamList){
    const teamListBody = teamList.getElementsByTagName('team-select');
}


async function fetchTeams() {
    try {
        const resp =  await fetch(GET_TEAM_URL);
        const status = resp.status;
        if(status == 200) {
            const body = await resp.json();
            console.log("fetchTeams(): success", body);
            return body;
        } else {
            // some other status code
            throw {status};
        }
    } catch(err) {
        throw {err};
    }
}

function buildTeamSelect(teamSelect){
    fetchTeams().then(json => {
        console.log('buildTeamSelect', json);
        for(teamName of json){
            const option = document.createElement('option');
            option.value = teamName;
            option.innerText = teamName;
            teamSelect.appendChild(option);
        }
    })
}

function myFunction() {
    document.getElementById("dropdown").classList.toggle("show");
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

function reload_page(batterTable, pitcherTable){
    fetchRoster().then(json => {
        console.log('roster', json);
        displayRoster(batterTable, pitcherTable, json);
    });

}

function loadTeamForCompare(e) {
    const teamName = e.target.value;
    console.log('loadTeamForCompare', teamName)
    fetchTeams(teamName).then(json => {
        console.log('loadTeamForCompare', teamName, json);
        // build compare table
        const batterTable2 = document.getElementById("batter-table2");
        const pitcherTable2 = document.getElementById("pitcher-table2");
        buildTable(batterTable2, BATTER_FIELDS);
        buildTable(pitcherTable2, PITCHER_FIELDS);
        reload_page(batterTable2, pitcherTable2);
    })
}

window.addEventListener("DOMContentLoaded", ()=>{
    const batterTable = document.getElementById("batter-table");
    const pitcherTable = document.getElementById("pitcher-table");
    const teamSelect = document.getElementById("team-select");
    buildTeamSelect(teamSelect);
    teamSelect.addEventListener('change', loadTeamForCompare);
    buildTable(batterTable, BATTER_FIELDS);
    buildTable(pitcherTable, PITCHER_FIELDS);
    reload_page(batterTable, pitcherTable);
    setInterval(()=>reload_page(batterTable, pitcherTable), 10000);
})