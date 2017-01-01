# Генератор уведомлений #

Данный модуль позволяет сгенерировать html код любого необходимого типа уведомления.

Данный код может включать в себя ссылки на другие страницы, кнопки, и все что только можно сгенерировать согласно этой справке.

Каждый метод должен начинаться со слова generate_, а дальше то, что вы хотите сгенерировать.

Например, стандартная генерация уведомления о заявке на добавление в коллеги:

```
@staticmethod
def generate_add_colleague(author_nickname,
                           author_email,
                           author_id,
                           author_text,
                           id_addressee)
```

Данный код сгенерирует и вернет html форму с запросом о добавлении в коллеги, с кнопкой о согласии.

Каждый элемент уведомления располагается строго друг за другом по порядку сверху вниз. Каждый из элементов можно выровнять согласно правилам bootstrap.

* * *

Такой интерфейс создания уведомлений позволяет достаточно просто создавать новые типы уведомлений.

При создании нового уведомления, вам абсолютно не нужно заботиться о фронтенде пользователя и не нужно лазить в шаблоны.

Вам лишь необходимо добавить генерацию уведомления сюда в этот модуль, а также добавить `url` с запросом от этого уведомления, если ваше уведомление представляет из себя форму, а не набор ссылок с информацией.

При создании генератора, вы можете указывать любые нужные вам поля.

Во вьюшках, которые отправляют уведомления, код выглядит предельно просто. Например, отправка заявки в коллеги:

```
def get_send_request_colleagues(request, id):
    if request.method == "POST":

        try:
            # Получаем id отправителя и получателя
            current_user = User.objects.get(id_user=get_user_id(request))
            send_user = User.objects.get(id_user=id)

            # Получаем текущую дату
            date = str(datetime.datetime.now())
            date = date[:len(date) - 7]

            # Генериуем html уведомления
            html_text = WikiNotify.generate_add_colleague(author_nickname=current_user.nickname,
                                                          author_email=current_user.email,
                                                          author_id=current_user.id_user,
                                                          author_text=request.POST.get('notify-text'),
                                                          id_addressee=send_user.id_user)

            new_notify = Notification(title="Заявка на добавление в коллеги",
                                      type="add_colleague",
                                      id_sender=current_user,
                                      id_addressee=send_user,
                                      is_read=False,
                                      date=date,
                                      html_text=html_text)

            new_notify.save()

        except User.DoesNotExist:
            return get_error_page(request, ["User mot found!"])
    else:
        return get_error_page(request, ["Sorry, could not send the request to add the college for technical reasons!"])
```

Как видите, все просто! А как именно вы будете генерировать html уведомления, зависит только от Вас. Но вам все равно необходимо следовать следующим правилам, которые накладывает на вас главный frontend разработчик. Правила складываются из общих правил дизайна интерфейса платформы.

Единственная сложность, вам необходимо будет согласовать внедрение нового типа формы, если ваше новое уведомление представляет из себя форму.

**На данный момент, существуют следующие типы форм:**

1. `simple` - самое обычное уведомление
2. `add_colleague` - заявка на добавление в коллеги

**Правила генерации html уведомления:**










