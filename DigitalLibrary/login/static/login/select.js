        //全选
        function ckAll(){
            //check元素应该有个属性是checked，代表是否被选中
            var flag = document.getElementById("allChecks").checked;
            var cks = document.getElementsByName("input[]");
            for(var i=0;i<cks.length;i++){
                cks[i].checked=flag;
            }
        }
        
        //批量添加至检索结果页面
        function searchhis_multi_Add(){
            if(!confirm("确定添加这些到您的检索结果记录中吗?")){
                return;
            }
            var cks=document.getElementsByName("input[]");
            var str = "";
            //拼接所有的id
            for(var i=0;i<cks.length;i++){
            //被checked了的就获取其值进行拼接
                if(cks[i].checked){
                    str+=cks[i].value+",";
                }
            }
            //去掉字符串未尾的','
            str=str.substring(0, str.length-1);
            location.href='/readerCenter/searchlist_multi_add/?multiISBN='+str;
        }


        //从检索结果页面批量删除
        function searchhis_multi_Del(){
            if(!confirm("确定删除这些记录吗?")){
                return;
            }
            var cks=document.getElementsByName("input[]");
            var str = "";
            //拼接所有的id
            for(var i=0;i<cks.length;i++){
                if(cks[i].checked){
                    str+=cks[i].value+",";
                }
            }
            //去掉字符串未尾的','
            str=str.substring(0, str.length-1);
            //此处的地址问题怎么处理？为什么仍旧为相对位置（相对于search）
            location.href='/readerCenter/searchlist_multi_del/?multiID='+str;
        }

        
        //批量添加至我的图书馆页面
        function mylib_multi_Add(){
            if(!confirm("确定添加这些到您的检索结果记录中吗?")){
                return;
            }
            var cks=document.getElementsByName("input[]");
            var str = "";
            //拼接所有的id
            for(var i=0;i<cks.length;i++){
            //被checked了的就获取其值进行拼接
                if(cks[i].checked){
                    str+=cks[i].value+",";
                }
            }
            //去掉字符串未尾的','
            str=str.substring(0, str.length-1);
            location.href='/readerCenter/mylib_multi_add/?multiISBN='+str;
        }