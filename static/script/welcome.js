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
    console.log(entry);

    fetch(`${window.location}/settings`, {
        method: "POST",
        credentials: "include",
    });
}