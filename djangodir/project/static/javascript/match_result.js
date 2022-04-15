//クリックによる画面遷移時にロード画面を表示する
function transitWithLoadingCircle(nextUrl){
    $.get("loading", {}, function(data){
        $("#frame_body", parent.document).replaceWith(data);
    });
    parent.window.location.href = nextUrl;
}

//formのPost時にロード画面を表示させる
$(function(){
    $(".commit_button").on("submit", function(){
        setTimeout( function(){
            $(".loading_circle").removeClass("invisible");
        }, 200);
        //認証に失敗してformにfocusが戻った場合はloading_circleを除去
        $(".input_form").on("focus", function(){
            $(".loading_circle").addClass("invisible");
        });
    });
});

//ユーザー評価から各記事の名詞の一致率を計算する関数を呼び出し、
//計算中は右側のフレームにロード画面を表示させる
$(function(){
    $("#apply").on("click", function(){
        $("#right_frame", parent.document).attr("src", "/loading").on("load", function(){
            $("#right_frame", parent.document).off("load");
            $("#right_frame", parent.document).attr("src", "/call_apply_choices");
        });
    });
});
