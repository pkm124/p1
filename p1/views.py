from django.shortcuts import render
from p1.models import RandomForm
from django.contrib import messages
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

def InsertForm(request):
    if request.method=='POST':
        #if request.POST.get('id') and request.POST.get('username') and request.POST.get('email') and request.POST.get('password') and request.POST.get('address'):
        SaveRecords = RandomForm()
        generate_key()
        #print(str(encrypt_message(request.POST.get('id')),'UTF-8'))
        SaveRecords.id = request.POST.get('id')
        SaveRecords.username = encrypt_message(request.POST.get('username'))
        SaveRecords.email = encrypt_message(request.POST.get('email'))
        SaveRecords.password = encrypt_message(request.POST.get('password'))
        SaveRecords.address = encrypt_message(request.POST.get('address'))
        SaveRecords.save()
        messages.success(request,'Records Inserted of Random Form')
        return render(request, 'forms.html')
    else:
        return render(request, 'forms.html')


def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(bytes(encrypted_message, 'UTF-8')[2:-1])
    return decrypted_message.decode()

def fetch_records(request):
    display_obj = RandomForm.objects.all()
    temp=list(display_obj)
    store = []
    store_dict = {'id':'', 'username':'', 'email':'', 'address':'', 'password':''}
    print(type(temp))
    store.clear()
    for i in temp:
        store_dict['id'] = i.id
        store_dict['username'] = decrypt_message(i.username)
        store_dict['email'] = decrypt_message(i.email)
        store_dict['password'] = decrypt_message(i.password)
        store_dict['address'] = decrypt_message(i.address)
        store.append(store_dict)
        print(store)
        # print(type(bytes(i.username,'utf-8')))
    # display_obj_list = []
    # for i in display_obj:
    #     print(i.id)
    #     display_obj_list.append(decrypt_message(i.username))
    #     display_obj_list.append(decrypt_message(i.email))
    #     display_obj_list.append(decrypt_message(i.address))
    #     display_obj_list.append(decrypt_message(i.password))
    #     #i.append(i)
    return render(request, 'display_records.html', {'RandomForm': store})