import os, shutil, glob, random, json, math, uuid, time, datetime, inspect, re
import jieba
import jieba.analyse
try:
    from textrank4zh import TextRank4Sentence
except:
    TextRank4Sentence=None
from wk.io import db, Piu
from wk import Folder, join_path, PointDict, web, DefaultDict, get_file_info
import wk
from .utils import get_keywords


class User(DefaultDict):
    default = dict(
        id=lambda: uuid.uuid4().hex,
        username=None,
        email=None,
        password=None,
        signature=None,
        avatar=lambda this: 'http://www.gravatar.com/avatar/%s?s=256&d=retro' % (wk.generate_hash(this['email'])),
        followers=0,
        following=0,
        zan=0,
        cai=0,
        favList=[],
        articles=[],
        public_articles=[],
        private_articles=[],
        recycled_articles=[],
        drafts=[],
        link=lambda this: join_path('/u', this['id']),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def publish_article(self, doc_id):
        self['public_articles'].append(doc_id)
        self['private_articles'].remove(doc_id)

    def new_article(self, doc_id):
        self['private_articles'].append(doc_id)

    def delete_recycled_article(self, doc_id):
        self['recycled_articles'].remove(doc_id)

    def delete_private_article(self, doc_id, hard=False):
        self['recycled_articles'].append(doc_id)
        self['private_articles'].remove(doc_id)
        if hard:
            self.delete_recycled_article(doc_id)

    def delete_public_article(self, doc_id, hard=False):
        self['recycled_articles'].append(doc_id)
        self['public_articles'].remove(doc_id)
        if hard:
            self.delete_recycled_article(doc_id)

    def is_own_article(self, doc_id):
        state = self._get_article_state(doc_id)
        if state == 3:
            return False
        return True

    def _get_article_state(self, doc_id):
        if doc_id in self['private_articles']:
            return 0
        elif doc_id in self['public_articles']:
            return 1
        elif doc_id in self['recycled_articles']:
            return 2
        else:
            return 3


class Document(DefaultDict, PointDict):
    default = dict(
        id=lambda: uuid.uuid4().hex,
        title=None,
        author=None,
        content=None,
        digest=None,
        keywords=None,
        category=None,
        tags=None,

        topic=None,
        introduction=None,
        picture=None,
        url=None,
        filename=None,

        click=None,
        view=None,
        zan=None,
        cai=None,
        created=time.time,
        last_edit=time.time,
        contributors=None,
        links=None,

        contentType=None,
        html=None,
        text=None,
        data=None,
    )
    info_fields = list(filter(lambda key: key not in ['content', 'html', 'text', 'data'], default.keys()))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def gen_search_context(self):
        searchable_keys=[
            'title','content','text','digest','keywords','category','tags','topic','introduction',
        ]
        context=''
        for key in searchable_keys:
            v=self.get(key,None)
            if v:
                if isinstance(v,(list,tuple,set)):
                    context+=';'.join([str(x) for x in v])+';'
                else:
                    context+=str(v)+';'
        return context




    def info(self):
        return {k: self[k] for k in self.info_fields}

    def set_default(self, name, value):
        if name not in self.keys() or self[name] is None or self[name]=='':
            self[name] = value

    def check_fields(self):
        assert self['html']
        assert self['text']
        assert self['title']

        t = time.time()
        self.set_default('created', t)
        self.set_default('last_edit', t)
        self.set_default('content', self['html'])
        use_textrank=False
        if not use_textrank:
            self.set_default('digest', self['text'][:min(100, len(self['text']))])
        else:
            tr4s=TextRank4Sentence()
            if not  self.get('digest',None):
                tr4s.analyze(text=self['text'])
                # print(tr4s.get_key_sentences(num=3))
                self['digest']=';'.join([x['sentence'] for x in tr4s.get_key_sentences(num=3)])
        self['digest'] = self['digest'][:min(100, len(self['digest']))]
        return self


class DocumentStorage:
    '''
    Worries:
        function id2url is given when called, once it changed, all the articles' urls are changed,
        then those references would become invalid.

    '''

    def __init__(self, path, id2url, update_when_start=True):
        self.id2url = id2url
        '''用于生成文章链接'''
        if not os.path.exists(path):
            os.makedirs(path)
        assert os.path.isdir(path)
        self.path = path
        dbpath = path + '/db'
        files_dir = path + '/files'
        self.db = db.Piu(dbpath)
        self.files_dir = Folder(files_dir)
        if update_when_start:
            self.update_all_article_fields()
    def update_all_article_fields(self):
        for k, v in self.db.dic.items():
            # print(k,v)
            if not 'filename' in v.keys() or not v['filename']:
                filename = k
                print('warning***: no filename for %s' % (k))
            else:
                filename = v['filename']
            with self.files_dir.open(filename, 'r') as f:
                doc = json.load(f)
                doc['id'] = k
                doc['filename'] = filename
                doc['url'] = self.id2url(doc['id'])
                doc = Document(**doc)

            with self.files_dir.open(filename, 'w') as f:
                json.dump(doc, f)
            info = doc.info()
            self.db.set(info['id'], info)

    def check(self, doc):
        def check_field(doc, name):
            if not name in doc.keys() or not doc[name]:
                return False
            return True

        if not check_field(doc, 'title'):
            return wk.StatusError(message='标题不能为空')
        if not check_field(doc, 'html'):
            return wk.StatusError(message='正文不能为空')
        if not check_field(doc, 'text'):
            return wk.StatusError(message='正文不能为空')
        return wk.StatusSuccess()

    def delete(self, doc_id, hard=False):
        assert self.db.exists(doc_id)
        info = self.db.get(doc_id)
        self.db.delete(doc_id)
        if hard:
            fn = info['filename']
            self.files_dir.remove(fn)
        return info

    def update_document(self, id, doc):
        document = self.get(id)
        document.update(**doc)
        document.update(keywords=get_keywords(document['text']))
        document = Document(**document).check_fields()
        info = document.info()
        with self.files_dir.open(id, 'w') as f:
            json.dump(document, f, ensure_ascii=False, indent=2)
        self.db.set(id, info)
        return info

    def save(self, doc):
        id = uuid.uuid4().hex
        doc.update(
            id=id, keywords=get_keywords(doc['text']),
            filename=id, url=self.id2url(id)
        )
        doc = Document(**doc).check_fields()
        info = doc.info()
        with self.files_dir.open(id, 'w') as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        self.db.set(id, info)
        return info

    def get_info(self, doc_id):
        return self.db.get(doc_id, None)

    def get(self, doc_id, default=None):
        if doc_id in self.db.dic.keys():
            filename = self.db.get(doc_id)['filename']
            with self.files_dir.open(filename, 'r') as f:
                return Document(**json.load(f))
        return default




class DocumentStorageEngine(DocumentStorage):
    def __init__(self, path, index_engine, usman, id2url, update_when_start=True):
        from wk import web
        assert isinstance(usman, web.UserManager)
        assert isinstance(index_engine, IndexEngine)
        super().__init__(path, id2url, update_when_start)
        self.index_engine = index_engine
        self.usman = usman
        self.recycle_bin = db.Piu(self.path + '/recycleBinDB')
        self.doc_market = db.Piu(self.path + '/publicDocumentsDB')

    def get_public(self, doc_id):
        if doc_id in self.doc_market.keys():
            return self.get(doc_id, None)
        return None

    def publish(self, user, doc_id):
        assert isinstance(user, User)
        self.doc_market.add(doc_id, doc_id)
        user.publish_article(doc_id)
        self.usman.update_user(user['id'], user)
        doc = self.get(doc_id)
        assert isinstance(doc,Document)
        self.index_engine.add_document(doc_id, doc.gen_search_context())
        return self.id2url(doc_id)

    def new(self, user, doc):
        assert isinstance(user, User)
        doc['author'] = user['id']
        info = self.save(doc)
        user.new_article(info['id'])
        self.usman.update_user(user['id'], user)
        return info

    def update(self, id, doc):
        return self.update_document(id, doc)

    def is_private(self, doc_id):
        return self.article_status(doc_id) == 0

    def is_public(self, doc_id):
        return self.article_status(doc_id) == 1

    def is_recycled(self, doc_id):
        return self.article_status(doc_id) == 2

    def article_status(self, doc_id):
        if self.doc_market.exists(doc_id):
            return 1
        elif self.recycle_bin.exists(doc_id):
            return 2
        elif self.db.exists(doc_id):
            return 0
        else:
            return 3

    def delete_article(self, user, doc_id, hard=False):
        assert isinstance(user, User)
        state = user._get_article_state(doc_id)
        if state == 0:
            return self.delete_private(user, doc_id, hard=hard)
        elif state == 1:
            return self.delete_public(user, doc_id, hard=hard)
        elif state == 2:
            return self.delete_recycled(user, doc_id)
        else:
            return 'Article Not Found.'

    def delete_recycled(self, user, doc_id):
        assert isinstance(user, User)
        self.recycle_bin.delete(doc_id)
        info = self.db.delete(doc_id)
        DocumentStorage.delete(self, doc_id, hard=True)
        user.delete_recycled_article(doc_id)
        self.usman.update_user(user['id'], user)
        return info

    def delete_public(self, user, doc_id, hard=False):
        assert isinstance(user, User)
        doc = self.get(doc_id)
        assert doc
        self.index_engine.remove_document(doc_id)
        if hard:
            self.doc_market.delete(doc_id)
            DocumentStorage.delete(self, doc_id, hard=True)
            user.delete_public_article(doc_id, hard=True)
        else:
            self.doc_market.delete(doc_id)
            self.recycle_bin.add(doc_id, doc_id)
            user.delete_public_article(doc_id, hard=False)
        self.usman.update_user(user['id'], user)

    def delete_private(self, user, doc_id, hard=False):
        assert isinstance(user, User)
        if hard:
            DocumentStorage.delete(self, doc_id, hard=True)
            user.delete_private_article(doc_id, hard=True)
        else:
            self.recycle_bin.add(doc_id, doc_id)
            user.delete_private_article(doc_id, hard=False)
        self.usman.update_user(user['id'], user)
    def topk_public(self,k):
        return sorted(list(self.doc_market.keys()),key=lambda key:self.db.get(key)['created'],reverse=True)[:k]

class FileDescriptor(DefaultDict):
    default = dict(
        id=lambda: uuid.uuid4().hex,
        original_filename=None,
        filename=None,
        name=lambda this: os.path.basename(this['original_filename']),
        keywords=None,
        absolute_filepath=None,
        relative_filepath=None,
        type='file',
        description=None,
        category=None,
        tags=None,
        topic=None,
        provider=None,
        owner=None,
        permission=None,
        size=None,
        mimetype=None,
        create_time=None,
        likes=0,
        dislikes=0,
        zan=0,
        cai=0,
        view=0,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class StaticStorageEngine(Folder):
    def __init__(self, path, check_when_start=False, include_dirs=[]):
        super().__init__(path)
        self.dbpath = path + '/db'
        self.db = db.Piu(self.dbpath)
        self.files_dir = Folder(self.path + '/file')
        self.images_dir = Folder(self.path + '/image')
        self.type2folder = {
            'file': self.files_dir,
            'image': self.images_dir,
        }
        self.include_dirs = include_dirs
        self.track_db = db.Piu(self.path + '/track_db')
        if check_when_start:
            self.startup()
            self.track_include_dirs()

    def track_include_dirs(self):
        def get_subject(tags):
            subjects = ['语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理']
            res=list(set(tags).intersection(set(subjects)))
            return res[0] if res else None

        for dir in self.include_dirs:
            folder = Folder(dir)
            print("Finding files...")
            fs = folder.glob('/**/*.*', recursive=True)
            self.db.pause_save()
            self.track_db.pause_save()
            for i, f in enumerate(fs):

                fn = os.path.basename(f)
                absolute_filepath = folder._truepath(f)
                tags = jieba.analyse.extract_tags(f, topK=10)
                subject=get_subject(tags)
                if self.track_db.exists(absolute_filepath):
                    id = self.track_db.get(absolute_filepath)
                    self.db.delete(id)
                    print('delete %s' % id)
                    # continue
                print('including:', absolute_filepath)
                fd = FileDescriptor(
                    filename=fn,
                    original_filename=fn,
                    absolute_filepath=absolute_filepath,
                    description=f,
                    category=os.path.dirname(f),
                    keywords=tags,
                    tags=tags,
                    subject=subject,
                )
                self.db.set(fd['id'], fd)
                self.track_db.set(absolute_filepath, fd['id'])
            self.db.resume_save(save_now=True)
            self.track_db.resume_save(save_now=True)

    def startup(self):
        self.db.pause_save()
        for k in list(self.db.keys()):
            v = self.db.get(k)
            v = FileDescriptor(**v)
            self.db.set(k, v)
            if ( not v['relative_filepath'] )and not  v['absolute_filepath']:
                self.db.delete(k)
                print('delete file %s'%k)
            elif v['relative_filepath'] and not self.exists( v['relative_filepath']):
                self.db.delete(k)
                print("File %s not exists. delete the record."%(v['relative_filepath']))
            elif v['absolute_filepath'] and not os.path.exists( v['absolute_filepath']):
                self.db.delete(k)
                print("File %s not exists. delete the record."%(v['absolute_filepath']))


        self.db.resume_save()
        # self.db.pprint()
    def update_file(self,id,file):
        info=self.db.get(id)
        info.update(**file)
        self.db.set(id,info)

    def send_file(self, id):
        info = self.db.get(id)
        if info:
            if info['absolute_filepath']:
                return web.send_file(info['absolute_filepath'])
            return web.send_file(self._truepath(info['relative_filepath']))
        else:
            return web.StatusErrorResponse(message='File Not Found.').jsonify()

    def get_file_info(self, id):
        info = self.db.get(id)
        # print(info)
        if not info['absolute_filepath']:
            # print(info['relative_filepath'])
            info['absolute_filepath'] = self._truepath(info['relative_filepath'])
        info.update(get_file_info(info['absolute_filepath']))
        return info
    def get(self,id,default=None):
        return self.db.get(id,default)
    def saveImage(self, file):
        return self._saveFile(file, dict(type='image'))

    def saveFile(self, file):
        return self._saveFile(file, dict(type='file'))

    def _saveFile(self, file, info={}):
        '''file:
        filename , name , save , mimetype , close
        '''
        type = info.get('type', 'file')
        id = uuid.uuid4().hex
        original_filename = file.filename
        mimetype = file.mimetype
        filename = '%s-%s' % (id, original_filename)
        folder = self.type2folder[type]
        relative_path = folder.name + '/' + filename
        absolute_path = folder._truepath(filename)
        folder.save_http_file(file, filename)
        fd = FileDescriptor(
            id=id,
            type=type,
            mimetype=mimetype,
            filename=filename,
            original_filename=original_filename,
            relative_filepath=relative_path,
            absolute_filepath=absolute_path,
        )
        fd.update(**folder.info(filename))
        self.db.set(id, fd)
        return fd

    def select(self, func=None, **kwargs):
        return self.db.select(func=func, **kwargs)

    def search(self, q, match_all=True, candidates=None):
        assert isinstance(candidates, (list, tuple))
        query = []
        for word in q.split():
            query += list(jieba.cut(word))

        def get_search_context(id):
            file = self.get_file_info(id)
            return '\t'.join([str(v) if v is not None else '' for v in file.values()])

        files = candidates if not candidates is None else self.db.keys()
        if match_all:

            for word in query:
                files = list(filter(lambda id: re.findall(word, get_search_context(id)), files))
            return files
        else:
            def match(text, ptns):
                for ptn in ptns:
                    if re.findall(ptn, text): return True
                return False

            files = list(filter(lambda id: match(get_search_context(id), query), files))
            return files


class IndexEngine:
    def __init__(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        dbpath = path + '/db'
        self.db = Piu(dbpath)
        self.path = path
        self.inverted, self.doc_num, self.idf, self.id2doc = self.restore()

    def restore(self):
        inverted = self.db.get('inverted', None)
        doc_num = self.db.get('doc_num', None)
        idf = self.db.get('idf', None)
        id2doc = self.db.get('id2doc', None)
        if inverted is None:
            inverted = {}
            doc_num = 0
            idf = {}
            self.db.set('inverted', inverted)
            self.db.set('doc_num', doc_num)
            self.db.set('idf', idf)
            self.db.set('id2doc', id2doc)
        return inverted, doc_num, idf, id2doc

    def save_all(self):
        self.db.set('inverted', self.inverted)
        self.db.set('doc_num', self.doc_num)
        self.db.set('idf', self.idf)
        self.db.set('id2doc', self.id2doc)

    def remove_document(self, doc_id, save=True):
        for term in self.inverted.keys():
            if doc_id in self.inverted[term]:
                self.inverted[term].pop(doc_id)
        self.doc_num -= 1
        for term in list(self.idf.keys()):
            if not self.doc_num:
                self.idf.pop(term)
                continue
            self.idf[term] = math.log10(self.doc_num / (len(self.inverted[term]) + 1e-10))
        if save:
            self.save_all()

    def remove_document_batch(self, doc_ids: list, save=True):
        for doc_id in doc_ids:
            for term in self.inverted.keys():
                if doc_id in self.inverted[term]:
                    self.inverted[term].remove(doc_id)
            self.doc_num -= 1
        self.compute_idf(save=False)
        if save:
            self.save_all()

    def compute_idf(self, save=True):
        for term in self.idf.keys():
            self.idf[term] = math.log10(self.doc_num / len(self.inverted[term]))
        if save:
            self.save_all()

    def add_document(self, doc_id, text, save=True):
        terms = []
        for txt in text.split():
            terms += list(jieba.cut_for_search(txt))
        for term in terms:
            if term in self.inverted.keys():
                if doc_id in self.inverted[term].keys():
                    self.inverted[term][doc_id] += 1
                else:
                    self.inverted[term][doc_id] = 1
            else:
                self.inverted[term] = {doc_id: 1}
        self.doc_num += 1
        for term in terms:
            self.idf[term] = math.log10(self.doc_num / len(self.inverted[term]))
        if save:
            self.save_all()


class SearchEngine:
    def __init__(self, index_engine):
        self.index_engine = index_engine

    def search(self, query):
        doc_id = self._search_doc(query)
        return doc_id

    def _search_doc(self, query):
        terms = []
        for txt in query.split():
            terms += list(jieba.cut_for_search(txt))
        tf_idf = {}
        for term in terms:
            if term in self.index_engine.inverted.keys():
                for doc_id, freq in self.index_engine.inverted[term].items():
                    score = 1 + math.log10(freq) * self.index_engine.idf[term]
                    if doc_id in tf_idf.keys():
                        tf_idf[doc_id] += score
                    else:
                        tf_idf[doc_id] = score
        doc_scores = sorted(list(tf_idf.items()), key=lambda doc: doc[1], reverse=True)
        result = [doc_id for doc_id, score in doc_scores]
        return result

class RecommenderSystem:
    '''
    调用document_engine获取推荐度最高的文章
    '''
    def __init__(self,document_engine):
        assert isinstance(document_engine,DocumentStorageEngine)
        self.document_engine=document_engine
    def recommend_latest(self,n=20):
        return self.document_engine.topk_public(k=n)
