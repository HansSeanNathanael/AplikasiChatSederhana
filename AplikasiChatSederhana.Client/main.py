import flet as ft
import base64
import threading
from time import sleep
from signin_form import *
from signup_form import *
from database import *
from chat_message import *
from server_connection import Server

nekot = ""

def main(page: ft.Page):
    # server = Server('0.tcp.ap.ngrok.io', 16590)
    # server = Server('0.tcp.ap.ngrok.io', 19955)
    server = Server('127.0.0.1', 9000)
    db = Database()
    # thread = threading.Thread(target=listen, daemon=True)
    # thread.start()
    page.title = "Chat Flet Messenger"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def add_chat():
        while True:
            if server.getGlobalMsg() == "":
                sleep(1)
            if server.getGlobalMsg() != "":
                value = server.getGlobalMsg()
                # print("ini main" + value)
                if value["keperluan"] == "PRIVATE":
                    isExist = db.is_room_exist(value['id_pengirim'], value['keperluan'])
                    if not isExist:
                        db.write_room(value['id_pengirim'], "")
                    roomId = db.get_room(value['id_pengirim'], value['keperluan'])
                    # emoji_list.options.append(ft.dropdown.Option(roomId))
                    contentChat = ""
                    if value['bentuk_chat'] == "CHAT" :
                        db.write_chat(roomId, value["chat"], "")
                        contentChat = value["chat"]
                    else :
                        db.write_chat(roomId, value["nama_file"], "")
                        isifile = base64.b64decode(value["isi_file"])
                        fp = open("receivedFile/" + value["nama_file"],'wb+')
                        contentChat = value["nama_file"]
                        fp.write(isifile)
                        fp.close()
                        print("Berhasil")
                    chat.controls.append(ChatMessage(                            
                            Message(
                                user=value['id_pengirim'],
                                text=value["chat"],
                                message_type="chat_message",
                            )
                        )
                    )
                else:
                    isExist = db.is_room_exist(value['id_tujuan'], value['keperluan'])
                    if not isExist:
                        db.write_room(value['id_tujuan'], value['id_pengirim'])
                    roomId = db.get_room(value['id_tujuan'], value['keperluan'])
                    # emoji_list.options.append(ft.dropdown.Option(roomId))
                    if value['bentuk_chat'] == "CHAT" :
                        db.write_chat(roomId, value["chat"], "")
                        contentChat = value["chat"]
                    else :
                        db.write_chat(roomId, value["nama_file"], "")
                        isifile = base64.b64decode(value["isi_file"])
                        fp = open("receivedFile/" + value["nama_file"],'wb+')
                        contentChat = value["nama_file"]
                        fp.write(isifile)
                        fp.close()
                        print("Berhasil")
                    
                    chat.controls.append(ChatMessage(                            
                            Message(
                                user=value['id_pengirim'],
                                text=contentChat,
                                message_type="chat_message",
                            )
                        )
                    )
                server.setGlobalMsgEmpty()
                page.update()

    # ***************  Functions             *************
    def dropdown_changed(e):
        if (emoji_list.value == "Chat Room"):
            page.clean()
            page.add(
                ft.Row(
                    controls=[
                        emoji_list,
                        ft.ElevatedButton(
                            text="Log Out",
                            bgcolor=ft.colors.CYAN_300,
                            color=ft.colors.BLACK,
                            on_click=btn_exit,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )
            page.add(
                ft.Text(value="Pilih room chat terlebih dahulu", size=50, color=ft.colors.BLACK),
            )
        elif page.session.contains_key("user"):
            page.clean()
            chat.controls.clear()

            if (emoji_list.value == "Add Private Room"):           
                page.add(
                    ft.Row(
                        controls=[
                            emoji_list,
                            ft.Text(value="Add New Private Room", color=ft.colors.BLACK),
                            ft.ElevatedButton(
                                text="Log Out",
                                bgcolor=ft.colors.CYAN_300,
                                color=ft.colors.BLACK,
                                on_click=btn_exit,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                )
                page.add(
                    ft.Row(
                        controls=[
                            add_new_receiver_edit_text,
                            ft.IconButton(
                                icon=ft.icons.SEND_ROUNDED,
                                tooltip="Tuliskan id tujuan",
                                on_click=add_new_receiver_click,
                            ),
                        ],
                    )
                )
            else:
                # server.stopListen()
                
                roomId = emoji_list.value
                isGroupRoom = db.is_group_room(roomId)
                user_logged_in = page.session.get('user')
                room_title = "Group"
                chats = db.get_chat(roomId)
                if (isGroupRoom):
                    room_title = db.get_group_room_name(roomId)
                    if chats:
                        for chatItem in chats:
                            if (chatItem[4] == "1"):
                                chat.controls.append(ChatMessage(                            
                                        Message(
                                            user=user_logged_in,
                                            text=chatItem[2],
                                            message_type="chat_message",
                                        )
                                    )
                                )
                            else:
                                chat.controls.append(ChatMessage(                            
                                        Message(
                                            user=room_title,
                                            text=chatItem[2],
                                            message_type="chat_message",
                                        )
                                    )
                                )
                else:
                    room_title = db.get_user_from_private_room(roomId)
                    if chats:
                        for chatItem in chats:
                            if (chatItem[4] == "1"):
                                chat.controls.append(ChatMessage(                            
                                        Message(
                                            user=user_logged_in,
                                            text=chatItem[2],
                                            message_type="chat_message",
                                        )
                                    )
                                )
                            else:
                                chat.controls.append(ChatMessage(                            
                                        Message(
                                            user=room_title,
                                            text=chatItem[2],
                                            message_type="chat_message",
                                        )
                                    )
                                )
                page.session.set("curr_receiver", room_title)
                page.session.set("room_id", roomId)
                page.add(
                    ft.Row(
                        controls=[
                            emoji_list,
                            ft.Text(value=room_title, color=ft.colors.BLACK),
                            ft.ElevatedButton(
                                text="Log Out",
                                bgcolor=ft.colors.CYAN_300,
                                color=ft.colors.BLACK,
                                on_click=btn_exit,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                )
                page.add(
                    ft.Container(
                        content=chat,
                        border=ft.border.all(1, ft.colors.OUTLINE),
                        border_radius=5,
                        padding=10,
                        expand=True,
                    )
                )
                page.add(
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                icon_size=40,
                                tooltip="Add File",
                                on_click=dialog_picker_file
                            ),
                            new_message,
                            ft.IconButton(
                                icon=ft.icons.SEND_ROUNDED,
                                tooltip="Send message",
                                on_click=send_message_click,
                            ),
                        ],
                    )
                )
                thread = threading.Thread(target=add_chat, daemon=True)
                thread.start()
            
            page.update()

    def open_dlg_sign_up_success():
        page.dialog = dlg_sign_up_success
        dlg_sign_up_success.open = True
        page.update()

    def open_dlg_sign_un_failed():
        page.dialog = dlg_sign_up_failed
        dlg_sign_up_failed.open = True
        page.update()
    
    def open_dlg_sign_in_failed():
        page.dialog = dlg_sign_in_failed
        dlg_sign_in_failed.open = True
        page.update()

    def close_dlg(e):
        if (dlg_sign_up_success.open):
            dlg_sign_up_success.open = False
            page.route = "/"
        elif (dlg_sign_up_failed.open):
            dlg_sign_up_failed.open = False
        elif (dlg_sign_in_failed.open):
            dlg_sign_in_failed.open = False
        page.update()

    def sign_in(user: str, password: str):
        data = server.sign_in(user, password)
        print(data)
        if "token" in data:
            if db.write_token_to_db(user, data["token"], password):
                global nekot
                nekot = data["token"]
                print("Redirecting to chat...")
                page.session.set("user", user)
                page.route = "/chat"
                page.pubsub.send_all(
                    Message(
                        user=user,
                        text=f"{user} has joined the chat.",
                        message_type="login_message",
                    )
                )
            else :
                print("Failed to save token to database...")
        else:
            print("User no exist ...")
            open_dlg_sign_in_failed()
        page.update()

    def sign_up(user: str, password: str):
        data = server.sign_up(user, password)
        print(data)
        if "id_akun" in data:
            print(f'{data["id_akun"]} Successfully Registered User...')
            open_dlg_sign_up_success()
        else:
            print("Register Failed...")
            open_dlg_sign_un_failed()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK, size=12)
        elif message.message_type == "logout_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    def send_message_click(e):
        if new_message.value == "":
            return
        global nekot
        usr = page.session.get("user")
        curr_rec = page.session.get("curr_receiver")
        room_id = page.session.get("room_id")
        data = server.send_chat(nekot, curr_rec, new_message.value)
        if "success" in data:
            print("[SUCCESS SEND CHAT MAIN]")
            print(data)
            db.write_chat(room_id, new_message.value, "", "1")
            page.pubsub.send_all(
                Message(
                    user=usr,
                    text=new_message.value,
                    message_type="chat_message",
                )
            )
            new_message.value = ""
            page.update()

    def add_new_receiver_click(e):
        if add_new_receiver_edit_text.value == "":
            return
        isExist = db.is_room_exist(add_new_receiver_edit_text.value, "PRIVATE")
        if not isExist:
            rooms = db.get_rooms()
            for roomItem in rooms:
                option = find_option(roomItem[0])
                if option != None:
                    emoji_list.options.remove(option)
            db.write_room(add_new_receiver_edit_text.value, "")
            rooms = db.get_rooms()
            for room in rooms:
                emoji_list.options.append(ft.dropdown.Option(room[0]))
        add_new_receiver_edit_text.value = ""
        page.update()

    def dialog_picker_file(e):
        page.dialog = dlg_ask_file
        dlg_ask_file.open = True
        page.update()
    
    def close_dlg_ask_file(e):
        dlg_ask_file.open = False
        page.update()

        file_name = "sendFile/" + file_name_tf.value

        with open(file_name, "rb") as img_file:
            my_string = base64.b64encode(img_file.read()).decode()

        curr_rec = page.session.get("curr_receiver")
        global nekot

        # print("tes" + my_string + "tes")
        server.send_file(nekot, curr_rec, file_name_tf.value, my_string)
        file_name_tf.value = ""

    def btn_signin(e):
        page.route = "/"
        page.update()

    def btn_signup(e):
        page.route = "/signup"
        page.update()

    def btn_exit(e):
        user = page.session.get("user")
        token = db.get_user_token(user)
        data = server.logout(token)
        if "success" in data:
            status_delete_token = db.delete_user_token(token)
            if (status_delete_token):
                emoji_list.value = "Chat Room"
                global nekot
                nekot = ""
                rooms = db.get_rooms()
                for roomItem in rooms:
                    option = find_option(roomItem[0])
                    if option != None:
                        emoji_list.options.remove(option)
                page.pubsub.send_all(
                    Message(
                        user=user,
                        text=f"{user} has logout from the chat.",
                        message_type="logout_message",
                    )
                )
                page.session.remove("user")
                page.route = "/"
                page.update()
        else :
            print("Logout Failed")
    
    def find_option(option_name):
        for option in emoji_list.options:
            if option_name == option.key:
                return option
        return None

    # ************          Aplication UI              **********************************
    principal_content = ft.Column(
        [
            ft.Icon(ft.icons.WECHAT, size=200, color=ft.colors.BLUE),
            ft.Text(value="Realm Kelompok 6", size=50, color=ft.colors.WHITE),
        ],
        height=400,
        width=600,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    emoji_list = ft.Dropdown(
        on_change=dropdown_changed,
        options=[
            ft.dropdown.Option("Chat Room"),
            ft.dropdown.Option("Add Private Room"),
        ],
        value="Chat Room",
        alignment=ft.alignment.center,
    )

    signin_UI = SignInForm(sign_in, btn_signup)
    signup_UI = SignUpForm(sign_up, btn_signin)

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    file_name_tf = ft.TextField(
        hint_text="Write file name...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=close_dlg_ask_file
    )

    add_new_receiver_edit_text = ft.TextField(
        hint_text="Tuliskan id tujuan",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=add_new_receiver_click,
    )

    dlg_sign_up_success = ft.AlertDialog(
        modal=True,
        title=ft.Container(
            content=ft.Icon(
                name=ft.icons.CHECK_CIRCLE_OUTLINED, color=ft.colors.GREEN, size=100
            ),
            width=120,
            height=120,
        ),
        content=ft.Text(
            value="Congratulations\nYour account has been successfully created\nPlease Sign In",
            text_align=ft.TextAlign.CENTER,
        ),
        actions=[
            ft.ElevatedButton(
                text="Continue", color=ft.colors.BLACK, on_click=close_dlg
            )
        ],
        actions_alignment="center",
        on_dismiss=lambda e: print("Dialog dismissed!"),
    )

    dlg_ask_file = ft.AlertDialog(
        modal=True,
        content=file_name_tf,
        actions=[
            ft.ElevatedButton(
                text="Continue", color=ft.colors.BLACK, on_click=close_dlg_ask_file
            )
        ],
        actions_alignment="center",
        on_dismiss=lambda e: print("Dialog dismissed!"),
    )

    dlg_sign_up_failed = ft.AlertDialog(
        modal=True,
        title=ft.Container(
            content=ft.Icon(
                name=ft.icons.ERROR_OUTLINE, color=ft.colors.GREEN, size=100
            ),
            width=120,
            height=120,
        ),
        content=ft.Text(
            value="Sorry\nFailed to create an account\nPlease Try Again",
            text_align=ft.TextAlign.CENTER,
        ),
        actions=[
            ft.ElevatedButton(
                text="Continue", color=ft.colors.BLACK, on_click=close_dlg
            )
        ],
        actions_alignment="center",
        on_dismiss=lambda e: print("Dialog dismissed!"),
    )

    dlg_sign_in_failed = ft.AlertDialog(
        modal=True,
        title=ft.Container(
            content=ft.Icon(
                name=ft.icons.ERROR_OUTLINE, color=ft.colors.GREEN, size=100
            ),
            width=120,
            height=120,
        ),
        content=ft.Text(
            value="Log In Failed,\nIncorrect User Name or Password\nPlease Try Again",
            text_align=ft.TextAlign.CENTER,
        ),
        actions=[
            ft.ElevatedButton(
                text="Continue", color=ft.colors.BLACK, on_click=close_dlg
            )
        ],
        actions_alignment="center",
        on_dismiss=lambda e: print("Dialog dismissed!"),
    )

    # chatdb = ChatsDB()
    # chats = chatdb.read_db(database)
    # if chats != None:
    #     for chatItem in chats:
    #         chat.controls.append(ChatMessage(                            
    #                     Message(
    #                         user=chatItem[1],
    #                         text=chatItem[2],
    #                         message_type="chat_message",
    #                     )
    #                 )
    #             )
    # page.update()

    # ****************        Routes              ******************
    def route_change(route):
        if page.route == "/":
            page.clean()
            page.add(
                ft.Row(
                    [principal_content, signin_UI],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        if page.route == "/signup":
            page.clean()
            page.add(
                ft.Row(
                    [principal_content, signup_UI],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        if page.route == "/chat":
            if page.session.contains_key("user"):
                global nekot

                # Inbox Feature
                data = server.get_inbox(nekot)
                for keys, values in data.items():
                    # print(keys, values)
                    for value in values:                
                        if value["keperluan"] == "PRIVATE":
                            isExist = db.is_room_exist(value['id_pengirim'], value['keperluan'])
                            if not isExist:
                                db.write_room(value['id_pengirim'], "")
                            roomId = db.get_room(value['id_pengirim'], value['keperluan'])
                            # emoji_list.options.append(ft.dropdown.Option(roomId))
                            if value['bentuk_chat'] == "CHAT" :
                                db.write_chat(roomId, value["chat"], "")
                            else :
                                db.write_chat(roomId, value["nama_file"], "")
                                isifile = base64.b64decode(value["isi_file"])
                                fp = open("receivedFile/" + value["nama_file"],'wb+')
                                fp.write(isifile)
                                fp.close()
                                print("Berhasil")
                        else:
                            isExist = db.is_room_exist(value['id_tujuan'], value['keperluan'])
                            if not isExist:
                                db.write_room(value['id_tujuan'], value['id_pengirim'])
                            roomId = db.get_room(value['id_tujuan'], value['keperluan'])
                            # emoji_list.options.append(ft.dropdown.Option(roomId))
                            if value['bentuk_chat'] == "CHAT" :
                                db.write_chat(roomId, value["chat"], "")
                            else :
                                db.write_chat(roomId, value["nama_file"], "")
                                isifile = base64.b64decode(value["isi_file"])
                                fp = open("receivedFile/" + value["nama_file"],'wb+')
                                fp.write(isifile)
                                fp.close()
                                print("Berhasil")
                
                rooms = db.get_rooms()
                for room in rooms:
                    emoji_list.options.append(ft.dropdown.Option(room[0]))
                
                page.clean()
                page.add(
                    ft.Row(
                        controls=[
                            emoji_list,
                            ft.ElevatedButton(
                                text="Log Out",
                                bgcolor=ft.colors.CYAN_300,
                                color=ft.colors.BLACK,
                                on_click=btn_exit,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                )
                page.add(
                    ft.Text(value="Pilih room chat terlebih dahulu", size=50, color=ft.colors.BLACK),
                )

            else:
                page.route = "/"
                page.update()

    page.on_route_change = route_change
    page.add(
        ft.Row([principal_content, signin_UI], alignment=ft.MainAxisAlignment.CENTER)
    )


ft.app(target=main, view=ft.WEB_BROWSER)
# ft.app(target=main)

if(nekot != ""):
    # server = Server('0.tcp.ap.ngrok.io', 19955)
    server = Server('127.0.0.1', 9000)
    db = Database()
    data = server.logout(nekot)
    if "success" in data:
        print(data["success"])
        db.delete_user_token(nekot)
    