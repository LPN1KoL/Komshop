function delete_product(pid) {
    document.getElementById('delete_modal').style.display = 'flex'
    let tr = document.getElementById(`p-${pid}`)
    let name = tr.childNodes[1].innerText

    document.getElementById('rm-modal-h').innerText = `Вы действительно хотите удалить товар с серийным номером ${name}?`
    document.getElementById('rm-button').setAttribute('onclick', `confirm_delete_product(${pid})`)
}


function confirm_delete_product(pid) {

    let xhr = new XMLHttpRequest();
    xhr.open('POST', `/admin_panel/delete_product`, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.responseType = 'json';

    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {

            document.getElementById(`delete_modal`).style.display = 'none'
            document.getElementById(`p-${pid}`).remove()

        }
    }

    xhr.send(`pid=${pid}`)

}
