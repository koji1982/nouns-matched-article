$(function(){
    $("#apply").on("click", function(){
        $("#right_frame", parent.document).attr("src", "/loading").on("load", function(){
            $("#right_frame", parent.document).attr("src", "/loading").off("load");
            $("#right_frame", parent.document).attr("src", "/call_apply_choices").on("load");
        });
    });
});
