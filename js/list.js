// tbody要素を生成する関数
function makeTable(data)
{
    let tbl = document.getElementById('table-questions');

    let tbody = document.createElement('tbody');

    for (var i = 0; i < data.length; i++) {
        var row = data[i];

        var tr = document.createElement('tr');
        var qid = document.createElement('td');
        var qtitle = document.createElement('td');
        var qrating = document.createElement('td');
        var link = document.createElement('td');

        qid.innerHTML = row["id"];
        
        var afortitle = document.createElement('a');
        afortitle.setAttribute('href', row["url"]);
        afortitle.innerHTML = row["title"];
        qtitle.appendChild(afortitle); 
        
        var aforlink = document.createElement('a');
        var lnk = 'analyze.php?qid=' + row["id"];
        aforlink.setAttribute('href', lnk);
        aforlink.innerHTML = '問題を解く';
        link.appendChild(aforlink);

        qrating.innerHTML = row["rating"];

        tr.appendChild(qid);
        tr.appendChild(qtitle);
        tr.appendChild(qrating);
        tr.appendChild(link);
        
        tbody.appendChild(tr);
    }

    tbl.appendChild(tbody);
}

// data.jsonを読み込み、makeTableを実行
fetch('./data.json')
    .then(response => response.json())
    .then(data => makeTable(data))
    .catch(error => console.log('Error fetching JSON: ', error));