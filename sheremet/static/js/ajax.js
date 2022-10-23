function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function CreateRequest()
{
    var Request = false;

    if (window.XMLHttpRequest)
    {
        //Gecko-совместимые браузеры, Safari, Konqueror
        Request = new XMLHttpRequest();
    }
    else if (window.ActiveXObject)
    {
        //Internet explorer
        try
        {
             Request = new ActiveXObject("Microsoft.XMLHTTP");
        }
        catch (CatchException)
        {
             Request = new ActiveXObject("Msxml2.XMLHTTP");
        }
    }

    if (!Request)
    {
        console.log("Ошибка создания запроса");
    }

    return Request;
}

function SendRequest(r_method, r_path, r_args, r_handler, r_bad = function(request) { console.log("Ошибка запроса" + request.status) })
{
    //Создаём запрос
    console.log(r_path);
    var Request = CreateRequest();

    //Проверяем существование запроса еще раз
    if (!Request)
    {
        return;
    }

    //Назначаем пользовательский обработчик
      Request.onreadystatechange = function(){
        switch (Request.readyState) {
          //case 1: //console.log("<br/><em>1: Подготовка к отправке...</em>"); break
          //case 2: //console.log("<br/><em>2: Отправлен...</em>"); break
          //case 3: //console.log("<br/><em>3: Идет обмен..</em>"); break
          case 4:{
           if(Request.status==200){
                        r_handler(Request);
                     }else if(Request.status==404){
                        console.log("Ошибка запроса 404");
                     }
                      else r_bad(Request);

            break
            }
        }
    }

    //Проверяем, если требуется сделать GET-запрос
    if (r_method.toLowerCase() == "get" && r_args.length > 0)
    r_path += "?" + r_args;

    //Инициализируем соединение
    Request.open(r_method, r_path, true);

    if (r_method.toLowerCase() == "post")
    {
        //Если это POST-запрос

        //Устанавливаем заголовок
        Request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        //Посылаем запрос

        Request.send(r_args);
    }
    else
    {
        //Если это GET-запрос

        //Посылаем нуль-запрос
        Request.send(null);
    }
}
