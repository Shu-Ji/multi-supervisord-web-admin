!(function($){
    // get the detail infomation of each host:port
    var tr = '<tr><td colspan="4" class="ns-red">' +
        '连接到服务器失败。可能的原因：目标服务器未开启supervisord;' +
        ' 您的用户名或密码不正确。' + '</td></tr>';
    var $hosts = $('#hosts');
    $('[data-host]', $hosts).each(function(){
        var self = $(this);
        var $tbody = self.find('tbody').empty();
        $.get($hosts.data('detail'), {
            host: self.data('host'), port: self.data('port')
        }, function(res){
            if(res.err === false){  // DO NOT use `if(!res.err){...}`
                var html = [];

                function td(text){
                    return '<td>' + text + '</td>';
                }

                for(var i in res.info){
                    var one = res.info[i];
                    html.push('<tr>');
                    html.push(td(one.statename));
                    html.push(td(one.description));
                    html.push(td(one.name));
                    html.push(td('restart'));
                    html.push('</tr>');
                }

                $tbody.append(html.join(''));
            }else{
                $tbody.append(tr);
            }
        });
    });
})(jQuery);
