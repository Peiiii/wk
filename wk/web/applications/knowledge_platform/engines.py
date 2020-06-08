import os, shutil, glob, random, json, math, uuid, time, datetime, inspect
import jieba
from wk.io import db, Piu
from wk import Folder, join_path, PointDict ,web
import wk
from .utils import get_keywords


class Document(PointDict):
    default_info = dict(
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
    info_fields=list(filter(lambda key: key not in ['content','html','text','data'],default_info.keys()))

    def __init__(self, **kwargs):
        def run_func_with_context(func, arg=None):
            # print(func)
            try:
                args = inspect.getfullargspec(func)
            except TypeError as e:
                return func()

            args = args.args
            if len(args):
                return func(arg)
            else:
                return func()

        info = kwargs
        for k, v in self.default_info.items():
            if k not in info.keys() or info[k] is None:
                info[k] = self.default_info[k] if not hasattr(self.default_info[k],
                                                              '__call__') else run_func_with_context(self.default_info[
                                                                                                         k], info)
        super().__init__(**info)

    def info(self):
        return {k: self[k] for k in self.info_fields}

    def set_default(self, name, value):
        if name not in self.keys() or self[name] is None:
            self[name] = value

    def check_fields(self):
        assert self['html']
        assert self['text']
        assert self['title']

        t = time.time()
        self.set_default('created', t)
        self.set_default('last_edit', t)
        self.set_default('content', self['html'])
        self.set_default('digest', self['text'][:min(30, len(self['text']))])
        self['digest'] = self['digest'][:min(50, len(self['digest']))]
        return self


class DocumentStorage:
    def __init__(self, path, id2url, update_when_start=True):
        self.id2url=id2url
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
                filename=k
                print('warning***: no filename for %s'%(k))
            else:
                filename = v['filename']
            with self.files_dir.open(filename, 'r') as f:
                doc = json.load(f)
                doc['id'] = k
                doc['filename']=filename
                # if not doc['url']:
                doc['url'] = self.id2url(doc['id'])
                doc = Document(**doc)

            with self.files_dir.open(filename, 'w') as f:
                json.dump(doc, f)
            info=doc.info()
            self.db.set(info['id'],info)


    def check(self, doc):
        def check_filed(doc, name):
            if not name in doc.keys() or not doc[name]:
                return False
            return True

        if not check_filed(doc, 'title'):
            return wk.StatusError(message='标题不能为空')
        if not check_filed(doc, 'html'):
            return wk.StatusError(message='正文不能为空')
        if not check_filed(doc, 'text'):
            return wk.StatusError(message='正文不能为空')
        return wk.StatusSuccess()
    def delete(self,doc_id,hard=False):
        assert self.db.exists(doc_id)
        info=self.db.get(doc_id)
        self.db.delete(doc_id)
        if hard:
            fn=info['filename']
            self.files_dir.remove(fn)
        return info

    def update_document(self,id,doc):
        document=self.get(id)
        document.update(**doc)
        document.update(keywords=get_keywords(document['text']))
        document=Document(**document).check_fields()
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
        info=doc.info()
        with self.files_dir.open(id, 'w') as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        self.db.set(id, info)
        return info
    def get_info(self,doc_id):
        return self.db.get(doc_id,None)
    def get(self, doc_id, default=None):
        if doc_id in self.db.dic.keys():
            filename = self.db.get(doc_id)['filename']
            with self.files_dir.open(filename, 'r') as f:
                return json.load(f)
        return default


class DocumentManageEngine:
    '''
    article:
        new:
            add to:document engine, user.articles ,
        edit:
            check permission, get from document engine
        publish:

        delete
    '''

class DocumentStorageEngine(DocumentStorage):
    def __init__(self,path, id2url, update_when_start=True):
        super().__init__(path,id2url,update_when_start)
        self.recycle_bin=db.Piu(self.path+'/recycleBinDB')
    def delete(self,doc_id,hard=False):
        info=DocumentStorage.delete(self,doc_id,hard)
        if not hard:
            self.recycle_bin.add(doc_id,info)


class StaticStorageEngine(Folder):
    def __init__(self, path,check_when_start=False):
        super().__init__(path)
        self.dbpath = path + '/db'
        self.db = db.Piu(self.dbpath)
        self.files_dir = Folder(self.path + '/file')
        self.images_dir = Folder(self.path + '/image')
        if check_when_start:
            self.check_fields()
    def check_fields(self):
        for k in list(self.db.dic.keys()):
            v=self.db.get(k)
            if not  'id' in v.keys():
                v['id']=uuid.uuid4().hex
            self.db.set(k, v)
            if not 'filename' in v.keys() or not 'filepath' in v.keys():
                self.db.delete(k)

    def send_file(self,id):
        info=self.db.get(id)
        if info:
            return web.send_file(self._truepath(info['filepath']))
        else:
            return web.StatusErrorResponse(message='File Not Found.').jsonify()
    def file_info(self,id):
        info=self.db.get(id)
        filepath=info['filepath']
        info2=self.info(filepath)
        info.update(**info2)
        return info
    def search(self,keywords,match_all=True):
        import re
        def get_search_context(id):
            return self.db.get(id)['original_filename']
        fs=self.db.keys()
        if match_all:
            for word in keywords:
                fs = list(filter(lambda id: re.findall(word,get_search_context(id) ), fs))
            return fs
        else:
            def match(text, ptns):
                for ptn in ptns:
                    if re.findall(ptn, text): return True
                return False
            fs = list(filter(lambda id: match(get_search_context(id), keywords), fs))
            return fs
    def saveImage(self, file):
        return self._saveFile(file, type='image')

    def saveFile(self, file):
        return self._saveFile(file, type='file')

    def _saveFile(self, file, type):
        '''file:
        filename , name , save , mimetype , close
        '''

        def get_info(file):
            info = {
                'original_filename': file.filename,
                'mimetype': file.mimetype
            }
            return info

        def gen_filename(id, file):
            filename = '%s-%s' % (id, file.filename)
            return filename

        id = uuid.uuid4().hex
        filename = gen_filename(id, file)
        info = get_info(file)
        info['id'] = id
        info['filename'] = filename
        info['type'] = type
        if type == 'image':
            folder = self.images_dir
        else:
            folder = self.files_dir
        filepath = folder.name + '/' + filename
        info['filepath'] = filepath
        folder.save_http_file(file, filename)
        self.db.set(id, info)
        return info

    def getFileURL(self, id):
        filename = self.getFileName(id)
        if filename:
            return join_path(self.url_prefix, self.files_dir.name, filename)
        else:
            return None

    def getFileName(self, id):
        info = self.db.get(id, None)
        if info:
            filename = info['filename']
            return filename
        else:
            return None


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

    def remove_document(self,doc_id,save=True):
        for term in self.inverted.keys():
            if doc_id in self.inverted[term]:
                self.inverted[term].remove(doc_id)
        self.doc_num-=1
        for term in self.idf.keys():
            self.idf[term] = math.log10(self.doc_num / len(self.inverted[term]))
        if save:
            self.save_all()
    def remove_document_batch(self,doc_ids:list,save=True):
        for doc_id in doc_ids:
            for term in self.inverted.keys():
                if doc_id in self.inverted[term]:
                    self.inverted[term].remove(doc_id)
            self.doc_num -= 1
        self.compute_idf(save=False)
        if save:
            self.save_all()

    def compute_idf(self,save=True):
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
