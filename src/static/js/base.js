var console = window.console || {
    log: function(){}
};

window.ns = {
    datatable_i18n: {
        oPaginate: {
            sFirst: '首页',
            sPrevious: '上一页',
            sNext: '下一页',
            sLast: '尾页'
        },
        sProcessing: '正在加载数据...',
        sSearch: '搜索',
        sLengthMenu: '每页显示 _MENU_ 条记录',
        sZeroRecords: '抱歉，没有找到符合的记录',
        sInfo: '显示第 _START_ 到 _END_ 条记录(共 _TOTAL_ 条记录)',
        sInfoEmpty: '暂无记录',
        sInfoFiltered: '(从 _MAX_ 条数据中检索)'
    },
    show_dialog: function(body, title, color){
        var title = title || '提示';
        var $dlg = $('#ns-dialog');
        $('.modal-header h3', $dlg).html(title);
        var $body = $('.modal-body', $dlg).html(body);
        $body.removeClass('ns-red ns-green');
        if(color){
            $body.addClass(color);
        }
        $dlg.modal('show');
    }
};


(function(){
    // do not cache ajax request
    $.ajaxSetup({cache:false, timeout: 59 * 1000});

    // logout click
    $('#logout').click(function(){
        var request = new XMLHttpRequest();
        request.open('get', '/', false, 'hello', 'kitty');
        request.send();
        request.abort();
        location.reload();
    });
})();
