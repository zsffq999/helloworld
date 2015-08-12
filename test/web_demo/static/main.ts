///<reference path="jquery.d.ts" />
///<reference path="moment.d.ts" />

var dt;

function append_data() {
    $.ajax({
        url: '/getdata/' + moment().format("YYYYMMDD"),
        success: function (ret) {
            var obj = JSON.parse(ret);
            dt.row.add(obj).draw();
            $("#msg").html("reload data on " + moment().format("YYYY-MM-DD HH:mm:ss.SSS") + " : " + JSON.stringify(obj));
        }
    });
}

$(document).ready(function () {

        // 初始化table
        dt = $("#tbl").DataTable({
            "columns": [
                {"title": "Days since 0001-1-1"},
                {"title": "Weekday"},
                {"title": "Timestamp"}
            ]
        });

        // 配置自动刷新数据的定时器
        setInterval(append_data, 1000);

        $("#btn1").click(function () {
            $("#msg2").html(JSON.stringify([1, 2, 3]));
            $.ajax({
                type: "POST",
                url: "/postdata",
                data: JSON.stringify([1, 2, 3]),
                dataType: "json",
                contentType: 'application/json',
                success: function (ret) {
                    $("#msg2").text(ret);
                }
            });
        });
    }
);