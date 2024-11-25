// list.htmlのtbody要素を生成する関数
function setTable(data)
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

/*
var data = [
    {
        "id":"1",
        "title":"A. 積雪深差",
        "url":"https://atcoder.jp/contests/abc001/tasks/abc001_1",
        "rating":"100"
    }, {
        "id":"2",
        "title":"B. 視程の通報",
        "url":"https://atcoder.jp/contests/abc001/tasks/abc001_2",
        "rating":"200"
    }, {
        "id":"3",
        "title":"C. 風力観測",
        "url":"https://atcoder.jp/contests/abc001/tasks/abc001_3",
        "rating":"300"
    }, {
        "id":"4",
        "title":"D. 感雨時刻の整理",
        "url":"https://atcoder.jp/contests/abc001/tasks/abc001_4",
        "rating":"400"
    }
]
*/

window.addEventListener('load', function() {
    fetch('./data.json')
        .then(response => response.json())
        .then(data => setTable(data))
        .catch(error => console.log('Error fetching JSON: ', error));
})