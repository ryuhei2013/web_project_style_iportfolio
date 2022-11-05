from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.
        # ブランク登録フォームを表示する
        form = UserCreationForm()
    else:
        # Process completed form
        # 完成されたフォームを処理する
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            # ユーザーをログインして、ホームページにリダイレクトします。
            login(request, new_user)
            return redirect('ryuhei:index')

    # Display a blank or invalid form.
    # 空白または無効なフォームを表示します。
    context = {'form': form}
    return render(request, 'registration/register.html', context)

