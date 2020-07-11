import uuid, time, enum, contextlib
from sqlalchemy import Column, Integer, Text, String, DateTime, Sequence, Date, Boolean, Float, ForeignKey, Enum, \
    PickleType

from wk import generate_random_id, generate_hash


class IdentityType(enum.Enum):
    user_name = 1
    phone = 2
    email = 3
    qq = 4
    wechat = 5
    weibo = 6


class ArticleContentType(enum.Enum):
    text_plain = 1
    text_html = 2
    text_markdown = 3


class SiteContentType(enum.Enum):
    article = 1
    document = 2
    collection = 3
    entry = 4
    video = 5
    question = 6
    answer = 7
    knowledge_card = 8
    mind_map = 9
    note = 10


class sql:
    from sqlalchemy import Column, Integer, Text, String, DateTime, Sequence, Date, Boolean, Float
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, scoped_session
    Model = declarative_base()

    class PrettyPrint:

        def __repr__(self):
            from sqlalchemy import inspect
            mapper = inspect(self.__class__)
            keys = []
            for column in mapper.attrs:
                keys.append(column.key)
            return '''<%s object : %s>''' % (
                self.__class__.__name__, ' , '.join(['%s=%s' % (key, getattr(self, key)) for key in keys]))

    class Engine:
        def __init__(self, engine_uri, echo=True, *args, **kwargs):
            self.engine = sql.create_engine(engine_uri, echo=echo, *args, **kwargs)

            RealSession = sql.scoped_session(sql.sessionmaker(bind=self.engine))

            class Session:
                def __init__(self, autocommit=True, autoclose=True, autoexpunge=False, autofill=False):
                    self.autocommit = autocommit
                    self.autoclose = autoclose
                    self.autoexpunge = autoexpunge
                    self.autofill = autofill
                    self.real_sess = RealSession()

                def expunge(self, x):
                    return self.real_sess.expunge(x)

                def expunge_all(self):
                    return self.real_sess.expunge_all()

                def query(self, model):
                    return self.real_sess.query(model)

                def rollback(self):
                    return self.real_sess.rollback()

                def close(self):
                    return self.real_sess.close()

                def add(self, obj):
                    if self.autofill:
                        if hasattr(obj, 'auto_fill'):
                            obj.auto_fill()
                    return self.real_sess.add(obj)

                def commit(self):
                    return self.real_sess.commit()

                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc_val, exc_tb):
                    try:

                        if self.autocommit:
                            self.commit()
                    except:
                        self.rollback()
                        raise
                    finally:
                        if self.autoexpunge:
                            self.expunge_all()
                        if self.autoclose:
                            self.close()

            self.Session = Session
            self.PrettyPrint = sql.PrettyPrint
            self.Model = sql.Model

        def get_session(self, autocommit=True, autoclose=True, autoexpunge=False, autofill=False):
            sess = self.Session(autoclose=autoclose, autocommit=autocommit, autoexpunge=autoexpunge, autofill=autofill)
            return sess

        def create_all(self):
            return self.Model.metadata.create_all(self.engine)


