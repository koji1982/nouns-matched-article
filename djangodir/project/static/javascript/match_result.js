// $(function(){
//     $("#apply").on("click", function(){
//         $("#right_frame", parent.document).attr("src", "/loading").on("load", function(){
//             $.get("/result", function(data){
//                 $(document).ajaxComplete(function(){
//                     $("#right_frame", parent.document).replaceWith(data);
//                 });
//             });
//         });
//     });
// });
$(function(){
    $("#apply").on("click", function(){
        $("#right_frame", parent.document).attr("src", "/loading").on("load", function(){
            $("#right_frame", parent.document).attr("src", "/loading").off("load");
            $("#right_frame", parent.document).attr("src", "/result").on("load");
        });
    });
});
// $(function(){
//     $("#apply").on("click", function(){
//         $.get("/loading", function(data){
//             $(".right_frame", parent.document).remove();
//         });
//         // window.open("/loading", "right_frame");
//         // $.get("/result", function(){
//         //     $(document).ajaxComplete(function(){
//         //         alert("result");
//         //     });
//         // });
//     });
// });
// $(function(){
//     $("#apply").click(function(){
//         $(".right_frame").attr('src').append("<p>test_text</p>");
//     });
// });

// $("#apply").on("click", function (event) {
//     // alert("jquery");
//     window.location.href = '/loading';
//     showLoadingCircle();
//     applyEvaluation();
    
    // function showLoadingCircle() {
    //     $.get("/loading", function(data){
    //         $(document).ajaxComplete(function(){
    //             alert("jquery");
    //         });
    //     });
            // window.onload = function(){
            //     const loader = document.getElementById('loading_circle');
            //     loader.classList.add('completed');
        // windowObj = window.open('/loading', 'right_frame');
        // $(function(){
        //     windowObj.onload = function(){
        //         const loader = document.getElementById('loading_circle');
        //         loader.classList.add('completed');
        //     }
        // });
        
        // alert("loading function")
        // $.get("{% url 'articles:loading' %}", function(){
        //     alert("loading function")
        // });
    // }

    function applyEvaluation() {
        // $(function(){
        //     window.onload = function(){
        //         const loader = document.getElementById('loading_circle');
        //         loader.classList.add('completed');
        //     }
        // });
        
        // alert("apply Evaluation");
        // window.open('/result', 'right_frame');
        // window.onload = function(){
        //     const loader = document.getElementById('loading_circle');
        //     loader.classList.add('completed');
        // }
        
        // $.get("{% url 'articles:result' %}", function(){
        //     alert("apply Evaluation")
        // });
    }
// });