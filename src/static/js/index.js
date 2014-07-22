!(function($){
    // get the detail infomation of each host:port
    var tr = '<tr><td colspan="4" class="ns-red">' +
        '连接到服务器失败。可能的原因：目标服务器未开启supervisord;' +
        ' 您的用户名或密码不正确。' + '</td></tr>';
    var action = '<a href="#!" class="action restart" title="重启"><i class="fa fa-refresh"></i></a> ' +
        '<a href="#!" class="action stop" title="停止"><i class="fa fa-stop"></i></a>';
    var map = {'RUNNING': '运行中', 'FATAL': '有错误', 'RESTARTING': '重启中', 'STOPPED': '已停止'};

    var $hosts = $('#hosts');
    $('[data-host]', $hosts).each(function(){
        var self = $(this);
        var $tbody = self.find('tbody').empty();
        $.get($hosts.data('detail'), {
            host: self.data('host'), port: self.data('port')
        }, function(res){
            if(res.err === false){  // DO NOT use `if(!res.err){...}`
                var html = [];

                function td(text, center){
                    var center = center ? ' class="center"' : '';
                    return '<td' + center + '>' + text + '</td>';
                }

                for(var i in res.info){
                    var one = res.info[i];
                    html.push('<tr data-info="' + JSON.stringify(one).replace(/"/g, "'") + '">');
                    html.push(td(map[one.statename]));
                    html.push(td(one.description));
                    html.push(td(one.name));
                    html.push(td(action, 1));
                    html.push('</tr>');
                }

                $tbody.append(html.join(''));

                $tbody.find('tr').each(function(){
                    var self = $(this);
                    var info = JSON.parse(self.data('info').replace(/'/g, '"'));
                    self.data('info', info);
                    var $td0 = self.find('td:first').removeClass();
                    switch(info.statename){
                        case 'STOPPED':
                            $td0.addClass('muted');
                            break;
                        case 'RUNNING':
                            $td0.addClass('ns-green');
                            break;
                        case 'FATAL':
                            $td0.addClass('ns-red');
                            break;
                        case 'RESTARTING':
                            $td0.addClass('ns-yellow');
                            break;
                    }
                });
            }else{
                $tbody.append(tr);
            }
        });
    });

    $('table').on('click', '.action', function(){
        if(!confirm('确定吗？')){
            return false;
        }
        var self = $(this);
        var action = self.hasClass('stop') ? 'stop' : 'restart';
        var $tr = self.parents('tr:first');
        var $host = $tr.parents('[data-host]:first');
        var info = $tr.data('info');
        $.post('/', {
            action: action, name: info.name, group: info.group,
            host: $host.data('host'), port: $host.data('port')
        }, function(res){
        });
    });

    $hosts.on('click', '.action.del', function(){
        if(!confirm('确认删除吗？')){
            return;
        }
        var self = $(this);
        $.post('/', {action: 'del', id: self.data('id')}, function(res){
            if(res.err){
                ns.show_dialog(res.msg, '错误', 'ns-red');
            }else{
                ns.show_dialog('已删除', '成功', 'ns-green');
                self.parents('[data-host]:first').remove();
            }
        });
    });

})(jQuery);
