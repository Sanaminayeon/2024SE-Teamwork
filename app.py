from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
import bcrypt
import os

# SQLite 数据库连接
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 创建用户数据库模型
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    posts = relationship("Post", back_populates="user")

# 创建帖子数据库模型
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="posts")

Base.metadata.create_all(bind=engine)

# FastAPI 实例
app = FastAPI()

# Pydantic 模型
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserLogout(BaseModel):
    username: str

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 注册用户
@app.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

# 用户登录
@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return {"message": "Login successful!", "user_id": db_user.id}

# 创建帖子
@app.post("/create_post")
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == post.user_id).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="User not found or not logged in")

    new_post = Post(title=post.title, content=post.content, user_id=post.user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"message": "Post created successfully", "post_id": new_post.id, "user_id": post.user_id}

# 获取所有帖子
@app.get("/posts", response_model=list[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
        }
        for post in posts
    ]

# 用户登出
@app.post("/logout")
async def logout(user: UserLogout):
    return {"message": f"User {user.username} logged out successfully"}