class StateStore(sql.Model, sql.PrettyPrint):
    __tablename__ = 'state_store'
    id = sql.Column(sql.String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    c1 = sql.Column(sql.String(80))
    c2 = sql.Column(sql.String(80))
    c3 = sql.Column(sql.String(80))
    c4 = sql.Column(sql.String(80))
    c5 = sql.Column(sql.String(80))
    expire_time = sql.Column(sql.Float)


class StateManger:
    def __init__(self, engine, Model):
        assert isinstance(engine, sql.Engine)
        assert Model is StateStore
        self.engine = engine
        self.Model = Model

    def produce_key(self, timedelta=30 * 60):
        uid = uuid.uuid4().hex
        self.push('key', uid, timedelta=timedelta)
        return uid

    def delete(self, id):
        with self.engine.get_session() as sess:
            return sess.query(self.Model).filter(self.Model.id == id).delete()

    def check_key(self, key):
        self.get('key', key)

    def push(self, *args, timedelta=5 * 60, ):
        assert len(args) <= 5
        t = time.time()
        keys = ['c1', 'c2', 'c3', 'c4', 'c5']
        keys = keys[:len(args)]
        dic = dict(zip(keys, args))
        state = self.Model(**dic, expire_time=t + timedelta)
        with self.engine.get_session() as sess:
            sess.add(state)

    def flush(self):
        '''这个函数需要被定期地调用，但是目前还没有'''
        t = time.time()
        sess = self.engine.get_session()
        sess.query(self.Model).filter(self.Model.expire_time < t).delete()
        sess.commit()

    def get(self, *args):
        keys = [
            self.Model.c1, self.Model.c2, self.Model.c3, self.Model.c4, self.Model.c5
        ]
        t = time.time()
        keys = keys[:len(args)]
        dic = dict(zip(keys, args))
        dic = [k == v for k, v in dic.items()]
        with self.engine.get_session(autocommit=False) as sess:
            res = sess.query(self.Model).filter(*dic).filter(self.Model.expire_time > t).all()
            return res


class User(sql.Model, sql.PrettyPrint):
    __tablename__ = 'users'
    id = sql.Column(sql.String(80), primary_key=True, default=generate_random_id, nullable=False)
    username = sql.Column(sql.String(80), unique=True, default=lambda: '用户' + uuid.uuid4().hex)
    avatar = sql.Column(sql.String(80))
    gender = sql.Column(sql.String(10))
    introduction = sql.Column(sql.String(500))
    registered_at = sql.Column(sql.Float, default=lambda: time.time())

    def auto_fill(self):
        if not self.id:
            self.id = generate_random_id()
        if not self.avatar:
            self.avatar = 'http://www.gravatar.com/avatar/%s?s=256&d=retro' % (generate_hash(self.id))
        return self


class UserAuth(sql.Model, sql.PrettyPrint):
    __tablename__ = 'user_auths'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    user_id = Column(String(80), ForeignKey('users.id'), nullable=False)
    identity_type = Column(Enum(IdentityType))
    identifier = Column(String(80), unique=True)
    credential = Column(String(80))


class Article(sql.Model, sql.PrettyPrint):
    __tablename__ = 'articles'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    author_id = Column(String(80), ForeignKey('users.id', ondelete='SET NULL'))
    title = Column(Text, nullable=False)

    summary = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    content_type = Column(Enum(ArticleContentType), nullable=False)
    content_text = Column(Text)
    content_html = Column(Text)
    content_markdown = Column(Text)

    introduction = sql.Column(sql.String(500))
    created_at = Column(Float, default=time.time, nullable=False)
    updated_at = Column(Float)
    published_at = Column(Float)
class Draft(sql.Model, sql.PrettyPrint):
    __tablename__ = 'drafts'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    author_id = Column(String(80), ForeignKey('users.id', ondelete='SET NULL'))
    title = Column(Text, nullable=False)

    summary = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    content_type = Column(Enum(ArticleContentType), nullable=False)
    content_text = Column(Text)
    content_html = Column(Text)
    content_markdown = Column(Text)

    introduction = sql.Column(sql.String(500))
    created_at = Column(Float, default=time.time, nullable=False)
    updated_at = Column(Float)


class Document(sql.Model, sql.PrettyPrint):
    __tablename__ = 'documents'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    author_id = Column(String(80), ForeignKey('users.id', ondelete='SET NULL'))

    filename = Column(String(80))

    category = Column(String(200))
    introduction = Column(String(500))

    uploaded_at = Column(Float, default=time.time)
    mime_type = Column(String(80))


class Collection(sql.Model, sql.PrettyPrint):
    __tablename__ = 'collections'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    name = Column(String(80), nullable=False)
    author_id = Column(String(80), ForeignKey('users.id', ondelete='SET NULL'))
    introduction = Column(String(500))
    content = Column(PickleType, default=[])
    created_at = Column(Float, default=time.time, nullable=False)
    updated_at = Column(Float)
    published_at = Column(Float)


class Entry(sql.Model, sql.PrettyPrint):
    __tablename__ = 'entries'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    name = Column(String(80), nullable=False)
    author_id = Column(String(80), ForeignKey('users.id', ondelete='SET NULL'))
    introduction = Column(String(500))
    content = Column(Text)
    created_at = Column(Float, default=time.time, nullable=False)
    updated_at = Column(Float)
    published_at = Column(Float)


class Video(sql.Model, sql.PrettyPrint):
    __tablename__ = 'videos'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    title = Column(String(80), nullable=False)
    author_id = Column(String(80), ForeignKey('users.id', ondelete='SET NULL'))
    introduction = Column(String(500))
    filename = Column(String(80))
    created_at = Column(Float, default=time.time, nullable=False)
    updated_at = Column(Float)
    published_at = Column(Float)


class KnowledgeCard(sql.Model, sql.PrettyPrint):
    __tablename__ = 'knowledge_cards'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    title = Column(String(80), nullable=False)
    author_id = Column(String(80), ForeignKey('users.id', ondelete='SET NULL'))
    introduction = Column(String(500))
    content = Column(Text)
    created_at = Column(Float, default=time.time, nullable=False)
    updated_at = Column(Float)
    published_at = Column(Float)


class MindMap(sql.Model, sql.PrettyPrint):
    __tablename__ = 'mind_maps'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    title = Column(String(80), nullable=False)
    author_id = Column(String(80), ForeignKey('users.id', ondelete='SET NULL'))
    introduction = Column(String(500))
    content = Column(Text)
    created_at = Column(Float, default=time.time, nullable=False)
    updated_at = Column(Float)
    published_at = Column(Float)


class Note(sql.Model, sql.PrettyPrint):
    __tablename__ = 'notes'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    title = Column(String(80), nullable=False)
    author_id = Column(String(80), ForeignKey('users.id', ondelete='SET NULL'))
    introduction = Column(String(500))
    content = Column(Text)
    created_at = Column(Float, default=time.time, nullable=False)
    updated_at = Column(Float)
    published_at = Column(Float)


class Question(sql.Model, sql.PrettyPrint):
    __tablename__ = 'questions'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    title = Column(String(80), nullable=False)
    author_id = Column(String(80), ForeignKey('users.id', ondelete='SET NULL'))
    introduction = Column(String(500))
    content = Column(Text)
    created_at = Column(Float, default=time.time, nullable=False)
    updated_at = Column(Float)
    published_at = Column(Float)


class Answer(sql.Model, sql.PrettyPrint):
    __tablename__ = 'answers'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    title = Column(String(80), nullable=False)
    author_id = Column(String(80), ForeignKey('users.id', ondelete='SET NULL'))
    introduction = Column(String(500))
    content = Column(Text)
    created_at = Column(Float, default=time.time, nullable=False)
    updated_at = Column(Float)
    published_at = Column(Float)


class Comment(sql.Model, sql.PrettyPrint):
    __tablename__ = 'comments'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    target_type = Column(Enum(SiteContentType))
    target_id = Column(String(80), nullable=False)
    author_id = Column(String(80), ForeignKey('users.id', ondelete='SET NULL'))
    parent_id = Column(String(80))
    content = Column(Text)
    created_at = Column(Float, default=time.time, nullable=False)


class Poll(sql.Model, sql.PrettyPrint):
    __tablename__ = 'polls'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    target_type = Column(Enum(SiteContentType))
    target_id = Column(String(80), nullable=False)
    author_id = Column(String(80), ForeignKey('users.id', ondelete='SET NULL'))
    created_at = Column(Float, default=time.time, nullable=False)
    is_positive = Column(Boolean)


class Tag(sql.Model, sql.PrettyPrint):
    __tablename__ = 'tags'
    id = Column(String(80), primary_key=True, default=lambda: uuid.uuid4().hex, nullable=False)
    name = Column(String(20), nullable=False)
    articles = Column(PickleType, default=[], nullable=False)
    questions = Column(PickleType, default=[], nullable=False)
    answers = Column(PickleType, default=[], nullable=False)
    collections = Column(PickleType, default=[], nullable=False)
    documents = Column(PickleType, default=[], nullable=False)
    videos = Column(PickleType, default=[], nullable=False)
    entries = Column(PickleType, default=[], nullable=False)


class TableDesign:
    class users:
        id = ''
        username = ''
        avatar = ''
        introduction = ''
        registered_at = ''

    class user_auths:
        id = ''
        user_id = ''
        identity_type = ['username', 'phone', 'email']
        identifier = ''
        credential = ''

    class articles:
        id = ''
        author_id = ''
        title = ''
        summary = ''
        content = ''
        content_type = ['text/plain', 'text/html', 'text/markdown']
        content_text = ''
        created_at = ''
        updated_at = ''
        published_at = ''

    class comments:
        id = ''
        target_type = ['article', 'question', 'answer', 'collection', 'document', 'video', 'entry', '']
        target_id = ''
        author_id = ''
        parent_id = ''
        content = ''
        created_at = ''

    class polls:
        id = ''
        target_type = ['article', 'question', 'answer', 'collection', 'document', 'video']
        target_id = ''
        author_id = ''
        created_at = ''
        is_positive = ''

    class tags:
        id = ''
        name = ''
        articles = ''
        questions = ''
        answers = ''
        collections = ''
        documents = ''
        videos = ''

    class documents:
        pass

    class questions:
        pass

    class answers:
        pass
