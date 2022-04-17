//クリックによる画面遷移時にロード画面を表示する
function transitWithLoadingCircle(nextUrl){
    $.get("loading", {}, function(data){
        $("#frame_body", parent.document).replaceWith(data);
    });
    parent.window.location.href = nextUrl;
}

//サインアップ、ログインformのPost時のローディング表示
$(function(){
    $(".commit_button").on("click", function(){
        //サインアップなのかログインなのかで入力フォームの数を決定する
        title = document.getElementsByTagName('title');
        formCount = title[0].textContent == 'ログイン画面' ? 2 : 3;
        //入力フォームに空欄があった場合はそのまま終了
        //その他の入力エラーはDjango側で処理する
        inputForms = document.getElementsByClassName('input_form');
        for(i=0; i<formCount; i++){
            if(inputForms[i].value.length == 0){
                return true;
            }
        }
        //ローディング画面を表示させる
        setTimeout( function(){
            $(".loading_circle").removeClass("invisible");
        }, 200);
    });
});

//ゲストログイン時には認証失敗を考慮せずそのままロード画面を表示する
$(function(){
    $("#guest_button_id").on("click", function(){
        setTimeout( function(){
            $(".loading_circle").removeClass("invisible");
        }, 200);
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
