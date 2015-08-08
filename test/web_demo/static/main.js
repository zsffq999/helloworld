/**
 * Created by goldenbull on 2015/8/8.
 */

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

        // ��ʼ��table
        dt = $("#tbl").DataTable({
            "columns": [
                {"title": "Days since 0001-1-1"},
                {"title": "Weekday"},
                {"title": "Timestamp"}
            ]
        });

        // �����Զ�ˢ�����ݵĶ�ʱ��
        setInterval(append_data, 1000);
    }
);