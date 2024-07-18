function delete_category(cid) {

    document.getElementById('delete_modal').style.display = 'flex'
    document.getElementById('rm-button').setAttribute('onclick', `confirm_delete_cat(${cid})`)

}


function confirm_delete_cat(cid) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', `/admin_panel/categories/delete`, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.responseType = 'json';

    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {

            document.getElementById(`delete_modal`).style.display = 'none'
            document.getElementById(`c-${cid}`).remove()

        }
    }

    xhr.send(`cid=${cid}`)
}
