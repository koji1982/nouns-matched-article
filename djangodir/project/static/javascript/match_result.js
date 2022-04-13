$(function(){
    $("#apply").on("click", function(){
        $("#right_frame", parent.document).attr("src", "/loading").on("load.apply", function(){
            $("#right_frame", parent.document).off("load.apply");
            $("#right_frame", parent.document).attr("src", "/call_apply_choices");
        });
    });
});
$(function(){
    $(".commit_button").on("click", function(){
        $(".loading_circle").removeClass("invisible");
    });
});
// $(function(){
//     $("#logout_id").on("click", function(){
//         console.log("1");
//         $.get("loading", {}, function(data){
//             console.log("3");
//         }).done(function(data){
//             console.log("4");
//             $("#frame_body", parent.document).replaceWith(data);
//             console.log("5");
//             // $.get("logout", {}, function(data){
//             //     console.log("5");
//             //     parent.window.location.href = data;
//             // });
//         });
        
//         $.get("logout", {}, function(data){
//             console.log("6");
            
//         }).done(function(data){
//             console.log("7");
//             parent.window.location.href = "/";
//         });
//         console.log("2");
//         // $("#frame_body", parent.document).replaceWith().bind("unload",function(){
//         //     alert("3");
//         //     $("#frame_body", parent.document).unbind("unload", function(){
//         //         alert("4");
//         //         $("#frame_body", parent.document).load("/logout");
//         //     });
//         // });
        
//     });
// });

// $(function(){
//     $("#logout_id").on("click", function(){
//         transitWithLoadDisplay("logout");
//         // $.get("loading", {}, function(data){
//         //     $("#frame_body", parent.document).replaceWith(data);
//         // });
//         // parent.window.location.href = "logout";
//     });
// });

function transitWithLoadingCircle(nextUrl){
    $.get("loading", {}, function(data){
        $("#frame_body", parent.document).replaceWith(data);
    });
    parent.window.location.href = nextUrl;
}
// $(function(){
//     $("#logout_id").on("click", function(){
//         $("#frame_body", parent.document).load("/loading", {}, function(){
//             alert("3");
//             $("#frame_body", parent.document).off("load.logout", {}, function(){
//                 alert("4");
//                 $("#frame_body", parent.document).load("/logout");
//             });
            
//         });
//     });
// });


// $("#logout_id").on("click", function(){
//     alert(this.id+"1");
//     startLoading();
// });

// function startLoading(){
//     // window.addEventListener("load", function(){
//     //     alert(this.id+"2");
//     //     window.open("/logout", "_self");
//     // });
//     window.open("/loading", "_parent", function(){
//         alert(this.id+"2");
//         window.open("/logout", "_self");
//     });
// }

// function startLogout(){
//     alert(this.id+"3");
//     window.open("/logout", parent.document);
//     window.addEventListener("load",function(){
//         alert(this.id+"4");
//         // window.location.href = "/login";
//     });
// }
// $("#logout_id").on("click", function(){
//     alert(this.id+'1');
//     $(":root", parent.document).load("/loading").ready(fucntion{
//         $(":root", parent.document).load("/logout")
//     });
//     $(":root", parent.document).ready("/logout", function(){
//         alert(this.id+'4');
//         $(":root", parent.document).load("/loading").on("load");
//     }).load("/logout",function(){
//         alert(this.id+'3');
//         $(":root", parent.document).off("load");
//     });
//     alert(this.id+'2');
// });
// $(function(){
//     alert('1')
//     $("#logout_id").on("click", function(){
//         alert('2')
//         $.get("/loading", function(data){
//             alert('3')
//             $.get("/logout", function(){
//                 alert('4')
//                 $(document).ajaxComplete(function(){
//                     alert('5')
//                     $(data).off("load")
//                 });
//             })
//             .done(function (html) {
//                 var bodyInnerHTML = $('body', $(html)).html(); // 取得したHTMLからbodyタグの中身を抽出
//                 $('body').html(bodyInnerHTML); // 抽出したもので現在のページのbodyタグの中身を置き換える
//             })
//             .fail(function (html) { });
//         });
        
//         // $("body").attr(document, "/loading").on("load", function(){
//         //     alert(this.id)
//         //     $("body").attr(document, "/loading").off("load");
//         //     $("body").attr(document, "/logout").on("load");
//         // });
//     });
// });

