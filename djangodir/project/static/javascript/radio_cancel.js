var checkedArray = [];

function allClear() {
    for (let element of document.getElementsByClassName('radio_check')) {
        element.checked = false;
        checkedArray = [];
    }
}

function cancelCheck(clickedId) {
    let element = document.getElementById(clickedId);
    if( checkedArray.includes(clickedId) ){
        element.checked = false;
        clickedIndex = checkedArray.indexOf(clickedId);
        checkedArray.splice(clickedIndex, 1);
    } else {
        element.checked = true;
        checkedArray.push(clickedId);
    }
}

function setCheckedArray(prevCheckedArray){
    // alert("set " + prevCheckedArray.length);
    if( 0 < prevCheckedArray.length ){
        checkedArray = prevCheckedArray;
        alert( "0 < array");
    }
}

function loadRadioChecked(clickedId){
    let element = document.getElementById(clickedId);
    if( checkedArray.includes(clickedId)){
            element.checked = true;
        }
}

function isChecked(radioId){
    return checkedArray.includes(radioId);
}

function makeUrlWithCheckedArray(category){
    urlString = "{% url 'articles:src_link' '" + category + "' 'isChecked' %}";
    window.location.href = urlString.replace(/isChecked/, checkedArray);
}

function getCheckedArray(){
    alert("get " + checkedArray.length);
    return checkedArray;
}