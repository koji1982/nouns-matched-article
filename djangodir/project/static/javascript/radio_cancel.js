var checked_array = [];

function all_clear() {
    for (const element of document.getElementsByClassName('radio_check')) {
        element.checked = false;
        checked_array = [];
      }
}

function remove_check(clicked_id) {
    let element = document.getElementById(clicked_id);
    if( checked_array.includes(clicked_id) ){
        console.log(clicked_id);
        element.checked = false;
        clicked_index = checked_array.indexOf(clicked_id);
        checked_array.splice(clicked_index, 1);
    } else {
        element.checked = true;
        checked_array.push(clicked_id);
    }
}