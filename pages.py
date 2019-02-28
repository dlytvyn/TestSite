from app import app
from views import UserInformation, UserRegistration, LoginAPI, Logout

app.add_url_rule('/register',
                 view_func=UserRegistration.as_view('register'))

app.add_url_rule('/login',
                 view_func=LoginAPI.as_view('/login'))

app.add_url_rule('/user_info',
                 view_func=UserInformation.as_view('/user_info'))

app.add_url_rule('/logout',
                 view_func=Logout.as_view('/logout'))
