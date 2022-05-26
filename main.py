# FastAPIインポート
from fastapi import FastAPI
# 型ヒントを行えるpydanticをインポート
from pydantic import BaseModel  

# 作成したモデル定義ファイルと設定ファイルをインポート
import db_model as m 
import db_setting as s 

# データクラス定義
# POSTとPUTで使うデータクラス
class UserBase(BaseModel):
    name : str
    mail : str

# FastAPIのインスタンス作成
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# GETメソッドで /usersにアクセスしたときの処理
# ユーザーの全件取得
@app.get("/users", tags=["users"])
async def read_users():
    #DBからユーザ情報を取得
    result = s.session.query(m.Users).all()
    return result

# POSTメソッドで /usersにアクセスしたときの処理
# ユーザーの新規登録
@app.post("/users", tags=["users"])
async def create_user(data: UserBase):
    # Usersモデルを変数に格納
    user = m.Users()
    # セッションを新規作成
    session = s.session()
    s.session.add(user)
    try:
        #リクエストBodyで受け取ったデータを流し込む
        user.name = data.name
        user.mail = data.mail
        #永続的にDBに反映
        session.commit()
    except:
        # DBへの反映は行わない
        session.rollback()
        raise
    finally:
        # 正常・異常どちらでもセッションは終わっておく
        session.close()


