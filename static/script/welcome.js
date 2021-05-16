function save() {
    var share = document.getElementById('sharing').checked;
    var account = document.getElementById('account').checked;
    var lightMode = document.getElementById('light-mode').checked;
    var stocks = document.getElementById('stocks').checked;
    var notify = document.getElementById('notify').checked;
    var trash = document.getElementById('trash-set').checked;
    var encrypt = document.getElementById('encryption').checked;
    var auth = document.getElementById('2auth').checked;
    var entry = {
        Eshare: share,
        Eaccount: account,
        Elightmode: lightMode,
        Estocks: stocks,
        Enotify: notify,
        Etrash: trash,
        Eencrypt: encrypt,
        Eauth: auth
    };
    
    fetch(`${window.origin}/settings`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function(response) {
        if (response.status !== 200) {
            alert('Error');
        } else {
            response.json().then(function (data) {
                alert(data['message']);
            })
        }
    })
}
