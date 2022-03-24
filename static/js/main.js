/**
 * Created by Administrator on 2017/9/15 0015.
 */
$(document).ready(function() {
    $('#form1').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            product: {
                message: 'The product is not valid',
                validators: {
                    notEmpty: {
                        message: 'product不能为空'
                    }
                }
            },
            env: {
                message: 'The env is not valid',
                validators: {
                    notEmpty: {
                        message: 'env不能为空'
                    }
                }
            },
            database: {
                message: 'The database is not valid',
                validators: {
                    notEmpty: {
                        message: 'database不能为空'
                    }
                }
            },
            sql: {
                message: 'The sql is not valid',
                validators: {
                    notEmpty: {
                        message: 'sql不能为空'
                    }
                }
            },
        }
    });
});

$(document).ready(function() {
    $.ajax({
        url: '/select/product/',
        type: 'POST',
        async: true,
        success: function (callback){
            var product_list=JSON.parse(callback);
            var html='<option value selected disabled>----Please choose----</option>';
            $.each(product_list,function(index,value){
                html+="<option value='"+value+"'>"+value+"</option>";
            });

            $('#product').html(html);
        },
        error: function () {
            alert("网络错误");
        }
    })
});

function confirmAct(){
    //var action=action;
    $('#form1').data('bootstrapValidator').validate();//手动对表单进行校检
    if (!$('#form1').data('bootstrapValidator').isValid()) {//判断校检是否通过
        // alert("验证不通过");
        return;
    }else {
        showMask();
        return manage();
    }
}

function manage() {
    let formdata=new FormData($("#form1")[0]);
    $.ajax({
        url: '/',
        type: 'POST',
        data: formdata,
        async: true,
        cache: false,
        contentType: false,
        processData: false,
        success:function (callback) {
            hideMask();
            let result_list=JSON.parse(callback);
            let html_ele='';
            let html_ele1='';
            let html_ele2='';
            if (result_list['code'] === undefined){
                let column_list = result_list['column_list'];
                let value_list = result_list['value_list'];
                $.each(column_list,function (index,item) {
                    html_ele1 +='<th>'+item+'</th>';
                });
                html_ele1 = '<thead>' + html_ele1 +'</thead>';
                $.each(value_list,function (index,item_list) {
                    $.each(item_list,function (i,item) {
                        html_ele2 +='<td>'+item+'</td>';
                    });
                    html_ele2 ='<tr>'+html_ele2+'</tr>';
                });
                html_ele2 = '<tbody>'+html_ele2+'</tbody>';
                html_ele = html_ele1 + html_ele2
                $('#table').html(html_ele);
            }else{
                html_ele = '<p>'+result_list['message']+'</p>';
                $('#advisor').html(html_ele);
                $('#myModal').modal('show');
                $("#btn2").removeClass('hide');
            }

        },

    });
}




//显示遮罩层
function showMask(){
    $("#mask").css("height",$(document).height());
    $("#mask").css("width",$(document).width());
    $("#mask").show();
}
//隐藏遮罩层
function hideMask(){

    $("#mask").hide();
}



function get_database(){
    var product = $('#product').val();
    var env = $('#env').val();
    if (product === ''){
        alert("product不能为空");
        return;
    }
    if (env === '' || env === undefined){
        alert("env不能为空");
        return;
    }
    $.ajax({
        url: '/select/database/',
        type: 'POST',
        data: {product:product,env:env},
        async: true,
        success: function (callback){
            var database_list=JSON.parse(callback);
            var html='';
            $.each(database_list,function(index,value){
                html+="<option value='"+value+"'>"+value+"</option>";
            });

            $('#database').html(html);
        },
        error: function () {
            alert("数据库连接出错！")
        }
    })
}

function get_env() {
    var product = $('#product').val();
    if (product === ''){
        alert("product不能为空");
        return;
    }
    $.ajax({
        url: '/select/env/',
        type: 'POST',
        data: {product:product},
        async: true,
        success: function (callback){
            var env_list=JSON.parse(callback);
            var html='<option value selected disabled>----Please choose----</option>';
            $.each(env_list,function(index,value){
                html+="<option value='"+value+"'>"+value+"</option>";
            });

            $('#env').html(html);
        },
        error: function () {
            alert("网络错误");
        }
    })
}

function EnterPress(e){
  if(e.keyCode === 13) {
      confirmAct();
  }
}