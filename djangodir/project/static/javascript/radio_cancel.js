var checkedArray = [];

// window.onload = function(){
//     const loader = document.getElementById('loading_circle');
//     loader.classList.add('completed');
//     // window.open('/result', 'right_frame')
// }

function removeLoadingCircle(){
    const loader = document.getElementById('loading_circle');
    loader.classList.add('completed');
}

// async function fn() {
//     return 42;
// }

// fn().then(
//     result => {alert(result)}
//     );

// window.onloadeddata = function(){
//     const loader = document.getElementById('loading_circle');
//     loader.classList.add('completed');
//     alert('onloadeddata')
// }

// var httpRequest = new XMLHttpRequest();
// httpRequest.open('GET', 'https://www.selected-article-2021.info/');
// httpRequest.send();

// httpRequest.onreadystatechange = function(){
//     if(httpRequest.readyState === 4 && httpRequest.status === 200) {
//         alert("from ajax")
//         console.log( JSON.parse(xhr.responseText) );
//     }else{
//         alert("status invalid")

//     }
// }

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